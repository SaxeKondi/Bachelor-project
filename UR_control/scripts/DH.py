import math as m
import numpy as np
from numpy import pi
import sympy as sp
from sympy.physics.vector import init_vprinting, vprint
init_vprinting(use_latex='mathjax', pretty_print=True)
from sympy.physics.mechanics import dynamicsymbols
theta1, theta2, theta3, theta4, theta5, theta6, theta7, alpha1, alpha2, alpha3, alpha4, alpha5, alpha6, alpha7, l1, l2, l3, l4, l5, l6, l7, d1, d2, d3, d4, d5, d6, d7, theta, alpha, a, d = dynamicsymbols('theta1 theta2 theta3 theta4 theta5 theta6 theta7 alpha1 alpha2 alpha3 alpha4 alpha5 alpha6 alpha7 l1 l2 l3 l4 l5 l6 l7 d1 d2 d3 d4 d5 d6 d7 theta alpha a d')
l1 = 0; l2 = -0.24355; l3 = -0.2132; l4 = 0; l5 = 0; l6 = 0; l7 = 0
d1 = 0.15185; d2 = 0; d3 = 0; d4 = 0.13105; d5 = 0.08535; d6 = 0.0921
alpha1 = pi / 2; alpha2 = 0; alpha3 = 0; alpha4 = pi / 2; alpha5 = -(pi / 2); alpha6 = 0; alpha7 = 0

rot = sp.Matrix([[sp.cos(theta), -sp.sin(theta)*sp.cos(alpha), sp.sin(theta)*sp.sin(alpha)],
                 [sp.sin(theta), sp.cos(theta)*sp.cos(alpha), -sp.cos(theta)*sp.sin(alpha)],
                 [0, sp.sin(alpha), sp.cos(alpha)]])

trans = sp.Matrix([a*sp.cos(theta),a*sp.sin(theta),d])

last_row = sp.Matrix([[0, 0, 0, 1]])

m = sp.Matrix.vstack(sp.Matrix.hstack(rot, trans), last_row)
# vprint(m)
# print(' ')
# m01 = m.subs({alpha:alpha1, a:l1, theta:theta1, d:d1})
# m12 = m.subs({alpha:alpha2, a:l2, theta:theta2, d:d2})
# m23 = m.subs({alpha:alpha3, a:l3, theta:theta3, d:d3})
# m34 = m.subs({alpha:alpha4, a:l4, theta:theta4, d:d4})
# m45 = m.subs({alpha:alpha5, a:l5, theta:theta5, d:d5})
# m56 = m.subs({alpha:alpha6, a:l6, theta:theta6, d:d6})
m67 = m.subs({alpha:alpha7, a:l7, theta:theta7, d:d7})
m07 = m67
# vprint(m07)
# print(' ')
mbee= sp.Matrix([[m07[0,0].simplify().evalf(), m07[0,1].simplify().evalf(), m07[0,2].simplify().evalf(), m07[0,3].simplify().evalf()],
                 [m07[1,0].simplify().evalf(), m07[1,1].simplify().evalf(), m07[0,2].simplify().evalf(), m07[1,3].simplify().evalf()],
                 [m07[2,0].simplify().evalf(), m07[2,1].simplify().evalf(), m07[2,2].simplify().evalf(), m07[2,3].simplify().evalf()],
                 [m07[3,0].simplify().evalf(), m07[3,1].simplify().evalf(), m07[3,2].simplify().evalf(), m07[3,3].simplify().evalf()]])

vprint(mbee)
# print(mbee.jacobian)

