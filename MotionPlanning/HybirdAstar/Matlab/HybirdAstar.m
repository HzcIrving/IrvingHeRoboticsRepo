%% Hybird A star demo 

%% 1. Load the cost values of cells in the vehicle costmap of a parking lot 
load parkingLotCostVal.mat 

%% 2. Create a binaryOccupancyMap with cost values 
map = binaryOccupancyMap(costVal); 

%% 3. create a state validator object for collision checking  
validator = validatorOccupancyMap; 

%% 4. Assign the map to the state validator object 
% This step need the admission of Navigation Toolbox 
validator.Map = map;  

%% 5. Initialize the plannerHybridAStar object with the state validator object. 
% Specify the MinTurningRadius and MotionPrimitiveLength properties of the planner.
planner = plannerHybridAStar(validator,'MinTurningRadius',4,'MotionPrimitiveLength',6); 

%% 6. start and goal poses 
startpos = [6 10 pi/2]; 
goalpos = [90 54 -pi/2]; 

%% 7. Plan a path from the start pose to the goal pose 
refpath = plan(planner, startpos, goalpos); 

%% 8. visualize 
show(planner)