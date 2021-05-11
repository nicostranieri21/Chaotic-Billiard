import pygame
import random
import matplotlib.pyplot as plt

class Point():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = (self.x ** 2 + self.y ** 2) ** 0.5

    def __repr__(self):
        return "Point:" + repr((self.x, self.y))

    def __sub__(self, other):
        return ((self.x-other.x)**2+(self.y-other.y)**2)**0.5

    def normalize(self):
        return Point(self.x / self.length, self.y / self.length)


class Line():

    def __init__(self, starting_point, direction):
        if type(starting_point) == Point and type(starting_point) == Point:
            self.x0 = starting_point.x
            self.y0 = starting_point.y
            self.a = direction.x
            self.b = direction.y
        else:
            raise Exception("This should not be the case!")

    def __repr__(self):
        return f"x:{self.x0} +{self.a}*t \ny:{self.y0} +{self.b} * t\n"

    def intersect(self, other, border=False):

        if type(other) == Circle:
            # Since the line is described (x0 + at, y0 + bt) and the circle (x^2 + y^2 = 1)
            # the system of a line and a circle by substituting is (x0 + at)^2 + (y0 + bt)^2 =
            # = (a^2 + b^2) t^2 + (2a *x0 + 2b * y0) t + (x0^2 + y0^2 -1)

            delta = (2 * self.a * self.x0 + 2 * self.b * self.y0) ** 2 - 4 * (self.a ** 2 + self.b ** 2) * (
                        self.x0 ** 2 + self.y0 ** 2 - 1)
            t = 0

            if delta < 0: # they don't intersect
                return None

            elif delta == 0: #intersect only in one point
                t = -(2 * self.a * self.x0 + 2 * self.b * self.x0) / (2 * (self.a ** 2 + self.b ** 2))

            else: # intersect in two points
                t1 = (-(2 * self.a * self.x0 + 2 * self.b * self.y0) - (delta) ** 0.5) / (
                            2 * (self.a ** 2 + self.b ** 2))
                t2 = (-(2 * self.a * self.x0 + 2 * self.b * self.y0) + (delta) ** 0.5) / (
                            2 * (self.a ** 2 + self.b ** 2))
                # choose the nearest point of intersection
                if abs(t1) < abs(t2):
                    t = t1
                else:
                    t = t2

            #find the point and return it
            x = self.x0 + self.a * t
            y = self.y0 + self.b * t
            return Point(x, y)

        if type(other) == Line:
            # Since the line is described (x0 + at, y0 + bt) and the other (x1 + cs, y1 + ds)
            # the system of two lines is x0 + at = x1 + cs and yo + bt = y1 + ds
            # t = (x1 - x0 + cs)/ a , so s = [a(y0-y1) + b(x0-x1)]/[da - cb]
            s = (self.a * (self.y0 - other.y0) + self.b * (other.x0 - self.x0)) / (other.b * self.a - other.a * self.b)
            t = (other.x0 - self.x0 + other.a * s) / (self.a)
            x = other.x0 + other.a * s
            y = other.y0 + other.b * s
            if border == True:
                # have some space for computational errors
                if t > 0 and ((-2 - 10 ** -15 <= x <= 2 + 10 ** -15
                        and (2 - 10 ** -15 <= y <= 2 + 10 ** -15 or -2 - 10 ** -15 <= y <= -2 + 10 ** -15))
                        or (-2 - 10 ** -15 <= y <= 2 + 10 ** -15
                        and (2 - 10 ** -15 <= x <= 2 + 10 ** -15 or -2 - 10 ** -15 <= x <= -2 + 10 ** -15))):
                    return Point(x, y)
                else:
                    return None
            else: # intersection between normal and tangent
                return Point(x, y)

    def reflect(self, point):
        # reflection of a point given a line
        m = self.b / self.a
        q = -(self.b / self.a * self.x0 + self.y0)
        x = ((1 - m ** 2) * point.x + 2 * m * point.y - 2 * m * q) / (1 + m ** 2)
        y = (2 * m * point.x + (m ** 2 - 1) * point.y + 2 * q) / (1 + m ** 2)
        return Point(x, y)


class Circle():

    def __init__(self, center, radious):
        self.x0 = center.x
        self.y0 = center.y
        self.r = radious


def check_nearby(B, A):
    # check if we are nearby an object to don't collide with it again
    if B is not None and A.x - 10 ** (-14) < B.x < A.x + 10 ** (-14) and A.y - 10 ** (-14) < B.y < A.y + 10 ** (-14):
        return None
    else:
        return B


def get_D(A, line, n, Sinai=True):
    """
    :param A: Starting point
    :param line: directional line
    :param n: number of collision
    :param Sinai: if we are in a Sinai billiard or not
    :return: Vector of reflection
    """

    global interaction_object

    #Define the objects in the billiard
    center = Point(0, 0)
    c = Circle(center, 1)
    wall_up = Line(Point(-2, 2), Point(4, 0))
    wall_down = Line(Point(-2, -2), Point(4, 0))
    wall_dx = Line(Point(2, 2), Point(0, -4))
    wall_sx = Line(Point(-2, 2), Point(0, -4))

    B = None # B is the point of collision

    if Sinai:
        B = line.intersect(c)
        interaction_object = "circle"
        B = check_nearby(B, A)

    if B is None:
        interaction_object = "wallup"
        B = line.intersect(wall_up, border=True)
        B = check_nearby(B, A)

        if B is None:
            interaction_object = "walldown"
            B = line.intersect(wall_down, border=True)
            B = check_nearby(B, A)

            if B is None:
                interaction_object = "walldx"
                B = line.intersect(wall_dx, border=True)
                B = check_nearby(B, A)

                if B is None:
                    interaction_object = "wallsx"
                    B = line.intersect(wall_sx, border=True)
                    B = check_nearby(B, A)

                    if B is None:
                        # If it arrives here there are some errors
                        interaction_object = "NONE"
                        print(f"impossible {n}")

    if interaction_object == "circle":
        normal = Line(Point(0, 0), Point(B.x, B.y)) # find the normal to the point B
        D = normal.reflect(A) # reflect A on the normal
        return B, D

    # In all the walls reflect the vector AB and move it to B
    if interaction_object == "wallup" or interaction_object == "walldown":
        movement = Point(B.x - A.x, -B.y + A.y)
        D = Point(B.x + 2 * movement.x, B.y + 2 * movement.y)
        return B, D

    if interaction_object == "walldx" or interaction_object == "wallsx":
        movement = Point(-B.x + A.x, B.y - A.y)
        D = Point(B.x + 2 * movement.x, B.y + 2 * movement.y)
        return B, D


def main(array,color):
    for i in range(len(array)-1):
        A, B = array[i]
        C, D = array[i+1]
        r = 150  # resizing
        t = 350  # translation wrt the origin in calculations
        pygame.draw.line(window, color, (t + A.x * r, t - A.y * r),(t + C.x * r, t - C.y * r), 1)
        pygame.display.update()
        
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quit the game
                run = False


##------  CONTROL PANEL  ------##
N = 150
Sinai_Billiard = False
second_particle = False

error_in_posistion_x = 10**-16
error_in_posistion_y = 10**-16
error_in_velocity_x = 10**-16
error_in_velocity_y = 10**-16
distance_graph = True
average_distance_graph = True
##-----------------------------##

##------- Starting Form -------##
pygame.init()
WIDTH, HEIGHT = 700, 700
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sinai Billiard")
window.fill((255, 255, 255))
if Sinai_Billiard == True:
    pygame.draw.circle(window, "black", (350, 350), 150, width=4)
pygame.draw.rect(window, "black", pygame.Rect(47, 47, 606, 606), width=4)
pygame.display.update()
##-----------------------------##

##-------- First Ball ---------##
A = Point(-2, -2)
v = Point(random.random(), random.random())
print(v)
l = Line(A, v)
array = [(A, v.normalize())]
for n in range(N):  # number of collisions
    A, D = get_D(A, l, n,Sinai_Billiard)
    V = Point(D.x - A.x, D.y - A.y)
    l = Line(A, V)
    array.append((A, V.normalize()))
main(array,"red")
##-----------------------------##

##--- Second ball and graphs --##
difference_array = []
average_difference_array = []
if second_particle:
    A = Point(-2+error_in_posistion_x, -2+error_in_posistion_y)
    v = Point(v.x+error_in_velocity_x, v.y+error_in_velocity_y)
    print(v)
    l = Line(A, v)
    array2 = [(A, v.normalize())]
    for n in range(N):  # number of collisions
        A, D = get_D(A, l, n,Sinai_Billiard)
        V = Point(D.x - A.x, D.y - A.y)
        l = Line(A, V)
        array2.append((A, V.normalize()))
    main(array2,"blue")

    if distance_graph or average_distance_graph:
        difference = 0
        for n in range(1,N+1):
            diff = (array[n][0]-array2[n][0]) #The distance between two points
            difference_array.append(diff)
            difference += diff #Sum them up
            average_difference = difference/n # Divide by the number of the collisions
            average_difference_array.append(average_difference)

    if distance_graph:
        plt.style.use('ggplot')
        plt.figure(dpi=100)
        plt.plot(range(N), difference_array, color='r', linewidth=1)
        plt.title('Distance during time')
        plt.xlabel('Time function')
        plt.ylabel('Distance between particles')
        plt.legend()
        plt.show()

    if average_distance_graph:
        plt.style.use('ggplot')
        plt.figure(dpi=100)
        plt.plot(range(N), average_difference_array, color='r', linewidth=1)
        plt.title('Average distance during time')
        plt.xlabel('Time function')
        plt.ylabel('Average Distance')
        plt.legend()
        plt.show()

##-----------------------------##
