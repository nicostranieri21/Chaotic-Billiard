from tkinter import *
import time
import math


def counterclockwise(vx,vy,theta):
    alfa=math.pi-2*theta
    dx=vx*math.cos(alfa)+vy*math.sin(alfa)
    dy=(-1)*vx*math.sin(alfa)+vy*math.cos(alfa)
    return dx, dy

def clockwise(vx,vy,theta):
    alfa=math.pi-2*theta
    dx=vx*math.cos(alfa)-vy*math.sin(alfa)
    dy=vx*math.sin(alfa)+vy*math.cos(alfa)
    return dx, dy

def collide(x,y,vx,vy,x0,y0):
    nx=x-x0
    ny=y-y0
    dnx=nx/((nx**2+ny**2)**0.5)
    dny=ny/((nx**2+ny**2)**0.5)
    dvx=vx/((vx**2+vy**2)**0.5)
    dvy=vy/((vx**2+vy**2)**0.5)
    theta=math.acos((dnx*dvx+dny*dvy)/(((dvx**2+dvy**2)**0.5)+((dnx**2+dny**2)**0.5)))
    
    
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
            if(dvx>=0 and dvy<=0):
                if(dvx<=abs(dnx)):
                    vel=clockwise(vx,vy,theta)
                    vx=vel[0]
                    vy=vel[1]
                else:
                    vel=counterclockwise(vx,vy,theta)
                    vx=vel[0]
                    vy=vel[1]
            elif(dvx<=0 and dvy<=0):
                vel=clockwise(vx,vy,theta)
                vx=vel[0]
                vy=vel[1]
            else:
                vel=counterclockwise(vx,vy,theta)
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
            if(dvx<=0 and dvy>=0):
                if(abs(dvx)>=dnx):
                    vel=clockwise(vx,vy,theta)
                    vx=vel[0]
                    vy=vel[1]
                else:
                    vel=counterclockwise(vx,vy,theta)
                    vx=vel[0]
                    vy=vel[1]
            elif(dvx>0 and dvy>=0):
                vel=clockwise(vx,vy,theta)              
                vx=vel[0]
                vy=vel[1]
            else:
                vel=counterclockwise(vx,vy,theta)
                vx=vel[0]
                vy=vel[1]               
                
    return vx, vy, x+dnx, y+dny
            
   
def collide1(x,y,vx,vy, x0, y0):
    nx=x-x0
    ny=y-y0
    cx=x-vx
    cy=y-vy
    a=-(nx/ny)  
    b=1
    t1=(cx-x0-((cy*nx)/(ny**2))+((y0*nx)/(ny**2)))/((ny/nx)+(nx/(ny**2)))
    a1=cx - (2*((t1*ny)/nx))
    a2=cy + (2*t1)
    vx1=a1-x
    vy1=a2-y
    l=[vx1,vy1]
    return l
                   
                    
            
    

class Particle:


    def __init__(self,canvas,x,y,diameter,xVelocity,yVelocity,color,obstacles):
        self.canvas = canvas
        self.image = canvas.create_oval(x-diameter,y-diameter,diameter+x,diameter+y,fill=color)
        self.xVelocity = xVelocity
        self.yVelocity = yVelocity
        self.x=x
        self.y=y
        
        self.radius=obstacles.radius
        self.x0=obstacles.x
        self.y0=obstacles.y

    def move(self):
        coordinates = self.canvas.coords(self.image)
        self.x=coordinates[2]
        self.y=coordinates[3]
        #ifs are when it reaches boundaries
        if((self.x-self.x0)**2+(self.y-self.y0)**2<=(self.radius)**2):
            vel=collide1(self.x,self.y,self.xVelocity,self.yVelocity,self.x0,self.y0)
            self.xVelocity=vel[0]
            self.yVelocity=vel[1]
            #self.x=vel[2]
            #self.y=vel[3]
           # self.canvas.coords(self.image)[2]=vel[2]
           # self.canvas.coords(self.image)[3]=vel[3]

        if(coordinates[2]>=(self.canvas.winfo_width()) or coordinates[0]<0):
            self.xVelocity = -self.xVelocity
        if(coordinates[3]>=(self.canvas.winfo_height()) or coordinates[1]<0):
            self.yVelocity = -self.yVelocity

        self.canvas.move(self.image,self.xVelocity,self.yVelocity)
    

class Map():
    def __init__(self, canvas, x, y, diameter, color):
        self.image = canvas.create_oval(x-diameter,y-diameter,diameter+x,diameter+y)
        self.x=x
        self.y=y
        self.radius=diameter
    
root = Tk()

WIDTH = 800
HEIGHT = 800

canvas = Canvas(root,width=WIDTH,height=HEIGHT)
canvas.pack()

x=0
y=800
r=400


#this is creating set of particles
particles=[]
numOfParticles=2
x=10
y=10
x1=0
y1=0
obstacles=Map(canvas, 400,400, 250, "red")
for i in range(0, numOfParticles):
    particles.append(Particle(canvas, x, y, 5, 1+x1, 4+y1,"black",obstacles))
    y=y+10
    x=x+10
    x1=+2
    y1=+2
    
#this is where animation happens
while True:
    for i in range(0, numOfParticles):
        particles[i].move()
    root.update()
    time.sleep(0.01)

root.mainloop()
