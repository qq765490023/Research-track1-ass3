# Research track assignment
    Zhouyang Hong
    Sid: 5197402

# Overview
    This program consists of 3 modules, they are:
    1. Input a target in the format of "x y", Then the robot will arrive the    target position.
    2. Control the robot manually by pressing 'w','a','s','d' and 'x', respectively controls the robot move "forward", "turn left", "stop", "turn right", "backward".
    3. The same with module 2. but assisted with Collision avoidance.

# How to run this program UI.py
    To be noticed: run 5. before 6. or the robot might remain stationary.
    
    1. run this command on terminal "pip3 install getkey"
    2. clone this project to your <ros_workspace/src>
    3. run "catkin_make" on you work_space
    4. restart the terminal
    5. run "roslaunch final_assignment simulation_gmapping.launch"
    6. run "roslaunch final_assignment move_base.launch"
    7. run "rosrun final_assignment UI.py" %use "chmod +x UI.py" if failed
    8. Then you can just follow the instructions shown from UI.py
    
# Introduction of those three modules
## Input a target and robot go there
    This function is basing on /move_base/goal topic. By setting the desired postion x and y and another two parameters, we publish the MoveBaseActionGoal type message and the robot will move towards the goal.
## control the robot with keyboard
    To use the keyboard control the robot and with good experience, I used the "getkey" library, Which detects the pressed key and respond immediately. Basing on different hitten cases, the program publish different speed-controlling massages through "cmd_vel" topic. The program runs as follows:
    while true:
        detect_key_input()
        if 'w' hitten:
            set x-speed to 1
        elif 's' hitten:
            set x-speed to 0
        elif 'a' hitten:
            set w-speed to 10
            publish speed-message
            wait 0.1 second
            set w-speed to 0
        elif 'd' hitten:
            set w-speed to -10
            publish message
            wait 0.1 second
            set w-speed to 0
        elif 'x' hitten:
            set x-speed to -1
        publish speed-message
## control the robot with keyboard assisted with Collsion-Avoidance
    To assist keyboard control with Collision-Avoidance. There is a subscriber that subscribe to the /scan topic, which is the includes the information about obstacles around. There laser information is divided into 5 parts left, front-left, front, right-front and right. But only three of them are used which are left, front and right.
    According to if obstacle is within a specific range, we have 2*2*2=8 cases. Lets define the answer of "if there is a obstacle within 1 meter on there left" “No or Yes” as "L-0 and L-1". Then with front and right we can derive F-0,F-1,R-0,R-1. According to them, we can list all the cases.
    
    while /scan publishes message run:
        if F-0 and L-0 and R-0:
            set case 0
        if F-0 and L-0 and R-1:
            set case 1
        if F-0 and L-1 and R-0:
            set case 2
        if F-0 and L-1 and R-1:
            set case 3
        if F-1 and L-0 and R-0:
            set case 4
        if F-1 and L-0 and R-1:
            set case 5
        if F-1 and L-1 and R-0:
            set case 6
        if F-1 and L-1 and R-1:
            set case 7
        if F-1 and x-speed>0:
            set x-speed 0
        
    Now we have 8 different cases, we can take diffrent actions when we control the robot. As follows:
    
    while true:
        detect_key_input()
        if 'w' hitten and F-0:
            set x-speed to 1
        elif 's' hitten:
            set x-speed to 0
        elif 'a' hitten and (L-0 or x-speed==0):
            set w-speed to 10
            publish speed-message
            wait 0.1 second
            set w-speed to 0
        elif 'd' hitten and (R-0 or x-speed==0):
            set w-speed to -10
            publish message
            wait 0.1 second
            set w-speed to 0
        elif 'x' hitten:
            set x-speed to -1
        publish speed-message

# possible improvements:
    
    1 Reduce the threshold of which the robot assumes there is a obstacle around.
    2 Exploring new methods of setting x-speed when 'w' or 'x' was hitten.
    