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
        self.last_x = [] # 충전을 위한 경로 저장 변수
        self.last_y = [] # 충전을 위한 경로 저장 변수
        self.detecting_obstacle = [] # 장애물 발견을 위한 변수
        self.NOC = 0 # 배터리 충전 횟수
        self.map = [[0 for i in range(19)]for j in range(19)] # 맵 저장을 위한 변수
        self.isremain = [[0 for i in range(40)]for j in range(2)]
        self.backtowork = 0 # 충전 후에 복귀를 위한 변수
        self.isstart = 0 # 첫 시작인지 아닌지 판단하는 변수
        self.findremain = 0
        self.isremain_index = 0
        
    def algorithms( self, grid_map: UserMap ):
        x = self.position.x # 현재 위치 x
        y = self.position.y # 현재 위치 y
        right_side, left_side = 1, -1 # 방향을 새로 정의
        upside, downside = -1, 1 # 방향을 새로 정의
        battery = self._fuel
        print(self._fuel)
        map = self.map
        for i in range(19):
            self.map[0][i] = 2
            self.map[18][i] = 2
            self.map[i][0] = 2
            self.map[i][18] = 2

        D_req_E = self.detecting_obstacle
        D_req_E = [(grid_map.map[y][x].req_energy), # current location
                   (grid_map.map[y][min(x+1, 16)].req_energy), # east
                   (grid_map.map[y][max(x-1, 0)].req_energy),  # west
                   (grid_map.map[min(y+1, 16)][x].req_energy), # south
                   (grid_map.map[max(y-1, 0)][x].req_energy)]  # north
        
        def to_remain(to_x, to_y):
            print("moving for remains!")
            print(to_x, to_y)
            if x > to_x:
                if y > to_y: # 4사분면, 위쪽으로 가다가 안되면 위로 그것도 안되면 아래로
                    if D_req_E[4] != inf:
                        self.dir_x, self.dir_y = 0, upside
                    elif D_req_E[2] != inf:
                        self.dir_x, self.dir_y = left_side, 0
                    else: self.dir_x, self.dir_y = 0, downside
                else: # 2사분면, 왼쪽으로 가다가 안되면 아래로 그것도 안되면 위로
                    if D_req_E[2] != inf:
                        self.dir_x, self.dir_y = left_side, 0
                    elif D_req_E[3] != inf:
                        self.dir_x, self.dir_y = 0, downside  
                    else: self.dir_x, self.dir_y = 0, upside 
            elif x < to_x:
                if y > to_y: # 3사분면, 오른쪽으로 가다가 안되면 위로, 그것도 안되면 아래로
                    if D_req_E[1] != inf:
                        self.dir_x, self.dir_y = right_side, 0
                    elif D_req_E[4] != inf:
                        self.dir_x, self.dir_y = left_side, 0
                    else:
                        self.dir_x, self.dir_y = 0, downside
                else: # 1사분면, 오른쪽으로 가다가 안되면 아래로, 그것도 안되면 위로
                    if D_req_E[1] != inf:
                        self.dir_x, self.dir_y = right_side, 0
                    elif D_req_E[3] != inf:
                        self.dir_x, self.dir_y = 0, downside
                    else:
                        self.dir_x, self.dir_y = 0, upside
            elif x == to_x:
                if y > to_y: 
                    if D_req_E[4] != inf: self.dir_x, self.dir_y = 0, upside
                    elif D_req_E[1] != inf: self.dir_x, self.dir_y = right_side, 0
                    else: self.dir_x, self.dir_y = left_side, 0
                elif y < to_y:
                    if D_req_E[3] != inf: self.dir_x, self.dir_y = 0, downside
                    elif D_req_E[1] != inf: self.dir_x, self.dir_y = right_side, 0
                    else: self.dir_x, self.dir_y = left_side, 0
                else:
                    self.findremain += 1
                    if D_req_E[0] == 0:
                        self.mode = MOVE
                    else : self.mode = CLEN
                print("0") 
            if D_req_E[0] == 0:
                self.mode = MOVE
            else : self.mode = CLEN
        
        def find_remains():
            for i in range(17):
                for j in range(17):
                    if map[i+1][j+1] == 0:
                        if i+1>1 and i+1<17 and j+1>1 and j+1<17:
                            print("y: {}, x : {}".format(i+1, j+1))
                            self.isremain[0][self.isremain_index] = j+1
                            self.isremain[1][self.isremain_index] = i+1
                            self.isremain_index += 1 
            self.findremain = 1
            print(self.isremain)
        
        def cleaning():
            print("cleaning...")
            if self.NOC > 3:
                print("self.NOC = {}".format(self.NOC))
                if self.findremain == 0:
                    find_remains()
                else:
                    for i in range(self.isremain_index):
                        if self.findremain == i + 1:
                            to_remain(self.isremain[0][i], self.isremain[1][i])    
                        if self.findremain == self.isremain_index:
                            self.findremain = 0
            else:            
                print("self.NOC is not 3")
                if self.backtowork == 1:
                    back_to_field()
                else:
                    if D_req_E[1] == inf:
                        map[(y)+1][(x+1)+1] = 2
                    if D_req_E[2] == inf:
                        map[(y)+1][(x-1)+1] = 2
                    if D_req_E[3] == inf:
                        map[(y+1)+1][(x)+1] = 2
                    if D_req_E[4] == inf:
                        map[(y-1)+1][(x)+1] = 2
                    
                    map[(y)+1][(x)+1] = 1
                    if map[(y)+1][(x+1)+1] == 1 and map[(y-1)+1][(x)+1] != 2 and map[(y-1)+1][(x)+1] != 1: # if right block was visited or there is any obstacle, go upside
                        self.dir_x, self.dir_y = 0, upside
                        print("upside")
                    elif map[(y-1)+1][(x)+1] == 1 and map[(y)+1][(x-1)+1] != 2 and map[(y)+1][(x-1)+1] != 1 : # if upside block was visited or there is any obstacle, go leftside
                        self.dir_x, self.dir_y = left_side, 0
                        print("leftside")
                    elif map[(y)+1][(x-1)+1] == 1 and map[(y+1)+1][(x)+1] != 2 and map[(y+1)+1][(x)+1] != 1: # if left block was visited or there is any obstacle, go downside
                        self.dir_x, self.dir_y = 0, downside
                        print("downside")
                    elif map[(y+1)+1][(x)+1] == 1 and map[(y)+1][(x+1)+1] != 2 and map[(y)+1][(x+1)+1] != 1: # if downside block was visited or there is any obstacle, go rightside
                        self.dir_x, self.dir_y = right_side, 0
                        print("right")
                    else:
                        if map[(y)+1][(x-1)+1] == 2 and map[(y+1)+1][(x)+1] != 2: # if left block was visited or there is any obstacle, go downside
                            self.dir_x, self.dir_y = 0, downside
                            print("down")
                        elif map[(y)+1][(x+1)+1] == 2 and map[(y-1)+1][(x)+1] != 2: # if right block was visited or there is any obstacle, go upside
                            self.dir_x, self.dir_y = 0, upside
                            print("up")
                        elif map[(y-1)+1][(x)+1] == 2 and map[(y)+1][(x-1)+1] != 2: # if upside block was visited or there is any obstacle, go leftside
                            self.dir_x, self.dir_y = left_side, 0
                            print("left")
                        elif map[(y+1)+1][(x)+1] == 2 and map[(y)+1][(x+1)+1] != 2: # if downside block was visited or there is any obstacle, go rightside
                            self.dir_x, self.dir_y = right_side, 0
                            print("right")
                    if D_req_E[0] == 0:
                        self.mode = MOVE
                    else : self.mode = CLEN
                    print("1") 
                
        def battery_charge():
            print("moving for charge!")
            if x > 8:
                if y > 8:
                    if D_req_E[2] != inf:
                        self.dir_x, self.dir_y = left_side, 0
                    else:
                        self.dir_x, self.dir_y = 0, upside
                else:
                    if D_req_E[2] != inf:
                        self.dir_x, self.dir_y = left_side, 0
                    else:
                        self.dir_x, self.dir_y = 0, downside  
            elif x < 8:
                if y > 8:
                    if D_req_E[1] != inf:
                        self.dir_x, self.dir_y = right_side, 0
                    else:
                        self.dir_x, self.dir_y = 0, upside
                else:
                    if D_req_E[1] != inf:
                        self.dir_x, self.dir_y = right_side, 0
                    else:
                        self.dir_x, self.dir_y = 0, downside
            elif x == 8:
                if y > 8: 
                    if D_req_E[4] != inf: self.dir_x, self.dir_y = 0, upside
                    else: self.dir_x, self.dir_y = right_side, 0
                elif y < 8:
                    if D_req_E[3] != inf: self.dir_x, self.dir_y = 0, downside
                    else: self.dir_x, self.dir_y = right_side, 0
                else:
                    self.mode = CHAR
                    print("battery charged")
                    #if self._fuel == 3000:
                    self.NOC = self.NOC + 1
                    print("self.NOC: " + str(self.NOC))
                    self.backtowork = 1
            self.last_x.append(x)
            self.last_y.append(y)
            if self.mode == CHAR:
                self.mode = self.mode
            else:
                self.mode = MOVE
                print("2")
            
        def back_to_field():
            print("back to the last position")
            for i in (0, len(self.last_x)):
                past_x = self.last_x.pop()
                past_y = self.last_y.pop()
                self.dir_x = past_x - x
                self.dir_y = past_y - y
                self.mode = MOVE
                print("3")
            self.backtowork = 0
                
        def start():
            print("start!")   
            map[y][x] = 1
            if self.mode == STAY:
                print("this car is staying...")
                if D_req_E[3] == inf:
                    print("downside required energy is inf!")
                    self.dir_x, self.dir_y = 0, upside
                    if D_req_E[0] == 0: self.mode = MOVE
                    else: self.mode = CLEN
                    
                elif D_req_E[4] == inf:
                    print("upside required energy is inf!")
                    self.dir_x, self.dir_y = 0, downside
                    if D_req_E[0] == 0: self.mode = MOVE
                    else: self.mode = CLEN
                    
                elif D_req_E[1] == inf:
                    print("rightside required energy is inf!")
                    self.dir_x, self.dir_y = left_side, 0
                    if D_req_E[0] == 0: self.mode = MOVE
                    else: self.mode = CLEN
                    
                elif D_req_E[2] == inf:
                    print("leftside required energy is inf!")
                    self.dir_x = right_side
                    self.dir_y = 0
                    if D_req_E[0] == 0: self.mode = MOVE
                    else: self.mode = CLEN
                    
                else:
                    print("there are not any obstacles!")
                    self.dir_x, self.dir_y = left_side, 0 # 첫 출발에 아무 장애물도 없으면 왼쪽으로. 
                    if D_req_E[0] == 0: self.mode = MOVE
                    else: self.mode = CLEN
            self.isstart = 1
            print("3")
            
        if battery < 190:
            if self.NOC > 3:
                cleaning()
            else:
                print("battery: {}".format(battery))
                battery_charge()
        elif self.NOC == 0:
            if self.isstart == 0:
                start()
            cleaning()
        else:
            cleaning()
            
        new_x = x + self.dir_x
        new_y = y + self.dir_y
        print("new_x : {}, new_y : {}".format(new_x, new_y))
        #END OF EXAMPLE CODE

        ######################

        ##### DO NOT CHANGE RETURN VARIABLES! #####
        ## The below codes are fixed. The users only determine the mode and/or the next position (coordinate) of the robot.
        ## Therefore, you need to match the variables of return to simulate.
        (new_x, new_y) = self.tunning( [new_x, new_y] )
        return (new_x, new_y)

