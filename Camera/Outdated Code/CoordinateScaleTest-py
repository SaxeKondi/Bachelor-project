from math import *

v_init=[-0.0012, 3.1162, 0.03889]
v=[-0.06, 0.13, -0.04]

def length(v):
    return sqrt(pow(v[0],2)+pow(v[1],2)+pow(v[2],2)) 

def norm(v):
    l=length(v)
    norm=[v[0]/l, v[1]/l, v[2]/l]
    return norm

def _polyscope(x,y,z):
    if ( (abs(x) >= 0.001 and x < 0.0) or (abs(x) < 0.001 and abs(y) >= 0.001 and y < 0.0) or (abs(x) < 0.001 and abs(y) < 0.001 and z < 0.0) ):
        scale = 1 - 2*pi / length([x,y,z])
        ret = [scale*x, scale*y, scale*z]
        print("PolyScope SCALED value: ", ret)
        return ret
    else:
        ret = [x,y,z]
        print("PolyScope value: ", ret)
        return ret

def polyscope(v):
  return _polyscope(v[0], v[1], v[2])

polyscope(v_init)
polyscope(v)

def d2r(angle):
    return angle/180*pi


def r2d(angle):
    return angle*180/pi

def rpy2rv(roll,pitch,yaw):
  
    alpha = d2r(yaw)
    beta = d2r(pitch)
    gamma = d2r(roll)
    
    ca = cos(alpha)
    cb = cos(beta)
    cg = cos(gamma)
    sa = sin(alpha)
    sb = sin(beta)
    sg = sin(gamma)
    
    r11 = ca*cb
    r12 = ca*sb*sg-sa*cg
    r13 = ca*sb*cg+sa*sg
    r21 = sa*cb
    r22 = sa*sb*sg+ca*cg
    r23 = sa*sb*cg-ca*sg
    r31 = -sb
    r32 = cb*sg
    r33 = cb*cg
    
    theta = acos((r11+r22+r33-1)/2)
    sth = sin(theta)
    kx = (r32-r23)/(2*sth)
    ky = (r13-r31)/(2*sth)
    kz = (r21-r12)/(2*sth)
    
    return [(theta*kx),(theta*ky),(theta*kz)]
    
def rv2rpy(rx,ry,rz):
 
    theta = sqrt(rx*rx + ry*ry + rz*rz)
    kx = rx/theta
    ky = ry/theta
    kz = rz/theta
    cth = cos(theta)
    sth = sin(theta)
    vth = 1-cos(theta)
    
    r11 = kx*kx*vth + cth
    r12 = kx*ky*vth - kz*sth
    r13 = kx*kz*vth + ky*sth
    r21 = kx*ky*vth + kz*sth
    r22 = ky*ky*vth + cth
    r23 = ky*kz*vth - kx*sth
    r31 = kx*kz*vth - ky*sth
    r32 = ky*kz*vth + kx*sth
    r33 = kz*kz*vth + cth
    
    beta = atan2(-r31,sqrt(r11*r11+r21*r21))
  
    if(beta > d2r(89.99)):
        beta = d2r(89.99)
        alpha = 0
        gamma = atan2(r12,r22)
    elif(beta < -d2r(89.99)):
        beta = -d2r(89.99)
        alpha = 0
        gamma = -atan2(r12,r22)
    else:
        cb = cos(beta)
        alpha = atan2(r21/cb,r11/cb)
        gamma = atan2(r32/cb,r33/cb)
  
    return [r2d(gamma),r2d(beta),r2d(alpha)]




print(rv2rpy(1.075,1.627,-2.278))
print(rv2rpy(0.657,1.663,-2.003))

print(rv2rpy(0.662,-3.403,2.686))
print(rv2rpy(1.086,1.664,-2.335))

print(rv2rpy(1.938,0.61,-0.907))
print(rv2rpy(0.759,1.769,0.228))


print("PC: ")
print(rv2rpy(-0.317,1.426,-1.1))
print(rv2rpy(-0.631,-0.177,0.687))

print(rv2rpy(1.526, -3.769, 2.412))

