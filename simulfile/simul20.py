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
        self.rightComplete = False

    def modeChange(self, grid_map, robot_x, robot_y):
        if grid_map.map[robot_y][robot_x].req_energy == 0:
            self.mode = MOVE
        else:
            self.mode = CLEN

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

        robot_x = self.position.x
        robot_y = self.position.y

        self.max_h = grid_map.height - 1
        self.max_w = grid_map.width - 1

        if self.rightComplete == False:

            if self.mode == STAY:
                self.mode = MOVE
                self.dir_x = 0
                self.dir_y = -1
        
            if robot_x == 8 and robot_y == 0:
                self.dir_x = 1
                self.dir_y = 0
                self.modeChange(grid_map, robot_x, robot_y)

            if robot_x == self.max_w - 7:
                self.dir_x = 0
                self.dir_y = 1
                self.modeChange(grid_map, robot_x, robot_y)

            if robot_x == self.max_w - 7 and robot_y == self.max_h - 1:
                self.dir_x = 1
                self.dir_y = 0
                self.modeChange(grid_map, robot_x, robot_y)

            if robot_x == self.max_w - 6:
                self.dir_x = 0
                self.dir_y = -1
                self.modeChange(grid_map, robot_x, robot_y)

            if robot_x ==  self.max_w - 6 and robot_y == 0:
                self.dir_x = 1
                self.dir_y = 0
                self.modeChange(grid_map, robot_x, robot_y)

            if robot_x == self.max_w - 5:
                self.dir_x = 0
                self.dir_y = 1
                self.modeChange(grid_map, robot_x, robot_y)

            if robot_x == self.max_w - 5 and robot_y == self.max_h - 1:
                self.dir_x = 1
                self.dir_y = 0
                self.modeChange(grid_map, robot_x, robot_y)

            if robot_x == self.max_w - 4:
                self.dir_x = 0
                self.dir_y = -1
                self.modeChange(grid_map, robot_x, robot_y)

            if robot_x ==  self.max_w - 4 and robot_y == 0:
                self.dir_x = 1
                self.dir_y = 0
                self.modeChange(grid_map, robot_x, robot_y)

            if robot_x == self.max_w - 3:
                self.dir_x = 0
                self.dir_y = 1
                self.modeChange(grid_map, robot_x, robot_y) 

            if robot_x == self.max_w - 3 and robot_y == self.max_h - 1:
                self.mode = STAY
            
                self.rightComplete = True      

        
        else:
            if robot_x == self.max_w - 3 and robot_y == 15:
                self.dir_x = -1
                self.dir_y = 0
                self.modeChange(grid_map, robot_x, robot_y) 

            if robot_x == 8 :
                self.dir_x = 0
                self.dir_y = -1
                self.modeChange(grid_map, robot_x, robot_y) 
            
            if robot_x == 8 and robot_y == 8:
                self.dir_x = 0
                self.dir_y = 0
                self.mode = CHAR
            # 이 부분에서 충전이 안 됨

            if self.mode == CHAR:
                self.mode = MOVE
                self.dir_x = 0
                self.dir_y = -1
              
            if  robot_x == 8 and robot_y == 0:
                self.dir_x = -1
                self.dir_y = 0
                self.modeChange(grid_map, robot_x, robot_y) 

            if robot_x == 7 :
                self.dir_x = 0
                self.dir_y = 1
                self.modeChange(grid_map, robot_x, robot_y)

            if robot_x == 7 and robot_y == 14:
                self.dir_x = -1
                self.dir_y = 0
                self.modeChange(grid_map, robot_x, robot_y) 

            if robot_x == 5 :
                self.dir_x = 0
                self.dir_y = -1
                self.modeChange(grid_map, robot_x, robot_y)

            if robot_x == 5 and robot_y == 11:
                self.dir_x = -1
                self.dir_y = 0
                self.modeChange(grid_map, robot_x, robot_y)

            if robot_x == 4 :
                self.dir_x = 0
                self.dir_y = -1
                self.modeChange(grid_map, robot_x, robot_y)

            if robot_x == 4 and robot_y == 0:
                self.dir_x = -1
                self.dir_y = 0
                self.modeChange(grid_map, robot_x, robot_y)

            if robot_x == 3 :
                self.dir_x = 0
                self.dir_y = 1
                self.modeChange(grid_map, robot_x, robot_y)

            if robot_x == 3 and robot_y == 9:
                self.dir_x = -1
                self.dir_y = 0
                self.modeChange(grid_map, robot_x, robot_y)

            if robot_x == 2 :
                self.dir_x = 0
                self.dir_y = -1
                self.modeChange(grid_map, robot_x, robot_y)

            if robot_x == 2 and robot_y == 0:
                self.dir_x = -1
                self.dir_y = 0
                self.modeChange(grid_map, robot_x, robot_y)

            if robot_x == 0 :
                self.dir_x = 0
                self.dir_y = 1
                self.modeChange(grid_map, robot_x, robot_y)

            if robot_x == 0 and robot_y == 16:
                self.dir_x = 0
                self.dir_y = 0
                

        new_x = robot_x + self.dir_x
        new_y = robot_y + self.dir_y

        if grid_map.map[new_y][new_x].req_energy == inf:
            self.dir_x = 0
            self.dir_y = 0

        #END OF EXAMPLE CODE

        ######################

        ##### DO NOT CHANGE RETURN VARIABLES! #####
        ## The below codes are fixed. The users only determine the mode and/or the next position (coordinate) of the robot.
        ## Therefore, you need to match the variables of return to simulate.
        (new_x, new_y) = self.tunning( [new_x, new_y] )
        return (new_x, new_y)

