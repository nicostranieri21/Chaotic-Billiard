from shapely.geometry import LineString
from shapely.geometry import Point

A = Point(0,0)
c = A.buffer(1).boundary
l = LineString([(-2,2), (2, -2)])
i = c.intersection(l)
print(i)
B = None
if i.type == "Point":
    B = i
else:
    for point in i:
        if B is None:
            B = point
            break
print(B)
print("ey")


