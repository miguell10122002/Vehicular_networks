#!/usr/bin/env python
# #################################################
## FUNCTIONS USED IN VEHICLE - Motor control
#################################################

import time
import in_vehicle_network.obd2 as obd2
import in_vehicle_network.obu_hw_config as obu
import application.app_config as app_conf
import base64

if app_conf.local_test:
    RASPBERRY=False
else:
    RASPBERRY = True
    import RPi.GPIO as GPIO
    from io import BytesIO
    from picamera import PiCamera


#speed variation 
delta_speed = 10


#################################################
#  GPIO CONTROL FUNCTIONS - control the HW
#################################################
#------------------------------------------------------------------------------------------------
# init_gpio- configure GPIO pins used to control the car
#------------------------------------------------------------------------------------------------
def init_gpio():

    if (RASPBERRY==False):
        return
    GPIO.setmode(GPIO.BOARD)
    if (app_conf.debug_gpio):
        print ('gpio control functions:  init_gpio BOARD')

    GPIO.setup(obu.trigger, GPIO.OUT)
    GPIO.setup(obu.echo, GPIO.IN)
    
    # enable pin
    GPIO.setup(obu.standby, GPIO.OUT)
    GPIO.output(obu.standby, GPIO.LOW)
    if (app_conf.debug_gpio):
        print ('gpio control functions:  init_gpio  standby pin ', obu.standby, 'OUT LOW')

    #Motor A - traction motor pins
    #pwm_tm - movement control
    GPIO.setup(obu.pwm_tm, GPIO.OUT)
    GPIO.output(obu.pwm_tm, GPIO.LOW)
    if (app_conf.debug_gpio):
        print ('gpio control functions:  init_gpio  pwm_tm ', obu.pwm_tm,  'pwm_dm ', obu.pwm_dm,'OUT LOW')

    #in1_tm - backward movement
    GPIO.setup(obu.in1_tm, GPIO.OUT)
    GPIO.output(obu.in1_tm, GPIO.LOW)
    if (app_conf.debug_gpio):
        print ('gpio control functions:  init_gpio  in1_tm pin ', obu.in1tdm, 'OUT LOW')

    #in2_tm - forward movement
    GPIO.setup(obu.in2_tm, GPIO.OUT)
    GPIO.output(obu.in2_tm, GPIO.LOW)
    if (app_conf.debug_gpio):
        print ('gpio control functions:  init_gpio  in2_tm pin ', obu.in2_tm, 'OUT LOW')

    #Motor B - direction motor pins
    #pwm_dm  - movement control
    GPIO.setup(obu.pwm_dm, GPIO.OUT)
    GPIO.output(obu.pwm_dm, GPIO.LOW)
    if (app_conf.debug_gpio):
        print ('gpio control functions:  init_gpio  pwm_dm ', obu.pwm_dm, 'OUT LOW')

    #in1_dm - turn left
    GPIO.setup(obu.in1_dm, GPIO.OUT)
    GPIO.output(obu.in1_dm, GPIO.LOW)
    if (app_conf.debug_gpio):
        print ('gpio control functions:  init_gpio  in1_dm pin ', obu.in1_dm, 'OUT LOW')

    #ini1_dm - turn right
    GPIO.setup(obu.in2_dm, GPIO.OUT)
    GPIO.output(obu.in2_dm, GPIO.LOW)
    if (app_conf.debug_gpio):
        print ('gpio control functions:  init_gpio  in2_dm pin ', obu.in2_dm, 'OUT LOW')

    return True

#------------------------------------------------------------------------------------------------
# init_pwm - configure pwm for speed variation
#------------------------------------------------------------------------------------------------
def init_pwm (speed, pwm_tm, pwm_dm):
    
    if (RASPBERRY==False):
        return -1, -1
    pwm_tm_control = GPIO.PWM (pwm_tm, speed)
    pwm_tm_control.start(speed)
    if (app_conf.debug_gpio):
        print ('gpio control functions:    init_pwn  pwm_tm_control ', pwm_tm_control, '   speed ', speed)
    
    pwm_dm_control = GPIO.PWM (pwm_dm, speed)
    pwm_dm_control.start(speed)
    if (app_conf.debug_gpio):
        print ('gpio control functions:    init_pwn  ipwm_dm_control', pwm_dm_control, '   speed ', speed)  
    return pwm_tm_control, pwm_dm_control

#------------------------------------------------------------------------------------------------
# activate - activate movement by seting the standby pin oh the H-bridge 
#------------------------------------------------------------------------------------------------
def activate():
    if (RASPBERRY==True):
        GPIO.output(obu.standby, GPIO.HIGH)
    if (app_conf.debug_gpio):
        print ('gpio control functions:   activate   standby ', obu.standby, ' HGH') 

#------------------------------------------------------------------------------------------------
# deactivate - deactivate movement by resseting the standby pin oh the H-bridge 
#------------------------------------------------------------------------------------------------
def deactivate():
    if (RASPBERRY==True):
        GPIO.output(obu.standby, GPIO.LOW)
    if (app_conf.debug_gpio):
        print ('gpio control functions:   deactivate   standby ', obu.__file__standby, ' LOW')

#------------------------------------------------------------------------------------------------
# move - control the vehicle movement, by seting one of the entries and the enable of the H-bridge IC circuit (A or B)
#------------------------------------------------------------------------------------------------
def move(on,off,pwm):

    if (RASPBERRY==True):
        GPIO.output(pwm, GPIO.HIGH)
        GPIO.output(off, GPIO.LOW)
        GPIO.output(on, GPIO.HIGH)
    if (app_conf.debug_gpio):
        print ('gpio control functions:    move  pwm ', pwm, ' HIGH     pin1 ', off, ' LOW   pin 2', on, 'HIGH')  
    return

#------------------------------------------------------------------------------------------------
# stop - stop the vehicle movement, by reseting all the pins of the H-bridge IC that controls the traction motor
#------------------------------------------------------------------------------------------------
def stop(in1, in2, pwm):

    if (RASPBERRY==True):
        GPIO.output(pwm, GPIO.LOW)
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
    if (app_conf.debug_gpio):
        print ('gpio control functions:    stop  pwm ', pwm, ' LOW     pin1 ', off, ' LOW   pin 2', on, 'LOW')  
    return True

#------------------------------------------------------------------------------------------------
# change_speed - change the the vehicle vehicle speed by modyfing the duty clycle of the traction motor 
#------------------------------------------------------------------------------------------------
def change_speed(speed, pwm_control):

    if (RASPBERRY==True):
        pwm_control.ChangeDutyCycle(speed)
    if (app_conf.debug_gpio):
        print ('gpio control functions:   change_speed pwm ', pwm, ' speed ',speed)  
    return speed

#------------------------------------------------------------------------------------------------
# exit_gpio - cancel gpio configuration 
#------------------------------------------------------------------------------------------------
def exit_gpio():
    if (RASPBERRY==True):
        GPIO.cleanup()
    if (app_conf.debug_gpio):
        print ('gpio control functions:   exit_gpio   cleanup ')  



#################################################
# HIGH LEVEL CAR CONTROL FUNCTIONS - called by application layer protocol 
#################################################


#------------------------------------------------------------------------------------------------
# open_vehicle - start configuration 
#------------------------------------------------------------------------------------------------
def open_vehicle(obd_2_interface):
    
    init_gpio()
    pwm_tm_control, pwm_dm_control = init_pwm(obd_2_interface['speed'],obu.pwm_tm, obu.pwm_dm)
    obd_2_interface['vehicle_status']=obd2.opened
    obd_2_interface['time']=time.time()
    if (app_conf.debug_obu_control):
        print ('obu control functions:  open_vehicle        status: opened')
        print (' obu_control functions: obd_2_interface ', obd_2_interface) 
    return pwm_tm_control, pwm_dm_control, obd_2_interface

#------------------------------------------------------------------------------------------------
# close_vehicle - cleanup GPIO status
#------------------------------------------------------------------------------------------------
def close_vehicle(obd_2_interface):

    exit_gpio()
    obd_2_interface['vehicle_status']=obd2.closed
    obd_2_interface['time']=time.time()
    if (app_conf.debug_obu_control):
        print ('obu control functions:  close_vehicle        status: closed')
        print (' obu_control functions: obd_2_interface ', obd_2_interface) 
    return obd_2_interface

#------------------------------------------------------------------------------------------------
# turn_vehicle_on -
#------------------------------------------------------------------------------------------------
def turn_vehicle_on(obd_2_interface):
    
    activate()
    obd_2_interface['vehicle_status']=obd2.ready
    obd_2_interface['time']=time.time()
    if (app_conf.debug_obu_control):
        print ('obu control functions:  turn_vehicle_on        status: ready')
        print (' obu_control functions: obd_2_interface ', obd_2_interface) 
    return obd_2_interface

#------------------------------------------------------------------------------------------------
# turn_vehicle_off - 
#------------------------------------------------------------------------------------------------
def turn_vehicle_off(obd_2_interface):

    deactivate()

    obd_2_interface['vehicle_status']=obd2.not_ready
    obd_2_interface['time']=time.time()
    if (app_conf.debug_obu_control):
        print ('obu control functions:  turn_vehicle_off       status: not_ready') 
        print (' obu_control functions: obd_2_interface ', obd_2_interface) 
    return obd_2_interface

#------------------------------------------------------------------------------------------------
# new_movement - 
#------------------------------------------------------------------------------------------------
def new_movement(new_move, obd_2_interface):

    if (new_move == 'f'):
        move(obu.in2_tm,obu.in1_tm,obu.pwm_tm)
    elif (new_move == 'b'):
        move(obu.in1_tm,obu.in2_tm,obu.pwm_tm)
    obd_2_interface['vehicle_status']=obd2.moving
    obd_2_interface['direction']=new_move
    obd_2_interface['time']=time.time()
    if (app_conf.debug_obu_control):
        print ('obu control functions:  new movement ', new_move, '  status: moving')
        print (' obu_control functions: obd_2_interface ', obd_2_interface) 
    return obd_2_interface

#------------------------------------------------------------------------------------------------
# new_direction - 
#------------------------------------------------------------------------------------------------
def new_direction(new_dir, obd_2_interface):
    
    if  (new_dir == 'l'):
        move(obu.in1_dm,obu.in2_dm,obu.pwm_dm)
    elif (new_dir == 'r'):
        move(obu.in2_dm,obu.in2_dm,obu.pwm_dm)
    else:
        new_dir=obd2.front
    heading = obd_2_interface['heading']
    obd_2_interface['heading'] = obd2.next_heading[new_dir][heading]
    print ('last heading', heading, 'new_dir', new_dir, 'next heading',obd_2_interface['heading'] )
    obd_2_interface['steering_wheel']=new_dir
    obd_2_interface['time']=time.time()   
    if (app_conf.debug_obu_control):
        print ('obu control functions:  new direction ', new_dir)
        print (' obu_control functions: obd_2_interface ', obd_2_interface)
    return obd_2_interface
    
  
#------------------------------------------------------------------------------------------------
# new_speed - 
#------------------------------------------------------------------------------------------------
def new_speed(move_command, obd_2_interface, pwm_control):

    if (move_command=='i'): obd_2_interface['speed_var']=obd2.speed_inc
    elif (move_command=='d'): obd_2_interface['speed_var']= obd2.speed_dec
    new_speed = obd_2_interface['speed'] + obd_2_interface['speed_var']
    if new_speed < 0 or new_speed >100:
        return obd_2_interface
    change_speed(new_speed, pwm_control)
    obd_2_interface['speed']=new_speed
    obd_2_interface['time']=time.time()
    if (app_conf.debug_obu_control):
        print ('obu control functions:  new_speed ', new_speed)
        print (' obu_control functions: obd_2_interface ', obd_2_interface)
    return obd_2_interface


#------------------------------------------------------------------------------------------------
# stop_vehicle - 
#------------------------------------------------------------------------------------------------
def stop_vehicle(obd_2_interface):

    stop(obu.in1_tm, obu.in2_tm, obu.pwm_tm)
    obd_2_interface['vehicle_status']=obd2.stoped
    obd_2_interface['time']=time.time()
    if (app_conf.debug_obu_control):
        print ('obu control functions:  stop             status: stoped ')
        print (' obu_control functions: obd_2_interface ', obd_2_interface)
    return obd_2_interface
 

#################################################
# OBD2 INTERFACE - obd2 bus
# obd_2_interface: speed, speed_var, direction, steering_wheel, heading,  vehicle_status
#################################################
def init_vehicle_info(obd_2_interface):
    
    obd_2_interface['speed_var']=0
    obd_2_interface['steering_wheel']=obd2.front
    obd_2_interface['vehicle_status']=obd2.closed
    obd_2_interface['time']=time.time()
    if (app_conf.debug_obu_control):
        print ('obu control functions:  init_vehicle            status: closed ')
        print (' obu_control functions: obd_2_interface ', obd_2_interface)    
    return obd_2_interface


def get_vehicle_complete_info(obd_2_interface):

    node_type=obd_2_interface['node_type']

    speed=obd_2_interface['speed']
    speed_var=obd_2_interface['speed_var']
    dir=obd_2_interface['direction']
    steer_wheel=obd_2_interface['steering_wheel']
    head=obd_2_interface['heading']
    vehicle_st=obd_2_interface['vehicle_status']
    time_obd2=obd_2_interface['time'] 
    return node_type, speed, speed_var, dir, steer_wheel, head, vehicle_st, time_obd2

def get_vehicle_info(obd_2_interface):
 
    speed=obd_2_interface['speed']
    dir=obd_2_interface['direction']
    head=obd_2_interface['heading']
    return speed, dir, head

def set_vehicle_info(speed, dir,  head, obd_2_interface):

    obd_2_interface['speed']=speed
    obd_2_interface['direction']=dir
    obd_2_interface['heading']=head
    obd_2_interface['time']=time.time()
    return obd_2_interface

def set_vehicle_complete_info(speed, speed_var, dir, steer_wheel, head, vehicle_st, obd_2_interface):

    obd_2_interface['speed']=speed
    obd_2_interface['speed_var']=speed_var
    obd_2_interface['direction']=dir
    obd_2_interface['steering_wheel']=steer_wheel
    obd_2_interface['heading']=head
    obd_2_interface['vehicle_status']=vehicle_st
    obd_2_interface['time']=time.time() 
    return obd_2_interface
 

def init_obd_2_interface(obd_2_interface):
    
    obd_2_interface['speed_var']=0
    obd_2_interface['steering_wheel']=obd2.front
    obd_2_interface['vehicle_status']=obd2.closed
    return obd_2_interface

def read_distance():
    if RASPBERRY == False:
        return 30 #TODO Alterar
    
    # set Trigger to HIGH
    GPIO.output(obu.trigger, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(obu.trigger, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(obu.echo) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(obu.echo) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def read_camera_frame():
    if RASPBERRY == False:
        return 0
    stream = BytesIO()
    camera = PiCamera()
    #camera.resolution(640, 480)
    camera.capture(stream, 'jpeg', use_video_port=True)
    stream.truncate()
    stream.seek(0)
    camera.close()
    
    data = base64.b64encode(stream.read()).decode("utf-8")
    return data

def create_sensor_message(node, sensor_reading, sensor_type, time):
    
    sensor_msg = {'msg_type':'SEN', 'node':node, 'sensor_type':sensor_type, 'sensor_reading':sensor_reading, 'time':time}
    return sensor_msg