#!/usr/bin/env python
# #################################################
## FUNCTIONS USED IN VEHICLE - (x,y) location
#################################################
import time
from in_vehicle_network.car_motor_functions import get_vehicle_info
import in_vehicle_network.obd2 as obd2
import application.app_config as app_conf
from in_vehicle_network.conversion import *



#space_travelled =    [8, 16, 24, 32, 40], [2, 4, 6, 8, 10]

#------------------------------------------------------------------------------------------------
# position_update - updates x,y,t based on the current position, direction and heading. 
#       Note: No speed ot real behaviour of the vehicles is included
#       TIP: you can add here your position_update function. But, keep the parameters updated
#------------------------------------------------------------------------------------------------
def position_update(coordinates, obd_2_interface):

    speed, direction, heading=get_vehicle_info(obd_2_interface)
    

    x=coordinates['x']
    y=coordinates['y']
    

    if (obd_2_interface['vehicle_status']!=obd2.moving):
        return 
    current_time=time.time()
    delta_t=current_time-obd_2_interface['time']

    obd_2_interface['time']=current_time

    speed=obd_2_interface['speed']
    
    
    
    if (direction=='f'):
        distance = space_travelled[0][int(speed/20)-1]
    else:
        distance = space_travelled[1][int(speed/20)-1]   
    space=distance*delta_t

    if (app_conf.fixed_spaces): space=app_conf.delta_space


    if (((heading=='E') and (direction=='f')) or ((heading=='O') and (direction=='b'))):
        y=coordinates['y'] + space
    elif (((heading=='E') and (direction=='b')) or ((heading=='O') and (direction=='f'))):
         x=coordinates['x'] - space
         y=coordinates['y']
    elif (((heading=='N') and (direction=='f')) or ((heading=='S') and (direction=='b'))):
        x=coordinates['x']
        y=coordinates['y'] + space
    elif (((heading=='N') and (direction=='b')) or ((heading=='S') and (direction=='f'))):
        x=coordinates['x']
        y=coordinates['y'] - space  
  
    coordinates.update({'x':x, 'y':y, 't':current_time})
   
    if (app_conf.debug_location):
        print ('update location: x = ', coordinates['x'], '   y = ', coordinates['y'], '  time = ', coordinates['t'])

    return


#------------------------------------------------------------------------------------------------
# position_read - last known position
#------------------------------------------------------------------------------------------------
def old_position_read(coordinates):

    x=coordinates['x']
    y=coordinates['y']
    t=coordinates['t']

    return x,y,t
