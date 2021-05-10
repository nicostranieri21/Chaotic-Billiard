from tkinter import *
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
import time
import math
from matplotlib.animation import FuncAnimation


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
        #obstacle parameters(used for detecting collision) 
        self.radius=obstacles.radius
        self.x0=obstacles.x
        self.y0=obstacles.y
        self.rectBord=obstacles.rectangleBorders


    def move(self, dt, counter, counter2):
        coordinates = self.canvas.coords(self.image)
        self.x=coordinates[2]
        self.y=coordinates[3]
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


sinaiData={'centerX':400,
           'centerY':315,
           'circleRadius': 170,
           'billiard':[30,30,770,600]}

obstacles=SinaiMap(canvas,
                   sinaiData['centerX'],
                   sinaiData['centerY'],
                   sinaiData['circleRadius'],
                   sinaiData['billiard'], "red")

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
    particles.append(Particle(canvas, x, y, 1, -5, 0.3,"black",obstacles))
    y=y+0.01
    x=x+0.01
    
    
check=True

#dt determines the speed(lower=faster)
dt=0.000000000001
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