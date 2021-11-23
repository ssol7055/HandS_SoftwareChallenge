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
        self.count = 0
        self.corner = 0

        self.line1 = 8
        self.line2 = 8
        self.line3 = 8
        self.line4 = 8

        self.half = 0

        self.pathlog = set()

        self.infset1 = set()
        self.infset2 = set()
        self.infset3 = set()
        self.infset4 = set()
        self.clear1 = set()
        self.clear2 = set()
        self.clear3 = set()
        self.clear4 = set()

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

        self.max_h = grid_map.height - 1
        self.max_w = grid_map.width - 1
        ###################################################################################
        ### 1사분면 끝내고 돌아오기
        if self.count == 0 and self.half == 1:
            if robot_y < 8:
                if grid_map.map[robot_y+1][robot_x] != inf:
                    self.dir_x = 0
                    self.dir_y = 1
                    if grid_map.map[robot_y][robot_x].req_energy == 0:
                        self.mode = MOVE
                    else:
                        self.mode = CLEN
                # 끼는 경우
                if robot_x == 8:
                    if grid_map.map[robot_y+1][robot_x+1] == inf:
                        self.dir_x = 1
                        self.dir_y = 0
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                    if grid_map.map[robot_y+1][robot_x] == inf:
                        self.dir_x = 1
                        self.dir_y = 0
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                    if grid_map.map[robot_y][robot_x+1] == inf:
                        self.dir_x = 0
                        self.dir_y = -1
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                

                    
            if robot_x > 8:
                if grid_map.map[robot_y][robot_x-1] != inf:
                    self.dir_x = -1
                    self.dir_y = 0
                    if grid_map.map[robot_y][robot_x].req_energy == 0:
                        self.mode = MOVE
                    else:
                        self.mode = CLEN
                # 끼는 경우
                if robot_y == 8:
                    if grid_map.map[robot_y-1][robot_x-1] == inf:
                        self.dir_x = 0
                        self.dir_y = -1
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                    if grid_map.map[robot_y][robot_x-1] == inf:
                        self.dir_x = 0
                        self.dir_y = -1
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                    if grid_map.map[robot_y-1][robot_x] == inf:
                        self.dir_x = 1
                        self.dir_y = 0
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
            
            # 종료조건
            if robot_x == 8 and robot_y == 8:
                self.mode = CHAR
                self.count = self.count + 1
                self.half = 0

        elif self.count == 0 and self.half == 0:
            ### 반환점 ###
            if self._fuel < 500 or len(self.infset1) + len(self.clear1) == 72:
                self.half = 1
            if robot_x >= 8 and robot_y <= 7:
                if robot_y != 0:
                    if grid_map.map[robot_y-1][robot_x].req_energy == inf:
                        self.infset1.add((robot_y-1,robot_x))
                    if robot_x != self.max_w: 
                        if grid_map.map[robot_y-1][robot_x+1].req_energy == inf:
                            self.infset1.add((robot_y-1,robot_x+1))
                    if robot_x != 0:
                        if grid_map.map[robot_y-1][robot_x-1].req_energy == inf:
                            self.infset1.add((robot_y-1,robot_x-1))
                if robot_x != 0:
                    if grid_map.map[robot_y][robot_x-1].req_energy == inf:
                        self.infset1.add((robot_y,robot_x-1))
                    if robot_y != self.max_h:
                        if grid_map.map[robot_y+1][robot_x-1].req_energy == inf:
                            self.infset1.add((robot_y+1,robot_x-1))
                if robot_x != self.max_w:
                    if grid_map.map[robot_y][robot_x+1].req_energy == inf:
                        self.infset1.add((robot_y,robot_x+1))
                    if robot_y != self.max_h:
                        if grid_map.map[robot_y+1][robot_x+1].req_energy == inf:
                            self.infset1.add((robot_y+1,robot_x+1))
                if robot_y != self.max_h:
                    if grid_map.map[robot_y+1][robot_x].req_energy == inf:
                        self.infset1.add((robot_y+1,robot_x))

                if grid_map.map[robot_y][robot_x].req_energy == 0:
                    self.clear1.add((robot_y,robot_x))
            ###

            ###
            # 짝수 열
            if self.line1 % 2 == 0:
                if robot_x < self.line1:
                    self.dir_x = 1
                    self.dir_y = 0
                    if grid_map.map[robot_y][robot_x].req_energy == 0:
                        self.mode = MOVE
                    else:
                        self.mode = CLEN
                    # 오른쪽 끝임
                    if robot_x == self.max_w:
                        self.dir_x = 0
                        self.dir_y = -1
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                    # 오른쪽에 장애물
                    elif grid_map.map[robot_y][robot_x+1].req_energy == inf:
                        self.dir_x = 0
                        self.dir_y = -1
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                elif robot_x == self.line1:
                    # 코너에 막혀있지 않다
                    if self.corner == 0:
                        # 기본 상태
                        self.dir_x = 0
                        self.dir_y = -1
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                        ###
                        # 위 끝까지 도달
                        if robot_y == 0:
                            self.line1 = self.line1 + 1
                        # 위에 장애물 존재
                        elif grid_map.map[robot_y-1][robot_x].req_energy == inf:
                            self.dir_x = 1
                            self.dir_y = 0
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                            if grid_map.map[robot_y][robot_x+1].req_energy == inf:
                                self.corner = 1
                    # 진행방향 경로 다 막힌 경우
                    if self.corner == 1:
                        if grid_map.map[robot_y-1][robot_x+1].req_energy == inf:
                            self.dir_x = 1
                            self.dir_y = 0
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                            self.corner = 0
                        '''if grid_map.map[robot_y-1][robot_x].req_energy == inf:
                            self.dir_x = 1
                            self.dir_y = 0
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN'''
                        if grid_map.map[robot_y][robot_x+1].req_energy == inf:
                            self.dir_x = 0
                            self.dir_y = 1
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                elif robot_x > self.line1:
                    # 기본 상태
                    self.dir_x = -1
                    self.dir_y = 0
                    if grid_map.map[robot_y][robot_x].req_energy == 0:
                        self.mode = MOVE
                    else:
                        self.mode = CLEN
                    ###
                    # 비껴서 위로 가기
                    if robot_y > 0:
                        if grid_map.map[robot_y-1][robot_x-1].req_energy == inf:
                            self.dir_x = 0
                            self.dir_y = -1
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                    # 왼쪽에 장애물 존재
                    if grid_map.map[robot_y][robot_x-1].req_energy == inf:
                        self.dir_x = 0
                        self.dir_y = -1
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                    ###
                    # 위쪽에 장애물 존재
                    if robot_y > 0:
                        if grid_map.map[robot_y-1][robot_x].req_energy == inf:
                            self.dir_x = 1
                            self.dir_y = 0
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                            # 힘들어진다
                            if robot_x == self.max_w:
                                self.half == 1
                    if robot_y == 0:
                        self.line1 += 1
            
                    
            
            # 홀수 열
            elif self.line1 % 2 == 1:
                if robot_x < self.line1:
                    # 기본 상태
                    self.dir_x = 1
                    self.dir_y = 0
                    if grid_map.map[robot_y][robot_x].req_energy == 0:
                        self.mode = MOVE
                    else:
                        self.mode = CLEN
                    # 오른쪽 끝임
                    if robot_x == self.max_w:
                        self.dir_x = 0
                        self.dir_y = 1
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                    # 오른쪽에 장애물
                    elif grid_map.map[robot_y][robot_x+1].req_energy == inf:
                        self.dir_x = 0
                        self.dir_y = 1
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                elif robot_x == self.line1:
                    if self.corner == 0:
                        # 기본 상태
                        self.dir_x = 0
                        self.dir_y = 1
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                        ###
                        # 1사분면 아래 끝까지 도달
                        if robot_y == 7:
                            self.line1 += 1
                            
                        # 아래에 장애물 존재
                        elif grid_map.map[robot_y+1][robot_x].req_energy == inf:
                            self.dir_x = 1
                            self.dir_y = 0
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                            if grid_map.map[robot_y][robot_x+1].req_energy == inf:
                                self.corner = 1
                    # 진행방향 경로 다 막힌 경우
                    if self.corner == 1:
                        if grid_map.map[robot_y+1][robot_x+1].req_energy == inf:
                            self.dir_x = 1
                            self.dir_y = 0
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                            self.corner = 0
                        '''if grid_map.map[robot_y+1][robot_x].req_energy == inf:
                            self.dir_x = 1
                            self.dir_y = 0
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN'''
                        if grid_map.map[robot_y][robot_x+1].req_energy == inf:
                            self.dir_x = 0
                            self.dir_y = -1
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                elif robot_x > self.line1:
                    # 기본 상태
                    self.dir_x = -1
                    self.dir_y = 0
                    if grid_map.map[robot_y][robot_x].req_energy == 0:
                        self.mode = MOVE
                    else:
                        self.mode = CLEN
                    ###
                    # 비껴서 아래로 가기
                    if robot_y < 7:
                        if grid_map.map[robot_y+1][robot_x-1].req_energy == inf:
                            self.dir_x = 0
                            self.dir_y = 1
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                    # 왼쪽에 장애물 존재
                    if grid_map.map[robot_y][robot_x-1].req_energy == inf:
                        self.dir_x = 0
                        self.dir_y = 1
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                    ###
                    # 아래쪽에 장애물 존재
                    if grid_map.map[robot_y+1][robot_x].req_energy == inf:
                        self.dir_x = 1
                        self.dir_y = 0
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                        # 힘들어진다.
                        if robot_x == self.max_w:
                                self.half == 1
            
        ##########################################################################################


        ### 제2사분면
        elif self.count == 1 and self.half == 1:
            if robot_x < 8:
                if grid_map.map[robot_y][robot_x+1].req_energy != inf:

                    self.dir_x = 1
                    self.dir_y = 0
                    if grid_map.map[robot_y][robot_x].req_energy == 0:
                        self.mode = MOVE
                    else:
                        self.mode = CLEN

                    
            if robot_y < 8: ##################
                if grid_map.map[robot_y+1][robot_x].req_energy != inf:
                    self.dir_x = 0
                    self.dir_y = 1
                    if grid_map.map[robot_y][robot_x].req_energy == 0:
                        self.mode = MOVE
                    else:
                        self.mode = CLEN ###################
            
            if (robot_y+1,robot_x) not in self.pathlog and (robot_y,robot_x+1) not in self.pathlog:
                self.count = self.count + 1
            # 종료조건
            if robot_x == 8 and robot_y == 8:
                self.mode = CHAR
                self.count = self.count + 1
                self.half = 0

        elif self.count == 1 and self.half == 0:
            ### 반환점 ###
            if self._fuel < 500 or len(self.infset2) + len(self.clear2) == 72:
                self.half = 1
            if robot_x <= 7 and robot_y <= 8:
                if robot_y != 0:
                    if grid_map.map[robot_y-1][robot_x].req_energy == inf:
                        self.infset2.add((robot_y-1,robot_x))
                    if robot_x != self.max_w: 
                        if grid_map.map[robot_y-1][robot_x+1].req_energy == inf:
                            self.infset2.add((robot_y-1,robot_x+1))
                    if robot_x != 0:
                        if grid_map.map[robot_y-1][robot_x-1].req_energy == inf:
                            self.infset2.add((robot_y-1,robot_x-1))
                if robot_x != 0:
                    if grid_map.map[robot_y][robot_x-1].req_energy == inf:
                        self.infset2.add((robot_y,robot_x-1))
                    if robot_y != self.max_h:
                        if grid_map.map[robot_y+1][robot_x-1].req_energy == inf:
                            self.infset2.add((robot_y+1,robot_x-1))
                if robot_x != self.max_w:
                    if grid_map.map[robot_y][robot_x+1].req_energy == inf:
                        self.infset2.add((robot_y,robot_x+1))
                    if robot_y != self.max_h:
                        if grid_map.map[robot_y+1][robot_x+1].req_energy == inf:
                            self.infset2.add((robot_y+1,robot_x+1))
                if robot_y != self.max_h:
                    if grid_map.map[robot_y+1][robot_x].req_energy == inf:
                        self.infset2.add((robot_y+1,robot_x))

                if grid_map.map[robot_y][robot_x].req_energy == 0:
                    self.clear2.add((robot_y,robot_x))################################################
            ###

            ###
            # 짝수 열
            if self.line2 % 2 == 0:
                # 로봇이 더 아래에 있을 때
                if robot_y > self.line2:
                    self.dir_x = 0
                    self.dir_y = -1
                    if grid_map.map[robot_y][robot_x].req_energy == 0:
                        self.mode = MOVE
                    else:
                        self.mode = CLEN
                    # 위쪽 끝임
                    if robot_y == 0:
                        self.dir_x = -1
                        self.dir_y = 0
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                    # 위쪽에 장애물
                    elif grid_map.map[robot_y-1][robot_x].req_energy == inf:
                        self.dir_x = -1
                        self.dir_y = 0
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                elif robot_y == self.line2:
                    # 코너에 막혀있지 않다
                    if self.corner == 0:
                        # 기본 상태
                        self.dir_x = -1
                        self.dir_y = 0
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                        ###
                        # 왼쪽 끝까지 도달
                        if robot_x == 0:
                            self.line2 = self.line2 - 1
                        # 왼쪽에 장애물 존재
                        elif grid_map.map[robot_y][robot_x-1].req_energy == inf:
                            self.dir_x = 0
                            self.dir_y = -1
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                            if grid_map.map[robot_y-1][robot_x].req_energy == inf:
                                self.corner = 1
                    # 진행방향 경로 다 막힌 경우
                    if self.corner == 1:
                        if grid_map.map[robot_y-1][robot_x-1].req_energy == inf:
                            self.dir_x = 0
                            self.dir_y = -1
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                            self.corner = 0
                        '''if grid_map.map[robot_y][robot_x-1].req_energy == inf:
                            self.dir_x = 0
                            self.dir_y = -1
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN'''
                        if grid_map.map[robot_y-1][robot_x].req_energy == inf:
                            self.dir_x = 1
                            self.dir_y = 0
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                # 로봇이 더 위에 있음
                elif robot_y < self.line2:
                    # 기본 상태
                    self.dir_x = 0
                    self.dir_y = 1
                    if grid_map.map[robot_y][robot_x].req_energy == 0:
                        self.mode = MOVE
                    else:
                        self.mode = CLEN
                    ###
                    # 비껴서 위로 가기
                    if grid_map.map[robot_y+1][robot_x+1].req_energy == inf:
                        self.dir_x = 0
                        self.dir_y = 1
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                    # 아래쪽에 장애물 존재
                    if grid_map.map[robot_y+1][robot_x].req_energy == inf:
                        self.dir_x = -1
                        self.dir_y = 0
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                    ###
                    # 왼쪽에 장애물 존재
                    if robot_x > 0:
                        if grid_map.map[robot_y][robot_x-1].req_energy == inf:
                            self.dir_x = 0
                            self.dir_y = -1
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                            # 힘들어진다
                            if robot_y == 0:
                                self.half == 1
                    if robot_x == 0:
                        self.line2 -= 1
                    #if robot_x == 0:
                    #    self.line2 -= 1###############################################################                                   #########################################################################
                    
            
            # 홀수 열
            if self.line2 % 2 == 1:
                # 로봇이 더 아래에 있을 때
                if robot_y > self.line2:
                    self.dir_x = 0
                    self.dir_y = -1
                    if grid_map.map[robot_y][robot_x].req_energy == 0:
                        self.mode = MOVE
                    else:
                        self.mode = CLEN
                    # 위쪽 끝임
                    if robot_y == 0:
                        self.dir_x = 1
                        self.dir_y = 0
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                    # 위쪽에 장애물
                    elif grid_map.map[robot_y-1][robot_x].req_energy == inf:
                        self.dir_x = 1
                        self.dir_y = 0
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                elif robot_y == self.line2:
                    # 코너에 막혀있지 않다
                    if self.corner == 0:
                        # 기본 상태
                        self.dir_x = 1
                        self.dir_y = 0
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                        ###
                        # 오른쪽 끝까지 도달
                        if robot_x == 7:
                            self.line2 = self.line2 - 1
                        # 오른에 장애물 존재
                        elif grid_map.map[robot_y][robot_x+1].req_energy == inf:
                            self.dir_x = 0
                            self.dir_y = -1
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                            if grid_map.map[robot_y-1][robot_x].req_energy == inf:
                                self.corner = 1
                    # 진행방향 경로 다 막힌 경우
                    if self.corner == 1:
                        if grid_map.map[robot_y-1][robot_x+1].req_energy == inf:
                            self.dir_x = 0
                            self.dir_y = -1
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                            self.corner = 0
                        '''if grid_map.map[robot_y][robot_x+1].req_energy == inf:
                            self.dir_x = 0
                            self.dir_y = -1
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN'''
                        if grid_map.map[robot_y-1][robot_x].req_energy == inf:
                            self.dir_x = -1
                            self.dir_y = 0
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                # 로봇이 더 위에 있음
                elif robot_y < self.line2:
                    # 기본 상태
                    self.dir_x = 0
                    self.dir_y = 1
                    if grid_map.map[robot_y][robot_x].req_energy == 0:
                        self.mode = MOVE
                    else:
                        self.mode = CLEN
                    ###
                    # 비껴서 가기
                    if grid_map.map[robot_y+1][robot_x+1].req_energy == inf:
                        self.dir_x = 1
                        self.dir_y = 0
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:##################################################################################################################################################################
                            self.mode = CLEN
                    # 아래쪽에 장애물 존재
                    if grid_map.map[robot_y+1][robot_x].req_energy == inf:
                        self.dir_x = 1
                        self.dir_y = 0
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                    ###
                    # 오른쪽에 장애물 존재
                    #if robot_x < 7: 밑에 다 들여쓰기
                    if grid_map.map[robot_y][robot_x+1].req_energy == inf:
                        self.dir_x = 0
                        self.dir_y = -1
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                        # 힘들어진다
                        if robot_y == 0:
                            self.half == 1 #################################끝

        ####################################################################################################
        ####################### 제3사분면 ###################################################################
        if self.count == 2 and self.half == 1:
            if robot_y > 8:
                if grid_map.map[robot_y-1][robot_x] != inf:
                    self.dir_x = 0
                    self.dir_y = -1
                    if grid_map.map[robot_y][robot_x].req_energy == 0:
                        self.mode = MOVE
                    else:
                        self.mode = CLEN
                # 끼는 경우
                '''if robot_x == 8:
                    if grid_map.map[robot_y+1][robot_x+1] == inf:
                        self.dir_x = 1
                        self.dir_y = 0
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                    if grid_map.map[robot_y+1][robot_x] == inf:
                        self.dir_x = 1
                        self.dir_y = 0
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                    if grid_map.map[robot_y][robot_x+1] == inf:
                        self.dir_x = 0
                        self.dir_y = -1
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN'''
                

                    
            if robot_x < 8:
                if grid_map.map[robot_y][robot_x+1] != inf:
                    self.dir_x = 1
                    self.dir_y = 0
                    if grid_map.map[robot_y][robot_x].req_energy == 0:
                        self.mode = MOVE
                    else:
                        self.mode = CLEN
                # 끼는 경우
                '''if robot_y == 8:
                    if grid_map.map[robot_y-1][robot_x-1] == inf:
                        self.dir_x = 0
                        self.dir_y = -1
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                    if grid_map.map[robot_y][robot_x-1] == inf:
                        self.dir_x = 0
                        self.dir_y = -1
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                    if grid_map.map[robot_y-1][robot_x] == inf:
                        self.dir_x = 1
                        self.dir_y = 0
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN'''
            
            # 종료조건
            if robot_x == 8 and robot_y == 8:
                self.mode = CHAR
                self.count = self.count + 1
                self.half = 0

        elif self.count == 2 and self.half == 0: ######################################################## 시작
            ### 반환점 ###
            if self._fuel < 500 or len(self.infset3) + len(self.clear3) == 72:
                self.half = 1
            if robot_x <= 8 and robot_y >= 9:
                if robot_y != 0:
                    if grid_map.map[robot_y-1][robot_x].req_energy == inf:
                        self.infset3.add((robot_y-1,robot_x))
                    if robot_x != self.max_w: 
                        if grid_map.map[robot_y-1][robot_x+1].req_energy == inf:
                            self.infset3.add((robot_y-1,robot_x+1))
                    if robot_x != 0:
                        if grid_map.map[robot_y-1][robot_x-1].req_energy == inf:
                            self.infset3.add((robot_y-1,robot_x-1))
                if robot_x != 0:
                    if grid_map.map[robot_y][robot_x-1].req_energy == inf:
                        self.infset3.add((robot_y,robot_x-1))
                    if robot_y != self.max_h:
                        if grid_map.map[robot_y+1][robot_x-1].req_energy == inf:
                            self.infset3.add((robot_y+1,robot_x-1))
                if robot_x != self.max_w:
                    if grid_map.map[robot_y][robot_x+1].req_energy == inf:
                        self.infset3.add((robot_y,robot_x+1))
                    if robot_y != self.max_h:
                        if grid_map.map[robot_y+1][robot_x+1].req_energy == inf:
                            self.infset3.add((robot_y+1,robot_x+1))
                if robot_y != self.max_h:
                    if grid_map.map[robot_y+1][robot_x].req_energy == inf:
                        self.infset3.add((robot_y+1,robot_x))

                if grid_map.map[robot_y][robot_x].req_energy == 0:
                    self.clear3.add((robot_y,robot_x))
            ###

            ###
            # 짝수 열
            if self.line3 % 2 == 0:
                # 로봇이 더 오른쪽에 있음
                if robot_x > self.line3:
                    self.dir_x = -1
                    self.dir_y = 0
                    if grid_map.map[robot_y][robot_x].req_energy == 0:
                        self.mode = MOVE
                    else:
                        self.mode = CLEN
                    # 왼쪽 끝임
                    if robot_x == 0:
                        self.dir_x = 0
                        self.dir_y = 1
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                    # 왼쪽에 장애물
                    elif grid_map.map[robot_y][robot_x-1].req_energy == inf:
                        self.dir_x = 0
                        self.dir_y = 1
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                elif robot_x == self.line3:
                    # 코너에 막혀있지 않다
                    if self.corner == 0:
                        # 기본 상태
                        self.dir_x = 0
                        self.dir_y = 1
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                        ###
                        # 아래 끝까지 도달
                        if robot_y == self.max_h:
                            self.line3 = self.line3 - 1
                        # 아래에 장애물 존재
                        elif grid_map.map[robot_y+1][robot_x].req_energy == inf:
                            self.dir_x = -1
                            self.dir_y = 0
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                            if grid_map.map[robot_y][robot_x-1].req_energy == inf:
                                self.corner = 1
                    # 진행방향 경로 다 막힌 경우
                    if self.corner == 1:
                        if grid_map.map[robot_y+1][robot_x-1].req_energy == inf:
                            self.dir_x = -1
                            self.dir_y = 0
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                            self.corner = 0
                        '''if grid_map.map[robot_y+1][robot_x].req_energy == inf:
                            self.dir_x = -1
                            self.dir_y = 0
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN'''
                        if grid_map.map[robot_y][robot_x-1].req_energy == inf:
                            self.dir_x = 0
                            self.dir_y = -1
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN ####################################

                # 로봇이 더 왼쪽에 있음
                elif robot_x < self.line3:
                    # 기본 상태
                    self.dir_x = 1
                    self.dir_y = 0
                    if grid_map.map[robot_y][robot_x].req_energy == 0:
                        self.mode = MOVE
                    else:
                        self.mode = CLEN#####################################################3
                    ###
                    # 비껴서 아래로 가기
                    if robot_y < self.max_h:
                        if grid_map.map[robot_y+1][robot_x+1].req_energy == inf:
                            self.dir_x = 0
                            self.dir_y = 1
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                    # 오른쪽에 장애물 존재
                    if grid_map.map[robot_y][robot_x+1].req_energy == inf:
                        self.dir_x = 0
                        self.dir_y = 1
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                    ###
                    # 아래쪽에 장애물 존재
                    if robot_y < self.max_h:
                        if grid_map.map[robot_y+1][robot_x].req_energy == inf:
                            self.dir_x = -1
                            self.dir_y = 0
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                            # 힘들어진다
                            if robot_x == 0:
                                self.half == 1
                    if robot_y == self.max_h:#############################################
                        self.line3 -= 1
        
                    
            
            # 홀수 열
            elif self.line3 % 2 == 1:
                # 로봇이 오른쪽에 있음
                if robot_x > self.line3:
                    # 기본 상태
                    self.dir_x = -1
                    self.dir_y = 0
                    if grid_map.map[robot_y][robot_x].req_energy == 0:
                        self.mode = MOVE
                    else:
                        self.mode = CLEN
                    # 왼쪽 끝임
                    if robot_x == 0:
                        self.dir_x = 0
                        self.dir_y = -1
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                    # 왼쪽에 장애물
                    elif grid_map.map[robot_y][robot_x-1].req_energy == inf:
                        self.dir_x = 0
                        self.dir_y = -1
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                elif robot_x == self.line3:
                    if self.corner == 0:
                        # 기본 상태
                        self.dir_x = 0
                        self.dir_y = -1
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                        ###
                        # 3사분면 위 끝까지 도달
                        if robot_y == 9:
                            self.line3 -= 1
                            
                        # 위에 장애물 존재
                        elif grid_map.map[robot_y-1][robot_x].req_energy == inf:
                            self.dir_x = -1
                            self.dir_y = 0
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                            if grid_map.map[robot_y][robot_x-1].req_energy == inf:
                                self.corner = 1
                    # 진행방향 경로 다 막힌 경우
                    if self.corner == 1:
                        if grid_map.map[robot_y-1][robot_x-1].req_energy == inf:
                            self.dir_x = -1
                            self.dir_y = 0
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                            self.corner = 0
                        '''if grid_map.map[robot_y-1][robot_x].req_energy == inf:
                            self.dir_x = -1
                            self.dir_y = 0
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN'''
                        if grid_map.map[robot_y][robot_x-1].req_energy == inf:
                            self.dir_x = 0
                            self.dir_y = 1
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                # 로봇이 왼쪽에 있음
                elif robot_x < self.line3:################################################3
                    # 기본 상태
                    self.dir_x = 1
                    self.dir_y = 0
                    if grid_map.map[robot_y][robot_x].req_energy == 0:
                        self.mode = MOVE
                    else:
                        self.mode = CLEN
                    ###
                    # 비껴서 위로 가기
                    if robot_y > 9:###############################
                        if grid_map.map[robot_y-1][robot_x+1].req_energy == inf:
                            self.dir_x = 0
                            self.dir_y = -1
                            if grid_map.map[robot_y][robot_x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                    # 오른쪽에 장애물 존재
                    if grid_map.map[robot_y][robot_x+1].req_energy == inf:
                        self.dir_x = 0
                        self.dir_y = -1
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                    ###
                    # 위쪽에 장애물 존재
                    if grid_map.map[robot_y-1][robot_x].req_energy == inf:
                        self.dir_x = 1
                        self.dir_y = 0
                        if grid_map.map[robot_y][robot_x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                        # 힘들어진다.
                        if robot_x == 0:
                            self.half == 1
                    if robot_y == 9:
                        self.line3 -= 1
                

        print(self.line3)
        print(self.dir_x)
        print(self.dir_y)
        new_x = robot_x + self.dir_x
        new_y = robot_y + self.dir_y

        self.pathlog.add((new_x,new_y))




        #END OF EXAMPLE CODE

        ######################

        ##### DO NOT CHANGE RETURN VARIABLES! #####
        ## The below codes are fixed. The users only determine the mode and/or the next position (coordinate) of the robot.
        ## Therefore, you need to match the variables of return to simulate.
        (new_x, new_y) = self.tunning( [new_x, new_y] )
        return (new_x, new_y)

