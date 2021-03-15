from math import *
def circleIntersection1(a,b,r):
    from math import *
    d=min(.5*hypot(a[0]-b[0],a[1]-b[1]),r)
    return floor(2*(r*r*acos(d/r)-d*(r*r-d*d)**.5))

from math import *;circleIntersection=lambda a,b,r:[floor(2*(r*r*acos(d/r)-d*(r*r-d*d)**.5)) for d in [min([.5*hypot(a[0]-b[0],a[1]-b[1]),r]),]][0]
from math import *;circleIntersection=lambda a,b,r:exec('d=min([.5*hypot(a[0]-b[0],a[1]-b[1]),r]);e=floor(2*(r*r*acos(d/r)-d*(r*r-d*d)**.5))')

from math import*
def circleIntersection(a,b,A,B,r):d=min(1,hypot(A-a,B-b)/2/r);return(acos(d)-d*(1-d*d)**.5)*r*r//.5

from math import*;circleIntersection=lambda a,b,r:[(acos(d)-d*(1-d*d)**.5)*r*r//.5 for d in [min(1,hypot(a[0]-b[0],a[1]-b[1])/2/r),0]][0]
from math import*;circleIntersection=lambda ((a,y),(b,z),r):r*r*(lambda d:d<1and acos(d)-d*(1-d*d)**.5)(hypot(a-b,y-z)/2/r)//.5
from math import*;circleIntersection=lambda a,b,r:r*r*(lambda h:h<1and acos(h)-h*(1-h*h)**.5)(hypot(b[0]-a[0],b[1]-a[1])/r/2)//.5


if __name__ == "__main__":
    print(circleIntersection1([0, 0],[7, 0],5)) # 14

    print(circleIntersection1([0, 0],[0, 10],10)) #122

    print(circleIntersection1([5, 6],[5, 6],3)) #28

    print(circleIntersection([0, 0],[7, 0],5)) # 14

    print(circleIntersection([0, 0],[0, 10],10)) #122

    print(circleIntersection([5, 6],[5, 6],3)) #28