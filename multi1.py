from multiprocessing import Process, Array, cpu_count, Value
from PIL import Image
from time import time

multi = 1
finalRes = (512, 512)
res = (int(finalRes[0] * multi), int(finalRes[1] * multi))
position = (-0.5449634653, 0.61856500519)#(-0.101105000001498, 0.956000000012302)#(-0.721, 0.2)
scl = 1 * 10**10 #7
maximum = 1 * 10**14
deltaScale = 1#(10**0.2) / (10**0.0)

limit = 20000

cores = cpu_count()

def mapp(n, A, B, C, D):
    return (n-A)/(B-A) * (D-C) + C

def calc(i1, i2, data, scl):
    for i in range(i1, i2):
        for j in range(res[1]):
            pos = (mapp(i, 0, res[0]-1, -2/scl + position[0], 2/scl + position[0]), mapp(j, 0, res[1]-1, 2/scl + position[1], -2/scl + position[1]))

            z = 0
            c = complex(pos[0], pos[1])
            k = 0
            while abs(z) < 2 and k < limit:
                k += 1
                z = z**2 + c
            data[i + j*res[1]] = k

if __name__ == "__main__":
    iteration = 0 # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    while True:
        curr = time()
        processes = []

        im = Image.new("HSV", res)

        p = im.load()

        data = Array('i', res[0] * res[1])

        r = int(res[0] / cores)

        for i in range(cores):
            i1 = i * r
            i2 = (i+1) * r
            processes.append(Process(target=calc, args = (i1, i2, data, scl)))
            processes[i].start()

        for i in range(len(processes)):
            processes[i].join()
            pass
        
        delta = time() - curr

        print(data)

        #twoData = []
        m = 0
        for i in range(res[0]):
            #twoData.append([])
            for j in range(res[1]):
                #twoData[i].append(data[i + j *res[1]])
                s = 360#100
                co = (int(mapp(data[i + j * res[1]] % s, 0, (s-1), 0, 359 * 6/6)), 255, 255)
                if data[i + j * res[1]] == limit:
                    co = (0, 0, 0)
                p[i,j] = co
                m = max(m, data[i + j * res[1]])
        print('max: ' + str(m))
        print(p)
        im = im.resize(finalRes, Image.BICUBIC)#Image.LANCZOS)
        im.show()
        im.convert('RGB').save('frames3/mandelbrot{}.png'.format(iteration)) #im.convert('RGB').save('mandelbrot.png'.format(iteration))
        #print(twoData)

        #print(output)
        print(delta)

        iteration += 1
        if scl >= maximum:
            break
        scl = deltaScale * scl
        print(scl)
        break