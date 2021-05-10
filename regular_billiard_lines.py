from tkinter import *
import time
import math


            
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


    def move(self, dt):
        coordinates = self.canvas.coords(self.image)
        self.x=coordinates[2]
        self.y=coordinates[3]
        canvas.create_line(self.x, self.y, self.x-self.xVelocity,
                           self.y-self.yVelocity, fill=self.color, width=1)
        #checks if particle collided with top, bottom, right or left boundary
        #of billiard and calculates new velocity vector
        if(coordinates[2]>=(self.rectBord[2]) or coordinates[0]<=self.rectBord[0]):
            self.xVelocity = -self.xVelocity
        if(coordinates[3]>=(self.rectBord[3]) or coordinates[1]<=self.rectBord[1]):
            self.yVelocity = -self.yVelocity
        

        self.canvas.move(self.image,self.xVelocity,self.yVelocity)
    
class SinaiMap():
    def __init__(self, canvas, x, y, diameter, billiard, color):
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
numOfParticles=2       #number of particles
x=50                   #starting position for first particle
y=50                   #rest will be generated approximately near the first particle
particles.append(Particle(canvas, x, y, 3, -3, 3.1,"red",obstacles))
particles.append(Particle(canvas, x +0.1, y +0.1, 3, -3, 3.1,"blue",obstacles))


#this is where animation happens
#dt determines the speed(lower=faster)
dt=0.01
while True:
    for i in range(0, numOfParticles):
        particles[i].move(dt)
    root.update()
    time.sleep(dt)

root.mainloop()
