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
def _quit():
    root.quit()     
    root.destroy()  
def animate(i):
    
    plt.cla()
    plt.plot(data,2)
                  
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
        if(self.x>=counter[0] and self.x<=counter[2] and self.y>=counter[1] and self.y<=counter[3]):
            return 1
        elif(self.x>=counter2[0] and self.x<=counter2[2] and self.y>=counter2[1] and self.y<=counter2[3]):
            return 2
        else:
            return None
    
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


sinaiData={'centerX':400, 'centerY':315, 'circleRadius': 170, 'billiard':[30,30,770,600]}

obstacles=SinaiMap(canvas, sinaiData['centerX'],sinaiData['centerY'],sinaiData['circleRadius'],
                   sinaiData['billiard'], "red")

counter=[90,90,200,200]
counterArea=canvas.create_rectangle(counter[0],counter[1],counter[2],counter[3],
                                    width=2, outline='red')
counter2=[600,90,710,200]
counterArea2=canvas.create_rectangle(counter2[0],counter2[1],counter2[2],counter2[3],
                                    width=2, outline='blue')

plt.style.use('fivethirtyeight')



index=count()
#this is creating set of particles
particles=[]
numOfParticles=100     #number of particles
x=200                   #starting position for first particle
y=50                   #rest will be generated approximately near the first particle
for i in range(0, numOfParticles):
    particles.append(Particle(canvas, x, y, 1, -3, 3.1,"black",obstacles))
    y=y+0.01
    x=x+0.01

#button = Button(master=root, text="Quit", command=_quit)
#button.pack(side=BOTTOM)
#this is where animation happens
#dt determines the speed(lower=faster)
dt=0.001
t=dt
values1=[]
values2=[]

data1=[]
data2=[]

ani=FuncAnimation(plt.gcf(), animate, interval=1000)
plt.tight_layout()
plt.show()
counts=0
while True:
    numInArea1=0
    numInArea2=0
    for i in range(0, numOfParticles):
        state=particles[i].move(dt, counter, counter2)
        if(state==1):
            numInArea1=numInArea1+1
        elif(state==2):
            numInArea2=numInArea2+1        
    counts=counts+1
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
        counts=0
        values1.clear()
        values2.clear()
        print(data1[-1], data2[-1])   
    t=t+dt
    root.update()
    time.sleep(dt)


root.mainloop()