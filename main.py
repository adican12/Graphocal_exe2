# CREATED BY:
# Yarden Hazan
# Adi Cantor
# Yaron Daya

import os

from function import *
from tkinter import *
from tkinter import font, messagebox
import tkinter.filedialog
import shutil


# main application
class Application(Frame):
    # define variable
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.focus_force()
        self.create_widgets()
        self.type = ""
        self.total = []
        self.event_point = []
        # Center point for FIXED screen size
        self.center_screen = Point(self.screen_WIDTH / 2, self.screen_HEIGHT / 2)
        self.maxX, self.minX, self.maxY, self.minY = 0, 0, 0, 0
        self.center_paint = Point(0, 0)

    # start init gui
    def start_Paint(self):
        # initiate application parameters
        self.type = ""

        # new window pop up
        self.window = Toplevel()
        # name
        self.window.wm_title("Canvas - graphic")

        # get current screen resolution
        self.screen_WIDTH = int(self.winfo_screenwidth()*0.7)
        self.screen_HEIGHT = int(self.winfo_screenheight()*0.7)

        # make resolution string
        string_resolution = str(self.screen_WIDTH) + "x" + str(self.screen_HEIGHT)

        # dimension
        self.window.geometry(string_resolution)

        # create canvas
        self.window.canvas = Canvas(self.window, width=self.screen_WIDTH, height=self.screen_HEIGHT, bg="#ffffff")
        # attach canvas
        self.window.canvas.pack()
        # image for paint
        self.window.canvas.img = PhotoImage(width=self.screen_WIDTH, height=self.screen_HEIGHT)
        self.window.canvas.create_image((self.screen_WIDTH / 2, self.screen_HEIGHT / 2), image=self.window.canvas.img,
                                        state="normal")

        # set click counter to 0
        self.window.canvas.click2time = 0

        # Paint last paint again - try  if exist
        self.paintTotal()

        # event listener
        self.window.bind('<ButtonPress-1>', self.ActionListner)
        self.window.bind('<ButtonRelease-1>', self.dragging)

    # create widgets
    def create_widgets(self):
        self.frame = Frame(self, width=450, height=600)
        self.frame.grid(row=0, column=1)
        self.fontemp = font.Font(self, size=30, weight='bold')
        self.fontemp2 = font.Font(self, size=10, weight='bold')
        self.fontemp3 = font.Font(self, size=6, weight='normal')
        self.head = Label(self, text="Graphical Paint", font=self.fontemp)
        self.head.config(bg="#E8EAE6")
        self.head.place(x=80, y=10)

        self.Help = Button(self, text="Help", height=2, width=16, bg="#b2c8f2", font=self.fontemp2, command=self.Help)
        self.Help.place(x=60, y=100)

        self.File = Button(self, text="Open File", height=2, width=16, bg="#b2c8f2", font=self.fontemp2,
                           command=self.FileClick)
        self.File.place(x=240, y=100)

        self.Scale = Button(self, text="Scale Paint", height=2, width=16, bg="#b2c8f2", font=self.fontemp2,
                            command=self.ScaleClick)
        self.Scale.place(x=60, y=180)

        self.Move = Button(self, text="Move Paint", height=2, width=16, bg="#b2c8f2", font=self.fontemp2,
                           command=self.MoveClick)
        self.Move.place(x=240, y=180)

        self.Rotate = Button(self, text="Rotate Paint", height=2, width=16, bg="#b2c8f2", font=self.fontemp2,
                             command=self.RotateClick)
        self.Rotate.place(x=60, y=260)

        self.MirrorPoint = Button(self, text="Mirror Point", height=2, width=16, bg="#b2c8f2", font=self.fontemp2,
                                  command=self.MirrorPointClick)
        self.MirrorPoint.place(x=240, y=260)

        self.mirrorY = Button(self, text="Mirror Y", height=2, width=16, bg="#b2c8f2", font=self.fontemp2,
                              command=self.mirrorYClick)
        self.mirrorY.place(x=240, y=340)

        self.mirrorX = Button(self, text="Mirror X", height=2, width=16, bg="#b2c8f2", font=self.fontemp2,
                              command=self.mirrorXClick)
        self.mirrorX.place(x=60, y=340)

        self.ShearingX = Button(self, text="Shearing Vertical", height=2, width=16, bg="#b2c8f2", font=self.fontemp2,
                                command=self.ShearingXClick)
        self.ShearingX.place(x=60, y=420)

        self.ShearingY = Button(self, text="Shearing Horizontal", height=2, width=16, bg="#b2c8f2", font=self.fontemp2,
                                command=self.ShearingYClick)
        self.ShearingY.place(x=240, y=420)

        self.clearCanvasClick = Button(self, text="Clear Canvas", height=2, width=16, bg="#b2c8f2", font=self.fontemp2,
                                       command=self.clearCanvasClick)
        self.clearCanvasClick.place(x=60, y=500)

        self.openPaint = Button(self, text="Open Canvas", height=2, width=16, bg="#b2c8f2", font=self.fontemp2,
                                command=self.openPaintClick)
        self.openPaint.place(x=240, y=500)

        self.start_Paint()

    # main function to paint
    def paintTotal(self):
        print("patin total")
        try:
            for t in self.total:
                i = 0
                tmp = t[i]
                if (tmp == "Lines"):
                    for i in range(1, (len(t) - 1), 2):
                        self.MyLine(t[i], t[i + 1])

                elif (tmp == "Circels"):
                    for i in range(1, len(t), 2):
                        self.MyCircle(t[i], t[i + 1])

                elif (tmp == "Bezier"):
                    # print("Bezier here")
                    for i in range(1, (len(t) - 1), 4):
                        # print(i)
                        # print('i = %d, j = %d, k= %d, m= %d' % (i,i+1,i+2,i+3))
                        self.MyBezier(t[i], t[i + 1], t[i + 2], t[i + 3])
        except:
            print("total is empty")

    # read form insert file and paint
    def paintFile(self, path):
        ReadFromFile(self,path)

        # normalizePoints - find edge and center points
        normalizePoints(self)
        fixSize(self)
        # normalizePoints again after move to head (0,0) and scale- find edge and center points
        normalizePoints(self)

        # center the paint
        centerPaint(self)
        # paint again
        self.paintTotal()

    # drag event listener
    def dragging(self, event):

        # type Circle click on canvas
        if self.type == "Scale":
            if self.window.canvas.click2time == 0:
                print("something went wrong: click=0 type=Move")

            if self.window.canvas.click2time == 1:
               print("draggin heres")
               tmp2 = Point(event.x, event.y)
               self.event_point.append(tmp2)

               # calculate Move paint
               ScalePaint(self)

               # clear canvas
               self.clearCanvas()
               # paint again
               self.paintTotal()

               # initialize click counter + point array
               self.window.canvas.click2time = 0
               self.event_point = []

        elif self.type == "Move":
            print("Button Release move")
            if self.window.canvas.click2time == 0:
                print("something went wrong: click=0 type=Move")

            elif self.window.canvas.click2time == 1:
                tmp2 = Point(event.x, event.y)
                self.event_point.append(tmp2)

                # calculate Move paint
                movePaint(self)

                # clear canvas
                self.clearCanvas()
                print("after clear canvas")
                # paint again
                self.paintTotal()

                # initialize click counter + point array
                self.window.canvas.click2time = 0
                self.event_point = []

        elif self.type == "Rotate":
            print("Button Release Rotate")
            if self.window.canvas.click2time == 0:
                print("something went wrong: click=0 type=Rotate")

            elif self.window.canvas.click2time == 1:
                tmp2 = Point(event.x, event.y)
                self.event_point.append(tmp2)

                # calculate Move paint
                rotatePaint(self)

                # clear canvas
                self.clearCanvas()
                print("after clear canvas")
                # paint again
                self.paintTotal()

                # initialize click counter + point array
                self.window.canvas.click2time = 0
                self.event_point = []

        elif self.type == "ShearingX":
            print("Button Release ShearingX")
            if self.window.canvas.click2time == 0:
                print("something went wrong: click=0 type=ShearingX")

            elif self.window.canvas.click2time == 1:
                tmp2 = Point(event.x, event.y)
                self.event_point.append(tmp2)

                # calculate Move paint
                ShearingX(self)

                # clear canvas
                self.clearCanvas()
                print("after clear canvas")
                # paint again
                self.paintTotal()

                # initialize click counter + point array
                self.window.canvas.click2time = 0
                self.event_point = []

        elif self.type == "ShearingY":
            print("Button Release ShearingY")
            if self.window.canvas.click2time == 0:
                print("something went wrong: click=0 type=ShearingX")

            elif self.window.canvas.click2time == 1:
                tmp2 = Point(event.x, event.y)
                self.event_point.append(tmp2)

                # calculate Move paint
                ShearingY(self)

                # clear canvas
                self.clearCanvas()
                print("after clear canvas")
                # paint again
                self.paintTotal()

                # initialize click counter + point array
                self.window.canvas.click2time = 0
                self.event_point = []

    # click event listener
    def ActionListner(self, event):

        # type not defined
        if (self.type != ""):

            # get position event
            x, y = event.x, event.y
            print('event--  x = %s, y = %s, click= %s, type= %s ' % (x, y, self.window.canvas.click2time, self.type))

            # type Circle click on canvas
            if (self.type == "Scale"):
                # print("Scale")
                if (self.window.canvas.click2time == 0):
                    tmp1 = Point(x, y)
                    self.event_point.append(tmp1)
                    self.window.canvas.click2time = self.window.canvas.click2time + 1

            elif (self.type == "Move"):
                print("Button Release move")
                if (self.window.canvas.click2time == 0):
                    tmp1 = Point(event.x, event.y)
                    self.event_point.append(tmp1)

                    # add++ counter mouse press on canvas
                    self.window.canvas.click2time = self.window.canvas.click2time + 1

            elif (self.type == "Rotate"):
                print("Button Release Rotate")
                if (self.window.canvas.click2time == 0):
                    tmp1 = Point(event.x, event.y)
                    self.event_point.append(tmp1)

                    # add++ counter mouse press on canvas
                    self.window.canvas.click2time = self.window.canvas.click2time + 1

            elif (self.type == "MirrorPoint"):
                print("Button Release MirrorPoint")
                if (self.window.canvas.click2time == 0):
                    tmp1 = Point(event.x, event.y)
                    self.event_point.append(tmp1)

                    # calculate Move paint
                    mirrorPoint(self)

                    # clear canvas
                    self.clearCanvas()
                    print("after clear canvas")
                    # paint again
                    self.paintTotal()

                    # initialize click counter + point array
                    self.window.canvas.click2time = 0
                    self.event_point = []

            elif (self.type == "ShearingX"):
                print("Button Release ShearingX")
                if (self.window.canvas.click2time == 0):
                    tmp1 = Point(event.x, event.y)
                    self.event_point.append(tmp1)

                    # add++ counter mouse press on canvas
                    self.window.canvas.click2time = self.window.canvas.click2time + 1

            elif (self.type == "ShearingY"):
                print("Button Release ShearingY")
                if (self.window.canvas.click2time == 0):
                    tmp1 = Point(event.x, event.y)
                    self.event_point.append(tmp1)

                    # add++ counter mouse press on canvas
                    self.window.canvas.click2time = self.window.canvas.click2time + 1


        else:
            str_number = str(self.window.canvas.click2time)

            print("not choosen type , clicked:  " + str_number)

    #  -----------  drawing    function -----------
    # draw circle function
    def MyCircle(self, point1, point2):
        # get parameters

        x0 = point1.x
        y0 = point1.y
        x1 = point2.x
        y1 = point2.y

        # find radius
        radius = math.hypot(x1 - x0, y1 - y0)
        # print('radius = %s' % (radius))
        radius = round(radius)
        f = 1 - radius
        d_x = 1
        d_y = -2 * radius
        bx = 0
        by = radius
        # while loop - paint circle every time paint pixel in 8 location - til x<y
        while bx < by:
            if f >= 0:
                by -= 1
                d_y += 2
                f += d_y
            bx += 1
            d_x += 2
            f += d_x
            try:
                self.window.canvas.img.put("#000000", (round(x0 + bx), round(y0 + by)))
                self.window.canvas.img.put("#000000", (round(x0 - bx), round(y0 + by)))
                self.window.canvas.img.put("#000000", (round(x0 + bx), round(y0 - by)))
                self.window.canvas.img.put("#000000", (round(x0 - bx), round(y0 - by)))
                self.window.canvas.img.put("#000000", (round(x0 + by), round(y0 + bx)))
                self.window.canvas.img.put("#000000", (round(x0 - by), round(y0 + bx)))
                self.window.canvas.img.put("#000000", (round(x0 + by), round(y0 - bx)))
                self.window.canvas.img.put("#000000", (round(x0 - by), round(y0 - bx)))
            except Exception as e:
                print("problem with painting Circle - try again - out of boundaries ", e)

    # draw line function
    def MyLine(self, point1, point2):
        x, y = point1.x, point1.y

        ranger = max(abs(point2.x - point1.x), abs(point2.y - point1.y))

        dx = (point2.x - point1.x) / float(ranger)
        dy = (point2.y - point1.y) / float(ranger)

        # paint loop - for every step add dx dy and PUT PIXEL
        for i in range(int(ranger)):
            # print("draw process - i: " + str(i) )
            x += dx
            y += dy
            # print('x = %s, y = %s' % (((round(x), round(y)))))
            try:
                # print("try to put pixel")
                self.window.canvas.img.put("#000000", ((round(x), round(y))))
            except Exception as e:
                print("problem with painting Line - try again - out of boundaries ", e)

    # draw Bezier function
    def MyBezier(self, point1, point2, point3, point4):
        # print("MyBezier")

        array_point = []

        # get the selected point
        x1, y1 = point1.x, point1.y
        x2, y2 = point2.x, point2.y
        x3, y3 = point3.x, point3.y
        x4, y4 = point4.x, point4.y

        # X vector
        x_array = [x1, x2, x3, x4]

        # Y vector
        y_array = [y1, y2, y3, y4]

        # temp vairbale
        xu = 0.0
        yu = 0.0
        u = 0

        # calculate new PATH - every time with T change - 0 < t < 1
        while u <= 1:
            xu = pow(1 - u, 3) * x_array[0] + 3 * u * pow(1 - u, 2) * x_array[1] + 3 * pow(u, 2) * (1 - u) * x_array[
                2] + pow(u, 3) * x_array[3]
            yu = pow(1 - u, 3) * y_array[0] + 3 * u * pow(1 - u, 2) * y_array[1] + 3 * pow(u, 2) * (1 - u) * y_array[
                2] + pow(u, 3) * y_array[3]
            p = Point(xu, yu)
            array_point.append(p)
            u = u + 0.1

        for f in range(0, (len(array_point) - 1), 1):
            self.MyLine(array_point[f], array_point[f + 1])

    #  -----------  Opertion     function -----------
    # clear canvas function
    def clearCanvas(self):
        self.window.canvas.img = PhotoImage(width=self.screen_WIDTH, height=self.screen_HEIGHT)
        self.window.canvas.create_image((self.screen_WIDTH / 2, self.screen_HEIGHT / 2), image=self.window.canvas.img,
                                        state="normal")

    # open readme.txt file
    def Help(self):
        try:
            self.helpframe.destroy()
        except:
            print("help not open")

        self.helpframe = Toplevel()
        self.helpframe.geometry("700x500")

        self.helpframe.helphead = Label(self.helpframe, text="HELP", font=self.fontemp)
        self.helpframe.helphead.config(bg="#E8EAE6")
        self.helpframe.helphead.place(x=100, y=10)

        self.helpframe.helpText = Text(self.helpframe, height=100, width=100, bg="#b2c8f2", font=self.fontemp2)
        self.helpframe.helpText.place(x=0, y=80)

        quote = """Open file - press the button - choose "paint vector" file and press select

Scale Paint - press the button -  then drag the mouse on the canvas to indicate the scaling proportion

Move Paint - press the button - then drag the mouse on the canvas to indicated where the paint should be

Rotate Paint - press the button - then drag UP and DOWN the mouse on the canvas to indicate the rotation proportion

Mirror X - press on the button- to flip the paint horizontal

Mirror Y - press on the button- to flip the paint Vertical

Mirror point - press the button- press with the mouse on the canvas to indicate the mirror point of reflection

Shearing X - press on the button - then drag the mouse on the canvas to indicate the Shearing proportion for X

Shearing Y - press on the button - then drag the mouse on the canvas to indicate the Shearing proportion for Y

Clear Canvas - press on the button - clear the Canvas

Open Canvas - press on the button - reopen canvas window
"""
        self.helpframe.helpText.insert(END, quote)

    # open file from computer
    def FileClick(self):
        if (self.window.canvas.click2time == 0):
            self.type = "File"
            a = tkinter.filedialog.askopenfilename(initialdir='C:/', title='Choose file',
                                                   filetypes=[('.txt', 'txt')])
            b = "C:/Users/Public/"
            shutil.copy(a, b)
            b = b + os.path.basename(a)
            print(os.path.basename(a))
            print(b)
            self.paintFile(b)
            # print("LineClick")
        else:
            print("can't change right now! you using " + self.type)

    # -----------  button command -----------
    # button Scale
    def ScaleClick(self):
        # check for intercept
        if (self.window.canvas.click2time == 0):
            self.type = "Scale"
            # print("ScaleClick")
        else:
            print("can't change right now! you using " + self.type)

    # button Move
    def MoveClick(self):
        # check for intercept
        if (self.window.canvas.click2time == 0):
            self.type = "Move"
            # print("MoveClick")
        else:
            print("can't change right now! you using " + self.type)

    # button Rotate
    def RotateClick(self):
        # check for intercept
        if (self.window.canvas.click2time == 0):
            self.type = "Rotate"
            # print("RotateClick")
        else:
            print("can't change right now! you using " + self.type)

    # button MirrorPointClick
    def MirrorPointClick(self):
        # check for intercept
        if (self.window.canvas.click2time == 0):
            self.type = "MirrorPoint"
            # print("RotateClick")
        else:
            print("can't change right now! you using " + self.type)

    # button mirror Y
    def mirrorYClick(self):
        # check for intercept
        if (self.window.canvas.click2time == 0):
            self.type = "mirrorY"
            # print("mirrorYClick")
            mirrorYPaint(self)

            self.clearCanvas()
            print("after clear canvas")
            # paint again
            self.paintTotal()

            # initialize click counter + point array
            self.window.canvas.click2time = 0
            self.event_point = []

        else:
            print("can't change right now! you using " + self.type)

    # button mirror X
    def mirrorXClick(self):
        # check for intercept
        if (self.window.canvas.click2time == 0):
            self.type = "mirrorX"
            # print("mirrorXClick")
            mirrorXPaint(self)

            self.clearCanvas()
            print("after clear canvas")
            # paint again
            self.paintTotal()

            # initialize click counter + point array
            self.window.canvas.click2time = 0
            self.event_point = []

        else:
            print("can't change right now! you using " + self.type)

    # button Shearing X
    def ShearingXClick(self):
        # check for intercept
        if (self.window.canvas.click2time == 0):
            self.type = "ShearingX"
            # print("ShearingClick")
        else:
            print("can't change right now! you using " + self.type)

    # button Shearing Y
    def ShearingYClick(self):
        # check for intercept
        if (self.window.canvas.click2time == 0):
            self.type = "ShearingY"
            # print("ShearingClick")
        else:
            print("can't change right now! you using " + self.type)

    # button - open new Canvas
    def openPaintClick(self):
        print("start paint again")
        self.window.destroy()
        self.start_Paint()

    # button - clear canvas
    def clearCanvasClick(self):
        print("clear canvas")
        self.clearCanvas()


# start app - entry point
if __name__ == "__main__":
    root = Tk()
    app = Application(master=root)
    app.mainloop()
