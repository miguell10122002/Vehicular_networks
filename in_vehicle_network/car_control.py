#!/usr/bin/env python
# #################################################
## ACCESS TO IN-VEIHICLE SENSORS/ATUATORS AND GPS
#################################################
import time
from in_vehicle_network.car_motor_functions import init_vehicle_info, open_vehicle, close_vehicle, turn_vehicle_off, turn_vehicle_on, new_movement, new_direction, new_speed, stop_vehicle, read_distance, create_sensor_message, read_camera_frame
from in_vehicle_network.location_functions import position_update
import in_vehicle_network.obd2 as obd2
import application.app_config as app_conf

def read_image_sensor_data(node, start_flag, my_system_rxd_queue):
    
	while not start_flag.isSet():
		time.sleep (1)
	
	while True:
		time.sleep(1)
		if app_conf.read_heavy_data.isSet():
			image = read_camera_frame()
			sensor_msg = create_sensor_message(node, image, 'image', time.time())
			my_system_rxd_queue.put(sensor_msg)

def read_distance_sensor_data(node, start_flag, danger_flag, accident_flag, my_system_rxd_queue):
    
	while not start_flag.isSet():
		time.sleep (1)
	
	while True:
		time.sleep(0.5)
		distance = read_distance()
		if distance > app_conf.danger_threshold:
			danger_flag.clear()
		else:
			danger_flag.set()
			app_conf.read_heavy_data.set()
			sensor_msg = create_sensor_message(node, distance, 'distance', time.time())
			my_system_rxd_queue.put(sensor_msg)
			if distance <= app_conf.accident_threshold:
				accident_flag.set()
				app_conf.read_heavy_data.clear()
				while accident_flag.is_set():
					time.sleep(1)
	return
 
	
 
#-----------------------------------------------------------------------------------------
# Thread - update location based on last known position, movement direction and heading. 
#         Note: No speed information and vehicles measurements are included.
#         TIP: In case, you want to include them, use obd_2_interface for this purpose
#-----------------------------------------------------------------------------------------
def update_location(node, start_flag, coordinates, obd_2_interface):
	gps_time = 2

	while not start_flag.isSet():
		time.sleep (1)
	if (app_conf.debug_sys):
		print('STATUS: Ready to start - THREAD: update_location - NODE: {}\n'.format(node),'\n')

	while True:
		time.sleep(gps_time)
		position_update(coordinates, obd_2_interface)
	return


#-----------------------------------------------------------------------------------------
# Car Finite State Machine
# 		initial state: 	closed  - Car is closed and GPIO/PWN are not initialise
#				input: 	car_command = 'e' (open car): next_state: opened
#		next_state:		opened 	- Car is open and GPIO/PWN are initialised
#				input: 	car_command = '1' (turn on):	next_state: ready
#						car_command = 'x' (disconnect): next_state: closed
# 		next_state:		ready	- Car is able to move 
#				input: 	car_command in ['f','b'] (move forward or backward) - next_state: moving
#                       car_command in ['l','r'] (turn left or right) - next_state: same state
#                       car_command in ['i','d'] (increase or decrease speed) - next_state: same state  
#                       car_command = 's' (stop) - next_state: stop
# 						car_command = '0' (turn off):	next_state: not_ready
# 						car_command = 'x' (disconnect): next_state: closed	
# 		next_state:		moving/stopped	- car is moving or stop
#				input: 	car_command in ['f','b', 'l','r',i','d','s','0','x'] similar to ready state
# 		next_state:		not_ready	- Car is turned off and not reasy to move
#				input: 	car_command = '1' (turn on):	next_state: ready
# 						car_command = 'x' (disconnect): next_state: closed	 				
#-----------------------------------------------------------------------------------------
#obd_2_interface:  speed, speed_var, direction, steering_wheel, heading,  vehicle_status)
#-----------------------------------------------------------------------------------------
# Thread - control the car movement - uses the FSM described before
#-----------------------------------------------------------------------------------------
def movement_control(node, start_flag, coordinates, obd_2_interface, movement_control_txd_queue):
	
	
	while not start_flag.isSet():
		time.sleep (1)
	if (app_conf.debug_sys):
		print('STATUS: Ready to start - THREAD: movement_control - NODE: {}\n'.format(node),'\n')
	
	init_vehicle_info(obd_2_interface)

	while True:
		move_command=movement_control_txd_queue.get()

		if (obd_2_interface['vehicle_status'] == obd2.closed):
			if (move_command == 'e'):			
				pwm_tm_control, pwm_dm_control, obd_2_interface=open_vehicle(obd_2_interface)
		elif (obd_2_interface['vehicle_status'] == obd2.opened):
			if (move_command == '1'):	
				obd_2_interface=turn_vehicle_on(obd_2_interface) 
			elif (move_command == 'x'):
				obd_2_interface=close_vehicle(obd_2_interface)
		elif (obd_2_interface['vehicle_status'] == obd2.not_ready):
			if (move_command == 'x'):
				obd_2_interface=close_vehicle(obd_2_interface)
			elif (move_command == '1'):	
				obd_2_interface=turn_vehicle_on(obd_2_interface)
		elif ((obd_2_interface['vehicle_status'] == obd2.ready) or
			(obd_2_interface['vehicle_status'] == obd2.moving) or
			(obd_2_interface['vehicle_status'] == obd2.stoped)):
			if (move_command in ['f','b']):
				obd_2_interface=new_movement(move_command,obd_2_interface)
			elif (move_command in ['l','r','f','b']): #forward e backward para seguir com o movimento...
				obd_2_interface=new_direction(move_command,obd_2_interface)
			elif (move_command in ['i','d']):	
				obd_2_interface=new_speed(move_command, obd_2_interface, pwm_tm_control)
			elif (move_command == 's'):
				obd_2_interface=stop_vehicle(obd_2_interface)
			elif (move_command == '0'):
				obd_2_interface=turn_vehicle_off(obd_2_interface)
			elif (move_command == 'x'):
				obd_2_interface=close_vehicle(obd_2_interface)
			else:
				print ('\n\nobd_2_interface', obd_2_interface, 'movement', move_command)
				print ('ERROR: movement control -> invalid status\n\n')


		time.sleep(app_conf.time_interval)

	return
