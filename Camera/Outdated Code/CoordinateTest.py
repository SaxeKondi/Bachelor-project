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
    rotMat = sciRot.from_rotvec(rotvec)

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


matrix = [[1,0,0],[0,0,-1],[0,1,0]]
print(matrix)

Rot = sciRot.from_matrix(matrix)

rotVec = Rot.as_rotvec()

rotation = sciRot.from_rotvec(rotVec)



print(rotation.as_euler('xyz'))