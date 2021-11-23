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
        self.grav = 1
        self.lineclear = 1
        self.dir_lr = 1
        self.position.x = 8
        self.position.y = 8
        self.num = 1
        self.up_x = 0
        self.up_y = 0
        self.down_x = 0
        self.down_y = 0
        self.left_x = 0
        self.left_y = 0
        self.right_x = 0
        self.right_y = 0

    
    def sequenceLR_climb(self, grid_map, robot_x, robot_y):
        #Sequence_LEFT
        if self.dir_lr == 1:
            #General
            if robot_x != 8:
                #Case Left_Not Obstacle
                if grid_map.map[self.position.y +self.left_y][self.position.x +self.left_x].req_energy <= 20:
                    # Move Left #
                    self.dir_x = self.left_x
                    self.dir_y = self.left_y
                    if grid_map.map[self.position.y +self.left_y +self.down_y][self.position.x +self.left_x +self.down_x].req_energy == inf:
                        if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                    elif grid_map.map[self.position.y +self.left_y +self.down_y][self.position.x +self.left_x +self.down_x].req_energy <= 20 or robot_y-1 != 0:
                        if self.grav != self.lineclear:  
                            if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                                self.mode = MOVE
                                self.grav -= 1
                            else:
                                self.mode = CLEN

                        elif self.grav == self.lineclear:  
                            if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                    else:
                        if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN

                #Case Left_Obstacle                 
                elif grid_map.map[self.position.y +self.left_y][self.position.x +self.left_x].req_energy == inf:
                    #Case Up_Edge
                    if robot_y == 8:
                        # Move Right #
                        self.dir_x = self.right_x
                        self.dir_y = self.right_y
                        if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                            self.mode = MOVE
                            self.dir_lr = 0
                        else:
                            self.mode = CLEN

                    #Case Up_Not Obstacle
                    elif grid_map.map[self.position.y +self.up_y][self.position.x +self.up_x].req_energy <= 20:
                        # Move Up #
                        self.dir_x = self.up_x
                        self.dir_y = self.up_y
                        if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                            self.mode = MOVE
                            self.grav += 1
                        else:
                            self.mode = CLEN

                    #Case Up_Obstacle
                    elif grid_map.map[self.position.y +self.up_y][self.position.x +self.up_x].req_energy == inf:
                        if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                            self.mode = MOVE
                            self.dir_lr = 0
                            #turnback
                        else:
                            self.mode = CLEN                 

            #Edge
            elif robot_x == 8:
                #Case Down_Obstacle
                if grid_map.map[self.position.y +self.down_y][self.position.x +self.down_x].req_energy == inf:
                    # Move Up #
                    self.dir_x = self.up_x
                    self.dir_y = self.up_y
                    if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                        self.mode = MOVE
                        self.dir_lr = 0
                        self.lineclear += 1
                        self.grav += 1
                    else:
                        self.mode = CLEN
                        
                #Case Down_Not Obstacle
                elif grid_map.map[self.position.y +self.down_y][self.position.x +self.down_x].req_energy <= 20:
                    #Case Up_Not Obstacle
                    if grid_map.map[self.position.y +self.up_y][self.position.x +self.up_x].req_energy <= 20:
                        # Move Up #
                        self.dir_x = self.up_x
                        self.dir_y = self.up_y
                        if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                            self.mode = MOVE
                            self.dir_lr = 0
                            self.lineclear += 1
                            self.grav += 1
                        else:
                            self.mode = CLEN

        #Sequence_RIGHT
        else:
            #General
            if robot_x != 1:
                #Case Right_Not Obstacle
                if grid_map.map[self.position.y +self.right_y][self.position.x +self.right_x].req_energy <= 20:
                    # Move Right #
                    self.dir_x = self.right_x
                    self.dir_y = self.right_y
                    if grid_map.map[self.position.y +self.down_y +self.right_y][self.position.x +self.down_x +self.right_x].req_energy == inf:
                        if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN

                    elif grid_map.map[self.position.y +self.down_y +self.right_y][self.position.x+ +self.down_x +self.right_x].req_energy <= 20 or robot_y-1 != 0:
                        if self.grav != self.lineclear:   
                            if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                                self.mode = MOVE
                                self.grav -= 1
                            else:
                                self.mode = CLEN

                        elif self.grav == self.lineclear:  
                            if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                    else:
                        if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN

                #Case Right_Obstacle
                elif grid_map.map[self.position.y +self.right_y][self.position.x +self.right_x].req_energy == inf:
                    #Case Up_Not Obstacle
                    if grid_map.map[self.position.y +self.up_y][self.position.x +self.up_x].req_energy <= 20:
                        # Move Up #
                        self.dir_x = self.up_x
                        self.dir_y = self.up_y
                        if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                            self.mode = MOVE
                            self.grav += 1
                        else:
                            self.mode = CLEN

                    #Case Up_Obstacle
                    elif grid_map.map[self.position.y +self.up_y][self.position.x +self.up_x].req_energy == inf:
                        if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                            self.mode = MOVE
                            self.dir_lr = 1
                        else:
                            self.mode = CLEN

            #Edge
            elif robot_x == 1:
                if robot_y == 8:
                    # Move Right #
                    self.dir_x = self.right_x
                    self.dir_y = self.right_y
                    if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                        #Case Right_Obstacle
                        if grid_map.map[self.position.y +self.right_y][self.position.x +self.right_x].req_energy == inf:
                            self.mode = MOVE
                            self.grav -= 1

                        #Case Right_Not Obstacle
                        elif grid_map.map[self.position.y +self.right_y][self.position.x +self.right_x].req_energy <= 20:
                            self.mode = MOVE
                            # Move Right #
                            self.dir_x = self.right_x
                            self.dir_y = self.right_y
                    else:
                        self.mode = CLEN

                #Case Down_Obstacle
                elif grid_map.map[self.position.y +self.down_y][self.position.x +self.down_x].req_energy == inf:
                    if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                        self.mode = MOVE
                        self.dir_lr = 1
                        self.lineclear += 1
                    else:
                        self.mode = CLEN

                #Case Down_Not Obstacle
                elif grid_map.map[self.position.y +self.down_y][self.position.x +self.down_x].req_energy <= 20:
                    #Case Up_Edge
                    if robot_y == 8:
                        if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN

                    #Case Up_Not Obstacle
                    elif grid_map.map[self.position.y +self.up_y][self.position.x +self.up_x].req_energy <= 20:
                        # Move Up #
                        self.dir_x = self.up_x
                        self.dir_y = self.up_y
                        if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                            self.mode = MOVE
                            self.dir_lr = 1
                            self.lineclear += 1
                            self.grav += 1
                        else:
                            self.mode = CLEN


    def sequenceLR_fly(self, grid_map, robot_x, robot_y):
        #Sequence_LEFT
        if self.dir_lr == 1:
            #General
            if robot_x != 8:
                #Case Left_Not Obstacle
                if grid_map.map[self.position.y +self.left_y][self.position.x +self.left_x].req_energy <= 20:
                    # Move Left #
                    self.dir_x = self.left_x
                    self.dir_y = self.left_y
                    #Case Up_Edge
                    if robot_y == 8:
                        if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN
                            
                    elif grid_map.map[self.position.y +self.up_y +self.left_y][self.position.x +self.up_x +self.left_x].req_energy <= 20 or robot_y != 8:
                        if self.grav != self.lineclear:  
                            if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                                self.mode = MOVE
                                self.grav += 1
                            else:
                                self.mode = CLEN

                        elif self.grav == self.lineclear:  
                            if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                    else:
                        if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN

                #Case Left_Obstacle                 
                elif grid_map.map[self.position.y +self.left_y][self.position.x +self.left_x].req_energy == inf:
                    #Case Down_Not Obstacle
                    if grid_map.map[self.position.y +self.down_y][self.position.x +self.down_x].req_energy <= 20:
                        # Move Down #
                        self.dir_x = self.down_x
                        self.dir_y = self.down_y
                        if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                            self.mode = MOVE
                            self.grav -= 1
                        else:
                            self.mode = CLEN

                    #Case Down_Obstacle
                    elif grid_map.map[self.position.y +self.down_y][self.position.x +self.down_x].req_energy == inf:
                        if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                            self.mode = MOVE
                            self.dir_lr = 0
                        else:
                            self.mode = CLEN                 

            #Edge
            elif robot_x == 8:
                #Case Up_Obstacle
                if grid_map.map[self.position.y +self.up_y][self.position.x +self.up_x].req_energy == inf:
                    if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                        self.mode = MOVE
                        # Move Right #
                        self.dir_x = self.right_x
                        self.dir_y = self.right_y
                        self.dir_lr = 0
                        self.lineclear += 1
                    else:
                        self.mode = CLEN
                        
                #Case Up_Not Obstacle
                elif grid_map.map[self.position.y +self.up_y][self.position.x +self.up_x].req_energy <= 20:
                    #Case Down_Not Obstacle
                    if grid_map.map[self.position.y +self.down_y][self.position.x +self.down_x].req_energy <= 20:
                        # Move Up #
                        self.dir_x = self.up_x
                        self.dir_y = self.up_y
                        if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                            self.mode = MOVE
                            self.dir_lr = 0
                            self.lineclear += 1
                            self.grav += 1
                        else:
                            self.mode = CLEN

        #Sequence_RIGHT
        else:
            #General
            if robot_x != 1:
                #Case Right_Not Obstacle
                if grid_map.map[self.position.y +self.right_y][self.position.x +self.right_x].req_energy <= 20:
                    # Move Right #
                    self.dir_x = self.right_x
                    self.dir_y = self.right_y
                    #Case Up_Edge
                    if robot_y == 8:
                        if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN

                    elif grid_map.map[self.position.y +self.up_y +self.right_y][self.position.x +self.up_x +self.right_x].req_energy <= 20 or robot_y != 8:
                        if self.grav != self.lineclear:   
                            if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                                self.mode = MOVE
                                self.grav += 1
                            else:
                                self.mode = CLEN

                        elif self.grav == self.lineclear:  
                            if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                                self.mode = MOVE
                            else:
                                self.mode = CLEN
                    else:
                        if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                            self.mode = MOVE
                        else:
                            self.mode = CLEN

                #Case Right_Obstacle
                elif grid_map.map[self.position.y +self.right_y][self.position.x +self.right_x].req_energy == inf:
                    #Case Down_Not Obstacle
                    if grid_map.map[self.position.y +self.down_y][self.position.x +self.down_x].req_energy <= 20:
                        # Move Up #
                        self.dir_x = self.up_x
                        self.dir_y = self.up_y
                        if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                            self.mode = MOVE
                            self.grav -= 1
                        else:
                            self.mode = CLEN

                    #Case Down_Obstacle
                    elif grid_map.map[self.position.y +self.down_y][self.position.x +self.down_x].req_energy == inf:
                        if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                            self.mode = MOVE
                            self.dir_lr = 1
                        else:
                            self.mode = CLEN
                        
            #Edge
            elif robot_x == 1:
                if robot_y == 8:
                    # Move Right #
                    self.dir_x = self.right_x
                    self.dir_y = self.right_y
                    if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                        #Case Right_Obstacle
                        if grid_map.map[self.position.y +self.right_y][self.position.x +self.right_x].req_energy == inf:
                            self.mode = MOVE
                            self.grav -= 1

                        #Case Right_Not Obstacle
                        elif grid_map.map[self.position.y +self.right_y][self.position.x +self.right_x].req_energy <= 20:
                            self.mode = MOVE
                            # Move Right #
                            self.dir_x = self.right_x
                            self.dir_y = self.right_y
                    else:
                        self.mode = CLEN

                #Case Up_Obstacle
                elif grid_map.map[self.position.y +self.up_y][self.position.x +self.up_x].req_energy == inf:
                    if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                        self.mode = MOVE
                        self.dir_lr = 1
                        self.lineclear += 1
                    else:
                        self.mode = CLEN

                #Case Up_Not Obstacle
                elif grid_map.map[self.position.y +self.up_y][self.position.x +self.up_x].req_energy <= 20:
                    # Move Up #
                    self.dir_x = self.up_x
                    self.dir_y = self.up_y
                    if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                        self.mode = MOVE
                        self.dir_lr = 1
                        self.lineclear += 1
                        self.grav += 1
                    else:
                        self.mode = CLEN



    def climb(self, grid_map, robot_x, robot_y):
        #Sequence Left and Right
        if self.lineclear == 8 and robot_x == 0:
            # Move Down #
            self.dir_x = self.down_x
            self.dir_y = self.down_y
            if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                self.mode = MOVE
            else:
                self.mode = CLEN
        
        elif robot_y == self.grav:
            self.sequenceLR_climb(grid_map,robot_x,robot_y)

        #Sequence Up and Down
        else:
            #Case Down_Not Obstacle
            if grid_map.map[self.position.y +self.down_y][self.position.x +self.down_x].req_energy <= 20:
                # Move Down #
                self.dir_x = self.down_x
                self.dir_y = self.down_y
                if self.grav != self.lineclear:  
                    if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                        self.mode = MOVE
                        self.grav -= 1 
                    else:
                        self.mode = CLEN

                elif self.grav == self.lineclear:  
                    if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                        self.mode = MOVE
                    else:
                        self.mode = CLEN

            #Case Down_Obstacle
            elif grid_map.map[self.position.y +self.down_y][self.position.x +self.down_x].req_energy == inf:
                self.sequenceLR_climb(grid_map, robot_x, robot_y)


    def fly(self, grid_map, robot_x, robot_y):
        #Sequence Left and Right
        if self.lineclear == 8 and robot_x == 0:
            if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                self.mode = MOVE
                # Move Down #
                self.dir_x = self.down_x
                self.dir_y = self.down_y
            else:
                self.mode = CLEN
        
        elif robot_y == self.grav:
            if self.lineclear == 8 and robot_x == 0:
                #Case Down_Not Obstacle
                if grid_map.map[self.position.y +self.down_y][self.position.x +self.down_x].req_energy <= 20:
                    if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                        self.mode = MOVE
                        self.grav -= 1
                        self.fly(grid_map,robot_x,robot_y)
                    else:
                        self.mode = CLEN

            else:
                self.sequenceLR_fly(grid_map,robot_x,robot_y)

        #Sequence Up and Down
        else:
            #Case Up_Not Obstacle
            if grid_map.map[self.position.y +self.up_y][self.position.x +self.up_x].req_energy <= 20:
                # Move Up #
                self.dir_x = self.up_x
                self.dir_y = self.up_y
                if self.grav != self.lineclear:  
                    if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                        self.mode = MOVE
                        self.grav += 1 
                    else:
                        self.mode = CLEN

                elif self.grav == self.lineclear:  
                    if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                        self.mode = MOVE
                    else:
                        self.mode = CLEN

            #Case Up_Obstacle
            elif grid_map.map[self.position.y +self.up_y][self.position.x +self.up_x].req_energy == inf:
                self.sequenceLR_fly(grid_map, robot_x, robot_y)


    def quadrant(self, grid_map, robot_x, robot_y):
        if self.num == 1:
            self.mode = MOVE
            robot_x = 8 - self.position.x
            robot_y = 8 - self.position.y
            self.climb(grid_map, robot_x, robot_y)

        elif self.num == 2:
            self.mode = MOVE
            robot_x = 8 - self.position.y
            robot_y = self.position.x - 8
            self.climb(grid_map, robot_x, robot_y)

        elif self.num == 3:
            self.mode = MOVE
            robot_x = self.position.x - 8
            robot_y = self.position.y - 8
            self.climb(grid_map, robot_x, robot_y)

        elif self.num == 4:
            self.mode = MOVE
            robot_x = self.position.y - 8
            robot_y = 8 - self.position.x
            self.climb(grid_map, robot_x, robot_y)


    def algorithms( self, grid_map: UserMap ):

        if self.num == 1:
            self.up_x = 0
            self.up_y = -1
            self.down_x = 0
            self.down_y = 1
            self.left_x = -1
            self.left_y = 0
            self.right_x = 1
            self.right_y = 0

        elif self.num == 2:
            self.up_x = 1
            self.up_y = 0
            self.down_x = -1
            self.down_y = 0
            self.left_x = 0
            self.left_y = -1
            self.right_x = 0
            self.right_y = 1

        elif self.num == 3:
            self.up_x = 0
            self.up_y = 1
            self.down_x = 0
            self.down_y = -1
            self.left_x = 1
            self.left_y = 0
            self.right_x = -1
            self.right_y = 0
            
        elif self.num == 4:
            self.up_x = -1
            self.up_y = 0
            self.down_x = 1
            self.down_y = 0
            self.left_x = 0
            self.left_y = 1
            self.right_x = 0
            self.right_y = -1

        if self.num == 1:
            robot_x = 8 - self.position.x
            robot_y = 8 - self.position.y

        elif self.num == 2:
            robot_x = 8 - self.position.y
            robot_y = self.position.x - 8

        elif self.num == 3:
            robot_x = self.position.x - 8
            robot_y = self.position.y - 8

        elif self.num == 4:
            robot_x = self.position.y - 8
            robot_y = 8 - self.position.x

        if self.mode == CHAR:
            self.grav = 1
            self.lineclear = 1
            self.dir_lr = 1
            if self.num == 1:
                self.num = 2
                self.mode = MOVE
                self.dir_x = 1
                self.dir_y = 0
            elif self.num == 2:
                self.num = 3
                self.mode = MOVE
                self.dir_x = 0
                self.dir_y = 1
            elif self.num == 3:
                self.num = 4
                self.mode = MOVE
                self.dir_x = -1
                self.dir_y = 0
            elif self.num == 4:
                self.num = 1
                self.mode = MOVE
                self.dir_x = 0
                self.dir_y = 0

        elif self.mode == MOVE and self.position.x == 8 and self.position.y == 8:
            self.mode = CHAR

        elif self.mode == STAY:
            self.mode = MOVE
            self.dir_x = 0
            self.dir_y = -1

        else:
            self.quadrant(grid_map, robot_x, robot_y)


        if robot_x == 0 and robot_y == 1 and self.dir_y == self.up_y and self.dir_x == self.up_x:
            if grid_map.map[self.position.y][self.position.x].req_energy == 0:
                self.mode = MOVE
                self.dir_x = self.left_x
                self.dir_y = self.left_y
            else:
                self.mode = CLEN


        new_x = self.position.x + self.dir_x
        new_y = self.position.y + self.dir_y

        (new_x, new_y) = self.tunning( [new_x, new_y] )
        return (new_x, new_y)
