#Sinai Billiard
#Used purely and recommended for aesthethic purposes, no data
#Better than SinaiGraphicalRepresentation because
#it doesn't gather data therefore doesn't clog the program too much
#Starting parameters are defined here in code,but is also easy to change down in the code


from tkinter import *
import time
import math


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


    def move(self, dt):
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

#Geometry, not reccomended to change
sinaiData={'centerX':265, 'centerY':265, 'circleRadius': 100, 'billiard':[30,30,500,500]}

obstacles=SinaiMap(canvas, sinaiData['centerX'],sinaiData['centerY'],sinaiData['circleRadius'],
                   sinaiData['billiard'], "red")

#this is creating set of particles
#changes of  x and y recommended, but be careful not to exit the billiard's scope
#or putting the particles inside the disk(it shouldnt be passable space)
particles=[]
numOfParticles=1000     #number of particles best performance <=1000, change recommended
x=50                    #starting position for first particle, careful for out of scope coordinates
y=50                    #rest will be generated approximately near the first particle
#Particle attributes in order: (canvas, starting x and y coordinates,
#radius x velocity component and y velocity component, color, and geometry)
#This loop creates particles, idea is that they are all generated very close
#to eachother
for i in range(0, numOfParticles):
    particles.append(Particle(canvas, x, y, 1, -3, 3.1,"black",obstacles))
    y=y+0.01
    x=x+0.01


#this is where animation happens
#dt determines the speed(lower=faster), keep <=0.001
dt=0.001
while True:
    for i in range(0, numOfParticles):
        particles[i].move(dt)
    root.update()
    time.sleep(dt)


root.mainloop()