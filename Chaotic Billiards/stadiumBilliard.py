#Stadium Billiard
#Simulating Bunimovich stadium
#Handles 1000 particles well
#Used purely and recommended for aesthethic purposes, no data
#Faster than other versions of Stadium Billiard
#Starting parameters are defined here in code,but is also easy to change down in the code

from tkinter import *
import time
import math
#Function which returns new x and y velocity vectors
#Elegant and efficient solution
#uses formula v1 = v − [2 (n · v) n] (v-starting velocity, n-vector of normal line,
#and v1 new velocity)

def collide(x,y,vx,vy,x0,y0):
    nx=x-x0
    ny=y-y0
    dnx=nx/((nx**2+ny**2)**0.5)
    dny=ny/((nx**2+ny**2)**0.5)
    dx=vx - 2*((dnx**2)*vx+dny*dnx*vy)
    dy=vy - 2*((dnx*dny)*vx+(dny**2)*vy)
    return dx, dy

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
            
        self.canvas.move(self.image,self.xVelocity,self.yVelocity)
                
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
#Geometry, changes not recommendable
stadiumData={'centerX':200, 'centerY':300, 'circleRadius': 170, 'billiard':[200,130,500,470],
             'centerX1': 500, 'centerY1':300,'circleRadius1': 170}

stadium=StadiumMap(canvas, stadiumData['centerX'],stadiumData['centerY'],stadiumData['centerX1'],
                   stadiumData['centerY1'], stadiumData['circleRadius'],
                   stadiumData['circleRadius1'], stadiumData['billiard'],'red')
#this is creating set of particles
#changes of  x and y recommended, but be careful not to exit the billiard's scope
particles=[]
numOfParticles=1000     #number of particles, best performance <=1000, changes recommended
x=200                   #starting position for first particle
y=250                   #rest will be generated approximately near the first particle
#Particle attributes in order: (canvas, starting x and y coordinates,
#radius x velocity component and y velocity component, color, and geometry)
#This loop creates particles, idea is that they are all generated very close
#to eachother
for i in range(0, numOfParticles):
    particles.append(Particle(canvas, x, y, 1, 4.0, 4.1,"black",stadium))
    y=y+0.01
    x=x+0.01


#this is where animation happens
#dt determines the speed(lower=faster)
dt=0.001
while True:
    for i in range(0, numOfParticles):
        particles[i].move(dt)
    root.update()
    time.sleep(dt)

root.mainloop()