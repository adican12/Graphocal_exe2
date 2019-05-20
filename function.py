# CREATED BY:
# Yarden Hazan
# Adi Cantor
# Yaron Daya

import math


# Point structure
class Point:
    def __init__(self, x_, y_):
        self.x = x_
        self.y = y_

    def Point(self):
        self.x = 0
        self.y = 0

    def setX(self, x_):
        self.x = x_

    def setY(self, y_):
        self.y = y_

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def toString(self):
        print("point: x= %s , y= %s" % (self.x, self.y))


# get the first element in the array - indicate the type of shape to paint
def get_tag(line):
    # split the line - get first symbol
    l = line.split(":")

    # L - represent Line
    if (l[0] == "L"):
        return l[0]
    # C - represent Circle
    elif (l[0] == "C"):
        return l[0]
    # B - represent Biezier
    elif (l[0] == "B"):
        return l[0]
    else:
        print("something went wrong = function.py - get_tag")


# read from the insert file
def ReadFromFile(self, path):
    # init array
    Total = []
    Lines = ["Lines"]
    Circels = ["Circels"]
    Bezier = ["Bezier"]

    # get the path - error print
    if path == "":
        print("path is empty")
    try:
        # open file - parser to working array
        with open(path, 'r') as file:
            # read the first line
            line = file.readline()

            # while file has lines
            while line:

                # ignore empty line
                if line.strip():
                    # get the first letter from line- symbol for draw shape
                    key = get_tag(line)
                    # print(key)

                    # remove the first symbol from line
                    l = line.split(':')
                    l.pop(0)

                    #   split to array of point
                    for word in l:
                        if word != "":
                            # split each point - and insert to the correct Vector  based on key value (L , C , B)
                            b = word.split("_")
                            #
                            for t in b:
                                r = t.split(",")
                                if key == "L":
                                    p = Point(int(r[0]), int(r[1]))
                                    Lines.append(p)

                                elif key == "C":
                                    p = Point(int(r[0]), int(r[1]))
                                    Circels.append(p)

                                elif key == "B":
                                    p = Point(int(r[0]), int(r[1]))
                                    Bezier.append(p)

                                else:
                                    print("something went wrong = ReadFromFile -> line -> word -> fot t in b")

                # get the next line - till eof
                line = file.readline()
    except:
        print("file not open")

    # close the file
    file.close()
    # add the lines array to total
    Total.append(Lines)
    # add the Circle array to total
    Total.append(Circels)
    # add the Biezier array to total
    Total.append(Bezier)
    # put total
    self.total = Total


# Calculate distance between to points
def calcDistance(point_1, point_2):
    dx = (point_1.x - point_2.x)
    dy = (point_1.y - point_2.y)
    return math.sqrt((pow(dx, 2) + pow(dy, 2)))


# Calculate Scale - new position for point
def ScalePaint(self):
    # get the change ranger
    ranger = (self.event_point[0].y - self.event_point[1].y) / self.event_point[0].y
    # make sure ranger is nut 0
    if ranger != 0:
        # if ranger < 0 then add 1 and the value as ABS - Because ranger is ratio
        if ranger < 0:
            ranger = abs(ranger) + 1
        try:
            #  for every point multiply by ratio
            for t in self.total:
                if t[0] == "Lines" or t[0] == "Bezier":
                    for i in range(1, len(t)):
                        # print(t[i])
                        t[i].x = t[i].x * ranger
                        t[i].y = t[i].y * ranger
                #  circle are different - Because ine point represent center and the other radius
                if t[0] == "Circels":
                    for i in range(1, len(t) - 1, 2):
                        radius = int(calcDistance(t[i], t[i + 1]))
                        t[i].x = t[i].x * ranger
                        t[i].y = t[i].y * ranger
                        radius = int(radius * ranger)
                        t[i + 1].x = t[i].x + radius
                        t[i + 1].y = t[i].y
        except:
            print("total is empty")


# Calculate Move - new position for point
def movePaint(self):
    # check for valid distance
    ranger = max(abs(self.event_point[1].x - self.event_point[0].x), abs(self.event_point[1].y - self.event_point[0].y))

    # make sure ranger is none 0
    if ranger != 0:
        # calculate dx dy
        dx = (self.event_point[1].x - self.event_point[0].x)
        dy = (self.event_point[1].y - self.event_point[0].y)
        try:
            # for every point add dx dy accordingly
            for t in self.total:
                if t[0] == "Lines" or t[0] == "Circels" or t[0] == "Bezier":
                    for i in range(1, len(t)):
                        # print(t[i])
                        t[i].x = t[i].x + dx
                        t[i].y = t[i].y + dy
        except:
            print("total is empty")


# Calculate Rotation - new position for point
def rotatePaint(self):
    # calculate angel based on the y difference
    angleY = (self.event_point[0].y - self.event_point[1].y) / self.event_point[0].y

    # get the angle with right degree - radiant
    angle = angleY * (math.pi / 180)
    # calculate sin and cos
    sinAngle = math.sin(angle)
    cosAngle = math.cos(angle)
    try:
        # for every point - calc new position
        for t in self.total:
            if t[0] == "Lines" or t[0] == "Bezier":
                for i in range(1, len(t)):
                    t[i].x = int((t[i].x * cosAngle) - (t[i].y * sinAngle))
                    t[i].y = int((t[i].x * sinAngle) + (t[i].y * cosAngle))

            # 'circle' are different because of structure
            elif t[0] == "Circels":
                for i in range(1, len(t) - 1, 2):
                    radius = int(calcDistance(t[i], t[i + 1]))
                    t[i].x = int((t[i].x * cosAngle) - (t[i].y * sinAngle))
                    t[i].y = int((t[i].x * sinAngle) + (t[i].y * cosAngle))
                    t[i + 1].x = t[i].x + radius
                    t[i + 1].y = t[i].y
    except:
        print("total is empty")


# mirror according chosen point
def mirrorPoint(self):
    # mirror points based on event clicked
    # for every point calculate new position
    for t in self.total:
        if t[0] == "Lines" or t[0] == "Bezier" or t[0] == "Circels":
            for i in range(1, len(t), 1):
                if t[i].x < self.event_point[0].x:
                    t[i].x = self.event_point[0].x + (self.event_point[0].x - t[i].x)
                elif t[i].x > self.event_point[0].x:
                    t[i].x = self.event_point[0].x - (t[i].x - self.event_point[0].x)

                if t[i].y < self.event_point[0].y:
                    t[i].y = self.event_point[0].y + (self.event_point[0].y - t[i].y)
                elif t[i].y > self.event_point[0].y:
                    t[i].y = self.event_point[0].y - (t[i].y - self.event_point[0].y)


# Calculate Mirror Y - new position for point
def mirrorYPaint(self):
    # for every point - calculate new Y position based on half screen point
    for t in self.total:
        if t[0] == "Lines" or t[0] == "Bezier" or t[0] == "Circels":
            for i in range(1, len(t), 1):
                if t[i].y < (self.screen_HEIGHT / 2):
                    t[i].y = (self.screen_HEIGHT / 2) + ((self.screen_HEIGHT / 2) - t[i].y)
                elif t[i].y > (self.screen_HEIGHT / 2):
                    t[i].y = (self.screen_HEIGHT / 2) - (t[i].y - (self.screen_HEIGHT / 2))


# Calculate Mirror X - new position for point
def mirrorXPaint(self):
    # for every point - calculate new X position based on half screen point
    for t in self.total:
        if t[0] == "Lines" or t[0] == "Bezier" or t[0] == "Circels":
            for i in range(1, len(t), 1):
                if t[i].x < (self.screen_WIDTH / 2):
                    t[i].x = (self.screen_WIDTH / 2) + ((self.screen_WIDTH / 2) - t[i].x)
                elif t[i].x > (self.screen_WIDTH / 2):
                    t[i].x = (self.screen_WIDTH / 2) - (t[i].x - (self.screen_WIDTH / 2))


# Calculate Shearing X - new position for point
def ShearingX(self):
    # calculate ranger
    ranger = (self.event_point[1].y - self.event_point[0].y) / self.event_point[0].y
    # make sure ranger in none 0
    if ranger != 0:
        try:
            # for every Y - calculate new positon
            for t in self.total:
                if t[0] == "Lines" or t[0] == "Bezier":
                    for i in range(1, len(t)):
                        t[i].y = t[i].y + ranger * t[i].y

                if t[0] == "Circels":
                    for i in range(1, len(t), 2):
                        radius = int(calcDistance(t[i], t[i + 1]))
                        t[i].y = t[i].y + (t[i].y * ranger)
                        t[i + 1].y = t[i].y
                        t[i + 1].x = t[i].x + radius
        except:
            print("total is empty")


# Calculate Shearing Y - new position for point
def ShearingY(self):
    # calculate ranger
    ranger = (self.event_point[1].x - self.event_point[0].x) / self.event_point[0].x
    # make sure ranger in none 0
    if ranger != 0:
        try:
            # for every X - calculate new positon
            for t in self.total:
                if t[0] == "Lines" or t[0] == "Bezier":
                    for i in range(1, len(t)):
                        t[i].x = t[i].x + ranger * t[i].y
                if t[0] == "Circels":
                    for i in range(1, len(t), 2):
                        radius = int(calcDistance(t[i], t[i + 1]))
                        t[i].x = t[i].x + (t[i].y * ranger)
                        t[i + 1].y = t[i].y
                        t[i + 1].x = t[i].x + radius
        except:
            print("total is empty")


# normalize points
def normalizePoints(self):
    # check first if paint loaded
    if not self.total == 0:
        self.maxX = self.total[0][1].x
        self.minX = self.total[0][1].x
        self.maxY = self.total[0][1].y
        self.minY = self.total[0][1].y

        # find minimum and maximum points
        for t in self.total:
            if t[0] == "Lines" or t[0] == "Circels" or t[0] == "Bezier":
                for i in range(1, len(t)):
                    if t[i].x > self.maxX:
                        self.maxX = t[i].x
                    if t[i].y > self.maxY:
                        self.maxY = t[i].y
                    if t[i].x < self.minX:
                        self.minX = t[i].x
                    if t[i].y < self.minY:
                        self.minY = t[i].y

        # calculate center paint point
        self.center_paint.x = (self.maxX + self.minX) / 2
        self.center_paint.y = (self.maxY + self.minY) / 2


# fix paint size - and move to head point
def fixSize(self):
    # move paint to head start (0,0)
    dx = self.minX
    dy = self.minY
    try:
        for t in self.total:
            if t[0] == "Lines" or t[0] == "Circels" or t[0] == "Bezier":
                for i in range(1, len(t)):
                    t[i].x = t[i].x - dx
                    t[i].y = t[i].y - dy
    except:
        print("total is empty")

    # find Scale value
    ratioScaleX = (self.screen_WIDTH / self.maxX) * 0.8
    ratioScaleY = (self.screen_HEIGHT / self.maxY) * 0.8

    # make sure ratio in not 0
    if not ratioScaleY or ratioScaleY != 0:
        # if scale ratio for x is bigger - then scale based on Y
        if ratioScaleX > ratioScaleY:
            try:
                for t in self.total:
                    if t[0] == "Lines" or t[0] == "Bezier":
                        for i in range(1, len(t)):
                            t[i].x = t[i].x * ratioScaleY
                            t[i].y = t[i].y * ratioScaleY

                    if t[0] == "Circels":
                        for i in range(1, len(t) - 1, 2):
                            radius = int(calcDistance(t[i], t[i + 1]))
                            t[i].x = t[i].x * ratioScaleY
                            t[i].y = t[i].y * ratioScaleY
                            radius = int(radius * ratioScaleY)
                            t[i + 1].x = t[i].x + radius
                            t[i + 1].y = t[i].y
            except:
                print("total is empty")

        # if scale ratio for y is bigger - then scale based on X
        elif ratioScaleX < ratioScaleY:
            try:
                for t in self.total:
                    if t[0] == "Lines" or t[0] == "Bezier":
                        for i in range(1, len(t)):
                            t[i].x = t[i].x * ratioScaleX
                            t[i].y = t[i].y * ratioScaleX
                    if t[0] == "Circels":
                        for i in range(1, len(t) - 1, 2):
                            radius = int(calcDistance(t[i], t[i + 1]))
                            t[i].x = t[i].x * ratioScaleX
                            t[i].y = t[i].y * ratioScaleX
                            radius = int(radius * ratioScaleX)
                            t[i + 1].x = t[i].x + radius
                            t[i + 1].y = t[i].y
            except:
                print("total is empty")


# Center paint
def centerPaint(self):
    # find range between max point to center point
    ranger = max(abs((self.screen_WIDTH / 2) - self.center_paint.x),
                 abs((self.screen_HEIGHT / 2) - self.center_paint.y))
    # find dx and dy -- We used adjustment  = 50 pixel to center
    dx = (self.screen_WIDTH / 2) - self.center_paint.x - 50
    dy = (self.screen_HEIGHT / 2) - self.center_paint.y - 50

    # check range is not 0
    if ranger != 0:
        try:
            # move point with dx dy
            for t in self.total:
                if t[0] == "Lines" or t[0] == "Circels" or t[0] == "Bezier":
                    for i in range(1, len(t)):
                        # print(t[i])
                        t[i].x = t[i].x + dx
                        t[i].y = t[i].y + dy
        except:
            print("total is empty")
