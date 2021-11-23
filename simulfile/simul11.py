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
        self.path = []
        self.dir_x = 0
        self.dir_y = 0

    def move(self, robot_x, robot_y,grid_map):
        dir_ = [(-1,0),(0,1),(1,0),(0,-1)]

        for d in dir_:
            new_x = robot_x+d[0]
            new_y = robot_y+d[1]
            if new_x<0 or new_x>self.max_w or new_y<0 or new_y>self.max_h:
                continue
            # if obstacle
            if grid_map.map[new_y][new_x].req_energy == inf:
                continue
            # no dust
            if grid_map.map[new_y][new_x].req_energy == 0:
                continue                
            # dust
            else:                 
                self.dir_x = d[0]
                self.dir_y = d[1]
                return

        a,b=self.path.pop(-1)
        if(a==robot_x and b==robot_y):
            x, y = self.path.pop(-1)
            self.dir_x = x-robot_x
            self.dir_y = y-robot_y
            return
        else: 
            self.dir_x = a-robot_x
            self.dir_y = b-robot_y
            return

    def return_move(self, robot_x, robot_y,grid_map):
        if grid_map.map[robot_y][robot_x].req_energy!=0:
            self.mode=CLEN
            return

        if robot_x==8 and robot_y==8:
            self.mode=CHAR
            return

        dir_ = [(-1,0),(0,-1),(1,0),(0,1)]
        dist_lst=[]

        for d in dir_:
            new_x = robot_x+d[0]
            new_y = robot_y+d[1]
            
            if new_x<0 or new_x>self.max_w or new_y<0 or new_y>self.max_h:
                dist_lst.append(1000)
                continue
            elif grid_map.map[new_y][new_x].req_energy == inf:
                dist_lst.append(1000)
                continue
            else:
                dst=(new_x-8)**2+(new_y-8)**2
                dist_lst.append(dst)
                continue

        tmp=min(dist_lst)
        l=dir_[dist_lst.index(tmp)]
        self.dir_x = l[0]
        self.dir_y = l[1]
        self.mode=MOVE
        return


    def algorithms( self, grid_map: UserMap ):
    
        robot_x = self.position.x
        robot_y = self.position.y

        self.max_h = grid_map.height - 1
        self.max_w = grid_map.width - 1

        if self.mode == STAY:
            self.mode = MOVE
            self.dir_x = 1
            self.dir_y = 0
        
        else:
            if self._fuel<300:
                self.return_move(robot_x,robot_y,grid_map)
            else:
                if self.mode == MOVE:
                    self.move(robot_x,robot_y,grid_map)
                    if grid_map.map[robot_y][robot_x].req_energy == 0:
                        self.mode = MOVE
                    else:
                        self.mode = CLEN
                
                elif self.mode==CLEN:
                    if grid_map.map[robot_y][robot_x].req_energy == 0:
                        self.mode = MOVE
                    else:
                        self.mode = CLEN

                elif self.mode==CHAR:
                    self.move(robot_x,robot_y,grid_map)
                    self.mode=MOVE

        new_x = robot_x + self.dir_x
        new_y = robot_y + self.dir_y

        if self.mode==MOVE:
            self.path.append([new_x,new_y])

        (new_x, new_y) = self.tunning( [new_x, new_y] )
        return (new_x, new_y)
