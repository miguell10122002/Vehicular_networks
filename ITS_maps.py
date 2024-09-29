#!/usr/bin/env python

#################################################
## RSU or OBU
#################################################

rsu_range = 200
obu_range = 50

rsu_node = 1
obu_node = 2
person_node = 3

map = {"1":{'type': rsu_node, 'x':50,   'y':-50},
       "2":{'type': rsu_node, 'x':50,   'y':50},
       "3":{'type': rsu_node, 'x':-50,  'y':-50},
       "4":{'type': obu_node, 'x':0,    'y':-500, 'speed':70,   'direction':'f', 'heading':'N'},
       "5":{'type': obu_node, 'x':0,    'y':500,  'speed':70,   'direction':'f', 'heading':'S'},
       "6":{'type': obu_node, 'x':-500, 'y':-10,  'speed':100,  'direction':'f', 'heading':'N'},
       "7":{'type': obu_node, 'x':500,  'y':10,   'speed':100, 'direction':'f', 'heading':'N'},
       "8":{'type': obu_node, 'x':500,  'y':10,   'speed':100, 'direction':'f', 'heading':'N'}}

