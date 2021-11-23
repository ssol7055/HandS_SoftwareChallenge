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
            vision_sight=vision_sight,
        )
        self.dir_x = 0
        self.dir_y = 0 #for move
        self.choicey = 0
        self.choicex = 0
        self.dir = [1,0,0,1,-1,0,0,-1]
        self.dir1 = 0 #for selecting drection
        self.memory = [[-1 for col in range(17)] for row in range(17)] #recording req_energy
        self.path = [[0 for col in range(17)] for row in range(17)] #recording the number of times revisited
        self.obstacle = [[0 for col in range(17)] for row in range(17)] #recording locations with problems
        self.path2 = [[0 for col in range(17)] for row in range(17)] #recording the number of times visited
        self.path3 = 0
        self.object = [0,0] #long-term object location
        self.object1 = 0 #short-term object location
        self.prev1 = [0,0]
        self.prev2 = [0,0] #for path[][]
        self.loop = 0
        self.process = 0
        self.distance = inf
        self.distance1 = 0
        self.distance2 = 0 #distance among long-term, short-term, robot location
        self.charge = 0
        self.t = 0
        self.a = 0
        self.b = 0
        self.i = -1
        self.j = -1
        self.y = 0
        self.x = 0
        self.z = inf

    def algorithms( self, grid_map: UserMap ):
        #Submitted to HandS software challenge, written by 20211140655 Kim Sang Ock quadrat1c@korea.ac.kr
    
        robot_x = self.position.x
        robot_y = self.position.y

        if self._fuel < 500 and self.charge < 4:
            self.process = 1
        else:
            self.process = 0
        #determine process to charge (1) or not to charge (0)

        if self.path[robot_y][robot_x] > 5:
            self.obstacle[self.object[0]][self.object[1]] = inf
        #record object location which has revisiting issue
        
        if self.mode == MOVE:
            if self.prev1 == [robot_y, robot_x] or self.prev2 == [robot_y, robot_x]:
                self.path[robot_y][robot_x] = self.path[robot_y][robot_x] + 1
            self.prev2 = self.prev1
            self.prev1 = [robot_y, robot_x]
        #record revisiting when mode is MOVE

        if self.charge == 0:
            self.object1 = [0,0]
        elif self.charge == 1:
            self.object1 = [16,16]
        elif self.charge == 2:
            self.object1 = [0,16]
        elif self.charge == 3:
            self.object1 = [16,0]
        elif self.loop % 50 == 0:
            self.obstacle[self.object1[0]][self.object1[1]] = inf
            self.i = -1
            self.j = -1
            self.x = 0
            self.y = 0
            self.a = 0
            self.b = 0
            self.t = inf
            while self.y <= 16:
                while self.x <= 16:
                    while self.i <= 1:
                        while self.j <= 1:
                            self.a = min(max(self.y + self.i,0),16)
                            self.b = min(max(self.x + self.j,0),16)
                            if self.memory[self.a][self.b] == inf:
                                self.path3 = inf
                            else:
                                self.path3 = self.path3 + self.path2[self.a][self.b]
                            self.j = self.j + 1
                        self.i = self.i + 1
                        self.j = -1
                    if self.path3 <= self.t and self.obstacle[self.y][self.x] != inf:
                        self.t = self.path3
                        self.object1 = [self.y, self.x]
                    self.path3 = 0
                    self.x = self.x + 1
                    self.i = -1
                self.y = self.y + 1
                self.x = 0
        #set long-term object location according to numbers of times charged, then select the least visited location when the chance to charge is over

        if self.process == 0:
            self.x = 0
            self.y = 0
            self.z = inf
            while self.y <= 16:
                while self.x <= 16:
                    self.distance2 = pow(self.object1[0]-self.y, 2) + pow(self.object1[1]-self.x, 2)
                    if self.memory[self.y][self.x] != inf and self.distance2 <= self.z and self.obstacle[self.y][self.x] != inf:
                        self.z = self.distance2
                        self.object = [self.y, self.x]
                    if self.loop % 100 == 0 and self.memory[self.y][self.x] + self.memory[min(self.y+1,16)][self.x] + self.memory[self.y][min(self.x+1,16)] \
                        + self.memory[max(self.y-1,0)][self.x] + self.memory[self.y][max(self.x-1,0)] != inf:
                        self.obstacle[self.y][self.x] = 0
                    self.x = self.x + 1
                self.y = self.y + 1
                self.x = 0
        elif self.process == 1:
            if robot_y != 8:
                self.object = [8, robot_x]
            else:
                self.object = [8,8]
        else:
            self.process = 0
        #set short-term object location which does not have problems

        if self.process == 1 and robot_y == 8 and robot_x == 8:
            self.dir_x = 0
            self.dir_y = 0
            self.mode = CHAR
            self.process = 0
            self.charge = self.charge + 1
            self.loop = 0
            if self.charge == 3:
                self.path = [[0 for col in range(17)] for row in range(17)]
        elif grid_map.map[robot_y][robot_x].req_energy != 0:
            self.dir_x = 0
            self.dir_y = 0
            self.mode = CLEN
        else:
            while self.dir1 <= 3:
                self.choicey = robot_y + self.dir[self.dir1*2]
                self.choicex = robot_x + self.dir[self.dir1*2+1]
                if self.choicey in range(17) and self.choicex in range(17):
                    self.distance1 = pow(self.choicey-self.object[1],2) + pow(self.choicex-self.object[0],2) + pow(self.path[self.choicey][self.choicex],10)
                    if self.memory[self.choicey][self.choicex] != inf and self.distance1 < self.distance:
                        self.distance = self.distance1
                        self.dir_y = self.dir[self.dir1*2]
                        self.dir_x = self.dir[self.dir1*2+1]
                self.dir1 = self.dir1 + 1
            self.dir1 = 0
            self.distance = inf
            self.mode = MOVE
        #set mode among CHAR, CLEN, MOVE and direction

        self.x = 0
        self.y = 0
        self.i = -1
        self.j = -1
        while self.i <= 1:
            while self.j <= 1:
                self.y = min(max(robot_y + self.i,0),16)
                self.x = min(max(robot_x + self.j,0),16)
                self.memory[self.y][self.x] = grid_map.map[self.y][self.x].req_energy
                self.obstacle[robot_y][robot_x] = self.obstacle[robot_y][robot_x] + grid_map.map[self.y][self.x].req_energy
                self.j = self.j + 1
            self.i = self.i + 1
            self.j = -1
        #record the req_energy and obstacles around
             
        new_x = robot_x + self.dir_x
        new_y = robot_y + self.dir_y
        self.path2[robot_y][robot_x] = self.path2[robot_y][robot_x] + 1
        #set new location and record it to visited location

        if self._fuel % 500 == 10:
            print(self._fuel, self.charge, self.object1, self.object, (new_y, new_x))
        self.loop = self.loop + 1
        #report fuel, number of times charged, long-term object, short-term object, present locations in every 500 loops

        (new_x, new_y) = self.tunning( [new_x, new_y] )
        return (new_x, new_y)
