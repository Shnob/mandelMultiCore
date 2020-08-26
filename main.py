from PIL import Image
import time

constant = complex(-0.69,0.25)
julia = False

pos = (0, 0)#(-1.76, 0)#-0.24509848)
#pos = (-3/4, 0)
scl = 1#10**5

max = 1000#0

im = Image.new("HSV", (512, 512))

p = im.load()

currTime = time.time()
startTime = time.time()

def mapp(n, A, B, C, D):
    return (n-A)/(B-A) * (D-C) + C

for i in range(im.width):
    for j in range(im.height):
        x = mapp(i, 0, im.width, -2/scl, 2/scl) + pos[0]
        y = mapp(j, 0, im.height, -2/scl, 2/scl) + pos[1]
        c = complex(x, y)
        z = 0
        if julia:
            z = c
            c = constant

        it = 0
        while abs(z) < 2 and it < max:
            it+=1
            z = z**2 + c
        v = int(float(it)%100*(255*5/6)/100)
        co = (v, 255, 255)
        if it == max:
            co = (0, 0, 0)
        p[i,j] = co
    delTime = time.time() - currTime
    if delTime > 1:
        currTime = time.time()
        print("{}%".format(round(i/im.width*100, 1)))

im.show()
print(time.time() - startTime)
im.convert('RGB').save('mandelbrot.jpeg')