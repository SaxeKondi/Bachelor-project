import numpy as np
from scipy.spatial.transform import Rotation as sciRot

class Kinematics:
    def fixedAngleXYZ_2_RotMat(rotation):
        rx = rotation[0]
        ry = rotation[1]
        rz = rotation[2]
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
        #print([x,y,z])

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

        #print(f'theta: {theta}    u: {[ux, uy, uz]}')

        rotation = sciRot.from_rotvec(rotVec)

        return rotMat

    def rotMat_2_rotVec(rotMat):
        rotation = sciRot.from_matrix(rotMat)
        return rotation.as_rotvec().round(10).tolist()
        

    def TCPOffsetRotation(rotation):

        rotMat = fixedAngleXYZ_2_RotMat(rotation)

        rotVec = rotMat_2_rotVec(rotMat)

        return rotVec

    def rotateTCP(rotVec, rotation):
        Rbase2tcp = rotVec_2_rotMat(rotVec)

        Rtcp2tcpnew = fixedAngleXYZ_2_RotMat(rotation)

        RotMat = np.matmul(Rbase2tcp, Rtcp2tcpnew)

        angles = rotMat_2_FixedAngleXYZ(RotMat)

        return angles


    def xyzSpeedTCP_2_base(rotVec, xyzSpeed):
        RBase2TCP = rotVec_2_rotMat(rotVec)                                 #Get rotation matrix from base to tcp
        xyzSpeedBase = np.matmul(RBase2TCP, np.array(xyzSpeed))             #Find the speed of the TCP seen from base
        return xyzSpeedBase