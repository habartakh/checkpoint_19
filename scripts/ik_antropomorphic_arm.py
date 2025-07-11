#!/usr/bin/env python3
from math import atan2, pi, sin, cos, pow, sqrt, hypot


from dataclasses import dataclass
@dataclass
class EndEffectorWorkingSpace:
    # Pos of The P2, which is the one we resolved for
    Pee_x: float
    Pee_y: float
    Pee_z: float


class ComputeIk():
    def __init__(self, DH_parameters):
        # DH parameters
        self.DH_parameters_ = DH_parameters


    def get_dh_param(self, name):

        if name in self.DH_parameters_:
            return self.DH_parameters_[name]
        else:
            assert False, "Asked for Non existent param DH name ="+str(name)


    def compute_ik(self, end_effector_pose, theta_2_config = "down", theta_3_config = "down"):
        # Initialization
        Pee_x = end_effector_pose.Pee_x
        Pee_y = end_effector_pose.Pee_y
        Pee_z = end_effector_pose.Pee_z


        # We get all the DH parameters
        r1 = self.get_dh_param("r1")
        r2 = self.get_dh_param("r2")
        r3 = self.get_dh_param("r3")

        print("Input Data===== ELBOW theta_2_config = "+str(theta_2_config))
        print("Input Data===== ELBOW theta_3_config = "+str(theta_3_config))
        print("Pee_x = "+str(Pee_x))
        print("Pee_y = "+str(Pee_y))
        print("Pee_z = "+str(Pee_z))
        print("r1 = "+str(r1))
        print("r2 = "+str(r2))
        print("r3 = "+str(r3))

        # We declare all the equations for theta1, theta2, theta3 and auxiliary

        #########################################################################
        # theta 1 
        if theta_2_config == "down" : 
            theta_1 = atan2(Pee_y, Pee_x)
        else : 
            theta_1 = atan2(-Pee_y, -Pee_x)

        #########################################################################
        # theta_3
        D = hypot(Pee_x, Pee_y)
        L_sq = D**2 + Pee_z**2 

        
        c3 = (L_sq - r2**2 - r3**2) / (2 * r2 * r3) #  c3 : cos(theta3)
       
        ## WE HAVE TO CHECK THAT ITS POSSIBLE
        ## -1 <= G <= 1
        possible_solution = False
        if (c3 <= 1 ) and ( c3 >= -1):
            possible_solution = True
        else:
            pass
       
        theta_array = []

        if possible_solution:
            # We have to decide which solution we want
            if theta_3_config == "down":
                # Positive
                numerator_3 = -1.0 * sqrt(1-pow(c3,2))
            else:
                numerator_3 =  sqrt(1-pow(c3,2))

            denominator_3 = c3

            theta_3 = atan2(numerator_3, denominator_3)

            if (theta_3 <= 3.0*pi/4.0 and theta_3 >= -3.0*pi /4.0):
                possible_solution = True 
            else :
                possible_solution = False  
           
            #########################################################################
            # theta2

            k1 = r2 + r3 * c3
            k2 = r3 * numerator_3

            if theta_2_config == "down":
                # Positive
                numerator_2 =  D
            else:
                numerator_2 = -1.0 * D

            theta_2 = atan2(Pee_z, numerator_2) - atan2(k2, k1)


            if (theta_2 <= 3*pi/4 and theta_2 >= -pi /4):
                possible_solution = True 
            else :
                possible_solution = False  

            theta_array = [theta_1, theta_2, theta_3]


        return theta_array, possible_solution


def calculate_ik(Pee_x, Pee_y, Pee_z, DH_parameters, theta_2_config, theta_3_config):

    ik = ComputeIk(DH_parameters = DH_parameters)
    end_effector_pose = EndEffectorWorkingSpace(Pee_x = Pee_x,
                                                Pee_y = Pee_y,
                                                Pee_z = Pee_z)


    thetas, possible_solution = ik.compute_ik(end_effector_pose=end_effector_pose, 
                                                theta_2_config=theta_2_config , theta_3_config=theta_3_config)
    print("Angles thetas solved ="+str(thetas))
    print("possible_solution = "+str(possible_solution))

   # return thetas, possible_solution
    

if __name__ == '__main__':
    r1 = 0.0
    r2 = 1.0
    r3 = 1.0
    # theta_i here are valriables of the joints
    # We only fill the ones we use in the equations, the others were already
    # replaced in the Homogeneous matrix
    DH_parameters={"r1":r1,
                    "r2":r2,
                    "r3":r3}
    Pee_x = 0.5
    Pee_y = 0.6
    Pee_z = 0.7

    configs = [
        ('up', 'up'),
        ('up', 'down'),
        ('down', 'up'),
        ('down', 'down')
    ]

    for theta1_cfg, theta3_cfg in configs:
        calculate_ik(Pee_x=Pee_x, Pee_y=Pee_y, Pee_z=Pee_z,DH_parameters=DH_parameters, theta_2_config=theta1_cfg, theta_3_config=theta3_cfg)


    