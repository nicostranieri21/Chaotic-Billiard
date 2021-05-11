#Sinai Graphical Representation
#This is used to plot graphs for number of particles in area
#Used for showing the convergence and uniform distribution inside
#the billiard, best used with 100-300 particles, 
#1000 is doable but little slower.
#Lags because it takes a lot of data in real time
#Please first use stop/plot button before closing the window
#if you want to plot graph
#Starting parameters are defined here in code,but is also easy to change down in the code


from tkinter import *
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
import time
import math
from matplotlib.animation import FuncAnimation

#Counter clockwise rotational matrix
#returns new x and v components of velocity vector
#rotated by pi-2theta
def counterclockwise(vx,vy,theta):
    alfa=math.pi-2*theta
    dx=vx*math.cos(alfa)+vy*math.sin(alfa)
    dy=(-1)*vx*math.sin(alfa)+vy*math.cos(alfa)
    l=[dx,dy]
    return l
#Clockwise rotational matrix
def clockwise(vx,vy,theta):
    alfa=math.pi-2*theta
    dx=vx*math.cos(alfa)-vy*math.sin(alfa)
    dy=vx*math.sin(alfa)+vy*math.cos(alfa)
    l=[dx,dy]
    return l
#Function which determines which angle particle should 
#bounce at(returns new x and y components of the velocity vector)
#Probably has more elegant solution, but this one works perfectly and
#most importantly efficiently. Unreadable without proper graphical explanation,
#but the idea is to find the correct rotation(clockwise or counterclockwise).
#It depends on if collision occured at top left, top right, bottom left,
#bottom right part of the circle and direction of the vector
#Hence lot of ifs

def collide(x,y,vx,vy,x0,y0):
    nx=x-x0
    ny=y-y0
    dnx=nx/((nx**2+ny**2)**0.5)
    dny=ny/((nx**2+ny**2)**0.5)
    dvx=vx/((vx**2+vy**2)**0.5)
    dvy=vy/((vx**2+vy**2)**0.5)
    theta=math.acos((dnx*dvx+dny*dvy)/(((dvx**2+dvy**2)**0.5)*((dnx**2+dny**2)**0.5)))     
    if(x-x0>=0):   
        if(y-y0>=0):
            if(dvx<=0 and dvy<=0):
                if(abs(dvx)<=dnx):                   
                    vel=counterclockwise(vx,vy,theta)
                    vx=vel[0]
                    vy=vel[1]
                else:
                    vel=clockwise(vx,vy,theta)
                    vx=vel[0]
                    vy=vel[1]
            elif(dvx<=0 and dvy>=0):
                vel=clockwise(vx,vy,theta)
                vx=vel[0]
                vy=vel[1]
            else:
                vel=counterclockwise(vx,vy,theta)
                vx=vel[0]
                vy=vel[1]
        else:
            if(dvx<=0 and dvy>=0):
                if(abs(dvx)<=(dnx)):
                    vel=clockwise(vx,vy,theta)
                    vx=vel[0]
                    vy=vel[1]
                else:
                    vel=counterclockwise(vx,vy,theta)
                    vx=vel[0]
                    vy=vel[1]
            elif(dvx<=0 and dvy<=0):
                vel=counterclockwise(vx,vy,theta)
                vx=vel[0]
                vy=vel[1]
            else:
                vel=clockwise(vx,vy,theta)
                vx=vel[0]
                vy=vel[1]
    else:       
        if(y-y0<=0):
            if(dvx>=0 and dvy>=0):
                if(dvx<=abs(dnx)):
                    vel=counterclockwise(vx,vy,theta)
                    vx=vel[0]
                    vy=vel[1]
                else:
                    vel=clockwise(vx,vy,theta)
                    vx=vel[0]
                    vy=vel[1]
            elif(dvx>=0 and dvy <0):
                vel=clockwise(vx,vy,theta)
                vx=vel[0]
                vy=vel[1]
            else:
                vel=counterclockwise(vx,vy,theta)
                vx=vel[0]
                vy=vel[1]
        else:
            if(dvx>=0 and dvy<=0):
                if(abs(dvx)>=abs(dnx)):
                    vel=counterclockwise(vx,vy,theta)
                    vx=vel[0]
                    vy=vel[1]
                else:
                    vel=clockwise(vx,vy,theta)
                    vx=vel[0]
                    vy=vel[1]
            elif(dvx>0 and dvy>=0):
                vel=counterclockwise(vx,vy,theta)              
                vx=vel[0]
                vy=vel[1]
            else:
                vel=clockwise(vx,vy,theta)
                vx=vel[0]
                vy=vel[1]                         
    return vx, vy
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
        #obstacle parameters(used for detecting collision) 
        self.radius=obstacles.radius
        self.x0=obstacles.x
        self.y0=obstacles.y
        self.rectBord=obstacles.rectangleBorders
        
    #essential for animation,but lags the program a lot.
    def move(self, dt, counter, counter2):
        coordinates = self.canvas.coords(self.image)
        self.x=coordinates[2]
        self.y=coordinates[3]
        #checks if collision with disk in the middle occured
        if((self.x+(dt*self.xVelocity)-self.x0)**2+(self.y+(dt*self.yVelocity)-self.y0)**2<=(self.radius)**2):
            vel=collide(self.x,self.y,self.xVelocity,self.yVelocity,self.x0,self.y0)
            self.xVelocity=vel[0]
            self.yVelocity=vel[1]
        #checks if particle collided with top, bottom, right or left boundary
        #of billiard and calculates new velocity vector
        if(coordinates[2]>=(self.rectBord[2]) or coordinates[0]<=self.rectBord[0]):
            self.xVelocity = -self.xVelocity
        if(coordinates[3]>=(self.rectBord[3]) or coordinates[1]<=self.rectBord[1]):
            self.yVelocity = -self.yVelocity
        self.canvas.move(self.image,self.xVelocity,self.yVelocity)
        #Used for checking if the particle is inside the counter areas(used for graphing)
        if(self.x>=counter[0] and self.x<=counter[2] and self.y>=counter[1] and self.y<=counter[3]):
            return 1
        elif(self.x>=counter2[0] and self.x<=counter2[2] and self.y>=counter2[1] and self.y<=counter2[3]):
            return 2
        else:
            return None

#defining billiard geometry  
class SinaiMap():
    def __init__(self, canvas, x, y, diameter, billiard, color):
        self.imageCircle = canvas.create_oval(x-diameter,y-diameter,diameter+x,diameter+y)
        self.imageBilliard = canvas.create_rectangle(billiard[0], billiard[1],
                                             billiard[2], billiard[3])
        self.x=x
        self.y=y
        self.radius=diameter
        self.rectangleBorders=billiard
    
root = Tk()

WIDTH = 800
HEIGHT = 800

canvas = Canvas(root,width=WIDTH,height=HEIGHT)
canvas.pack()
#Defining geometry. Can be changed but not recommended
sinaiData={'centerX':265, 'centerY':265, 'circleRadius': 100, 'billiard':[30,30,500,500]}

obstacles=SinaiMap(canvas,
                   sinaiData['centerX'],
                   sinaiData['centerY'],
                   sinaiData['circleRadius'],
                   sinaiData['billiard'], "red")
#areas that count, used for graphs
counter=[60,90,170,200]
counterArea=canvas.create_rectangle(counter[0],counter[1],counter[2],counter[3],
                                    width=2, outline='red')
counter2=[360,90,470,200]
counterArea2=canvas.create_rectangle(counter2[0],counter2[1],counter2[2],counter2[3],
                                    width=2, outline='blue')

#this is creating set of particles
particles=[]
numOfParticles=300          #number of particles(Best performance <=300), 1000 doable
x=90                        #starting position for first particle,rest will
y=315                       #be generated approximately near the first particle
#Particle attributes in order: (canvas, starting x and y coordinates,
#radius x velocity component and y velocity component, color, and geometry)
#This loop creates particles, idea is that they are all generated very close
#to eachother
for i in range(0, numOfParticles):
    particles.append(Particle(canvas, x, y, 1, 0.3, 5,"black",obstacles))
    y=y+0.01
    x=x+0.01
    
check=True
#dt determines the speed(lower=faster)
dt=0.0001
#variables used for storing graph data
values1=[]
values2=[]
data1=[]
data2=[]
#some GUI
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
#time and i1 used to track and store time for plotting graphs
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

#Graphs will be plotted after closing the program 
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



