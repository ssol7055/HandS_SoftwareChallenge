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

        self.stack = []
        self.cycle_no = 0
        self.no_clen = 0
        
        
        self.dir_x = 0
        self.dir_y = 0

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

        self.max_h = grid_map.height - 1
        self.max_w = grid_map.width - 1
        
        #return absolute value
        def absolute(inp):
            if inp > 0:
                return inp
            else:
                return (-inp)
        
        new_x = robot_x + self.dir_x
        new_y = robot_y + self.dir_y
        

        #initial state
        if self.mode == STAY:
            self.mode = MOVE
            self.dir_x = 0
            self.dir_y = 1
        
        
        #running out of battery situation
        elif (self._fuel < 180):
            print('distance left:')
            print(robot_x-8)
            print(robot_y-8)
            if robot_x != 8:
                if robot_x > 8:
                    self.dir_x = -1
                    self.dir_y = 0
                elif robot_x < 8:
                    self.dir_x = 1
                    self.dir_y = 0
                
                if grid_map.map[robot_y][robot_x + self.dir_x].req_energy == inf:
                    if robot_y != 8:
                        if robot_y > 8:
                            self.dir_y = -1
                            self.dir_x = 0
                        elif robot_y < 8:
                            self.dir_y = 1
                            self.dir_x = 0
            else:
                if robot_y != 8:
                    if robot_y > 8:
                        self.dir_y = -1
                        self.dir_x = 0
                    elif robot_y < 8:
                        self.dir_y = 1
                        self.dir_x = 0
                else:
                    self.mode = CHAR
                    
                    self.dir_x = 0
                    self.dir_y = -1
                    
                    self.cycle_no += 1
            
            
            if robot_x == 8 and robot_y == 8:
                new_x = robot_x + self.dir_x
                new_y = robot_y + self.dir_y + 1
            else:
                new_x = robot_x + self.dir_x
                new_y = robot_y + self.dir_y                 


        elif (new_x > self.max_w and self.dir_x == 1) or (new_y > self.max_h and self.dir_y == 1) or (robot_x == 0 and self.dir_x == -1) or (robot_y == 0 and self.dir_y == -1):
            if self.dir_x == 1:
                self.dir_x = 0
                self.dir_y = -1
            elif self.dir_x == -1:
                self.dir_x = 0
                self.dir_y = 1
            elif self.dir_y == 1:
                self.dir_y = 0
                self.dir_x = 1
            elif self.dir_y == -1:
                self.dir_x = -1
                self.dir_y = 0   
            new_x = robot_x + self.dir_x
            new_y = robot_y + self.dir_y
            
            self.mode = CLEN
            self.no_clen = 0
        elif grid_map.map[new_y][new_x].req_energy == inf:

            if self.dir_x == 1:
                self.dir_x = 0
                self.dir_y = -1
            elif self.dir_x == -1:
                self.dir_x = 0
                self.dir_y = 1
            elif self.dir_y == 1:
                self.dir_y = 0
                self.dir_x = 1
            else:
                self.dir_x = -1
                self.dir_y = 0   
            
            new_x = robot_x + self.dir_x
            new_y = robot_y + self.dir_y
            
            if grid_map.map[new_y][new_x].req_energy == inf:
                self.dir_x = -self.dir_x
                self.dir_y = -self.dir_y
            
            new_x = robot_x + self.dir_x
            new_y = robot_y + self.dir_y
            
            
            self.mode = CLEN
            self.no_clen = 0
        elif grid_map.map[robot_y][robot_x].req_energy == 0:
            self.mode = MOVE
            self.no_clen += 1
            
            if self.no_clen > 2:
                if self.dir_x == 1:
                    self.dir_x = 0
                    self.dir_y = -1
                elif self.dir_x == -1:
                    self.dir_x = 0
                    self.dir_y = 1
                elif self.dir_y == 1:
                    self.dir_y = 0
                    self.dir_x = 1
                elif self.dir_y == -1:
                    self.dir_x = -1
                    self.dir_y = 0   
                new_x = robot_x + self.dir_x
                new_y = robot_y + self.dir_y
                
                
        else:
            self.mode = CLEN
            self.no_clen = 0

        print(self._fuel)
        #END OF EXAMPLE CODE

        ######################

        ##### DO NOT CHANGE RETURN VARIABLES! #####
        ## The below codes are fixed. The users only determine the mode and/or the next position (coordinate) of the robot.
        ## Therefore, you need to match the variables of return to simulate.
        (new_x, new_y) = self.tunning( [new_x, new_y] )
        return (new_x, new_y)

