import numpy as np

area = lambda a,b,c: 0.25*np.sqrt( ((a**2)+(b**2)+(c**2))**2 - 2.*((a**4)+(b**4)+(c**4)) )

dist = lambda p0, p1: np.sqrt(np.sum((p1 - p0) ** 2))

a = dist(p0=np.vstack([836.97338867, 752.80941772]), p1=np.vstack([831.60345459, 837.93103027]))
b = dist(p0=np.vstack([855.28308105, 860.90460205]), p1=np.vstack([831.60345459, 837.93103027]))
c = dist(p0=np.vstack([855.28308105, 860.90460205]), p1=np.vstack([836.97338867, 752.80941772]))

print (a)
print (b)
print (c)

print (np.sum([a, b, c]))
print (area(a, b, c))


