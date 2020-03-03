#!/usr/bin/python
import os, sys
import ctypes
KIPR=ctypes.CDLL("/usr/lib/libkipr.so")

tophat_left = 1
tophat_right = 0
front_button = 0
side_button = 1
back_right_button = 2
back_button = 3
top_button = 4
left_motor = 1
right_motor = 0

claw = 2
closed = 1000
opened = 2000

arm = 0
joint = 1

down = 1150
mostlydown = 1000
middown = 1180
mid = 450
up = 0
horizontal = 0
angled = 500
vertical = 1000

black = 2000

def drive(left_power, right_power, time = 5):
	KIPR.mav(left_motor, left_power)
	KIPR.mav(right_motor, right_power)
	KIPR.msleep(time)
	stop()

def pivot(motor, power, degrees):
	KIPR.mav(motor, power)
	KIPR.msleep(degrees*18)
	stop()

def line_follow_right(power):
	if tophat(tophat_right) < black:
		KIPR.mav(left_motor, power-200)
		KIPR.mav(right_motor, power+200)
		KIPR.msleep(5)
	else:
		KIPR.mav(left_motor, power+200)
		KIPR.mav(right_motor, power-200)
		KIPR.msleep(5)

def line_follow_left(power):
	if tophat(tophat_left) < black:
		KIPR.mav(left_motor, power+200)
		KIPR.mav(right_motor, power-200)
		KIPR.msleep(5)
	else:
		KIPR.mav(left_motor, power-200)
		KIPR.mav(right_motor, power+200)
		KIPR.msleep(5)

def button_follow():
	if button(back_right_button):
		pivot(right_motor, -1000, 10)
	else:
		drive(-1500, -1300, 5)


def tophat(port):
	return KIPR.analog(port)	

def button(port):
	return KIPR.digital(port)

def servo(port, position):
	KIPR.set_servo_position(port, position)
	KIPR.msleep(500)

def stop():
	KIPR.mav(left_motor, 0)
	KIPR.mav(right_motor, 0)
	KIPR.msleep(5)

def wait(long = False):
	if long:
		KIPR.msleep(100000)
	KIPR.msleep(5000)

def enable():
	KIPR.enable_servos()

def move_claw(degrees):
	KIPR.mav(arm, 100)
	msleep(200*degrees)
	KIPR.mav(arm, 0)
	
def main():
	#left_motor = motor(1)
	#right_motor = motor(0)
	#string_lift = motor(0)
	#arm = motor(1)
	#claw = servo(0)

	
	#setup
	KIPR.enable_servos()
	servo(joint, angled)
	servo(arm, mid)
	pivot(left_motor, 1000, 90)
	wait()
	servo(claw, opened)
	
	#grab coupler
	#KIPR.wait_for_light(5)
	#KIPR.shut_down_in(119)
	servo(joint, horizontal)
	servo(arm, down)
	drive(1500, 1500, 1500)
	servo(claw, closed)

	while tophat(tophat_right) < black:
		drive(-1500, 1500)

	servo(claw, opened)
	servo(arm, mostlydown)
	while not button(top_button):
		line_follow_right(1300)
	drive(-1500, -1500, 5000)
	wait()

	#while tophat(tophat_right) > black:
	#	drive(-600, 0)

	servo(arm, up)
	servo(joint, vertical)
#	pivot(left_motor, -1200, 40)
#	while tophat(tophat_left) < black:
#		pivot(left_motor, -1200, 1)
#	while tophat(tophat_right) < black:
#		pivot(right_motor, -600, 1)

	pivot(right_motor, 1200, 90)
	while tophat(tophat_right) < black:
		drive(-1200, -1200)
	while tophat(tophat_left) < black:
		drive(-600, 0)
	
	
	#back align and turn onto ramp
	drive(-1500, -1500, 2500)
	drive(1000, 1000, 200)
	pivot(left_motor, 1200, 90)

	#go up ramp
	while not button(front_button):
		line_follow_right(1300)
	stop()
	
	#drop coupler
	#servo(arm, middown)
	#servo(joint, horizontal)
	#move_claw(open)
	#wait()
	#servo(arm, mid)
	drive(-1000, -1000, 500)
	pivot(right_motor, 1200, 90)
	
	#go to center
	servo(arm, mid)
	servo(joint, angled)
	servo(claw, closed)
	while not button(side_button):
		line_follow_right(1300)
	drive(-1000, -1200, 100)
	stop()
	servo(claw, opened)
	servo(joint, vertical)
	servo(arm, down)
	
	servo(claw, 1000)
	servo(arm, 900)
	servo(claw, 1200)
	servo(arm, 800)
	servo(claw, 1400)
	servo(arm, 700)
	servo(claw, 1600)
	servo(arm, 600)
	servo(claw, closed)
	servo(arm, mid)
	servo(joint, angled)

	#go back to corner
	while not button(back_button):
		button_follow()

	#align to prepare for drop	
	servo(arm, up)
	pivot(right_motor, 1500, 35)
	pivot(left_motor, 1200, 30)
	while tophat(tophat_left) < 2000:
		pivot(left_motor, 1200, 1)
	while tophat(tophat_right) < 2000:
		pivot(right_motor, -1200, 1)
	while tophat(tophat_right) > 2000:
		pivot(right_motor, -1200, 1)
	while not button(front_button):
		drive(1000, 1000, 1)

	servo(arm, middown)
	#servo(joint, vertical)
	servo(claw, opened)
	
if __name__== "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(),"w",0)
    main();
