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
    rotation = np.array(rotation)

    rotMat = fixedAngleXYZ_2_RotMat(rotation)
    rotVec = rotMat_2_rotVec(rotMat)
    return rotVec

def rotateTCP(rotVec, rotation):
    rotVec = np.array(rotVec)
    rotation = np.array(rotation)

    RBase2TCP = rotVec_2_rotMat(rotVec)                                 #Get rotation matrix from base to tcp
    angles = np.matmul(RBase2TCP, rotation)             #Find the speed of the TCP seen from base
    return angles.round(10).tolist()


def speedTCP_2_base(rotVec, xyzSpeed):
    rotVec = np.array(rotVec)
    xyzSpeed = np.array(xyzSpeed)

    RBase2TCP = rotVec_2_rotMat(rotVec)                                 #Get rotation matrix from base to tcp
    xyzSpeedBase = np.matmul(RBase2TCP, xyzSpeed)             #Find the speed of the TCP seen from base
    return xyzSpeedBase.round(10).tolist()




