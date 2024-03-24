# getting the main GPIO libraly
import RPi.GPIO as GPIO
# getting the time libraly
import time

# setting a current mode
GPIO.setmode(GPIO.BCM)
#removing the warings 
GPIO.setwarnings(False)
#creating a list (array) with the number of GPIO's that we use 
pins = [23,24] 

#setting the mode for all pins so all will be switched on 
GPIO.setup(pins, GPIO.OUT)

#for loop where pin = 23 and 24, this refers to gpio pin numbers, not pin sequence
for pin in pins :
	#setting the GPIO to HIGH or 1 or true
	GPIO.output(pin,  GPIO.HIGH)
	#wait 0,5 second
	time.sleep(2)
	#setting the GPIO to LOW or 0 or false
	GPIO.output(pin,  GPIO.LOW)
	#wait 0,5 second
	time.sleep(2)

	#Checking if the current relay is running and printing it 
	if not GPIO.input(pin) : 
		print("Pin "+str(pin)+" is working" )
		

#same but the difference is that  we have 
#for loop where pin = 14 next 15,17,18
# backwards
for pin in reversed(pins) :
	GPIO.output(pin,  GPIO.HIGH)
	time.sleep(2)

	GPIO.output(pin,  GPIO.LOW)
	time.sleep(2)


#cleaning all GPIO's 
GPIO.cleanup()
print ("Shutdown All relays")