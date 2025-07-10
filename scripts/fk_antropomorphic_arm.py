#!/usr/bin/env python3

from sympy import Matrix, cos, sin, Symbol, simplify, trigsimp, pi
from sympy.interactive import printing
from sympy import preview


import generate_matrices
from generate_matrices import GenerateMatrices


def robot_arm_fk(theta_1_val, theta_2_val, theta_3_val):
    ''' Given joint values theta_i, 
        return position and orientation of the end_effector frame'''
    
    generate_matrix = GenerateMatrices()
    generate_matrix.generate_dh_matrix()

    A0_3_simplified = generate_matrix.A0_3_simplified 

    theta_1 = generate_matrix.theta_1
    theta_2 = generate_matrix.theta_2
    theta_3 = generate_matrix.theta_3

    # r_1 = generate_matrix.r_1
    r_2 = generate_matrix.r_2
    r_3 = generate_matrix.r_3

    # r_1_val = 0.0
    r_2_val = 1.0 
    r_3_val = 1.0 

    A03_simplify_evaluated = A0_3_simplified.subs(theta_1,theta_1_val).subs(theta_2,theta_2_val).subs(theta_3, theta_3_val).subs(r_2, r_2_val).subs(r_3, r_3_val)

    preview(A03_simplify_evaluated, viewer='file', filename="A03_simplify_evaluated.png", dvioptions=['-D','300'])

    print("A03_simplify_evaluated generated!\n")

    # Make a copy from where we will extract both position and orientation matrices
    A03_simplify_evaluated_copy = A03_simplify_evaluated
    
    position_matrix = A03_simplify_evaluated_copy.col(-1).row_del(3)
    # position_matrix.row_del(3)

    rotation_matrix = A03_simplify_evaluated_copy.row_del(-1).col_del(-1)
    
    print("Position Matrix:")
    print(position_matrix)
    print("\n")

    print("Orientation Matrix:")
    print(rotation_matrix)

def main():
    print("The robot arm will move following FK")
    
    print("Enter theta1 value:")
    theta1 = float(input())
    print("Enter theta2 value:")
    theta2 = float(input())
    print("Enter theta3 value:")
    theta3 = float(input())
    print("\n")

    # Then move the arm according to the provided joint values
    robot_arm_fk(theta1, theta2, theta3)

if __name__ == "__main__":
    main()