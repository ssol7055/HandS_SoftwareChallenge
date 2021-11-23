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

dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]
col_dirs = [[1, 0], [-1, 0]]
ver_dirs = [[0,1], [0, -1]]

charger_cnt = 0

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
            vision_sight: int = 2,
    ) -> None:
        super().__init__(
            fuel=fuel,
            energy_consumption=energy_consumption,
            move_consumption=move_consumption,
            postion=postion,
            vision_sight=vision_sight,
        )
        '''
            If you want to store some values, define your variables here.
            Using `self`-based variables, you can re-call the value of previous state easily.
        '''
        self.dir_x = 0
        self.dir_y = 0

    def algorithms(self, grid_map: UserMap):
        #### Code Here! ####

        # THIS IS AN EXAMPLE CODE. DELETE THIS CODE SEGMENT BEFORE YOU START YOUR OWN CODE.
        # START OF EXAMPLE CODE

        # Default information from robot and env.

        global charger_cnt
        robot_x = self.position.x
        robot_y = self.position.y

        new_x = robot_x
        new_y = robot_y

        charger_x = 8
        charger_y = 8

        self.max_h = grid_map.height - 1
        self.max_w = grid_map.width - 1

        if charger_cnt < 4 and self.mode != CHAR and robot_x == charger_x and robot_y == charger_y:
            self.mode = CHAR
            charger_cnt += 1
        else:

            if charger_cnt < 4 and (abs(robot_x - charger_x) + abs(robot_y - charger_y)) * 10 + 100 >= self._fuel:
                self.mode = MOVE
                if abs(robot_x - charger_x) != 0:
                    if robot_x > charger_x:
                        new_x = robot_x - 1
                    else:
                        new_x = robot_x + 1

                    if grid_map.map[new_y][new_x].req_energy == inf:
                        new_x = robot_x
                        new_y = robot_y
                        for dx, dy in ver_dirs:
                            new_y = robot_y + dy

                            if grid_map.map[new_y][new_x].req_energy != inf:
                                break

                else:
                    if robot_y > charger_y:
                        new_y = robot_y - 1
                    else:
                        new_y = robot_y + 1

                    if grid_map.map[new_y][new_x].req_energy == inf:
                        new_x = robot_x
                        new_y = robot_y
                        for dx, dy in col_dirs:
                            new_x = robot_x + dx

                            if grid_map.map[new_y][new_x].req_energy != inf:
                                break
            else:
                max_val = [0, robot_x, robot_y]
                for dx, dy in dirs:
                    nx = robot_x + dx
                    ny = robot_y + dy

                    if 0 <= nx <= self.max_w and 0 <= ny <= self.max_h:
                        if grid_map.map[ny][nx].req_energy == inf:
                            continue
                        if grid_map.map[ny][nx].req_energy > max_val[0]:
                            max_val = [grid_map.map[ny][nx].req_energy, nx, ny]

                new_x = max_val[1]
                new_y = max_val[2]

                if grid_map.map[new_y][new_x].req_energy > grid_map.map[robot_y][robot_x].req_energy or grid_map.map[robot_y][robot_x].req_energy == 0:
                    self.mode = MOVE
                else:
                    self.mode = CLEN



        # END OF EXAMPLE CODE

        ######################

        ##### DO NOT CHANGE RETURN VARIABLES! #####
        ## The below codes are fixed. The users only determine the mode and/or the next position (coordinate) of the robot.
        ## Therefore, you need to match the variables of return to simulate.
        (new_x, new_y) = self.tunning([new_x, new_y])

        return (new_x, new_y)
