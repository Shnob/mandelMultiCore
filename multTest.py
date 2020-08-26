from multiprocessing import Process, Array, cpu_count

def f(i, x, a):
    a[i] = (x)

if __name__ == "__main__":
    ps = []

    print(cpu_count())

    arr = Array('i', range(100))

    for i in range(100):
        ps.append(Process(target=f, args=(i, i, arr)))
        ps[i].start()
    
    for i in ps:
        i.join()
    
    print(list(arr))