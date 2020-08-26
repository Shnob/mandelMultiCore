from multiprocessing import Process, Array, cpu_count
from PIL import Image
from time import time

multi = 3
res = ((512 * multi), (512 * multi))
position = (-0.721, 0.2)
scl = 1 * 10**5

limit = 2000

cores = cpu_count()

def mapp(n, A, B, C, D):
    return (n-A)/(B-A) * (D-C) + C

def calc(i1, i2, data):
    for i in range(i1, i2):
        for j in range(res[1]):
            pos = (mapp(i, 0, res[0]-1, -2/scl + position[0], 2/scl + position[0]), mapp(j, 0, res[1]-1, -2/scl + position[1], 2/scl + position[1]))

            z = 0
            c = complex(pos[0], pos[1])
            k = 0
            while abs(z) < 2 and k < limit:
                k += 1
                z = z**2 + c
            data[i + j*res[1]] = k

if __name__ == "__main__":
    curr = time()
    processes = []

    im = Image.new("HSV", res)

    p = im.load()

    data = Array('i', res[0] * res[1])

    r = int(res[0] / cores)

    for i in range(cores):
        i1 = i * r
        i2 = (i+1) * r
        processes.append(Process(target=calc, args = (i1, i2, data)))
        processes[i].start()

    for i in range(len(processes)):
        processes[i].join()
        pass
    
    delta = time() - curr

    print(data)

    #twoData = []
    for i in range(res[0]):
        #twoData.append([])
        for j in range(res[1]):
            #twoData[i].append(data[i + j *res[1]])
            s = 100
            co = (int(mapp(data[i + j * res[1]] % s, 0, (s-1), 0, 360 * 6/6)), 255, 255)
            if data[i + j * res[1]] == limit:
                co = (0, 0, 0)
            p[i,j] = co
    print(p)
    im = im.resize(res, Image.ANTIALIAS)
    im.show()
    im.convert('RGB').save('mandelbrot.jpeg')
    #print(twoData)

    #print(output)
    print(delta)