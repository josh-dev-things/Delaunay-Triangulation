# An implementation by Leo, Josh.

from matplotlib import patches
import matplotlib.pyplot as plt
import numpy as np
import random
import utils

class point:
    def __init__(self, x, y) -> None:
        self.__x = x
        self.__y = y

    def X(self) -> float:
        return self.__x

    def Y(self) -> float:
        return self.__y

class circumCircle:
    def __init__(self, centrePoint : point, radius : float) -> None:
        self.radius = radius
        self.centre = centrePoint

    def isPointContained(self, testPoint : point) -> bool:
        distanceFromCentre = utils.getMagnitudeOfVector(self.centre.X(), testPoint.X(), self.centre.Y(), testPoint.Y())
        if(distanceFromCentre <= self.radius):
            return True
        else:
            return False

    def getCentre(self) -> tuple:
        return(self.centre.X(), self.centre.Y())

class triangle:
    def __init__(self, p1, p2, p3) -> None:
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.circumCircle = None

        self.generateCircumCircle()
        self.draw()

    def generateCircumCircle(self):
        p1 = self.p1
        p2 = self.p2
        p3 = self.p3

        m_1_2 = ((p1.X() - p2.X())/(p2.Y() - p1.Y())) #Finding the gradient of the bisector of points 1 & 2
        m_2_3 = ((p2.X() - p3.X())/(p3.Y() - p2.Y())) # 2 & 3
        c_1_2 = ((p1.Y() + p2.Y())/2)-(((p1.X()+p2.X())/2) * m_1_2) #Finding c (y intercept, consult GCSE Maths)
        c_2_3 = ((p2.Y() + p3.Y())/2)-(((p2.X()+p3.X())/2) * m_2_3)
        x = (c_1_2 - c_2_3)/(m_2_3 - m_1_2)
        y = (m_1_2 * x) + c_1_2
        radius = np.sqrt(pow(p1.X()-x, 2) + pow(p1.Y()-y, 2))

        centrePoint = point(x, y)
        self.circumCircle = circumCircle(centrePoint, radius)

    def draw(self):
        p1 = self.p1
        p2 = self.p2
        p3 = self.p3

        p1x = p1.X()
        p1y = p1.Y()
        p2x = p2.X()
        p2y = p2.Y()
        p3x = p3.X()
        p3y = p3.Y()

        x12, y12 = [p1x, p2x],[p1y, p2y]
        x23, y23 = [p2x, p3x],[p2y, p3y]
        x13, y13 = [p1x, p3x],[p1y, p3y]

        print(p1x)
        plt.plot(p1x, p1y, p2x, p2y, p3x, p3y, marker="o", c="black")
        plt.plot(x12,y12,x23,y23,x13,y13, marker='o', c="black")
        circumCircle = patches.Circle(xy=(self.circumCircle.getCentre()), radius=self.circumCircle.radius, fill=False)
        plt.gca().add_patch(circumCircle)
        plt.axis('scaled')

class mesh:
    def __init__(self, initialTriangles : list) -> None:
        self.triangles = []
        for i in range(len(initialTriangles)):
            self.triangles.append(initialTriangles[i])

    def addPoint(self, newPoint : point):
        containingTriangles = []
        indicesToPop = []
        for i in range(len(self.triangles)):
            triangle = self.triangles[i]
            if triangle.circumCircle.isPointContained(newPoint):
                containingTriangles.append(triangle)
                # self.triangles.pop(i)
                indicesToPop.append(i)

        for index in indicesToPop:
            self.triangles.pop(index)

        remesh = mesh(containingTriangles)

        #Now iterate through all triangles of mesh2 & add verticies to new array
        repoint = []
        for i in range(len(remesh)):
            thisTriangle = remesh[i]
            if not self.isOverlappingVertices(repoint, thisTriangle.p1): repoint.append(thisTriangle.p1)
            if not self.isOverlappingVertices(repoint, thisTriangle.p2): repoint.append(thisTriangle.p2)
            if not self.isOverlappingVertices(repoint, thisTriangle.p3): repoint.append(thisTriangle.p3)

        #Now create delta
        delta = []
        repointATan2 = []
        for point in repoint:
            dX = point.X() - newPoint.X()
            dY = point.Y() - newPoint.Y()
            delta.append(point(dX, dY))
            repointATan2.append(np.arctan2(dX, dY))

        #Sort (This may or may not work... who knows ~ Josh)
        for i in range(1, len(repoint)):
            key = repointATan2[i]
            keyPoint = repoint[i]

            # Move elements of repoint[0..i-1], that are
            # greater than key, to one position ahead
            # of their current position
            j = i-1
            while j >=0 and key < repointATan2[j] :
                    repointATan2[j+1] = repointATan2[j]
                    repoint[j+1] = repoint[j]
                    j -= 1
            repointATan2[j+1] = key
            repoint[j+1] = keyPoint


    def isOverlappingVertices(self, vertices : list, point : point) -> bool:
        isOverlap = False
        for i in range(len(vertices)):
            thisVertex = vertices[i]
            if point.X() == thisVertex.X() and point.Y() == thisVertex.Y():
                isOverlap = True
                return isOverlap
        return isOverlap




if __name__ == "__main__":
    numberOfPoints = int(input("Enter the number of points to generate: "))
    # p1 = point(random.random(), random.random())
    # p2 = point(random.random(), random.random())
    # p3 = point(random.random(), random.random())
    a1 = point(0.5, 10) #Anchor that will be eventually deleted. Anchors form the initial triangle
    a2 = point(-10, -10)
    a3 = point(9, -9)
    
    points = [] #Point cloud
    for i in range(numberOfPoints):
        newPoint = point(random.random(), random.random())
        points.append(newPoint)
        plt.plot(newPoint.X(), newPoint.Y(), marker="o", c="teal")

    masterTriangle = triangle(a1, a2, a3)
    plt.show()