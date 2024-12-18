# Графики остановочных путей
# v^2/2gu=s
# км/ч v^2/254=s

import matplotlib.pyplot as plt

# v в километрах в час, u - безразмерный коэффициент трения
def getMS(vh, u, minT, carSize):
    vm = vh/3.6
    
    # Расстояние в метрах M и в секундах S
    M = (vm*vm/2/9.8/u) + minT*vm
    if vm > 0:
        S  = M / vm
        Sn = (M + carSize) / vm
        N  = 3600 / Sn
    else:
        S = minT
        N = 0
    
    return (M, S, N)

def getaMS(minv, maxv, step, u, minT, carSize):
    M = []
    S = []
    N = []
    V = range(minv, maxv+step, step)
    for i, v in enumerate(V):
        [m, s, n] = getMS(v, u, minT, carSize)
        M.append(m)
        S.append(s)
        N.append(n)
    
    return (V, M, S, N)

def getMax(V, N):
    maxN = N[0]
    maxI = 0
    for i, n in enumerate(N):
        if n > maxN:
            maxN = n
            maxI = i
    
    return (maxI, V[maxI], maxN)

def getColorForI(base, length, j):
    b = [base[0], base[1], base[2]]
    
    for i, A in enumerate(b):
        colorK = A / length / 2
        b[i] = b[i] - colorK * j
    
    return (b[0], b[1], b[2])

def doPlot(us, maxv, maxs, minT = 2, carSize = 4.2, truckSize = 24.0):
    
    colorBase0 = (0, 1, 0)
    colorBase1 = (0, 0, 1)
    
    for i,u in enumerate(us):
        [V, M, S, N] = getaMS(0, maxv, 1, u, minT[0], carSize)
        line, = plt.plot(V, M, label=f"$\\mu={u}$ легковые", color=getColorForI(colorBase0, len(us), i))
    for i,u in enumerate(us):
        [V, M, S, N] = getaMS(0, maxv, 1, u, minT[1], truckSize)
        line, = plt.plot(V, M, label=f"$\\mu={u}$ грузовые", color=getColorForI(colorBase1, len(us), i))
    
    plt.title('Остановочный путь')
    plt.xlabel('V, км/ч')
    plt.ylabel('S, м')
    plt.axis([0, V[-1], 0, maxs])
    plt.legend()
    plt.grid(True, which='both')
    plt.show()
    
    plt.title('Дистанция в секундах')
    plt.xlabel('V, км/ч')
    plt.ylabel('t, c')
    for i,u in enumerate(us):
        [V, M, S, N] = getaMS(0, maxv, 1, u, minT[0], carSize)
        line, = plt.plot(V, S, label=f"$\\mu={u}$ легковые", color=getColorForI(colorBase0, len(us), i))
    for i,u in enumerate(us):
        [V, M, S, N] = getaMS(0, maxv, 1, u, minT[1], truckSize)
        line, = plt.plot(V, S, label=f"$\\mu={u}$ грузовые", color=getColorForI(colorBase1, len(us), i))
    
    plt.axis([0, V[-1], min(minT), maxs / maxv * 3.6])
    plt.legend()
    plt.grid(True, which='both')
    plt.show()
    
    shiftY = 10
    plt.title('Пропускная способность полосы')
    plt.xlabel('V, км/ч')
    plt.ylabel('n, шт/ч')
    maxN = 0
    for i,u in enumerate(us):
        [V, M, S, N] = getaMS(0, maxv, 1, u, minT[0], carSize)
        (j, maxvn, maxn) = getMax(V, N)
        labelText = f"Легковые {carSize:3} м: $\\mu={u:4}$, {round(maxvn)} км/ч {round(maxn):4} шт/ч"
        line, = plt.plot(V, N, label=labelText, color=getColorForI(colorBase0, len(us), i))
        plt.annotate(labelText, xy=(maxvn, maxn+shiftY))
        if maxN < maxn:
            maxN = maxn
    
    for i,u in enumerate(us):
        [V, M, S, N] = getaMS(0, maxv, 1, u, minT[1], truckSize)
        (j, maxvn, maxn) = getMax(V, N)
        labelText = f"Грузовые {truckSize:3} м: $\\mu={u:4}$, {round(maxvn)} км/ч {round(maxn):4} шт/ч"
        line, = plt.plot(V, N, label=labelText, color=getColorForI(colorBase1, len(us), i))
        plt.annotate(labelText, xy=(maxvn, maxn+shiftY))
        
        if maxN < maxn:
            maxN = maxn
    
    plt.axis([0, V[-1], 0, round((maxN+100)/100)*100])
    # plt.legend()
    plt.grid(True, which='both')
    plt.show()

minT = [2, 2.5]
doPlot([0.8, 0.6,  0.4], 150, 200, minT, 4.2, 24)
doPlot([0.4, 0.2, 0.08],  80, 200, minT, 4.2, 24)
