#!/usr/bin/env python
# #####################################################################################################
# SENDING/RECEIVING APPLICATION THREADS - add your business logic here!
# Note: you can use a single thread, if you prefer, but be carefully when dealing with concurrency.
#######################################################################################################
from socket import MsgFlag
import time
from application.message_handler import *
import application.app_config as app_conf
import application.app_config_obu as app_rsu_conf
from application.rsu_commands import *
import pickle

#-----------------------------------------------------------------------------------------
# Thread: rsu application transmission. In this example the thread is empty
#-----------------------------------------------------------------------------------------
#def rsu_application_txd(node, start_flag, my_system_rxd_queue, ca_service_txd_queue, den_service_txd_queue):
def rsu_application_txd(node, start_flag, bluetooth_txd_queue):

     while not start_flag.isSet():
          time.sleep (1)
     if (app_conf.debug_sys):
          print('STATUS: Ready to start - THREAD: application_txd - NODE: {}'.format(node),'\n')

     time.sleep(app_rsu_conf.warm_up_time)
          
     while (not app_rsu_conf.start_dc_txd.isSet()):
          time.sleep (1)

     data_center_msg = trigger_dc(node, time.time())
     bluetooth_txd_queue.put(data_center_msg)
     app_rsu_conf.start_dc_txd.clear()
     return


def rsu_application_rxd(node, start_flag, services_rxd_queue, my_system_rxd_queue):

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
		my_system_rxd_queue.put(msg_rxd)

	return

#-----------------------------------------------------------------------------------------
# Thread: my_system - In this example the thread is empty
#-----------------------------------------------------------------------------------------
def rsu_system(node, start_flag, coordinates, my_system_rxd_queue, rsu_control_txd_queue):
     while not start_flag.isSet():
          time.sleep (1)
          
     if (app_conf.debug_sys):
          print('STATUS: Ready to start - THREAD: my_system - NODE: {}'.format(node),'\n')

     start_rsu(rsu_control_txd_queue)
     turn_on(rsu_control_txd_queue)

     while True :
          msg_rxd=my_system_rxd_queue.get()
          if msg_rxd['msg_type']=='DC':
                if msg_rxd['information']['value'] == 1:
                    app_rsu_conf.dc_information = {'value':1}
                    app_rsu_conf.start_dc_txd.set()
                    
                    stored_sensor_messages_decoded = restore_bytes_io(msg_rxd['information']['sensor_messages'])
                    msg_rxd['information']['sensor_messages'] = stored_sensor_messages_decoded
                    print ('rsu_application - dc messsage received ', msg_rxd)
                    with open('information.pkl', 'wb') as file:
                         pickle.dump(msg_rxd, file)  
     return