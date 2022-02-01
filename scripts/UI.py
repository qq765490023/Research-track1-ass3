#!/usr/bin/env python3
import time
import rospy
from getkey import getkey, keys
from geometry_msgs.msg import Twist
from move_base_msgs.msg import MoveBaseActionGoal
from sensor_msgs.msg import LaserScan

pub_vel = rospy.Publisher("cmd_vel", Twist) 
pub_goal = rospy.Publisher("/move_base/goal", MoveBaseActionGoal)
CA_status = -1
state_description = ''
vel = Twist()

def clbk_laser(msg): #this is the laser data callback,and will be called any time when receiced scan data. the emergence brake is set inside this part
    regions = {
        'right':  min(min(msg.ranges[0:143]), 10),
        'fright': min(min(msg.ranges[144:287]), 10),
        'front':  min(min(msg.ranges[288:431]), 10),
        'fleft':  min(min(msg.ranges[432:575]), 10),
        'left':   min(min(msg.ranges[576:719]), 10),
    }
    take_action(regions)
def take_action(regions): #action of the laser data. In this part CA_status will be updated according to the current situation.
    global CA_status
    global state_description
    global vel
    if regions['front'] > 1 and regions['left'] > 1 and regions['right'] > 1:
        state_description = 'case 1 - OK'
        CA_status = 1
    elif regions['front'] < 1 and regions['left'] > 1 and regions['right'] > 1:
        state_description = 'case 2 - front_disable'
        CA_status = 2
    elif regions['front'] > 1 and regions['left'] > 1 and regions['right'] < 1:
        state_description = 'case 3 - right_disable'
        CA_status = 3
    elif regions['front'] > 1 and regions['left'] < 1 and regions['right'] > 1:
        state_description = 'case 4 - left_disable'
        CA_status =4
    elif regions['front'] < 1 and regions['left'] > 1 and regions['right'] < 1:
        state_description = 'case 5 - front_right_disable'
        CA_status = 5
    elif regions['front'] < 1 and regions['left'] < 1 and regions['right'] > 1:
        state_description = 'case 6 - front_left_disable'
        CA_status = 6
    elif regions['front'] < 1 and regions['left'] < 1 and regions['right'] < 1:
        state_description = 'case 7 - backward allowed'
        CA_status = 7
    elif regions['front'] > 1 and regions['left'] < 1 and regions['right'] < 1:
        state_description = 'case 8 - left_right_disable'
        CA_status = 8
    else:
        state_description = 'unknown case'
    if regions['front'] < 1 and vel.linear.x >0: #emergency brake
      vel.linear.x = 0
      pub_vel.publish(vel) 
    
def KB_control():
  print('please input the command:\nw: move forward and speed up\ns: stop\nx: backward\na: turn left\nd: turn right\nq: quit\n')
  vel = Twist()
  while True:  # making a loop
    time.sleep(0.01)
    key = getkey()
    if True:
        if key == 'w':
            vel.linear.x =  1
        elif key == 's':
            vel.linear.x = 0
        elif key == 'x':
            vel.linear.x = -1
        elif key == 'a':
            vel.angular.z = 10
            pub_vel.publish(vel)
            time.sleep(0.1)
            vel.angular.z = 0
        elif key == 'd':
            vel.angular.z = -10
            pub_vel.publish(vel)
            time.sleep(0.1)
            vel.angular.z = 0
        elif key == 'q':
            break 
        
    pub_vel.publish(vel)     

def KB_control_collision_avoidance(): #this part is for Keyboard control with assisted Collision Avoidance
  global CA_status
  print('please input the command:\nw: move forward and speed up\ns: stop\nx: backward\na: turn left\nd: turn right\nq: quit\n')
  global vel
  while True:  # making a loop
    time.sleep(0.01)
    key = getkey()
    if True:
        if key == 'w':
          if CA_status==2 or CA_status==5 or CA_status==6 or CA_status==7: 
            vel.linear.x = 0
          else:
            vel.linear.x = 1
        elif key == 's':
            vel.linear.x = 0
        elif key == 'x':
            vel.linear.x = -1
        elif key == 'a':
          if (CA_status==4 or CA_status==6 or CA_status==7 or CA_status==8) and vel.linear.x != 0 :
              vel.angular.z = 0
          else:
            vel.angular.z = 10
            pub_vel.publish(vel)
            time.sleep(0.1)
            vel.angular.z = 0
        elif key == 'd':
          if (CA_status==3 or CA_status==5 or CA_status==7 or CA_status==8) and vel.linear.x != 0 :
             vel.angular.z = 0
          else:
            vel.angular.z = -10
            pub_vel.publish(vel)
            time.sleep(0.1)
            vel.angular.z = 0
        elif key == 'q':
            print('You Pressed q!')
            break 
    pub_vel.publish(vel) 

def mov_goal():  #reach the desired goal inputed by user.
  pos = MoveBaseActionGoal()
  while True: 
   x, y = [float(x) for x in input("Enter target x and y in format:x y\nor input:-100 -100 to quit \n").split()]
   if x==-100:
    break
   print("heading to :"+str(x)+","+str(y))
   pos.goal.target_pose.pose.orientation.w = 1
   pos.goal.target_pose.header.frame_id = 'map'
   pos.goal.target_pose.pose.position.y = x
   pos.goal.target_pose.pose.position.x = y
   pub_goal.publish(pos)


rospy.init_node("UI")
sub_scan = None
while True:
 a = input("select option\n 1:input target and go reach there \n 2:control by keyboard \n 3:control by keyboard with collision-avoidance\n 4:quit \n" )
 if a=='1':
  mov_goal() #set a goal and reach there
 if a=='2':
  KB_control() #control with keyboard
 if a=='3':
  sub_scan = rospy.Subscriber('/scan', LaserScan, clbk_laser)
  KB_control_collision_avoidance() #control with keyboard and assisted with collision avoidance
 if a=='4':
  break
 pass
rospy.spin()
	
	
	
	
	
	
	
	
	
	
	
