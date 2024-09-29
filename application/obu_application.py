#!/usr/bin/env python
# #####################################################################################################
# SENDING/RECEIVING APPLICATION THREADS - add your business logic here!
# Note: you can use a single thread, if you prefer, but be carefully when dealing with concurrency.
#######################################################################################################
from socket import MsgFlag
import time
import ITS_maps as map
from application.message_handler import *
from application.obu_commands import *
import application.app_config as app_conf
import application.app_config_obu as app_obu_conf
from Queue import Empty

#-----------------------------------------------------------------------------------------
# Thread: appl ore fields to the dictionary
# 			  ii)  user interface is useful to allow the user to control your system execution.
#-----------------------------------------------------------------------------------------
def obu_application_txd(node, start_flag, my_system_rxd_queue, ca_service_txd_queue, den_service_txd_queue, bluetooth_txd_queue):

	while not start_flag.isSet():
		time.sleep (1)
	if (app_conf.debug_sys):
		print('STATUS: Ready to start - THREAD: application_txd - NODE: {}'.format(node),'\n')

	time.sleep(app_obu_conf.warm_up_time)

	if (app_conf.debug_app_ca):
		print ('obu_application - ca messsage  triggered with generation interval ', app_obu_conf.ca_generation_interval)
	ca_service_txd_queue.put(int(app_obu_conf.ca_generation_interval))

	while True:
		while (not app_obu_conf.start_den_txd.is_set()):
			time.sleep (1)
		#definir event information app_obu_conf.event_information = ....
		den_event = trigger_event(map.obu_node, app_obu_conf.accident_warning, 1) #TODO ver se o event_id deve ser SERIAL
		den_service_txd_queue.put(den_event)
		if (app_conf.debug_app_den):
			print ('obu_application - den messsage sent ', den_event)
	
		app_obu_conf.dc_information['value'] = 1
		dc_msg = trigger_dc(node, time.time())
		bluetooth_txd_queue.put(dc_msg)
		app_obu_conf.start_den_txd.clear()
		
	return



#-----------------------------------------------------------------------------------------
# Thread: application reception. In this example it receives CA and DEN messages. 
# 		Incoming messages are send to the user and my_system thread, where the logic of your system must be executed
# 		CA messages have 1-hop transmission and DEN messages may have multiple hops and validity time (if coded...)
#		Note: current version does not support multihop, roi and time validity. 
#-----------------------------------------------------------------------------------------
def obu_application_rxd(node, start_flag, services_rxd_queue, my_system_rxd_queue):

	while not start_flag.isSet():
		time.sleep (1)
	if (app_conf.debug_sys):
		print('STATUS: Ready to start - THREAD: application_rxd - NODE: {}'.format(node),'\n')

	while True :
		msg_rxd=services_rxd_queue.get()
		if (msg_rxd['msg_type']!="CA") and (app_conf.debug_app_ca):
			print ('obu_application - ca messsage received ',msg_rxd)
		elif (msg_rxd['msg_type']!="DEN") and (app_conf.debug_app_den):
			print ('obu_application - den messsage received ',msg_rxd)
		elif (msg_rxd['msg_type']!="DC") and (app_conf.debug_app_den):
			print ('obu_application - dc messsage received ',msg_rxd)
		#if msg_rxd['node']!=node:
		my_system_rxd_queue.put(msg_rxd)

	return


#-----------------------------------------------------------------------------------------
# Thread: my_system - implements the business logic of your system. This is a very straightforward use case 
# 			to illustrate how to use cooperation to control the vehicle speed. 
# 			The assumption is that the vehicles are moving in the opposite direction, in the same lane.
#			In this case, the system receives CA messages from neigbour nodes and, 
# 			if the distance is smaller than a warning distance, it moves slower,
#                         and warns other vehicles by sending a DEN message
# 			if distance is smaller that the emergency distance, it stops.
#-----------------------------------------------------------------------------------------
def obu_system(node, start_flag, accident_flag, coordinates, obd_2_interface, my_system_rxd_queue, movement_control_txd_queue):

	while not start_flag.isSet():
		time.sleep (1)
	if (app_conf.debug_sys):
		print('STATUS: Ready to start - THREAD: my_system - NODE: {}'.format(node),'\n')

	open_car(movement_control_txd_queue)
	turn_on_car(movement_control_txd_queue)
	car_move_forward(movement_control_txd_queue)

	stored_ca_messages = []
	stored_sensor_messages = []
	den_active = False
	while True :
		try:
			#msg_rxd=my_system_rxd_queue.get_nowait()
			msg_rxd=my_system_rxd_queue.get(timeout = 1)
			if msg_rxd['msg_type']=='SEN':
				stored_sensor_messages.append(msg_rxd)
				print("Sensor message: ", msg_rxd['sensor_type'])
    
			if msg_rxd['msg_type']=='CA':
				stored_ca_messages.append(msg_rxd)
				print("CA message")
    
			if msg_rxd['msg_type']=='DEN':
				stop_car(movement_control_txd_queue)
			
			if msg_rxd['msg_type']=='DC':
				if msg_rxd['information']['value']== 1:
					accident_flag.clear()
					#car_move_forward(movement_control_txd_queue)
		except Empty:
			pass
		
		if accident_flag.is_set():
			if not den_active:
				app_obu_conf.dc_information['ca_messages'] = stored_ca_messages
				app_obu_conf.dc_information['sensor_messages'] = stored_sensor_messages
				app_obu_conf.start_den_txd.set()
				den_active = True
		else:
			den_active = False

		stored_sensor_messages = clear_messages(stored_sensor_messages, app_obu_conf.sensor_max_time_stored)
		stored_ca_messages = clear_messages(stored_ca_messages, app_obu_conf.ca_max_time_stored)		
	return
  
	

