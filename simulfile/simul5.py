from typing import List
from math import inf, isnan, sqrt
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
        self.movemode = 0
        self.current_x =8 
        self.current_y =8
        self.direction =0
        self.clean_x = 8
        self.clean_y = 8
        self.x_add = 1
        self.y_add = 1
        self.switch = 0
        
    def findH(self, present_x, present_y, desig_x, desig_y):
        x = abs(desig_x-present_x)
        y = abs(desig_y-present_y)
        distance = x*x + y*y
        distance = 10 * sqrt(distance)
        return(int(distance))


    def boundarycheck(self, checknode, max_h, max_w):
        check = True
        check_x = checknode[0]
        check_y = checknode[1]
        if(check_x < 0): check = False
        if(check_y < 0): check = False
        if(check_x > max_h): check = False
        if(check_y > max_w): check = False
        return check
    def obstaclecheck(self, checknode, grid_map:UserMap):
        check = True
        check_x = checknode[0]
        check_y = checknode[1]
        if(grid_map.map[check_y][check_x] != None):
            if(grid_map.map[check_y][check_x].req_energy == inf): 
                check = False
        return check
        #obstacle check
    def undefinedcheck(self, checknode, grid_map:UserMap): #not used in this code
        check = True
        check_x = checknode[0]
        check_y = checknode[1]
        if(grid_map.map[check_y][check_x].req_energy == None): check = False #undefined area check
        return check
    
    def surroundNode(self, checknode, maxh, maxw, desig_x, desig_y, grid_map: UserMap):
        if(self.boundarycheck(checknode, maxh, maxw)): 
             if(self.obstaclecheck(checknode, grid_map)):
                #if(UserRobot.undefinedcheck(checknode)):
                checknode[5]=self.findH(checknode[0], checknode[1], desig_x, desig_y)
                checknode[4]= checknode[4]+ 10
                checknode[6] = checknode[4] + checknode[5]
                return checknode      
        return None

    def findpath(self, self_x, self_y,  desig_x, desig_y, grid_map:UserMap): #find path by A-star algorihm, unknown area is obstcle
        
        self.max_h = grid_map.height - 1
        self.max_w = grid_map.width - 1

        nodemap = []
        for i in range(0, self.max_h+1):
            temparr = []
            for j in range(0, self.max_w+1):
                temparr.append([i,j, None, None, 0, 0, 0])
            nodemap.append(temparr)

        startnode = nodemap[self_x][self_y]
        closedSet = []
        openSet = []
        path=[]
        openSet.append(startnode)
        currentNode = startnode
        while len(openSet) > 0:

            minnode = openSet[0]
            for fnode in openSet:
                if minnode[6] > fnode[6]:
                    minnode = fnode  #find smallest node with F value
            currentNode = minnode

            if currentNode[0] == desig_x:
                if currentNode[1] == desig_y:
                    break #if designode reached break
            
            closedSet.append(currentNode)
            openSet.remove(currentNode)
            current_x = currentNode[0]
            current_y = currentNode[1]
            surround = []
            if (current_x < self.max_w):
                surnode = nodemap[current_x +1][current_y] 
                surround.append(surnode)
            if (current_x > 0):
                surnode = nodemap[current_x -1][current_y] 
                surround.append(surnode)
            if (current_y < self.max_h):
                surnode = nodemap[current_x][current_y+1] 
                surround.append(surnode)
            if (current_y > 0):
                surnode = nodemap[current_x][current_y-1] 
                surround.append(surnode)
            #count 4 possibilities: diagonal move not allowed!
            
            for checknode in surround:
                var = self.surroundNode(checknode, self.max_h, self.max_w, desig_x, desig_y, grid_map)
                if var != None:
                    if((checknode not in closedSet)):
                        if(checknode not in openSet): 
                            var[2]=current_x
                            var[3]=current_y   
                            openSet.append(var)
                            nodemap[var[0]][var[1]]=var
                        else: #if checknode is in openset
                            #dist = self.findH(currentNode[0], currentNode[1], var[0], var[1])
                            dist =10
                            if (currentNode[4] +  dist) < var[4]:
                                var[2] = current_x
                                var[3] = current_y #var.parent = currentnode.parent
                                var[4] = currentNode[4]+dist
                                var[6] = var[4] + var[5]

                                openSet.remove(checknode)
                                openSet.append(var)
                                nodemap[var[0]][var[1]]=var

        countnode = currentNode[:4]
        path.append(countnode[:2])
        while not(countnode[0] == startnode[0] and countnode[1] == startnode[1]):
            countnode = nodemap[countnode[2]][countnode[3]][:4]     
            path.append(countnode[:2])
        return path


    def getdirection(self, current_x, current_y, desig_x, desig_y):
        direction =0
        if(current_x < desig_x and current_y == desig_y): #go right
            direction = 1
        if(current_x == desig_x and current_y > desig_y): #go up 
            direction = 2
        if(current_x > desig_x and current_y == desig_y): #go left
            direction = 3
        if(current_x == desig_x and current_y < desig_y): #go down
            direction =4
        return direction

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

        #self.position.x or y: present location
        #self.dir_x or _y :  moving direction
        #self.mode : present mode
        #grid_map.height: map height
        #grid_map.width: map width
        #grid_map.map[y][x]: position on gridmap
        #grid_map.map[y][x].req_energy: required energy to clean up on present tile

        robot_x = self.position.x
        robot_y = self.position.y
        self.max_h = grid_map.height - 1
        self.max_w = grid_map.width - 1
        
        homepath = self.findpath(robot_x, robot_y, 8, 8, grid_map)
        #choose mode
        #movemode : 0 charge
        #movemode : 1 clean
        #movemode : 2 home
        #movemode : 3 return
        #movemode : 4 move
        if self.mode == STAY:
            self.mode = MOVE
            self.movemode = 4
        if robot_x == 8 and robot_y == 8: #if robot is home, charge
            if self.mode == CHAR:
                self.mode = MOVE
                self.movemode = 3
            if (self._fuel)  < 2000:
                self.mode = CHAR
                self.movemode = 0
                self.direction = 0


        if(self.mode == MOVE or self.mode == CLEN):
            if self.movemode == 3 and [robot_x, robot_y] != [self.current_x, self.current_y]:
                path = self.findpath(robot_x, robot_y, self.current_x, self.current_y, grid_map)
                if len(path) == 1:
                    nextmove = path[0]
                else:
                    nextmove = path[-2]
            if self.movemode == 3 and [robot_x, robot_y] == [self.current_x, self.current_y]:
                self.movemode = 4
            if((self._fuel) - 20 < (10*len(homepath))): #if energy is low
                if self.movemode != 2:
                    self.mode = MOVE
                    self.current_x = robot_x
                    self.current_y = robot_y
                    self.movemode = 2
                  
                if len(homepath) == 1:
                    nextmove = homepath[0]
                else:
                    nextmove = homepath[-2]         
            else:
                if self.movemode == 4:
                    path = self.findpath(robot_x, robot_y, self.clean_x, self.clean_y, grid_map) #first find path to desig location
                    if [robot_x, robot_y] == [self.clean_x, self.clean_y] or path[0] != [self.clean_x, self.clean_y]:#if desig location reached or path not exist 
                        if (self.clean_y == 0 or self.clean_y == self.max_h) and self.switch == 0:#better traversing rule, head to next desig location
                            self.clean_x = self.clean_x + self.x_add
                            self.y_add = -self.y_add
                            self.switch = 1
                        else:
                            self.clean_y= self.clean_y + self.y_add
                            self.switch = 0
                        if((self.clean_x > self.max_w and (self.clean_y == 0 or self.clean_y == self.max_h)) or (self.clean_x < 0 and (self.clean_y == 0 or self.clean_y == self.max_h))):
                            self.clean_x=8
                            self.clean_y=8
                            self.x_add = -self.x_add
                        
                        '''self.clean_x = self.clean_x + 1 # traversing rule, not used
                        if self.clean_x > self.max_w:
                            self.clean_x = 0
                            self.clean_y = self.clean_y + 1
                        if self.clean_y > self.max_h:
                            self.clean_y = 0'''
                        while True:
                            path = self.findpath(robot_x, robot_y, self.clean_x, self.clean_y, grid_map) #find path to new desig location
                            if path[0] == [self.clean_x, self.clean_y]:#if path exists, break
                                break                                
                            else: #if path doesn't exists, 
                                if (self.clean_y == 0 or self.clean_y == self.max_h) and self.switch == 0: #find path to another location
                                    self.clean_x = self.clean_x + self.x_add
                                    self.y_add = -self.y_add
                                    self.switch = 1
                                else:
                                    self.clean_y= self.clean_y + self.y_add
                                    self.switch = 0
                                if((self.clean_x > self.max_w and (self.clean_y == 0 or self.clean_y == self.max_h)) or (self.clean_x < 0 and (self.clean_y == 0 or self.clean_y == self.max_h))):
                                    self.clean_x=8
                                    self.clean_y=8
                                    self.x_add = -self.x_add
                                '''self.clean_x = self.clean_x + 1 # traversing rule, not used
                                if self.clean_x > self.max_w:
                                    self.clean_x = 0
                                    self.clean_y = self.clean_y + 1
                                if self.clean_y > self.max_h:
                                    self.clean_y = 0'''
                        
                    '''if path[0] != [self.clean_x, self.clean_y]: 
                        print("path not found!")
                        self.direction =0
                        nextmove = [robot_x, robot_y]
                    else:'''
                   # print(str([robot_x, robot_y]) + "->" + str([self.clean_x, self.clean_y]) + ':' + str(self._fuel))
                    if len(path) == 1:
                        nextmove = path[0]
                    else:
                        nextmove = path[-2]
            self.direction = self.getdirection(robot_x, robot_y, nextmove[0], nextmove[1])


        if self.direction == 0: 
            self.dir_x=0
            self.dir_y =0
        elif self.direction ==1: #>
            self.dir_x=1
            self.dir_y =0
        elif self.direction ==2: #^
            self.dir_x=0
            self.dir_y =-1
        elif self.direction ==3: #<
            self.dir_x = -1
            self.dir_y =0
        elif self.direction ==4: #v
            self.dir_x=0
            self.dir_y =1
        
        if (self.movemode == 4):
            if(grid_map.map[robot_y][robot_x].req_energy == 0):
                self.mode = MOVE
            else:
                self.mode = CLEN
        

        new_x = robot_x + self.dir_x
        new_y = robot_y + self.dir_y
        #if self.direction != 0:
        #    print(str([robot_x, robot_y]) + "->"+ str([new_x, new_y]) )
        #END OF EXAMPLE CODE
        ######################

        ##### DO NOT CHANGE RETURN VARIABLES! #####
        ## The below codes are fixed. The users only determine the mode and/or the next position (coordinate) of the robot.
        ## Therefore, you need to match the variables of return to simulate.
        (new_x, new_y) = self.tunning( [new_x, new_y] )
        return (new_x, new_y) 