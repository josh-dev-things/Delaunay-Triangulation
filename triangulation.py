# An implementation by Leo, Josh.
from matplotlib import patches
import matplotlib.pyplot as plt
import numpy as np
import random
import utils
import sys

# Added because I liked the pretty progress bar.


def progressbar(it, prefix="", size=60, out=sys.stdout):  # Python3.3+
    count = len(it)

    def show(j):
        x = int(size*j/count)
        print("{}[{}{}] {}/{}".format(prefix, u"█"*x, "."*(size-x), j, count),
              end='\r', file=out, flush=True)
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("\n", flush=True, file=out)


class point:
    def __init__(self, x, y) -> None:
        self.__x = x
        self.__y = y

    def __str__(self) -> str:
        return f"Point: ({self.__x}, {self.__y})"

    def __repr__(self) -> str:
        return f"Point: ({self.__x}, {self.__y})"

    def X(self) -> float:
        return self.__x

    def Y(self) -> float:
        return self.__y


class circumCircle:
    def __init__(self, centrePoint: point, radius: float) -> None:
        self.radius = radius
        self.centre = centrePoint

    def isPointContained(self, testPoint: point) -> bool:
        distanceFromCentre = utils.getMagnitudeOfVector(
            self.centre.X(), testPoint.X(), self.centre.Y(), testPoint.Y())
        if (distanceFromCentre <= self.radius):
            return True
        else:
            return False

    def getCentre(self) -> tuple:
        return (self.centre.X(), self.centre.Y())


class triangle:
    def __init__(self, p1, p2, p3) -> None:
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.circumCircle = None

        self.generateCircumCircle()

    def generateCircumCircle(self):
        p1 = point(self.p1.X(), self.p1.Y())
        p2 = point(self.p2.X(), self.p2.Y())
        p3 = point(self.p3.X(), self.p3.Y())

        # BUG
        # if (p2.Y() - p1.Y()) != 0:
        #     m_1_2 = ((p1.X() - p2.X())/(p2.Y() - p1.Y())) #Finding the gradient of the bisector of points 1 & 2
        # else:
        m_1_2 = ((p1.X() - p2.X())/(p2.Y() - p1.Y())) if (p2.Y() - p1.Y()
                                                          ) != 0 else ((p1.X() - p2.X())/(p2.Y() - p1.Y() + 0.000001))

        # try:
        #     m_2_3 = ((p2.X() - p3.X())/(p3.Y() - p2.Y())) # 2 & 3
        # except:
        #     self.generateCircumCircle(p3YOffset = p3.Y()/1000 + 1/1000)
        #     return
        m_2_3 = ((p2.X() - p3.X())/(p3.Y() - p2.Y())) if (p3.Y() - p2.Y()
                                                          ) != 0 else ((p2.X() - p3.X())/(p3.Y() - p2.Y() + 0.000001))
        # BUG

        # Finding c (y intercept, consult GCSE Maths)
        c_1_2 = ((p1.Y() + p2.Y())/2)-(((p1.X()+p2.X())/2) * m_1_2)
        c_2_3 = ((p2.Y() + p3.Y())/2)-(((p2.X()+p3.X())/2) * m_2_3)

        # This prevents a divide by zero error later on.
        if (m_2_3 - m_1_2) == 0:
            m_2_3 = m_2_3 + 0.000001

        x = (c_1_2 - c_2_3)/(m_2_3 - m_1_2)
        y = (m_1_2 * x) + c_1_2
        radius = np.sqrt(pow(p1.X()-x, 2) + pow(p1.Y()-y, 2))

        centrePoint = point(x, y)
        self.circumCircle = circumCircle(centrePoint, radius)

    def pointIsVertex(self, pointToCheck: point) -> bool:
        if pointToCheck == self.p1 or pointToCheck == self.p2 or pointToCheck == self.p3:
            return True
        else:
            return False

    def draw(self, displayCircumCircle=False):
        p1 = self.p1
        p2 = self.p2
        p3 = self.p3

        p1x = p1.X()
        p1y = p1.Y()
        p2x = p2.X()
        p2y = p2.Y()
        p3x = p3.X()
        p3y = p3.Y()

        x12, y12 = [p1x, p2x], [p1y, p2y]
        x23, y23 = [p2x, p3x], [p2y, p3y]
        x13, y13 = [p1x, p3x], [p1y, p3y]

        # print(p1x)
        plt.plot(p1x, p1y, p2x, p2y, p3x, p3y, marker="o", c="black")
        plt.plot(x12, y12, x23, y23, x13, y13, marker='o', c="black")

        if displayCircumCircle:
            circumCircle = patches.Circle(xy=(self.circumCircle.getCentre(
            )), radius=self.circumCircle.radius, fill=False, edgecolor="grey", alpha=0.1)
            plt.gca().add_patch(circumCircle)


class mesh:
    def __init__(self, initialTriangles: list) -> None:
        self.triangles = []
        for i in range(len(initialTriangles)):
            self.triangles.append(initialTriangles[i])

    def __str__(self) -> str:
        return f"Mesh with {len(self.triangles)} triangles"

    def addPoint(self, newPoint: point):
        # print(self)
        containingTriangles = []
        indicesToPop = []
        for i in range(len(self.triangles)):
            __triangle = self.triangles[i]
            if __triangle.circumCircle.isPointContained(newPoint):
                containingTriangles.append(__triangle)
                # self.triangles.pop(i)
                indicesToPop.append(i)

        # Iterate through it backwards to not throw off other index
        for index in sorted(indicesToPop, reverse=True):
            #print(f"Popping triangle at index {index}. Len Triangles: {len(self.triangles)}")
            self.triangles.pop(index)

        remesh = mesh(containingTriangles)

        # Now iterate through all triangles of mesh2 & add verticies to new array
        repoint = []
        for i in range(len(remesh.triangles)):
            thisTriangle = remesh.triangles[i]
            if not self.isOverlappingVertices(repoint, thisTriangle.p1):
                repoint.append(thisTriangle.p1)
            if not self.isOverlappingVertices(repoint, thisTriangle.p2):
                repoint.append(thisTriangle.p2)
            if not self.isOverlappingVertices(repoint, thisTriangle.p3):
                repoint.append(thisTriangle.p3)

        # Now create delta
        delta = []
        repointATan2 = []
        for __point in repoint:
            dX = __point.X() - newPoint.X()
            dY = __point.Y() - newPoint.Y()
            delta.append(point(dX, dY))
            repointATan2.append(np.arctan2(dX, dY))

        # print(repoint)

        # Sort (This may or may not work... who knows ~ Josh)
        for i in range(1, len(repoint)):
            key = repointATan2[i]
            keyPoint = repoint[i]

            # Move elements of repoint[0..i-1], that are
            # greater than key, to one position ahead
            # of their current position
            j = i-1
            while j >= 0 and key < repointATan2[j]:
                repointATan2[j+1] = repointATan2[j]
                repoint[j+1] = repoint[j]
                j -= 1
            repointATan2[j+1] = key
            repoint[j+1] = keyPoint

        # print(repoint)

        # Now make some triangles?
        for i in range(len(repoint)):
            modulus = len(repoint)
            p1 = repoint[i % modulus]  # TODO Make sure this isnt broken
            p2 = repoint[(i+1) % modulus]
            newTriangle = triangle(p1, p2, newPoint)
            newTriangle.draw()
            self.triangles.append(newTriangle)  # Add new triangle to mesh data
        # print(self)

        # self.draw()

    def isOverlappingVertices(self, vertices: list, point: point) -> bool:
        isOverlap = False
        for i in range(len(vertices)):
            thisVertex = vertices[i]
            if point.X() == thisVertex.X() and point.Y() == thisVertex.Y():
                isOverlap = True
                return isOverlap
        return isOverlap

    def draw(self):
        plt.cla()
        for triangle__ in self.triangles:
            triangle__.draw(True)
        #print("Drawn all triangles")
        plt.axis('scaled')
        plt.show()

    def cullConnections(self, pointToCull: point):
        for i in reversed(range(len(self.triangles))):
            thisTriangle = self.triangles[i]
            if thisTriangle.pointIsVertex(pointToCull):
                self.triangles.pop(i)


if __name__ == "__main__":
    # Anchor that will be eventually deleted. Anchors form the initial triangle
    a1 = point(50, 100)
    a2 = point(-100, -100)
    a3 = point(90, -90)

    points = []  # Point cloud
    masterTriangle = triangle(a1, a2, a3)
    trianglesForMesh = [masterTriangle]
    thisMesh = mesh(trianglesForMesh)
    n = int(input("Enter number of points to generate: "))
    for i in progressbar(range(n), prefix="Triangulating Mesh: "):
        plt.cla()
        # BUG Does not like overlapping points
        newPoint = point(random.random() * 10, random.random() * 10)
        thisMesh.addPoint(newPoint)
        # points.append(newPoint)
        plt.plot(newPoint.X(), newPoint.Y(), marker="o", c="teal")
        # plt.show()

    anchors = [a1, a2, a3]
    for i in progressbar(range(3), prefix="Culling Anchors: "):
        thisMesh.cullConnections(anchors[i])

    thisMesh.draw()
