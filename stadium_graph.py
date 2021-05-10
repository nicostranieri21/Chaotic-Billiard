from tkinter import *
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
import time
import math
from matplotlib.animation import FuncAnimation

#Counter clockwise rotational matrix
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
def stop(button):
    # Assign global variable and set value to stop
    global check
    check = False
    button['state']=DISABLED
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


    def move(self, dt):
        coordinates = self.canvas.coords(self.image)
        self.x=coordinates[2]
        self.y=coordinates[3]
      
        #checks if collision with left arc occured(I am pretty sure it works correctly)
        if(self.x<self.x0l and 
          (self.x+(dt*self.xVelocity)-self.x0l)**2+(self.y+(dt*self.yVelocity)-self.y0l)**2>=(self.radiusl)**2):
            #this is where we get new vector, but function needs work
            vel=collide(self.x,self.y,self.xVelocity,self.yVelocity,self.x0l,self.y0l)
            self.xVelocity=vel[0]
            self.yVelocity=vel[1]

        #checks if collision with right arc occured(I am pretty sure it works correctly)
        elif(self.x>self.x0r and 
          (self.x+(dt*self.xVelocity)-self.x0r)**2+(self.y+(dt*self.yVelocity)-self.y0r)**2>=(self.radiusr)**2):
            #this is where we get new vector, but function needs work
            vel=collide(self.x,self.y,self.xVelocity,self.yVelocity,self.x0r,self.y0r)
            self.xVelocity=vel[0]
            self.yVelocity=vel[1]

        #checks if particle collided with top, bottom boundary
        #of billiard and calculates new velocity vector(works perfectly)
        elif(coordinates[3]<=(self.rectBord[0]) or coordinates[3]>=self.rectBord[1]):
            self.yVelocity = -self.yVelocity 
            
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

WIDTH = 800
HEIGHT = 800

canvas = Canvas(root,width=WIDTH,height=HEIGHT)
canvas.pack()


stadiumData={'centerX':200, 'centerY':300, 'circleRadius': 170, 'billiard':[200,130,500,470],
             'centerX1': 500, 'centerY1':300,'circleRadius1': 170}

stadium=StadiumMap(canvas, stadiumData['centerX'],stadiumData['centerY'],stadiumData['centerX1'],
                   stadiumData['centerY1'], stadiumData['circleRadius'],
                   stadiumData['circleRadius1'], stadiumData['billiard'],'red')

counter=[90,90,200,200]
counterArea=canvas.create_rectangle(counter[0],counter[1],counter[2],counter[3],
                                    width=2, outline='red')
counter2=[600,90,710,200]
counterArea2=canvas.create_rectangle(counter2[0],counter2[1],counter2[2],counter2[3],
                                    width=2, outline='blue')

#this is creating set of particles
particles=[]
numOfParticles=300     #number of particles
x=30                   #starting position for first particle
y=315                 #rest will be generated approximately near the first particle
for i in range(0, numOfParticles):
    particles.append(Particle(canvas, x, y, 1, 0.9, 0.91,"black",stadium))
    y=y+0.01
    x=x+0.01
    
    
check=True

#dt determines the speed(lower=faster)
dt=0.0000000001
t=dt
values1=[]
values2=[]

data1=[]
data2=[]
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
timeF=[]
i1=0
while check==True:
    numInArea1=0
    numInArea2=0
    for i in range(0, numOfParticles):
        state=particles[i].move(dt)
        if(state==1):
            numInArea1=numInArea1+1
        elif(state==2):
            numInArea2=numInArea2+1        
    counts=counts+1
    labelRed.config(text=("Number of particles: "+str(numInArea1)))
    labelBlue.config(text=("Number of particles: "+str(numInArea2)))
    values1.append(numInArea1)
    values2.append(numInArea2)
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
        #print("data1:", data1[-1],"   data2:", data2[-1])
    t=t+dt
    root.update()
    time.sleep(dt)


plt.style.use('ggplot')
#plt.tight_layout()
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
