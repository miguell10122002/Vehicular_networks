#!/usr/bin/env python
# #################################################
## FUNCTIONS USED TO CONTROL THE TRAFFIC LIGHT SYSTEM
#################################################
RASPBERRY = False
import rsu_legacy_systems.rsu_hw_config as rsu
import application.app_config as app_conf

if app_conf.local_test:
    RASPBERRY=False
else:
    RASPBERRY = True
    import RPi.GPIO as GPIO



#------------------------------------------------------------------------------------------------
# init_gpio- configure GPIO pins used to control the rsu
#------------------------------------------------------------------------------------------------
def init_gpio():

    if (RASPBERRY==True):
        GPIO.setmode(GPIO.BOARD)
        #   Blinking led pin configuration
        GPIO.setup(rsu.blinking_led, GPIO.OUT)
        GPIO.output(rsu.blinking_led, GPIO.LOW)
    if (app_conf.debug_gpio):
         print ('gpio control functions:  init_gpio BOARD')
         print ('gpio control functions:  init_gpio  blinking_led ', rsu.blinking_led, 'OUT LOW')
    
    if (RASPBERRY==True):
        GPIO.setup(rsu.green, GPIO.OUT)
        GPIO.output(rsu.green, GPIO.LOW)
        GPIO.setup(rsu.yellow, GPIO.OUT)
        GPIO.output(rsu.yellow, GPIO.LOW)
        GPIO.setup(rsu.red, GPIO.OUT)
        GPIO.output(rsu.red, GPIO.LOW)
    if (app_conf.debug_gpio):
        print ('gpio control functions:  init_gpio  green ', rsu.green, 'OUT LOW')
        print ('gpio control functions:  init_gpio  yellow ', rsu.yellow, 'OUT LOW')
        print ('gpio control functions:  init_gpio  red ', rsu.red, 'OUT LOW')
        #insert here other pins to configure (example: traffic light system)
    return True


#------------------------------------------------------------------------------------------------
# read_pin - read value from input pin
#------------------------------------------------------------------------------------------------
def read_pin ():

    if (RASPBERRY==True):
        value=GPIO.input(pin)
    if (app_conf.debug_gpio):
        print ('gpio control functions:  read_pin  pin ', pin, 'value = ', value)
    return value


#------------------------------------------------------------------------------------------------
# write_pin - write value to output pin
#------------------------------------------------------------------------------------------------
def write_pin (pin, value):

    if (RASPBERRY==True):
        if value == '1':
            GPIO.output(pin, GPIO.HIGH)
        else:
            GPIO.output(pin, GPIO.LOW)
    if (app_conf.debug_gpio):
        print ('gpio control functions:  write_pin  pin ', pin, 'value = ', value)
    return

#------------------------------------------------------------------------------------------------
# traffic_light - control the traffic light colours
#------------------------------------------------------------------------------------------------
def traffic_light (pin1, pin2, pin3):

    if (RASPBERRY==True):
        GPIO.output(pin3, GPIO.LOW)
        GPIO.output(pin2, GPIO.HIGH)
        GPIO.output(pin1, GPIO.HIGH)
    if (app_conf.debug_gpio):
        print ('gpio control functions:  traffic_light pin1 ', pin1, ' pin2  ', pin2, ' LOW pin3 ', pin3)
 
    return

def exit_gpio():

    if (RASPBERRY==True):
        GPIO.cleanup()
    if (app_conf.debug_gpio):
        print ('gpio control functions:   exit_gpio   cleanup ') 
    
    return

#################################################
# HIGH LEVEL CAR CONTROL FUNCTIONS - called by application layer protocol 
#################################################

def start_rsu(rsu_interface):
  
    if (app_conf.debug_rsu_control):
        print ('rsu control functions:  start rsu')
    init_gpio()
    rsu_interface['rsu_status']='ready'
    return rsu_interface

def stop_rsu(rsu_interface):
  
    if (app_conf.debug_rsu_control):
        print ('rsu control functions:  stop rsu')
    exit_gpio()
    rsu_interface['rsu_status']='not_ready'
    return rsu_interface

  
def change_sensor_status(rsu_interface, command):
        
    if (app_conf.debug_rsu_control):
        print ('rsu control functions:  pin on')
    write_pin (rsu.blinking_led, command)
    rsu_interface['rsu_status']='write_led'
    return rsu_interface

def set_tl_status(rsu_interface, command):   

    if command == 's_green':
        traffic_light (rsu.green, rsu.yellow, rsu.red)
        if (app_conf.debug_rsu_control):
            print ('rsu control functions:  traffic light green ', rsu.green, ' yellow ', rsu.yellow, '  red', rsu.red)
    elif command == 's_yellow':
        traffic_light (rsu.yellow, rsu.red, rsu.yellow)
        if (app_conf.debug_rsu_control):
            print ('rsu control functions:  traffic light yellow', rsu.green, ' yellow ', rsu.yellow, '  red', rsu.red)
    elif command == 's_red':
        traffic_light (rsu.red, rsu.yellow, rsu.green)
        if (app_conf.debug_rsu_control):
            print ('rsu control functions:  traffic light red   ', rsu.green, ' yellow ', rsu.yellow, '  red', rsu.red)
    rsu_interface['rsu_status']='write_tls'
    return rsu_interface

