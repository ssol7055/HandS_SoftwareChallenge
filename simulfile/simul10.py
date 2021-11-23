from typing import List
from math import inf
from math import sin, cos
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
    def turn_left(self):
        """turn 90 degree counter-clockwise"""
        self.current_direction = (self.current_direction + 1) % 4
        self.turn_count += 1
        return self

    def turn_right(self):
        """turn 90 degree clockwise"""
        self.current_direction = (self.current_direction + 3) % 4
        self.turn_count += 1
        return self

    def move(self):
        """move ahead"""
        next_pos_x = self.current_position['x'] + cos(self.current_direction)
        next_pos_y = self.current_position['y'] - sin(self.current_direction)
        if not self.__can_move(next_pos_x, next_pos_y):
            self.__visited_position[str(next_pos_x) + "_" + str(next_pos_y)] = -1
            return False
        self.move_count += 1
        self.current_position['x'] = next_pos_x
        self.current_position['y'] = next_pos_y
        self.__visited_position[str(next_pos_x) + "_" + str(next_pos_y)] = 1
        #print("[x,y]" + str(self.current_position['x']) + "," + str(self.current_position['y']))
        self.path_history.append([self.current_position['x'], self.current_position['y']])
        if self.loggable:
            self.log()
        return True

    def __can_move(self, next_pos_x, next_pos_y):
        if next_pos_x < 0 or next_pos_y < 0:
            return False
        if next_pos_y >= len(self.matrix):
            return False
        if next_pos_x >= len(self.matrix[0]):
            return False
        return self.matrix[next_pos_y][next_pos_x] == 0

    def log(self):
        for i in range(len(self.matrix)):
            text = ""
            for j in range(len(self.matrix[i])):
                if i == self.current_position['y'] and j == self.current_position['x']:
                    if self.current_direction == 0:
                        text += '>'
                    elif self.current_direction == 1:
                        text += '^'
                    elif self.current_direction == 2:
                        text += '<'
                    else:
                        text += 'v'
                elif self.__visited_position.get(str(j) + "_" + str(i), None) == 1:
                    text += '*'
                elif self.matrix[i][j] == 0:
                    text += '.'
                else:
                    text += '|'
            print(text)
        print('')
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
                    grid_map.height : 8
                        Example::
                            >>> print( grid_map.height )

                    grid_map.width : 8
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

        self.max_h = grid_map.height - 1
        self.max_w = grid_map.width - 1

        if self.mode == STAY:
            self.mode = MOVE
            self.dir_x = 1
            self.dir_y = 0

        if robot_x == self.max_w - 2:
            self.dir_x = 0
            self.dir_y = 1
            if grid_map.map[robot_y][robot_x].req_energy == 0:
                self.mode = MOVE
            else:
                self.mode = CLEN

        if robot_x == self.max_w - 2 and robot_y == self.max_h - 2:
            self.dir_x = -1
            self.dir_y = 0
            if grid_map.map[robot_y][robot_x].req_energy == 0:
                self.mode = MOVE
            else:
                self.mode = CLEN

        if robot_x == 2 and robot_y == self.max_h - 2:
            self.dir_x = 0
            self.dir_y = -1
            if grid_map.map[robot_y][robot_x].req_energy == 0:
                self.mode = MOVE
            else:
                self.mode = CLEN

        if robot_x == 2 and robot_y == 2:
            self.dir_x = 1
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

