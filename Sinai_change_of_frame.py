from tkinter import *
import time
import math
import numpy as np


def slide(x, y,xVelocity, yVelocity ,circle_x,circle_y):
    # x,y are coordinates of the intersection
    # circle_x,circle_y coord of center of the circle
    vector_1 = [x - circle_x, y - circle_y]
    vector_2 = [0,1]

    unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
    unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    #angle = np.arccos(dot_product)
    #angle = math.pi - angle
    angle = math.atan2(vector_2[0], vector_2[1])
    xprimevel= xVelocity*math.cos(angle) - yVelocity*math.sin(angle)
    xprimevel*=(-1)
    yprimevel= yVelocity*math.cos(angle) - xVelocity*math.sin(angle)
    return (xprimevel*math.cos(angle) + yprimevel*math.sin(angle), yprimevel*math.cos(angle) + xprimevel*math.sin(angle))
            
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
            if np.dot([self.y - self.y0,self.x - self.x0], [self.x - (dt*self.xVelocity), self.y - (dt*self.yVelocity)] ) == 0:
                self.xVelocity*=(-1)
                self.yVelocity*=(-1)
            else:
                vel=slide(self.x,self.y,self.xVelocity,self.yVelocity,self.x0,self.y0)
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
        self.image = canvas.create_oval(x-diameter,y-diameter,diameter+x,diameter+y)
        self.image = canvas.create_rectangle(billiard[0], billiard[1],
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


sinaiData={'centerX':370, 'centerY':285, 'circleRadius': 170, 'billiard':[30,30,770,600],
           'billiardX0': 30, 'billiardY0':30,'billiardX1': 770, 'billiardY1': 400}

obstacles=SinaiMap(canvas, sinaiData['centerX'],sinaiData['centerY'],sinaiData['circleRadius'],
                   sinaiData['billiard'], "red")

#this is creating set of particles
particles=[]
numOfParticles=100     #number of particles
x=50                   #starting position for first particle
y=50                   #rest will be generated approximately near the first particle
for i in range(0, numOfParticles):
    particles.append(Particle(canvas, x, y, 1, -3, 3.1,"black",obstacles))
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
