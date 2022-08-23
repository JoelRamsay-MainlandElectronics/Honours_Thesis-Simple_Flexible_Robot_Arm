#!/usr/bin/env python

import numpy as np
from roboticstoolbox.robot.ERobot import ERobot, ERobot2
from spatialmath import SE3


class EGH400_robot(ERobot):
    """
    Class that imports a Panda URDF model

    ``Panda()`` is a class which imports a Franka-Emika Panda robot definition
    from a URDF file.  The model describes its kinematic and graphical
    characteristics.

    .. runblock:: pycon

        # >>> import roboticstoolbox as rtb
        # >>> robot = rtb.models.URDF.Panda()
        # >>> print(robot)

    Defined joint configurations are:

    - qz, zero joint angle configuration, 'L' shaped configuration
    - qr, vertical 'READY' configuration
    - qs, arm is stretched out in the x-direction
    - qn, arm is at a nominal non-singular configuration

    .. codeauthor:: Jesse Haviland
    .. sectionauthor:: Peter Corke
    """

    def __init__(self):

        links, name, urdf_string, urdf_filepath = self.URDF_read(
            "EGH400_planar_robot_1_description/robot.urdf.xacro"
        )

        super().__init__(
            links,
            name=name,
            manufacturer="Joel Ramsay",
            gripper_links=None,
            urdf_string=urdf_string,
            urdf_filepath=urdf_filepath,
        )
        #print(links)

        # self.grippers[0].tool = SE3(0, 0, 0.1034)
        #
        # self.qdlim = np.array(
        #     [2.1750, 2.1750]
        # )
        #
        # self.qr = np.array([0, 0])
        # self.qz = np.zeros(7)
        #
        # self.addconfiguration("qr", self.qr)
        # self.addconfiguration("qz", self.qz)


# if __name__ == "__main__":  # pragma nocover
#
#     #r = Panda()
#
#     #r.qz
#
#     for link in r.grippers[0].links:
#         print(link)
