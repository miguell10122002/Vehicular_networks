#!/usr/bin/env python
# ##########################################################################
## FUNCTIONS USED BY APPLICATION LAYER TO TRIGGER C-ITS MESSAGE GENERATION
# ##########################################################################
import application.app_config as app_conf

import ITS_maps as map
import application.app_config as app_conf
import application.app_config_obu as app_obu_conf
import application.app_config_rsu as app_rsu_conf


#------------------------------------------------------------------------------------------------
# trigger_ca -trigger the generation of CA messages- Funcao nao usada!
#       (out) - time between ca message generation
#-------------------------------------------------------------------------------------------------
def trigger_ca(node):
	trigger_node=-1
	while trigger_node!= node:
		trigger_node  = input (' CA message - node id >   ')
	ca_user_data  = input ('\nCA message - Generation interval >   ')
	ca_user_data=10
	return int(ca_user_data)

#------------------------------------------------------------------------------------------------
# trigger_even -trigger an event that will generate a DEN messsge
#       (out) - event message payload with: 
#						type: 'start' - event detection OU + 'stop'  - event termination 
#						rep_interval - repetition interval of the same DEN message; 0 for no repetiion
#						n_hops - maximum number of hops that the message can reach
#						(roi_x, roi_y) 
#-------------------------------------------------------------------------------------------------

def trigger_event(node_type, event_number, event_id, information = {}):
	
	if (node_type == map.obu_node):
		event_type = app_obu_conf.event_type[event_number]
		event_status = app_obu_conf.event_status[event_number] 
		event_id = event_id
		event_information = app_obu_conf.event_information
		if event_status == 'start':
			rep_interval = app_obu_conf.rep_interval[event_number] 
			n_hops = app_obu_conf.n_hops[event_number]
			roi_x  = app_obu_conf.roi_x[event_number] 
			roi_y  = app_obu_conf.roi_y[event_number]
			latency = app_obu_conf.latency[event_number]
	elif  (node_type == map.rsu_node):
		event_type = app_rsu_conf.event_type[event_number]
		event_status = app_rsu_conf.event_status[event_number] 
		event_id = event_id
		event_information = app_rsu_conf.event_information
		if event_status == 'start':
			rep_interval = app_rsu_conf.rep_interval[event_number] 
			n_hops = app_rsu_conf.n_hops[event_number]
			roi_x  = app_rsu_conf.roi_x[event_number] 
			roi_y  = app_rsu_conf.roi_y[event_number]
			latency = app_rsu_conf.latency[event_number]
	event_msg={'event_type':event_type, 'event_information': event_information, 'event_status': event_status, 'event_id': int(event_id), 'rep_interval':int(rep_interval), 'n_hops': int(n_hops), 'roi_x':int(roi_x), 'roi_y': int(roi_y), 'latency':int(latency)}
	return event_msg

def trigger_dc(node, time, information = {}):
	node = node
	time = time
	dc_information = app_obu_conf.dc_information
	dc_msg={'msg_type':'DC', 'node':node, 'information': dc_information, 'time': time}
	return dc_msg

#------------------------------------------------------------------------------------------------
# position_node - retrieve nodes's position from the message
#------------------------------------------------------------------------------------------------
def position_node(msg):
	
	x=msg['pos_x']
	y=msg['pos_y']
	t=msg['time']

	return x, y, t


#------------------------------------------------------------------------------------------------
# movement_node - retrieve nodes's dynamic information from the message
#------------------------------------------------------------------------------------------------
def movement_node(msg):
	
	s=msg['speed']
	d=msg['dir']
	h=msg['heading']

	return s, d, h


