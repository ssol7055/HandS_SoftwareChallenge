from typing import List
from math import inf
from SBSim import (
    VacuumCleaner,
    STAY,
    MOVE,
    CLEN,
    CHAR,
)
from SBSim.base import UserMap
import random
'''
    WARNING
    Do not change def name, arguments and return.
    ---
'''

class UserRobot(VacuumCleaner):
    def __init__(
        self,
        fuel: int = 100,
        energy_consumption: int = 10,
        move_consumption: int = 10,
        postion: List[int] = ...,
        vision_sight: int = 2
    ) -> None:
        super().__init__(
            fuel=fuel,
            energy_consumption=energy_consumption, 
            move_consumption=move_consumption,
            postion=postion, 
            vision_sight=vision_sight
        )
        '''
            If you want to store some values, define your variables here.
            Using `self`-based variables, you can re-call the value of previous state easily.
        '''
        self.dir_x = 0
        self.dir_y = 0
        self.num1 = 0
        self.num2 = 0

    def algorithms( self, grid_map: UserMap ):
        '''
            You can code your algorithm using robot.position and map.information. The following
            introduces accessible data; 1) the position of robot, 2) the information of simulation
            map.

            Here, you should build an algorithm that determines the next action of 
            the robot.

            Robot::
                - position (list-type) : (x, y)
                - mode (int-type) ::
                    You can determine robot state using 'self.mode', and we provide 4-state.
                    (STAY, MOVE, CLEN, CHAR)
                    Example::
                        1) You want to move the robot to target position.
                        >>> self.mode = MOVE
                        2) Clean-up tail.
                        >>> self.mode = CLEN
            
            map::
                - grid_map :
                    grid_map.height : the value of height of map.
                        Example::
                            >>> print( grid_map.height )

                    grid_map.width : the value of width of map.
                        Example::
                            >>> print( grid_map.width )

                    grid_map[ <height/y> ][ <width/x> ] : the data of map, it consists of 2-array.
                        - grid_map[<h>][<w>].req_energy : the minimum energy to complete cleaning.
                            It is assigned randomly, and it is int-type data.
                        - grid_map[<h>][<w>].charger : is there a charger in this tile? boolean-type data.
                        Example::
                            >>> x = self.position.x
                            >>> y = self.position.y
                            >>> print( grid_map[y][x].req_energy )
                            >>> if grid_map[y][x].req_energy > 0:
                            >>>     self.mode = CLEN

            Tip::
                - Try to avoid loop-based codes such as `while` as possible. It will make the problem harder to solve.
        '''
        #### Code Here! ####
        
        #THIS IS AN EXAMPLE CODE. DELETE THIS CODE SEGMENT BEFORE YOU START YOUR OWN CODE.
        #START OF EXAMPLE CODE

        # Default information from robot and env.
        robot_x = self.position.x
        robot_y = self.position.y
        
        if grid_map.map[robot_y][robot_x].charger:
            if self.dir_x != 0 or self.dir_y != 0:
                self.mode = CHAR
                if self._fuel == self._init_fuel:
                    self.mode = MOVE

        if self.mode == STAY:
            self.mode = MOVE
            self.dir_x = 1
            self.dir_y = 0

        if self.dir_x == 1 and robot_x == 16:
            self.dir_x = 0
            self.dir_y = -1          
            
        if self.dir_y == -1 and robot_y == 0:
            self.dir_x = -1
            self.dir_y = 0
        
        if self.dir_x == -1 and robot_x == 8 and robot_y == 0:
            self.dir_x = 0
            self.dir_y = 1

        if self.dir_y == 1 and robot_x == 0 and robot_y == 16:
            self.dir_x = 1
            self.dir_y = 0

        if self.dir_x == 1 and robot_x == 8 and robot_y == 16:
            self.dir_x = 0
            self.dir_y = -1
                    
        if self.dir_y == 1 and robot_y == 16:
            if self.num2 % 2:
                self.dir_x = -1
                self.dir_y = 0
            else:
                self.dir_x = 1
                self.dir_y = 0

        if self.dir_x == -1 and robot_x == 0:
            if self.num1 % 2:
                self.dir_x = 0
                self.dir_y = -1
                self.num1 += 1
            else:
                self.dir_x = 0
                self.dir_y = 1
                self.num1 += 1

        if robot_x+self.dir_x < 0 or robot_x+self.dir_x > 16:
            self.dir_x, self.dir_y = self.dir_y, self.dir_x

        if robot_y+self.dir_y < 0 or robot_y+self.dir_y > 16:
            self.dir_x, self.dir_y = self.dir_y, self.dir_x

        if grid_map.map[robot_y+self.dir_y][robot_x+self.dir_x].req_energy == inf:
            self.dir_x, self.dir_y = random.choice([1, -1]) * self.dir_y, random.choice([-1, 1]) * self.dir_x
        
        if grid_map.map[robot_y][robot_x].req_energy != 0 and grid_map.map[robot_y][robot_x].charger == False:
            self.mode = CLEN
        elif grid_map.map[robot_y][robot_x].charger == False:
            self.mode = MOVE

        new_x = robot_x + self.dir_x
        new_y = robot_y + self.dir_y
            

        #END OF EXAMPLE CODE

        ######################

        ##### DO NOT CHANGE RETURN VARIABLES! #####
        ## The below codes are fixed. The users only determine the mode and/or the next position (coordinate) of the robot.
        ## Therefore, you need to match the variables of return to simulate.
        (new_x, new_y) = self.tunning( [new_x, new_y] )
        return (new_x, new_y)
