#import pyuarm
from time import sleep
import serial
#from pyuarm.tools.list_uarms import uarm_ports

#print uarm_ports()

print serial.tools.list_ports

try:
	uarm1 = serial.Serial('/dev/cu.usbserial-AI04I16J')
	#uarm1.readline()
	#uarm1 = pyuarm.UArm(debug=False, port_name='/dev/cu.usbserial-AI04I16J')
	#uarm1.set_position(0, 0, 0)
	sleep(2)

except:
	print "WHAT THE FUCK"
	print "Uarm 1 Not Available"

try:
	#uarm2 = pyuarm.UArm(debug=False, port_name='/dev/cu.usbserial-AI04I16Q')
	#uarm2.set_position(0, 0, 0)
	uarm2 = serial.Serial('/dev/cu.usbserial-AI04I16Q')

	sleep(2)
except:
	print "Uarm 2 Not Available"

#Cartesian variables

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

a1 = 90
s1 = 1
h1 = 1


a2 =90
s2 = 1
h2 = 1



p1 = False
p2 = False

speed = 55


while True:


	try:

		var = raw_input()
	
		#UARM 1 - UP

		if var == 'q':
			x1 += 5
			if x1 > 180:
				x1=180
		elif var == 'w':
			x1 -= 5
			if x1 < 0:
				x1 = 0
		elif var == 'a':
			y1 +=5
			if y1 > 40:
				y1=40
		elif var =='s':
			y1 -=5
			if y1 < -100:
				y1 = -100
		elif var == 'z':
			z1 += 5
			if z1 > 50:
				z1 = 50
		elif var == 'x':
			z1 -= 5
			if z1 < -150:
				z1 = -150

		if var == '1':
			a2 += 5
			if a2 > 180:
				a2 = 180
		elif var == '2':
			a2 -= 5
			if a2 < 0:
				a2 = 0
		elif var == '3':
			s2 +=5
			if s2 > 45:
				s2 = 45
		elif var =='4':
			s2 -=5
			if s2 < -500:
				s2 = -500
		elif var == '5':
			h2 += 5
			if h2 > 500:
				h2 = 500
		elif var == '6':
			h2 -= 5
			if h2 < -500:
				h2 = -500

		elif var == 'r':
			x1 = 0
			y1 = 0
			z1 = 0
			x2 = 0
			y2 = 0
			z2 = 0
			try:
				uarm1.write("'#'25 G0 X0 Y0 Z0 F"+speed+"\n")
				#uarm1.set_position(0,0,0)
			except:
				print "UArm1 not connected"

			try:
				uarm2.write("'#'25 G0 X0 Y0 Z0 F"+speed+"\n")
				#uarm2.set_position(0,0,0)
			except:
				print "UArm2 not connected"

		elif var == ' ':
			try:
				print 'Python Cartesian Coords: Arm1 ' + ' : ' + 'x1:' + str(x1) + ' ' + 'y1:'+ str(y1) + ' ' + 'z1:'+ str(z1)
				print 'Python Cartesian Coords: Arm2 ' + ' : ' + 'x2:'+ str(x2) + ' ' + 'y2:' + str(y2) + ' ' + 'z2:'+ str(z2)
				print 'Python Polar Coords: Arm1 ' + ' : ' + 'a1:' + str(a1) + ' ' + 's1:'+ str(s1) + ' ' + 'h1:'+ str(h1)
				print 'Python Polar Coords: Arm2 ' + ' : ' + 'a2:'+ str(a2) + ' ' + 's2:' + str(s2) + ' ' + 'h2:'+ str(h2)
				print '\n'
				#print 'UArm1 Cartesian Position: ' + str(uarm1.get_position()) 
				#print 'UArm2 Cartesian Position: ' + str(uarm2.get_position()) 
				#print 'UArm1 Polar Coords: ' + str(uarm1.get_polar())
				#print 'UArm2 Polar Coords: ' + str(uarm2.get_polar())
				#print 'UArm1 Servo Angle: ' + str(uarm1.get_servo_angle())
				#print 'UArm2 Servo Angle: ' + str(uarm2.get_servo_angle())
			except:
				print "only 1 arm"
		elif var == 'p':
			p1 = not p1
		elif var =='o':
			p2 = not p2

		

		try:
			#uarm1.set_position(x1, y1, z1, speed=100, relative=False, wait=True)
		
			#uarm1.set_servo_angle(0, ax1)
			#uarm1.set_servo_angle(1, ay1)
			#uarm1.set_servo_angle(2, az1)
		
			#uarm1.set_polar_coordinate(a1, s1, h1, speed=200, wait=True)
			uarm1.write("'#'25 G0 X" + x1 +" Y"+y1+" Z"+ z1+" F"+speed+"\n")
			#uarm1.set_pump(p1)
		except:
			"Uarm1 not connected"
		try:
			#uarm2.set_position(x2, y2, z2, speed=100, relative=False, wait=True)
		
			#uarm2.set_servo_angle(0, ax2)
			#uarm2.set_servo_angle(1, ay2)
			#uarm2.set_servo_angle(2, az2)
			uarm2.write("'#'25 G0 X" + x2 +" Y"+y2+" Z"+ z2+" F"+speed+"\n")

			#uarm2.set_polar_coordinate(a2, s2, h2, speed=200, wait=True)


			#uarm2.set_pump(p2)
		except:
			print "Uarm2 not connected"
		sleep(0.1)

	except KeyboardInterrupt:
	
		#uarm1.disconnect()
		#uarm2.disconnect()
		try:
			uarm1.close()
		except:
			print "Uarm1 not connected"
		try:
			uarm2.close()
		except:
			print "Uarm2 not connected"
		print "Serial ports closed"

