import numpy as np
from scipy.spatial.transform import Rotation as sciRot

def vecLength(vec):
    return np.sqrt(sum(i**2 for i in vec))

def normalizeVec(vec):
    return np.array(vec) / vecLength(vec)

def GiveVecLength(vec, length):
    return normalizeVec(vec) * length

def fixedAngleXYZ_2_RotMat(rx, ry, rz):
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(rx), -np.sin(rx)],
                   [0, np.sin(rx), np.cos(rx)]])

    Ry = np.array([[np.cos(ry), 0, np.sin(ry)],
                   [0, 1, 0],
                   [-np.sin(ry), 0, np.cos(ry)]])

    Rz = np.array([[np.cos(rz), -np.sin(rz), 0],
                   [np.sin(rz), np.cos(rz), 0],
                   [0, 0, 1]])

    rotMat = np.matmul(np.matmul(Rz,Ry),Rx)

    return rotMat

def rotMat_2_FixedAngleXYZ(rotMat):
    x = np.arctan2(rotMat[2,1],rotMat[2,2])
    y = np.arcsin(-rotMat[2,0])
    z = np.arctan2(rotMat[1,0], rotMat[0,0])
    print([x,y,z])

    return [x,y,z]

def rotVec_2_rotMat(rotVec):
    theta = vecLength(rotVec)
    ux = rotVec[0]/theta
    uy = rotVec[1]/theta
    uz = rotVec[2]/theta

    c = np.cos(theta)
    s = np.sin(theta)
    C = 1-np.cos(theta)

    rotMat = np.array([[ux*ux*C+c, ux*uy*C-uz*s, ux*uz*C+uy*s],
                          [uy*ux*C+uz*s, uy*uy*C+c, uy*uz*C-ux*s],
                          [uz*ux*C-uy*s, uz*uy*C+ux*s, uz*uz*C+c]])

    print(f'theta: {theta}    u: {[ux, uy, uz]}')

    return rotMat

def rotMat_2_rotVec(rotMat):
    rotation = sciRot.from_matrix(rotMat)


    return rotation.as_rotvec().round(10)
    

def TCPOffsetRotation(rotVec, rx, ry, rz):
    Rbase2tcp = rotVec_2_rotMat(rotVec)

    print(f'base til tcp: {Rbase2tcp}')

    Rtcp2tcpnew = fixedAngleXYZ_2_RotMat(rx, ry, rz)

    print(f'TCP til new tcp: {Rtcp2tcpnew}')

    R = np.matmul(Rbase2tcp, Rtcp2tcpnew)

    print(f'Base til new tcp: {R}')

    rotvecNew = rotMat_2_rotVec(R)

    return rotvecNew

def rotateTCP(rotVec, rx, ry, rz):
    Rbase2tcp = rotVec_2_rotMat(rotVec)

    print(f'base til tcp: {Rbase2tcp}')

    Rtcp2tcpnew = fixedAngleXYZ_2_RotMat(rx, ry, rz)

    print(f'TCP til new tcp: {Rtcp2tcpnew}')

    R = np.matmul(Rbase2tcp, Rtcp2tcpnew)

    print(f'Base til new tcp: {R}')

    angles = rotMat_2_FixedAngleXYZ(R)

    return angles

def xySpeedTCP_2_base(rotVec, xySpeed):
    xyzSpeed = [xySpeed[1], xySpeed[2], 0]                  #Make 3D vector so it can be multiplied with rotation matrix
    RBase2TCP = rotVec_2_rotMat(rotVec)                     #Get rotation matrix from base to tcp
    xyzSpeedBase = np.matmul(RBase2TCP, xyzSpeed)           #Find the speed of the TCP seen from base
    xySpeedBase = xyzSpeedBase[0:2]                         #Remove z component of speed as a speed in only xy is desired
    return GiveVecLength(xySpeedBase, vecLength(xySpeed))   #Give the xy-speed seen from base the desired velocity

def xyzSpeedTCP_2_base(rotVec, xyzSpeed):
    RBase2TCP = rotVec_2_rotMat(rotVec)                     #Get rotation matrix from base to tcp
    xyzSpeedBase = np.matmul(RBase2TCP, xyzSpeed)           #Find the speed of the TCP seen from base
    return xyzSpeedBase


# rotvec = [-0.3463, 1.5149263896, -1.476148737
rotvec = [-0.20849481538089476, 1.5356036402259001, -0.8114280234844693]
rotvec = [1.577, 1.346, -2.232]



# print(getRotationVector(rotvec, 10, 10, 90))

vec = [3, 4, 0, 1, 8]

npvec = np.array([5,6,7])

vec[1:3] = npvec[1:3]

# [[-0.16080479  0.3332909   0.92900969]
#  [-0.57970248  0.72990098 -0.36220105]
#  [-0.79880339 -0.59679288  0.07583799]]

# [[-0.46073588  0.52605671 -0.7148334 ]
#  [ 0.38675732 -0.60591907 -0.69518404]
#  [-0.79883742 -0.59676328  0.07571237]]
