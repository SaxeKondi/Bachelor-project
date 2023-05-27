import numpy as np
from scipy.spatial.transform import Rotation as sciRot


def fixedAngleXYZ_2_RotMat(rotation):
    rot = sciRot.from_euler('xyz', rotation) #Small xyz means extrinsic rotation ie. around axes of original coordinate system in the order xyz. Big XYZ means intrinsic rotation (around axes of the rotating system)

    return rot.as_matrix().round(10)

def rotMat_2_FixedAngleXYZ(rotMat):
    rot = sciRot.from_matrix(rotMat)

    return rot.as_euler('xyz').round(10)

def rotVec_2_rotMat(rotVec):
    rot = sciRot.from_rotvec(rotVec)

    return rot.as_matrix().round(10)

def rotMat_2_rotVec(rotMat):
    rot = sciRot.from_matrix(rotMat)

    return rot.as_rotvec().round(10).tolist()
    

def TCPOffsetRotation(rotation):

    rotMat = fixedAngleXYZ_2_RotMat(rotation)

    rotVec = rotMat_2_rotVec(rotMat)

    return rotVec.tolist()

def rotateTCP(rotVec, rotation):
    RBase2TCP = rotVec_2_rotMat(rotVec)                                 #Get rotation matrix from base to tcp
    angles = np.matmul(RBase2TCP, np.array(rotation))             #Find the speed of the TCP seen from base
    return angles.round(10).tolist()


def xyzSpeedTCP_2_base(rotVec, xyzSpeed):
    RBase2TCP = rotVec_2_rotMat(rotVec)                                 #Get rotation matrix from base to tcp
    xyzSpeedBase = np.matmul(RBase2TCP, np.array(xyzSpeed))             #Find the speed of the TCP seen from base
    return xyzSpeedBase.round(10).tolist()


# def rotateTCP(rotVec, rotation):
#     Rbase2tcp = rotVec_2_rotMat(rotVec)

#     Rtcp2tcpnew = fixedAngleXYZ_2_RotMat(rotation)

#     RotMat = np.matmul(Rbase2tcp, Rtcp2tcpnew)

#     angles = rotMat_2_FixedAngleXYZ(RotMat)

#     return angles.tolist()


rotmat = fixedAngleXYZ_2_RotMat([np.pi/2,0,0])
rotvec = rotMat_2_rotVec(rotmat)
angles = [0,0,0.1]
print("base til tcp:")
print(rotmat)
rotspeed = xyzSpeedTCP_2_base(rotvec, angles)
print("rotation om base:")
print(rotspeed)
rotmatnew = np.matmul(rotmat, fixedAngleXYZ_2_RotMat(angles))
print(rotmatnew)
rotvecnew = rotMat_2_rotVec(rotmatnew)
rotspeed2 = xyzSpeedTCP_2_base(rotvecnew, angles)
print(rotspeed2)