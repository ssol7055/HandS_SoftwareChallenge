***
## 1. Introduction
### 1. Goal
Develop an algorithm that cleans the given room within a limited battery. Try to clean the room as much as possible & as fast as possible!

### 2. Participants
Each participant will be scored separately.  
Please do not share or copy others’ codes. However, you may freely discuss with others about your algorithm.

### 3. Schedule
- 10.November 6 pm ~ 21.November 11:59 pm.  
Winners will be announced on 24.November.

***

## 2. Details
### 1. Map overview
A map is a n by n grid with a charger in the middle and some required energy value assigned to each grid. Components of the map are

- **Charger**
- **Obstacle**
- **Grid with dust**

Except the charger grid, other grids have some “required energy” value assigned. If the required energy of that grid is:

- **Infinite**: the grid is an obstacle. The robot cannot go to that grid.
- **Constant energy in range [0,20]**: The grid has that amount of dust. The robot must consume at least that much energy to clean that grid.

### 2. Example map
![example map](/images/example_map.png)

The example map included in the simulator has 17 by 17 grids.  
We will now think of this map as a room.

As you can see, there are three types of grids.

	1. Robot charger (🔋)
	2. Obstacles (🔵)
	3. Dust (🟥🟧🟨..)

- **Robot charger (🔋)**  
The charger is in the middle of the room (position (8,8)).

- **Obstacle (🔵)**  
These grids have infinite energy, meaning that the robot cannot go to these grids.  
They can be understood as the legs of 4 pieces of furniture. The 4 pieces of furniture are as follows.

	- Bed
	- Desk
	- Closet
	- Rocking chair

![furniture](/images/furniture.PNG)

- **Dust (🟥🟧🟨..)**  
These grids have some required energy value assigned. The values are in range [0,20] and represent the amount of dust.  
In order to clean this dust, the robot must consume at least that much energy from its battery.

### 3. Robot  
- Starting position  
	- The robot starts from the position of the charger with a full battery. The charger is located at the middle of the map (8,8)

- Battery  
	- The robot has a battery capacity of 3000. The battery can be charged  up to 3 times at the charger. The battery is charged instantly. 

- Sight
	- Initially, the map information (location of obstacle, amount of dust, etc.) is hidden. At this point, all the robot can see is the 3 by 3 square around it.
	- Each time the robot changes its position, it acquires additional information about the 3 by 3 square around it.
	- If the robot has never seen a particular grid yet, the required energy of that grid is "None".  

- Modes
	- At each turn, the robot can choose among these 4 modes.  
      
		- `STAY`:  The robot stays in current grid. This is the initial mode at the start of simulation.
		- `MOVE`: The robot moves to another grid. The robot can only move one grid at a turn and consumes energy of 10.
		- `CLEN`: The robot cleans a grid. Each time this mode is selected, the robot consumes 10 energy from its battery, then cleans 10 or less dust depending on the remaining dust.  
		(ex. grid with 13 energy: after the first CLEN grid has 3 energy left, after the second CLEN grid has 0 energy left. The total energy consumption is 20.)
		- `CHAR`: The robot charges its battery. It has to be located at the charger if it wants to be charged. The battery is charged instantly.


### 4. Terminating condition
The simulation ends as soon as your algorithm satisfies one of the conditions below.

	1. the robot runs out of battery
	2. the room is perfectly cleaned

If you get stuck in an infinite loop, the code will automatically terminate after some amount of time.

***

## 3. Simulator guideline
### 1. Download the simulator
You have 2 options.
- clone the git repository
```
git clone https://github.com/ssol7055/HandS_SoftwareChallenge
```
- download the zip file provided in the link below
	- https://drive.google.com/drive/folders/137wgPzpYsJf2TBS93FO72gqy4HzZ3jQT?usp=sharing
         
### 2. Setting environment
Assuming you already have Anaconda and VS Code installed, please run the following commands on your anaconda prompt to make and code in your virtual environment using VS code.
```
conda create -n robot python=3.7
conda activate robot
conda install -c conda-forge toml
code
```
### 3. Code your algorithm
You can code your algorithm in `simul.py`. If you want to define any global variables, define them in `__init__` function.  Code your algorithm in `algorithms` function.
- Caution: do not change any arguments and returns in `algorithms` function.
```python
class UserRobot(VacuumCleaner):
    def __init__(...):
        # Define your variables

    def algorithms(...):
        # Write your algorithm in here, but do not change input arguments and returns.
```
### 4. Run the simulator
Run `main.py` to simulate your robot.
- Simulation
```
$ python main.py
>>> Simple Robot Sim (SBSim) <<<
[Simulator]
 - mode(skip?): True
[Robot]
 - fuel: 200
 - energy consumption: 10
 - start position: (0, 0)
 - vision sight: 2
[Map]
 - map name: example vacuum static
 - random?: False
 - map size: (8, 8)

Debug map
🚕🟥🟥🟨..🟥🟨🟥
🟥🔵🟨🟨🟧🟧🟥🟥
🟨🟥🔵🟧🟥🟧🟨🟨
🟥🟥🟧🔵🟥🟨🟧🟧
🟥🟧🟨🟨🟢🟨....
🟨🟨🟧🟧🟥🟥🟥🟧
..🟥🟥🟧🟨🟨🟨🟨
🟨🟧..🟧🟨🟨🟧🟥

Time : 0 -------
🚕🟥🟥🟪🟪🟪🟪🟪
🟥🔵🟨🟪🟪🟪🟪🟪
🟨🟥🔵🟪🟪🟪🟪🟪
🟪🟪🟪🟪🟪🟪🟪🟪
🟪🟪🟪🟪🟪🟪🟪🟪
🟪🟪🟪🟪🟪🟪🟪🟪
🟪🟪🟪🟪🟪🟪🟪🟪
🟪🟪🟪🟪🟪🟪🟪🟪

Time : 50 -------
................
🟥🔵🟨🟨🟧🟧🟥..
🟨🟥🔵🟧🟥🟧🟨..
🟪🟪🟪🟪🟪🟨🟧..
🟪🟪🟪🟪🟪🟨....
🟪🟪🟪🟪🟪🟥🟥..
🟪🟪🟪🟪🟪🟨🟨🚕
🟪🟪🟪🟪🟪🟨🟧🟥
Robot, fuel : 0
Robot, postion:
[0, 0]->[0, 0]->(1, 0)->(1, 0)->(2, 0)->(3, 0)->(4, 0)->(4, 0)->(4, 0)->(5, 0)->(6, 0)->(6, 0)->(7, 0)->(7, 0)->(7, 0)->(7, 1)->(7, 2)->(7, 3)->(7, 4)->(7, 5)->(7, 6)->(7, 6)->(7, 6)->(7, 6)->(7, 6)->(7, 6)->(7, 6)->(7, 6)->(7, 6)->(7, 6)->(7, 6)->(7, 6)->(7, 6)->(7, 6)->(7, 6)->(7, 6)->(7, 6)->(7, 6)->(7, 6)->(7, 6)->(7, 6)->(7, 6)->(7, 6)->(7, 6)->(7, 6)->(7, 6)->(7, 6)->(7, 6)->(7, 6)->(7, 6)->(7, 6)*
Evaluate : 23.396226415094333 %
```
### 5. Viewer guideline
- 🟪: not detected
- 🟥: 13.33 ~ 20 dust
- 🟧: 6.66 ~ 13.33 dust
- 🟨: 0 ~ 6.66 dust
- .. : no dust (cleaned)
- 🚕: current location of the robot
- 🔋: charger
- 🔵: obstacle (furniture)

***

## 4. Scoring
- We will run your submitted code on a map with different furniture arrangements from the example map.
- The specific characteristics of the scoring map are as follows.
	- 17*17 grid
	- 4 pieces of furniture (same as the example map)
	- The furniture will be in different positions, and some furniture might be rotated.
	- The furniture will not overlap each other.
	   
- Your final score is the evaluation percentage of your submitted code on the scoring map.
- If more than two participants have the same evaluation percentage, the participant who spends less turns gets higher score.
- The top three high score winners will receive 70,000won, 50,000won, 30,000won, respectively.

***
## 5. Submission
- All participants must submit their “simul.py” file to the following google form until 21.nov 11:59 pm.
	- zip your simul.py file into (your name).zip
	- submit this zip file to https://forms.gle/mnWg4GY3nFWJNRuq6
