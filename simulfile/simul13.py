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

        
        self.dir_x = 0
        self.dir_y = 0

    def algorithms( self, grid_map: UserMap ):


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

        
        (new_x, new_y) = self.tunning( [new_x, new_y] )
        return (new_x, new_y)

