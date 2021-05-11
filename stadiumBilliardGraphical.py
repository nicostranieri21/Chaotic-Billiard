#Stadium Billiard Data
#Used for data and plotting graphs
#Slower than standard Stadium Billiard, because of real time data gathering
#Used for plotting graphs
#Starting parameters are defined here in code,but is also easy to change down in the code

from tkinter import *
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
import time
import math

#Using dot product formula, same as StadiumBilliard.py
def collide(x,y,vx,vy,x0,y0):
    nx=x-x0
    ny=y-y0
    dnx=nx/((nx**2+ny**2)**0.5)
    dny=ny/((nx**2+ny**2)**0.5)
    dx=vx - 2*((dnx**2)*vx+dny*dnx*vy)
    dy=vy - 2*((dnx*dny)*vx+(dny**2)*vy)
    return dx, dy
#Assign global variable and set value to stop, used for one button.
def stop(button):
    global check
    check = False
    button['state']=DISABLED
#used for hide button
def hide(canvas,button, area1, area2):
    if button['text']=="Hide areas":
        button.config(text="Show areas")        
        canvas.itemconfigure(area1, state='hidden')
        canvas.itemconfigure(area2, state='hidden')
    else:
        button.config(text="Hide areas")
        canvas.itemconfigure(area1, state='normal')
        canvas.itemconfigure(area2, state='normal')

class Particle:
    def __init__(self,canvas,x,y,diameter,xVelocity,yVelocity,color,obstacles):
        self.canvas = canvas
        self.image = canvas.create_oval(x-diameter,y-diameter,diameter+x,diameter+y,fill=color)
        self.xVelocity = xVelocity
        self.yVelocity = yVelocity
        self.x=x
        self.y=y
        self.color=color
        #obstacle parameters(used for detecting collision) 
        self.radiusl=obstacles.radiusl
        self.x0l=obstacles.xl
        self.y0l=obstacles.yl
        self.radiusr=obstacles.radiusr
        self.x0r=obstacles.xr
        self.y0r=obstacles.yr
        self.rectBord=obstacles.rectangleBorders


    def move(self, dt, counter, counter2):
        coordinates = self.canvas.coords(self.image)
        self.x=coordinates[2]
        self.y=coordinates[3]
        #checks if collision with left arc occured
        if(self.x<self.x0l and 
          (self.x+(dt*self.xVelocity)-self.x0l)**2+(self.y+(dt*self.yVelocity)-self.y0l)**2>=(self.radiusl)**2):
            
            vel=collide(self.x,self.y,self.xVelocity,self.yVelocity,self.x0l,self.y0l)
            self.xVelocity=vel[0]
            self.yVelocity=vel[1]

        #checks if collision with right arc occured
        elif(self.x>self.x0r and 
          (self.x+(dt*self.xVelocity)-self.x0r)**2+(self.y+(dt*self.yVelocity)-self.y0r)**2>=(self.radiusr)**2):
            
            vel=collide(self.x,self.y,self.xVelocity,self.yVelocity,self.x0r,self.y0r)
            self.xVelocity=vel[0]
            self.yVelocity=vel[1]

        #checks if particle collided with top, bottom boundary
        #of billiard and calculates new velocity vector
        elif(coordinates[3]<=(self.rectBord[0]) or coordinates[3]>=self.rectBord[1]):
            self.yVelocity = -self.yVelocity 
        #Used for checking if the particle is inside the counter areas(used for graphing)
        self.canvas.move(self.image,self.xVelocity,self.yVelocity)
        if(self.x>=counter[0] and self.x<=counter[2] and self.y>=counter[1] and self.y<=counter[3]):
            return 1
        elif(self.x>=counter2[0] and self.x<=counter2[2] and self.y>=counter2[1] and self.y<=counter2[3]):
            return 2
        else:
            return None
                
class StadiumMap():
    def __init__(self, canvas, x, y,x1,y1, diameter,diameter1, billiard, color):
        self.imageCircleLeft = canvas.create_arc(x-diameter,y-diameter,diameter+x,
                                        diameter+y,start=90, extent=180)
        
        self.imageBilliard = canvas.create_rectangle(billiard[0], billiard[1],
                                             billiard[2], billiard[3])
        
        self.imageCircleRight = canvas.create_arc(x1-diameter1,y1-diameter1,diameter1+x1,
                                        diameter1+y1,start=270, extent=180)
        self.whiteLeft=canvas.create_oval(billiard[0]-30,billiard[1],
                                           billiard[0]+30,billiard[3],
                                           fill=canvas['background'],outline='')
        self.whiteRight=canvas.create_oval(billiard[2]-30,billiard[1],
                                           billiard[2]+30,billiard[3],
                                           fill=canvas['background'],outline='')
        self.xl=x
        self.yl=y
        self.radiusl=diameter
        self.xr=x1
        self.yr=y1
        self.radiusr=diameter1
        self.rectangleBorders=[billiard[1], billiard[3]]
        
        
root = Tk()
canvas = Canvas(root, width=800, height=800)
canvas.pack()

stadiumData={'centerX':200, 'centerY':300, 'circleRadius': 170, 'billiard':[200,130,500,470],
             'centerX1': 500, 'centerY1':300,'circleRadius1': 170}

stadium=StadiumMap(canvas, stadiumData['centerX'],stadiumData['centerY'],stadiumData['centerX1'],
                   stadiumData['centerY1'], stadiumData['circleRadius'],
                   stadiumData['circleRadius1'], stadiumData['billiard'],'red')
counter=[310,170,390,250]
counterArea=canvas.create_rectangle(counter[0],counter[1],counter[2],counter[3],
                                    width=2, outline='red')
counter2=[310,350,390,430]
counterArea2=canvas.create_rectangle(counter2[0],counter2[1],counter2[2],counter2[3],
                                    width=2, outline='blue')

#this is creating set of particles
particles=[]
numOfParticles=300     #number of particles, suggested number is 300
x=90                   #starting position for first particle, changes recommended but be careful not to exit billiard
y=315                  #rest will be generated approximately near the first particle
#Particle attributes in order: (canvas, starting x and y coordinates,
#radius x velocity component and y velocity component, color, and geometry)
#This loop creates particles, idea is that they are all generated very close
#to eachother
for i in range(0, numOfParticles):
    particles.append(Particle(canvas, x, y, 1, 1, 5.1,"black",stadium))
    y=y+0.01
    x=x+0.01
    
    
check=True

#dt determines the speed(lower=faster)
dt=0.001
#Lists used for data storing, later for graphing
values1=[]
values2=[]
data1=[]
data2=[]
#GUI
button = Button(master=root, text="Stop and Graph",
                command=lambda: stop(button),
                height = 2, width = 15)
button.pack()
button.place(x=30, y=630)

label=Label(root,text=("Number of particles: "+str(numOfParticles)),
               fg='black')
label.pack()
label.place(x=370, y=715)
labelRed=Label(root,text=("Number of particles: "+str(0)),
               fg='red')
labelRed.pack()
labelRed.place(x=370, y=632.5)
labelBlue=Label(root,text=("Number of particles: "+str(0)),
                fg='blue')
labelBlue.pack()
labelBlue.place(x=370, y=672.5)

hidebutton = Button(master=root, text="Hide areas",
                command=lambda: hide(canvas,hidebutton,counterArea,counterArea2),
                height = 2, width = 15)
hidebutton.pack()
hidebutton.place(x=30, y=700)

counts=0
#timeF and i1 used to track and store time for plotting graphs
timeF=[]
i1=0
#Animation and real time data gathering
while check==True:
    numInArea1=0
    numInArea2=0
    #moving particles and checking if they are in 2 area counters
    #happens every single iteration
    for i in range(0, numOfParticles):
        state=particles[i].move(dt, counter, counter2)
        if(state==1):
            numInArea1=numInArea1+1
        elif(state==2):
            numInArea2=numInArea2+1        
    counts=counts+1
    labelRed.config(text=("Number of particles: "+str(numInArea1)))
    labelBlue.config(text=("Number of particles: "+str(numInArea2)))
    values1.append(numInArea1)
    values2.append(numInArea2)
    #each 50 iterations averaging the value from last 50 values
    #lower counts== number for more 'crowded' graph
    if counts==50:
        sm=0
        for x in values1:
            sm=sm+x
        data1.append(sm/counts)
        sm=0
        for y in values2:
            sm=sm+y
        data2.append(sm/counts)
        timeF.append(i1)
        i1=i1+1
        counts=0
        values1.clear()
        values2.clear()
    root.update()
    time.sleep(dt)

#Graphing after the simulation
plt.style.use('ggplot')
plt.figure(dpi=1200)
plt.plot(timeF,data1, color='r', linewidth=1,
         label="Particles in red square")
plt.plot(timeF,data2, color='b', linewidth=1,
         label="Particles in blue square")
plt.title('Number of particles in designated areas over time')
plt.xlabel('Time function')
plt.ylabel('Number of particles')
plt.legend()
#plt.savefig('Sinai_graph.png')
plt.show()

root.mainloop()