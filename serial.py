#import pyuarm
from time import sleep
import serial
#from pyuarm.tools.list_uarms import uarm_ports
import OSC
import time, threading


try:
	uarm1 = pyuarm.UArm(debug=False, port_name='/dev/cu.usbserial-AI04I16J')
	uarm1.set_position(0, 0, 0)
	uarm1.set_wrist(90)
	sleep(2)

except:
	print "Uarm 1 Not Available"

try:
	uarm2 = pyuarm.UArm(debug=False, port_name='/dev/cu.usbserial-AI04I16Q')
	uarm2.set_position(0, 0, 0)
	uarm2.set_wrist(90)
	sleep(2)
except:
	print "Uarm 2 Not Available"

server = OSC.OSCServer( ("127.0.0.1", 5005) )
server.addDefaultHandlers()


#Cartesian variables

#X: -300-300
#Y: 50 - 330
#Z: -150-250 ideal 100

x1 = 0
y1 = 0
z1 = 0

x2 = 0
y2 = 0
z2 = 0

#Angle Variables

ax1 = 90
ay1 = 150
az1 = 170

ax2 = 90
ay2 = 150
az2 = 170


#Polar Variables

#a goes between 0 degrees and 180 degrees from left to right
#S seems to work between 0-50 but doesn't have a great range
#h

global a1
global s1
global h1
global a2
global s2
global h2


global rot1
global rot2

a1 = 90
s1 = 1
h1 = 1


a2 =90
s2 = 1
h2 = 1


#Rotation
rot1 = 90
rot2 = 90




def arm1(addr, tags, args, source):
	if args[0] == "UP" or args[0] == "up" or args[0] == "Up":
		print "ARM1 UP"
		global a1
		global s1
		global h1
		h1 += 5
		if h1 > 40:
			h1=40
		print "a1: " + str(a1)+ " s1: " + str(s1)+ " h1: " + str(h1) 
		uarm1.set_polar_coordinate(a1, s1, h1, speed=200, wait=True)


	elif args[0] == "DOWN" or args[0] == "down" or args[0] == "Down":
		print "ARM1 DOWN"
		global a1
		global s1
		global h1 
		h1 -= 5
		if h1 < -100:
			h1 = -100
		print "a1: " + str(a1)+ " s1: " + str(s1)+ " h1: " + str(h1)
		uarm1.set_polar_coordinate(a1, s1, h1, speed=200, wait=True)

	elif args[0] == "LEFT" or args[0] == "left" or args[0] == "Left":
		print "ARM1 LEFT"
		global a1
		global s1
		global h1
		a1 -=5
		if a1 < 0:
			a1= 0
		print "a1: " + str(a1)+ " s1: " + str(s1)+ " h1: " + str(h1)
		uarm1.set_polar_coordinate(a1, s1, h1, speed=200, wait=True)


	elif args[0] == "RIGHT" or args[0] == "right" or args[0] == "Right":
		print "ARM1 RIGHT"
		global a1
		global s1
		global h1
		a1 +=5
		if a1 > 180:
			a1 = 180
		print "a1: " + str(a1)+ " s1: " + str(s1)+ " h1: " + str(h1)
		uarm1.set_polar_coordinate(a1, s1, h1, speed=200, wait=True)


	elif args[0] == "FORWARD" or args[0] == "forward" or args[0] == "Forward":
		print "ARM1 FORWARD"
		global a1
		global s1
		global h1
		s1 += 10
		if s1 > 50:
			s1 = 50
		print "a1: " + str(a1)+ " s1: " + str(s1)+ " h1: " + str(h1)
		uarm1.set_polar_coordinate(a1, s1, h1, speed=200, wait=True)


	elif args[0] == "BACK" or args[0] == "back" or args[0] == "Back":
		print "ARM1 BACK"
		global a1
		global s1
		global h1
		s1 -= 10
		if s1 < -150:
			s1 = -150
		print "a1: " + str(a1)+ " s1: " + str(s1)+ " h1: " + str(h1)
		uarm1.set_polar_coordinate(a1, s1, h1, speed=200, wait=True)


	elif args[0] == "CLOCKWISE" or args[0] == "clockwise" or args[0] == "Clockwise":
		print "ARM1 CLOCKWISE"
		global rot1
		rot1 += 5
		print "rot1: " + str(rot1)
		uarm1.set_wrist(rot1)

	elif args[0] == "COUNTERCLOCKWISE" or args[0] == "counterclockwise" or args[0] == "Counterclockwise" or args[0] == "Counter clockwise" or args[0] == "counter clockwise" or args[0] == "COUNTER CLOCKWISE" or args[0] == "Counter Clockwise":
		print "ARM1 COUNTERCLOCKWISE"
		global rot1
		rot1 += 5
		print "rot1: " + str(rot1)
		uarm1.set_wrist(rot1)

	elif args[0] == "CATCH" or args[0] == "catch" or args[0] == "Catch":
		print "ARM1 CATCH"
		p1 = True
		uarm1.set_pump(p1)
	elif args[0] == "RELEASE" or args[0] == "release" or args[0] == "Release":
		print "ARM1 RELEASE"
		p1 = False
		uarm1.set_pump(p1)
		
	elif args[0] == "RESET" or args[0] == "reset" or args[0] == "Reset":

		global a1
		global s1
		global h1
		global a2
		global s2
		global h2
		
		a1 = 90
		a2 = 90
		s1 = 1
		s2 = 1
		h1 = 1
		h2 = 1

		x1 = 0
		y1 = 0
		z1 = 0
		x2 = 0
		y2 = 0
		z2 = 0
		try:
			uarm1.set_position(0,0,0)
			uarm1.set_wrist(90)
		except:
			print "UArm1 not connected"

		try:
			uarm2.set_position(0,0,0)
			uarm2.set_wrist(90)
		except:
			print "UArm2 not connected"
        
	else:
		print("%s is not a valid command") % args


def arm2(addr, tags, args, source):
	if args[0] == "UP" or args[0] == "up" or args[0] == "Up":
		print "ARM2 UP"
		global a2
		global s2
		global h2
		h2 += 5
		if h2 > 45:
			h2 = 45
		print "a2: " + str(a2)+ " s2: " + str(s2)+ " h2: " + str(h2)
		uarm2.set_polar_coordinate(a2, s2, h2, speed=200, wait=True)

	elif args[0] == "DOWN" or args[0] == "down" or args[0] == "Down":
		print "ARM2 DOWN"
		global a2
		global s2
		global h2
		h2 -= 5
		if h2 < -50:
			h2 = -50
		print "a2: " + str(a2)+ " s2: " + str(s2)+ " h2: " + str(h2)
		uarm2.set_polar_coordinate(a2, s2, h2, speed=200, wait=True)

	elif args[0] == "LEFT" or args[0] == "left" or args[0] == "Left":
		print "ARM2 LEFT"
		global a2
		global s2
		global h2
		a2 -=5
		if a2 < 0:
			a2 = 0
		print "a2: " + str(a2)+ " s2: " + str(s2)+ " h2: " + str(h2)
		uarm2.set_polar_coordinate(a2, s2, h2, speed=200, wait=True)

	elif args[0] == "RIGHT" or args[0] == "right" or args[0] == "Right":
		print "ARM2 RIGHT"
		global a2
		global s2
		global h2
		a2 +=5
		if a2 > 180:
			a2 = 180
		print "a2: " + str(a2)+ " s2: " + str(s2)+ " h2: " + str(h2)
		uarm2.set_polar_coordinate(a2, s2, h2, speed=200, wait=True)

	elif args[0] == "FORWARD" or args[0] == "forward" or args[0] == "Forward":
		print "ARM2 FORWARD"
		global a2
		global s2
		global h2
		s2 += 5
		if s2 > 500:
			s2 = 500
		print "a2: " + str(a2)+ " s2: " + str(s2)+ " h2: " + str(h2)
		uarm2.set_polar_coordinate(a2, s2, h2, speed=200, wait=True)

	elif args[0] == "BACK" or args[0] == "back" or args[0] == "Back":
		print "ARM2 BACK"
		global a2
		global s2
		global h2
		s2 -= 5
		if s2 < -100:
			s2 = -100
		print "a2: " + str(a2)+ " s2: " + str(s2)+ " h2: " + str(h2)
		uarm2.set_polar_coordinate(a2, s2, h2, speed=200, wait=True)

	elif args[0] == "CLOCKWISE" or args[0] == "clockwise" or args[0] == "Clockwise":
		print "ARM2 CLOCKWISE"
		global rot2
		rot2 += 5
		print "rot2: " + str(rot2)
		uarm2.set_wrist(rot2)

	elif args[0] == "COUNTERCLOCKWISE" or args[0] == "counterclockwise" or args[0] == "Counterclockwise" or args[0] == "Counter clockwise" or args[0] == "counter clockwise" or args[0] == "COUNTER CLOCKWISE" or args[0] == "Counter Clockwise":
		print "ARM2 COUNTERCLOCKWISE"
		global rot2
		rot2 -= 5
		print "rot2: " + str(rot2)
		uarm2.set_wrist(rot2)

	elif args[0] == "CATCH" or args[0] == "catch" or args[0] == "Catch":
		print "ARM2 CATCH"
		p2 = True
		uarm2.set_pump(p2)
	elif args[0] == "RELEASE" or args[0] == "release" or args[0] == "Release":
		print "ARM2 RELEASE"
		p2 = False
		uarm2.set_pump(p2)
	elif args[0] == "RESET" or args[0] == "reset" or args[0] == "Reset":
		
		global a1
		global s1
		global h1
		global a2
		global s2
		global h2
		
		a1 = 90
		a2 = 90
		s1 = 1
		s2 = 1
		h1 = 1
		h2 = 1

		x1 = 0
		y1 = 0
		z1 = 0
		x2 = 0
		y2 = 0
		z2 = 0
		try:
			uarm1.set_position(0,0,0)
			uarm1.set_wrist(90)
		except:
			print "UArm1 not connected"

		try:
			uarm2.set_position(0,0,0)
			uarm2.set_wrist(90)
		except:
			print "UArm2 not connected"
	else: 
		print("%s is not a valid command") % args

server.addMsgHandler( "/uarm1", arm1)
server.addMsgHandler("/uarm2", arm2)



# just checking which handlers we have added
print("Registered Callback-functions are :")
for addr in server.getOSCAddressSpace():
    print(addr)


# Start OSCServer
print("\nStarting OSCServer. Use ctrl-C to quit.")
st = threading.Thread( target = server.serve_forever )
st.start()


try :
    while 1 :
        sleep(1)

except KeyboardInterrupt :
	
	try:
		uarm1.disconnect()
	except:
		print "UArm 1 not available"
	try:
		uarm2.disconnect()
	except:
		print "Uarm 2 not available"
	print "Serial ports closed"
	print("\nClosing OSCServer.")
	server.close()
	print("Waiting for Server-thread to finish")
	st.join() ##!!!
	print("Done")