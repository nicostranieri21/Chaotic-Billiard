#Default billiard
#Simple to code, used mainly for comparisons with chaotic billiards
#Starting parameters are defined here in code,but is also easy to change down in the code

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
        self.lastx=x
        self.lasty=y
        self.color=color
        #obstacle parameters(used for detecting collision) 
        self.rectBord=obstacles.rectangleBorders


    def move(self, dt):
        coordinates = self.canvas.coords(self.image)
        self.x=coordinates[2]
        self.y=coordinates[3]
        #checks if particle collided with top, bottom, right or left boundary
        #of billiard and calculates new velocity vector
        if(coordinates[2]>=(self.rectBord[2]) or coordinates[0]<=self.rectBord[0]):
            self.xVelocity = -self.xVelocity        
            self.lastx=self.x
            self.lasty=self.y
        if(coordinates[3]>=(self.rectBord[3]) or coordinates[1]<=self.rectBord[1]):
            self.yVelocity = -self.yVelocity         
            self.lastx=self.x
            self.lasty=self.y
        self.canvas.move(self.image,self.xVelocity,self.yVelocity)
        
    
class DefaultMap():
    def __init__(self, canvas,billiard, color):     
        self.imageBilliard = canvas.create_rectangle(billiard[0], billiard[1],
                                             billiard[2], billiard[3])

        self.rectangleBorders=billiard
    
root = Tk()

WIDTH = 800
HEIGHT = 800

canvas = Canvas(root,width=WIDTH,height=HEIGHT)
canvas.pack()


Data={'centerX':265, 'centerY':265, 'circleRadius': 100, 'billiard':[30,30,500,300]}

obstacles=DefaultMap(canvas,Data['billiard'], "red")

#this is creating set of particles
particles=[]
numOfParticles=300     #number of particles
x=200                   #starting position for first particle
y=50                   #rest will be generated approximately near the first particle
for i in range(0, numOfParticles):
    particles.append(Particle(canvas, x, y, 1, -3, 3.1,"black",obstacles))
    y=y+0.01


#this is where animation happens
#dt determines the speed(lower=faster)
dt=0.001
while True:
    for i in range(0, numOfParticles):
        particles[i].move(dt)
    root.update()
    time.sleep(dt)


root.mainloop()