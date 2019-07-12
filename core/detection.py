import RPi.GPIO as GPIO
import os, sys, datetime, logging
from time import sleep

#Set variable for folder path and date
pwd = os.path.dirname(os.path.abspath(__file__))
currentDT = datetime.datetime.now()

#logging
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename="%s/logfile"%pwd, filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.info("Script started at %s" %currentDT)

#gpio initalisation
GPIO.setmode(GPIO.BCM) #bcm mode
GPIO.setup(23, GPIO.IN) #lighting sensor
GPIO.setup(14, GPIO.OUT) #green led, used as on/off variable
GPIO.setup(15, GPIO.OUT) #red led, just initialising, used in php
GPIO.setup(24, GPIO.IN) #motion detector

#laser function
def laser(channel):
	if GPIO.input(23): #check if gpio 23 == 1
        	logging.info("Laser separated")
		print('---------------------------------')
		print('%s: laser separated' %currentDT )
		if GPIO.input(14): #check if alarm system is activated
			logging.critical("!!!Alarmsystem activated!!!")
			print('%s: !ALARMSYSTEM ACTIVATED!' %currentDT )
			os.system("python %s/alert.py"%pwd)
		else:
			logging.info("Alarmsystem deactivated")
			print('%s: Alarmsystem deactivated' %currentDT )
	else:
        	logging.info("Laser connected")
		print('%s: laser connected' %currentDT )
		print('---------------------------------')

#motion function
def motion(channel):
	logging.info("Motion detected")
	print('%s: motion detected' %currentDT )
	if GPIO.input(14): #check if alarm system is activated
		logging.critical("!!!Alarmsystem activated!!!")
		print('%s: !ALARMSYSTEM ACTIVATED!' %currentDT )
		os.system("python %s/alert.py"%pwd)
	else:
		logging.info("Alarmsystem deactivated")
		print('%s: Alarmsystem deactivated' %currentDT )

#detect both flanks on GPIO23, callback to "laser"
GPIO.add_event_detect(23, GPIO.BOTH, callback=laser)
#detect rising flank on GPIO24, callback to "motion"
GPIO.add_event_detect(24, GPIO.RISING, callback=motion)

#loop
try:
    while True:
            sleep(0.5)
	    currentDT = datetime.datetime.now()
#Keyboard interrupt
except KeyboardInterrupt:
	print "Stopped by user"
	logging.info("Stopped by user")
#GPIO cleanup
finally:
    GPIO.cleanup()
