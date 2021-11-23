import random
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
        self.position = [8,8]
        self.fuel = 3000
        self.dir_x = 0
        self.dir_y = 0


    def algorithms( self, grid_map: UserMap ):
        robot_x = self.position.x
        robot_y = self.position.y

        self.max_h = grid_map.height -1
        self.max_w = grid_map.width -1

        if self.mode == STAY :  #robot이 stay할 경우, x 방향으로의 + 이동 및 청소 (시작점에서 시작)
            self.mode = MOVE
            self.dir_x = 1
            self.dir_y = 0
            new_x = robot_x + self.dir_x
            new_y = robot_y + self.dir_y
            if grid_map[new_y][new_x].req_energy == 0 :
                self.mode = MOVE
                self.dir_x = 1
                self.dir_y = 0
            if grid_map[new_y][new_x].req_energy <= 10 : #먼지가 10 이하일때
                self.mode = CLEN
                self.fuel -= grid_map.req_energy
            if grid_map[new_y][new_x].req_energy > 10 : #먼지가 10 이상일때
                self.mode = CLEN
                self.fuel -= 10
                grid_map[new_y][new_x].req_energy -= 10
                self.mode = CLEN
                self.fuel -= grid_map[new_y][new_x].req_energy
            if grid_map[new_y][new_x].req_energy == inf : #장애물을 만났을 때
                self.mode = MOVE
                self.dir_x = -1
                self.dir_y = 0
            if self.fuel == 0 : #연료가 소진되었을 때
                print("terminate")
                quit()

        new_x += self.dir_x
        new_y += self.dir_y

        if self.mode == STAY :  #robot이 stay할 경우, x 방향으로의 + 이동 및 청소 (시작점에서 시작하지 않을 경우)
            self.mode = MOVE
            self.dir_x = 1
            self.dir_y = 0
            new_x += self.dir_x
            new_y += self.dir_y
            if new_x == self.max_w : # x 값이 오른쪽 벽에 닿았을 때
                self.mode = MOVE
                self.dir_x = -1
                self.dir_y = 0
                if grid_map[new_y][new_x].req_energy == 0 :
                    self.mode = MOVE
                    self.dir_x = -1
                    self.dir_y = 0
                if grid_map[new_y][new_x].req_energy <= 10 : #먼지가 10 이하일때
                    self.mode = CLEN
                    self.fuel -= grid_map.req_energy
                if grid_map[new_y][new_x].req_energy > 10 : #먼지가 10 이상일때
                    self.mode = CLEN
                    self.fuel -= 10
                    grid_map[new_y][new_x].req_energy -= 10
                    self.mode = CLEN
                    self.fuel -= grid_map[new_y][new_x].req_energy
                if grid_map[new_y][new_x].req_energy == inf : #장애물을 만났을 때
                    self.mode = MOVE
                    self.dir_x = -1
                    self.dir_y = 0
                if self.fuel == 0 : #연료가 소진되었을 때
                    print("terminate")
                    quit()
            if grid_map[new_y][new_x].req_energy == 0 :
                self.mode = MOVE
                self.dir_x = 1
                self.dir_y = 0
            if grid_map[new_y][new_x].req_energy <= 10 : #먼지가 10 이하일때
                self.mode = CLEN
                self.fuel -= grid_map.req_energy
            if grid_map[new_y][new_x].req_energy > 10 : #먼지가 10 이상일때
                self.mode = CLEN
                self.fuel -= 10
                grid_map[new_y][new_x].req_energy -= 10
                self.mode = CLEN
                self.fuel -= grid_map[new_y][new_x].req_energy
            if grid_map[new_y][new_x].req_energy == inf : #장애물을 만났을 때
                self.mode = MOVE
                self.dir_x = -1
                self.dir_y = 0
            if self.fuel == 0 : #연료가 소진되었을 때
                print("terminate")
                quit()

        new_x += self.dir_x
        new_y += self.dir_y



        if self.mode == STAY :  #robot이 stay할 경우, y 방향으로의 + 이동 및 청소 (시작점에서 시작하지 않을 경우)
            self.mode = MOVE
            self.dir_x = 0
            self.dir_y = 1
            new_x += self.dir_x
            new_y += self.dir_y
            if new_y == self.max_h : # y 값이 위쪽 벽에 닿았을 때
                self.mode = MOVE
                self.dir_x = 0
                self.dir_y = -1
                if grid_map[new_y][new_x].req_energy == 0 :
                    self.mode = MOVE
                    self.dir_x = 0
                    self.dir_y = -1
                if grid_map[new_y][new_x].req_energy <= 10 : #먼지가 10 이하일때
                    self.mode = CLEN
                    self.fuel -= grid_map.req_energy
                if grid_map[new_y][new_x].req_energy > 10 : #먼지가 10 이상일때
                    self.mode = CLEN
                    self.fuel -= 10
                    grid_map[new_y][new_x].req_energy -= 10
                    self.mode = CLEN
                    self.fuel -= grid_map[new_y][new_x].req_energy
                if grid_map[new_y][new_x].req_energy == inf : #장애물을 만났을 때
                    self.mode = MOVE
                    self.dir_x = 0
                    self.dir_y = -1
                if self.fuel == 0 : #연료가 소진되었을 때
                    print("terminate")
                    quit()            
            if grid_map[new_y][new_x].req_energy == 0 :
                    self.mode = MOVE
                    self.dir_x = 0
                    self.dir_y = 1
            if grid_map[new_y][new_x].req_energy <= 10 : #먼지가 10 이하일때
                    self.mode = CLEN
                    self.fuel -= grid_map.req_energy
            if grid_map[new_y][new_x].req_energy > 10 : #먼지가 10 이상일때
                    self.mode = CLEN
                    self.fuel -= 10
                    grid_map[new_y][new_x].req_energy -= 10
                    self.mode = CLEN
                    self.fuel -= grid_map[new_y][new_x].req_energy
            if grid_map[new_y][new_x].req_energy == inf : #장애물을 만났을 때
                    self.mode = MOVE
                    self.dir_x = 0
                    self.dir_y = -1
            if self.fuel == 0 : #연료가 소진되었을 때
                    print("terminate")
                    quit()

        new_x += self.dir_x
        new_y += self.dir_y



        if self.mode == STAY :  #robot이 stay할 경우, x 방향으로의 - 이동 및 청소 (시작점에서 시작하지 않을 경우)
            self.mode = MOVE
            self.dir_x = -1
            self.dir_y = 0
            new_x += self.dir_x
            new_y += self.dir_y
            if new_x == 0 : # x 값이 왼쪽 벽에 닿았을 때
                self.mode = MOVE
                self.dir_x = 1
                self.dir_y = 0
                if grid_map[new_y][new_x].req_energy == 0 :
                    self.mode = MOVE
                    self.dir_x = 1
                    self.dir_y = 0
                if grid_map[new_y][new_x].req_energy <= 10 : #먼지가 10 이하일때
                    self.mode = CLEN
                    self.fuel -= grid_map.req_energy
                if grid_map[new_y][new_x].req_energy > 10 : #먼지가 10 이상일때
                    self.mode = CLEN
                    self.fuel -= 10
                    grid_map[new_y][new_x].req_energy -= 10
                    self.mode = CLEN
                    self.fuel -= grid_map[new_y][new_x].req_energy
                if grid_map[new_y][new_x].req_energy == inf : #장애물을 만났을 때
                    self.mode = MOVE
                    self.dir_x = 1
                    self.dir_y = 0
                if self.fuel == 0 : #연료가 소진되었을 때
                    print("terminate")
                    quit()
            if grid_map[new_y][new_x].req_energy == 0 :
                self.mode = MOVE
                self.dir_x = -1
                self.dir_y = 0
            if grid_map[new_y][new_x].req_energy <= 10 : #먼지가 10 이하일때
                self.mode = CLEN
                self.fuel -= grid_map.req_energy
            if grid_map[new_y][new_x].req_energy > 10 : #먼지가 10 이상일때
                self.mode = CLEN
                self.fuel -= 10
                grid_map[new_y][new_x].req_energy -= 10
                self.mode = CLEN
                self.fuel -= grid_map[new_y][new_x].req_energy
            if grid_map[new_y][new_x].req_energy == inf : #장애물을 만났을 때
                self.mode = MOVE
                self.dir_x = 1
                self.dir_y = 0
            if self.fuel == 0 : #연료가 소진되었을 때
                print("terminate")
                quit()

        new_x += self.dir_x
        new_y += self.dir_y


        if self.mode == STAY :  #robot이 stay할 경우, y 방향으로의 - 이동 및 청소 (시작점에서 시작하지 않을 경우)
            self.mode = MOVE
            self.dir_x = 0
            self.dir_y = -1
            new_x += self.dir_x
            new_y += self.dir_y
            if new_y == 0 : # y 값이 아래쪽 벽에 닿았을 때
                self.mode = MOVE
                self.dir_x = 0
                self.dir_y = 1
                if grid_map[new_y][new_x].req_energy == 0 :
                    self.mode = MOVE
                    self.dir_x = 0
                    self.dir_y = 1
                if grid_map[new_y][new_x].req_energy <= 10 : #먼지가 10 이하일때
                    self.mode = CLEN
                    self.fuel -= grid_map.req_energy
                if grid_map[new_y][new_x].req_energy > 10 : #먼지가 10 이상일때
                    self.mode = CLEN
                    self.fuel -= 10
                    grid_map[new_y][new_x].req_energy -= 10
                    self.mode = CLEN
                    self.fuel -= grid_map[new_y][new_x].req_energy
                if grid_map[new_y][new_x].req_energy == inf : #장애물을 만났을 때
                    self.mode = MOVE
                    self.dir_x = 0
                    self.dir_y = 1
                if self.fuel == 0 : #연료가 소진되었을 때
                    print("terminate")
                    quit()
            if grid_map[new_y][new_x].req_energy == 0 :
                    self.mode = MOVE
                    self.dir_x = 0
                    self.dir_y = -1
            if grid_map[new_y][new_x].req_energy <= 10 : #먼지가 10 이하일때
                    self.mode = CLEN
                    self.fuel -= grid_map.req_energy
            if grid_map[new_y][new_x].req_energy > 10 : #먼지가 10 이상일때
                    self.mode = CLEN
                    self.fuel -= 10
                    grid_map[new_y][new_x].req_energy -= 10
                    self.mode = CLEN
                    self.fuel -= grid_map[new_y][new_x].req_energy
            if grid_map[new_y][new_x].req_energy == inf : #장애물을 만났을 때
                    self.mode = MOVE
                    self.dir_x = 0
                    self.dir_y = 1
            if self.fuel == 0 : #연료가 소진되었을 때
                    print("terminate")
                    quit()

        new_x += self.dir_x
        new_y += self.dir_y


# main.py 오류 문의하기 / 시작점 코드는 하나만 설정해야 중간에 시작점으로 초기화되는 문제가 발생하지 않을 것 같음(고민)'




        (new_x, new_y) = self.tunning( [new_x, new_y] )
        return (new_x, new_y)

