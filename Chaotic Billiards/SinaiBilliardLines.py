#Sinai Lines simulation
#IMPORTANT: particles draw lines behind them ONLY at colisions instances
#in order to prevent generating millions small lines and to not slow down 
#the program
#Gathers no data, but visualises trajectories of particles
#Used for 2 particle experiment
#Starting parameters are defined here in code,but is also easy to change down in the code


from tkinter import *
import time
import math


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
            npp=+1
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
        self.radius=obstacles.radius
        self.x0=obstacles.x
        self.y0=obstacles.y
        self.rectBord=obstacles.rectangleBorders
        self.lastx=self.x
        self.lasty=self.y


    def move(self, dt):
        coordinates = self.canvas.coords(self.image)
        self.x=coordinates[2]
        self.y=coordinates[3]
      
        #checks if collision with disk in the middle occured
        if((self.x-self.x0)**2+(self.y-self.y0)**2<=(self.radius)**2):
            vel=collide(self.x,self.y,self.xVelocity,self.yVelocity,self.x0,self.y0)
            self.xVelocity=vel[0]
            self.yVelocity=vel[1]
            canvas.create_line(self.x, self.y, self.lastx,
                          self.lasty, fill=self.color, width=1)          
            self.lastx=self.x
            self.lasty=self.y
        #checks if particle collided with top, bottom, right or left boundary
        #of billiard and calculates new velocity vector
        #if collisions are detected, it draws one line from last collision
        #coordinates to current position coordinates
        if(coordinates[2]>=(self.rectBord[2]) or coordinates[0]<=self.rectBord[0]):
            self.xVelocity = -self.xVelocity
            canvas.create_line(self.x, self.y, self.lastx,
                           self.lasty, fill=self.color, width=1)          
            self.lastx=self.x
            self.lasty=self.y
        if(coordinates[3]>=(self.rectBord[3]) or coordinates[1]<=self.rectBord[1]):
            self.yVelocity = -self.yVelocity
            canvas.create_line(self.x, self.y, self.lastx,
                           self.lasty, fill=self.color, width=1)          
            self.lastx=self.x
            self.lasty=self.y
        self.canvas.move(self.image,self.xVelocity,self.yVelocity)
    
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

#geometry
sinaiData={'centerX':265, 'centerY':265, 'circleRadius': 100, 'billiard':[30,30,500,500]}

obstacles=SinaiMap(canvas, sinaiData['centerX'],sinaiData['centerY'],sinaiData['circleRadius'],
                   sinaiData['billiard'], "red")

#this is creating set of particles
particles=[]
numOfParticles=2       #number of particles(NO MORE THAN 2 are suggested, for visual's sake)
x=90                   #starting position for first particle
y=35                   #second particles generates close
#here we generate particles manually, because we want to define their color and coordinates
#and also because we essentially only need 2 to show everything
#they are also a little larger for better visuals
particles.append(Particle(canvas, x, y, 3, -0.35, 0.36,"red",obstacles))
particles.append(Particle(canvas, x , y + 15, 3, -0.35, 0.36,"blue",obstacles))

#this is where animation happens
#dt determines the speed(lower=faster)
dt=0.001
while True:
    for i in range(0, numOfParticles):
        particles[i].move(dt)
    root.update()
    time.sleep(dt)

root.mainloop()
