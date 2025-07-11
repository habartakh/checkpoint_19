#!/usr/bin/env python3
import math 
from sympy import Matrix, cos, sin, Symbol, simplify, trigsimp, pi
from sympy.interactive import printing
from sympy import preview


class GenerateMatrices : 

    def __init__(self): 
        # To make display prety
        printing.init_printing(use_latex = True) 
    
    
    def generate_dh_matrix(self):
        theta_i = Symbol("theta_i")
        alpha_i = Symbol("alpha_i")
        r_i = Symbol("r_i")
        d_i = Symbol("d_i")


        DH_Matric_Generic = Matrix([[cos(theta_i), -sin(theta_i)*cos(alpha_i), sin(theta_i)*sin(alpha_i), r_i*cos(theta_i)],
                                    [sin(theta_i), cos(theta_i)*cos(alpha_i), -cos(theta_i)*sin(alpha_i), r_i*sin(theta_i)],
                                    [0, sin(alpha_i), cos(alpha_i), d_i],
                                    [0,0,0,1]])


        result_simpl = simplify(DH_Matric_Generic)

        # Save to local file
        # preview(result_simpl, viewer='file', filename="out.png", dvioptions=['-D','300'])

        # Now create A0_1, A1_2, A2_3

        self.theta_1 = Symbol("theta_1")
        self.theta_2 = Symbol("theta_2")
        self.theta_3 = Symbol("theta_3")

        alpha_planar = 0.0

        alpha_1 = pi / 2 
        alpha_2 = alpha_planar
        alpha_3 = alpha_planar

        self.r_1 = 0.0
        self.r_2 = Symbol("r_2")
        self.r_3 = Symbol("r_3")

        d_planar = 0.0
        d_1 = d_planar
        d_2 = d_planar
        d_3 = d_planar

        self.A0_1 = DH_Matric_Generic.subs(r_i,self.r_1).subs(alpha_i,alpha_1).subs(d_i,d_1).subs(theta_i, self.theta_1)
        self.A1_2 = DH_Matric_Generic.subs(r_i,self.r_2).subs(alpha_i,alpha_2).subs(d_i,d_2).subs(theta_i, self.theta_2)
        self.A2_3 = DH_Matric_Generic.subs(r_i,self.r_3).subs(alpha_i,alpha_3).subs(d_i,d_3).subs(theta_i, self.theta_3)

        self.A0_3 = self.A0_1 * self.A1_2 * self.A2_3
        self.A0_2 = self.A0_1 * self.A1_2

        self.A0_3_simplified = trigsimp(self.A0_3)
        self.A0_2_simplified = trigsimp(self.A0_2)
    

    def preview_matrices(self):
        # We save
        preview(self.A0_1, viewer='file', filename="A0_1.png", dvioptions=['-D','300'])
        preview(self.A1_2, viewer='file', filename="A1_2.png", dvioptions=['-D','300'])
        preview(self.A2_3, viewer='file', filename="A2_3.png", dvioptions=['-D','300'])

        preview(self.A0_3, viewer='file', filename="A0_3.png", dvioptions=['-D','300'])
        preview(self.A0_3_simplified, viewer='file', filename="A0_3_simplified.png", dvioptions=['-D','300'])
        preview(self.A0_2_simplified, viewer='file', filename="A0_2_simplified.png", dvioptions=['-D','300'])


def main():
    
    matrices_generator = GenerateMatrices()

    # Call a method on the object
    matrices_generator.generate_dh_matrix()
    matrices_generator.preview_matrices()

    print("DH Matrices generated!")

if __name__ == "__main__":
    main()