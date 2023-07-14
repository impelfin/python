import numpy as np
import cv2
import time
from PIL import Image, ImageDraw

gif_frames = []
def save_gif(frames, gifname, speed):   #speed 100
    frames[0].save(gifname, format='GIF', append_images=frames[1:], save_all=True, duration=speed, loop=0)

num_0 = (
    (2, 5, 4, 16, 0),
    (4, 7, 2, 16, 1),
    (3, 4, 0, 16, 1),
    (6, 6, 1, 16, 1),
    (5, 1, 4, 14, 0),
    (6, 6, 0, 13, 3),
    (5, 1, 4, 12, 0),
    (5, 1, 0, 11, 0),
    (6, 6, 4, 10, 1),
    (6, 6, 0, 9, 1),
    (5, 1, 1, 8, 1),
    (2, 5, 3, 8, 3))


num_1 = (
    (2, 5, 4, 16, 0),
    (3, 4, 4, 15, 1),
    (3, 4, 5, 13, 3),
    (2, 5, 4, 11, 2),
    (0, 0, 4, 8, 0))


num_2 = (
    (0, 0, 4, 16, 0),
    (3, 4, 0, 16, 1),
    (1, 2, 1, 16, 3),
    (1, 2, 1, 15, 0),
    (3, 4, 1, 12, 2),
    (1, 2, 0, 12, 1),
    (2, 5, 3, 12, 3),
    (0, 0, 4, 10, 0),
    (3, 4, 1, 8, 0),
    (2, 5, 3, 8, 3),
    (1, 2, 0, 8, 1))

num_3 = (
    (1, 2, 3, 16, 3),
    (2, 5, 0, 16, 1),
    (3, 4, 1, 15, 2),
    (0, 0, 4, 14, 0),
    (3, 4, 1, 12, 2),
    (1, 2, 0, 12, 1),
    (3, 4, 5, 12, 3),
    (2, 5, 3, 11, 0),
    (3, 4, 1, 8, 0),
    (1, 2, 0, 8, 1),
    (2, 5, 3, 8, 3))
num_4 = (
    (0, 0, 4, 16, 0),
    (0, 0, 4, 14, 0),
    (3, 4, 1, 12, 0),
    (1, 2, 0, 12, 1),
    (2, 5, 0, 10, 0),
    (2, 5, 3, 12, 3),
    (3, 4, 4, 10, 3),
    (2, 5, 0, 9, 2),
    (3, 4, 5, 10, 1))

num_5 = (
    (0, 0, 0, 16, 0),
    (2, 5, 2, 16, 1),
    (2, 5, 3, 15, 0),
    (3, 4, 5, 16, 1),
    (3, 4, 1, 12, 0),
    (1, 2, 0, 12, 1),
    (2, 5, 3, 12, 3),
    (0, 0, 0, 10, 0),
    (3, 4, 1, 8, 2),
    (1, 2, 0, 8, 1),
    (2, 5, 3, 8, 3))

num_6 = (
    (2, 5, 0, 16, 1),
    (5, 1, 2, 16, 1),
    (6, 6, 0, 15, 3),
    (6, 6, 4, 16, 3),
    (5, 1, 4, 14, 0),
    (3, 4, 1, 12, 2),
    (2, 5, 0, 13, 2),
    (3, 4, 2, 11, 0),
    (0, 0, 0, 10, 0),
    (3, 4, 1, 8, 0),
    (1, 2, 0, 8, 1),
    (2, 5, 3, 8, 3))

num_7 = (
    (0, 0, 4, 16, 0),
    (1, 2, 4, 14, 0),
    (3, 4, 5, 13, 1),
    (2, 5, 4, 11, 2),
    (3, 4, 1, 8, 2),
    (2, 5, 3, 8, 3),
    (1, 2, 0, 8, 1))

num_8 = (
    (3, 4, 1, 16, 0),
    (6, 6, 0, 16, 1),
    (3, 4, 5, 16, 1),
    (1, 2, 2, 15, 3),
    (4, 7, 0, 14, 0),
    (1, 2, 1, 12, 3),
    (6, 6, 4, 13, 1),
    (2, 5, 0, 11, 1),
    (4, 7, 0, 10, 0),
    (4, 7, 4, 11, 0),
    (5, 1, 0, 8, 1),
    (5, 1, 2, 8, 1),
    (1, 2, 4, 9, 2))

num_9 = (
    (0, 0, 0, 16, 0),
    (3, 4, 2, 16, 0),
    (1, 2, 2, 15, 3),
    (1, 2, 4, 15, 2),
    (3, 4, 1, 12, 2),
    (3, 4, 5, 12, 3),
    (5, 1, 0, 12, 0),
    (1, 2, 2, 11, 3),
    (5, 1, 4, 9, 0),
    (6, 6, 0, 10, 1),
    (5, 1, 0, 8, 1),
    (6, 6, 2, 8, 2))

'''BGR'''
myRED = (0, 0, 255)
myGREEN = (0, 255, 0)
myBLUE = (255, 73, 48)
myWHITE = (255, 255, 255)
myYELLOW = (0, 255, 255)
myCYAN = (255, 255, 0)
myMAGENTA = (255, 0, 255)
myORANGE = (255, 165, 0)
myBLACK = (45, 45, 45)

myCOLORS = (myRED, myGREEN, myBLUE, myWHITE, myYELLOW, myCYAN, myMAGENTA, myORANGE)
mynums = (num_0, num_1, num_2, num_3, num_4, num_5, num_6, num_7, num_8, num_9)
scale = 20
x_shift = 2
y_shift = 1

'''
Don't make shape, just paint the pixel.
rotate:  %4 => 0 ~ 3 
'''
def draw_shape(canvas, x, y, color, shape, rotate, y_pos):
    tcanvas = canvas.copy()
    rot = rotate % 4
    ret = False
    if shape == 0:  #rantangle
        if rot == 0 or rot == 1 or rot == 2 or rot == 3:
            for i in range(x, x + 2*scale):
                for j in range(y + 0*scale, y + 2*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
    elif shape == 1: 
        if rot == 3:
            for i in range(x + 2*scale, x + 3*scale):
                for j in range(y + 1*scale, y + 2*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
            for i in range(x , x + 3*scale):
                for j in range(y + 2*scale, y + 3*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
        elif rot == 0:
            for i in range(x , x + 1*scale):
                for j in range(y, y + 3*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
            for i in range(x + 1*scale, x + 2*scale):
                for j in range(y + 2*scale, y + 3*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
        elif rot == 1:
            for i in range(x , x + 3*scale):
                for j in range(y + 1*scale, y + 2*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
            for i in range(x, x + 1*scale):
                for j in range(y + 2*scale, y + 3*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
        elif rot == 2:
            for i in range(x , x + 2*scale):
                for j in range(y + 1*scale, y + 2*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
            for i in range(x + 1*scale, x + 2*scale):
                for j in range(y + 2*scale, y + 4*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
    elif shape == 2: 
        if rot == 1:
            for i in range(x, x + 1*scale):
                for j in range(y + 1*scale, y + 2*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
            for i in range(x , x + 3*scale):
                for j in range(y + 2*scale, y + 3*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
        elif rot == 2:
            for i in range(x, x + 2*scale):
                for j in range(y + 0*scale, y + 1*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
            for i in range(x , x + 1*scale):
                for j in range(y + 0*scale, y + 3*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
        elif rot == 3:
            for i in range(x, x + 3*scale):
                for j in range(y + 1*scale, y + 2*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
            for i in range(x + 2*scale , x + 3*scale):
                for j in range(y + 2*scale, y + 3*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
        elif rot == 0:
            for i in range(x, x + 1*scale):
                for j in range(y + 2*scale, y + 3*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
            for i in range(x + 1*scale , x + 2*scale):
                for j in range(y, y + 3*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True

    elif shape == 3:
        if rot == 0 or rot == 2:
            for i in range(x, x + 4*scale):
                for j in range(y + 2*scale, y + 3*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
        elif rot == 1 or rot == 3:
            for i in range(x, x + 1*scale):
                for j in range(y, y + 4*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True

    elif shape == 4:
        if rot == 0:
            for i in range(x, x + 1*scale):
                for j in range(y, y + 2*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
            for i in range(x + 1*scale, x + 2*scale):
                for j in range(y + 1*scale, y + 3*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
        elif rot == 1:
            for i in range(x + 1*scale, x + 3*scale):
                for j in range(y, y + 1*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
            for i in range(x , x + 2*scale):
                for j in range(y + 1*scale, y + 2*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
        elif rot == 2:
            for i in range(x, x + 1*scale):
                for j in range(y, y + 2*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
            for i in range(x + 1*scale , x + 2*scale):
                for j in range(y + 1*scale, y + 3*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
        elif rot == 3:
            for i in range(x + 1*scale, x + 3*scale):
                for j in range(y, y + 1*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
            for i in range(x, x + 2*scale):
                for j in range(y + 1*scale, y + 2*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True

    elif shape == 5:
        if rot == 0:
            for i in range(x, x + 1*scale):
                for j in range(y + 1*scale, y + 3*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
            for i in range(x + 1*scale, x + 2*scale):
                for j in range(y, y + 2*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
        elif rot == 1:
            for i in range(x, x + 2*scale):
                for j in range(y, y + 1*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
            for i in range(x + 1*scale, x + 3*scale):
                for j in range(y + 1*scale, y + 2*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
        elif rot == 2:
            for i in range(x, x + 1*scale):
                for j in range(y + 1*scale, y + 3*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
            for i in range(x + 1*scale, x + 2*scale):
                for j in range(y, y + 2*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
        elif rot == 3:
            for i in range(x, x + 2*scale):
                for j in range(y, y + 1*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
            for i in range(x + 1*scale, x + 3*scale):
                for j in range(y + 1*scale, y + 2*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True

    elif shape == 6:
        if rot == 0:
            for i in range(x + 1*scale, x + 2*scale):
                for j in range(y, y + 1*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
            for i in range(x, x + 3*scale):
                for j in range(y + 1*scale, y + 2*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
        elif rot == 1:
            for i in range(x, x + 1*scale):
                for j in range(y, y + 3*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
            for i in range(x + 1*scale, x + 2*scale):
                for j in range(y + 1*scale, y + 2*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
        elif rot == 2:
            for i in range(x, x + 3*scale):
                for j in range(y, y + 1*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
            for i in range(x + 1*scale, x + 2*scale):
                for j in range(y + 1*scale, y + 2*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
        elif rot == 3:
            for i in range(x, x + 1*scale):
                for j in range(y + 1*scale, y + 2*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True
            for i in range(x + 1*scale, x + 2*scale):
                for j in range(y, y + 3*scale):
                    tcanvas[j, i] = color
                    if j == (y_pos - 1):
                        ret = True

    return tcanvas, ret

def animate_number(canvas, n, x_shift,  y_shift):
    tcanvas = canvas.copy()
    num = mynums[n]
    for i in num:
        print(i)
        shape = i[0]
        color = myCOLORS[i[1]]
        x_pos = i[2] + x_shift
        y_pos = i[3] - y_shift
        rotation = i[4]
        y = 0
        rot = 0

        while True:
            mycanvas, ret = draw_shape(tcanvas, x_pos * scale, y * scale, color, shape, rot, y_pos * scale)
            # cv2.imshow("%d"%(n), mycanvas)
            cv2.imshow("Tetris", mycanvas)
            rgb = cv2.cvtColor(mycanvas, cv2.COLOR_BGR2RGB) 
            im_pil = Image.fromarray(rgb)
            gif_frames.append(im_pil)

            cv2.waitKey(50)
            y += 1
            if rot != rotation:
                rot += 1
            if ret == True:
                break    
        tcanvas = mycanvas.copy()
        cv2.waitKey(100)
    return mycanvas

    cv2.waitKey(0)

def make_canvas(h, w, color):
    # canvas = np.zeros([(h + 1) * scale,(w + 1) * scale,3], dtype=np.uint8)
    canvas = np.zeros([(h ) * scale,(w ) * scale,3], dtype=np.uint8)
    canvas.fill(color)
    return canvas

def test_shape():
    for shape in range(0, 7):
        for rotate in range(0, 4):
            print(shape)
            tcanvas, _ = draw_shape(canvas, 0, 0, myBLUE, shape, rotate, y_shift)
            cv2.imshow("tetris", tcanvas)
            cv2.waitKey(0)

def set_scale(s):
    global scale
    scale = s


if __name__ == '__main__':
    set_scale(20)
    canvas = make_canvas(16 * int(scale / 20 + 0.5), 32 * int(scale / 4 + 0.5), 0)
    # test_shape()
    tcanv = canvas
    shift = x_shift
    for i in range(0, 10):
        tcanv = animate_number(tcanv, i,  shift , y_shift)
        shift += 11

    # save_gif(gif_frames, "f:\\tmp\\tetris.gif", 50)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
