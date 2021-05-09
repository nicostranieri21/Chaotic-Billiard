def get_intersection(line, object):
    i = object.intersection(line)
    B = None
    if i.type == "Point":
        B = i
    elif i.type == "LineString":
        return None
    else:
        min = None
        min_dist = 5
        for point in i:
            if min is None:
                min = point
                x = line.coords[0][0]
                y = line.coords[0][1]
                min_dist = ((point.x-x)**2+(point.y-y)**2)**0.5
            elif ((point.x-x)**2+(point.y-y)**2)**0.5 < min_dist:
                min = point
        B = min

    return Point(list(B.coords)[0][0],list(B.coords)[0][1])

def check_nearby(B,A):
    if B is not None and A.x-10**(-15)<B.x<A.x+10**(-15) and A.y-10**(-15)<B.y<A.y+10**(-15):
        return None
    else:
        return B

def get_D(A,line):
    center = Point(0,0)
    c = Circle(center,1)
    wallup = Line(Point(-2,2),Point(4,0))
    walldown = Line(Point(-2,-2),Point(4,0))
    wallsx = Line(Point(-2,2),Point(0,-4))
    walldx = Line(Point(2,2),Point(0,-4))
    B = line.intersect(c)
    interaction_object = "circle"
    B = check_nearby(B,A)
    if B is None:
        interaction_object = "wallup"
        B = line.intersect(wallup)
        B = check_nearby(B, A)
        if B is None:
            interaction_object = "walldown"
            B = line.intersect(walldown)
            B = check_nearby(B, A)
            if B is None:
                interaction_object = "walldx"
                B = line.intersect(walldx)
                B = check_nearby(B, A)
                if B is None:
                    interaction_object = "wallsx"
                    B = line.intersect(wallsx)
                    B = check_nearby(B, A)
                    if B is None:
                        print("impossible")

    if interaction_object == "circle":
        normal = Line(Point(0, 0), Point(B.x, B.y))
        parallel_tangent = Line(A,Point(B.y,-B.x))
        C = parallel_tangent.intersect(normal)
        D = normal.reflect(C)
        return B,D

    if interaction_object == "wallup" or interaction_object == "walldown":
        movement = Point(B.x-A.x,-B.y+A.y)
        D = Point(B.x+2*movement.x,B.y+2*movement.y)
        return B, D

    if interaction_object == "walldx" or interaction_object == "wallsx":
        movement = Point(-B.x+A.x,B.y-A.y)
        D = Point(B.x+2*movement.x,B.y+2*movement.y)
        return B, D

class Point():
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __repr__(self):
        return repr((self.x,self.y))

class Line():
    def __init__(self,starting_point, direction):
        self.x0 = starting_point.x
        self.y0 = starting_point.y
        self.a = direction.x
        self.b = direction.y

    def intersect(self,other):
        if type(other) == Circle:
            delta = (2*self.a*self.x0 + 2*self.b*self.y0)**2 - 4 * (self.a**2 + self.b ** 2) * (self.x0**2 + self.y0**2 - 1)
            # print(delta)
            t = 0
            if delta < 0:
                return None
            elif delta == 0:
                t = -(2*self.a*self.x0 + 2*self.b*self.x0)/(2*(self.a**2 + self.b ** 2))
            else:
                t1 = (-(2 * self.a*self.x0 + 2 * self.b*self.y0) - (delta)**0.5) / (2 * (self.a ** 2 + self.b ** 2))
                t2 = (-(2 * self.a*self.x0 + 2 * self.b*self.y0) + (delta) ** 0.5) / (2 * (self.a ** 2 + self.b ** 2))
                if abs(t1) < abs(t2):
                    t = t1
                else:
                    t = t2
            x = self.x0 + self.a * t
            y = self.y0 + self.b * t
            return Point(x, y)

        if type(other) == Line:
            t = (other.a*other.y0 - other.a*self.y0 + self.x0*other.b - other.x0*other.b)/(self.b*other.a - self.a*other.b)
            s = (self.x0 - other.x0 + self.a * t)/(other.a)
            x = self.x0 + self.a * t
            y = self.y0 + self.b * t
            return Point(x, y)

    def reflect(self,point):
        m = self.b / self.a
        q = -(self.b/self.a*self.x0 + self.y0)
        x = ((1 - m**2)*point.x + 2 * m * point.y - 2 * m * q) / (1 + m**2)
        y = (2*m*point.x + (m**2 -1)*point.y + 2*q)/(1 + m**2)
        return Point(x, y)

    def __repr__(self):
        return f"{self.x0} {self.a}*t\n{self.y0}+{self.b} * t"



class Circle():
    def __init__(self,center, radious):
        self.x0 = center.x
        self.y0 = center.y
        self.r = radious


A = Point(-2,2)
v = Point(3,-2)
l = Line(A,v)
for n in range(10):
    A, D = get_D(A, l)
    print(f"B{n+1}:", A, f"D{n+1}:", D)
    l = Line(A, Point(D.x, D.y))
