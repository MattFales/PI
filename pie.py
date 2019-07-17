#===============================Team Memebers======================================
# Yaobing Ni    Email: yaobingn@gmail.com
# Matthew Fales Email: msfales1@gmail.com
# Lei Wang      Email: 5763352@qq.com
#===================================================================================
# CODE for raspberry pie b3+
#==========================Imports==================================================
import RPi.GPIO as GPIO
import time
import Adafruit_CharLCD as LCD
from w1thermsensor import W1ThermSensor #temperature
GPIO.setmode(GPIO.BOARD)
GPIO.setup(port, GPIO.OUT)
port = 29 #fan,change on diagram to gpio 5 and pin 29 working with pin 12
#=====================Raspbery Pi pin setup============================================
lcd_rs = 38 # pin 38 GPIO 20
lcd_en = 12 # pin 12 GPIO 18
lcd_d4 = 16 # pin 16 GPIO 23
lcd_d5 = 18 # pin 18 GPIO 24
lcd_d6 = 22 # pin 22 GPIO 25
lcd_d7 = 32 # pin 32 GPIO 12 
lcd_backlight = 2  # default set to 2
#=====================Define LCD column and row size for 16 by 2 LCD===================
lcd_columns = 16       # these are built into the physical display 16 columes
lcd_rows = 2           # 2 rows of 16 32 total spots for character 
#=====================Tells lcd screen where to get infromation from ====================
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
#==============================define circuit===================================
pin_to_circuit = 31                             # pin 31 GPIO 6
def rc_time(pin_to_circuit):                    # to control photo sensor
	count = 0	                        # set count to 0
#---------------------------output on the ppin-------------------------------------------
	GPIO.setup(pin_to_circuit, GPIO.OUT)   # setup GPIO to work with on whats going out 
	GPIO.output(pin_to_circuit, GPIO.LOW)  # sets to low on the start  0/GPIO.LOW/False
	time.sleep(0.5)                        # need a second to catch up with what is being connected to the board .5 seconds is fine
	GPIO.setup(pin_to_circuit, GPIO.IN)   # Set up for rasb to read what is being taken in
#---------------------------count until the pin goes high---------------------------------
	while (GPIO.input(pin_to_circuit) == GPIO.LOW): # set each GPIO pin to a low setting 0/GPIO.LOW/False resets
		count += 1                              # return count of how mnay times this happens not needed but good for testing
	return count                                    # retrun count if needed
	pass
#======================================temperature def===================================== 	
def temper():                     # nothing passed in
	sensor1 = "04172100f2ff"  # sets it then the raspie see physical connections
	sensor2 = "041721089dff"  # sets it then the raspie see physical connections
	for sensor in W1ThermSensor.get_available_sensors():  # sees avaible meaning if they are hooked up
		if sensor.id == sensor1:                      # sensor1              
			temp1 = sensor.get_temperature(W1ThermSensor.DEGREES_F) # get data from temp 1 for sensor1
		if sensor.id == sensor2:                      # sensor2
			temp2 = sensor.get_temperature(W1ThermSensor.DEGREES_F) # get data from temp 1 for sensor2
		time.sleep(1) # pauses for a second there is lag at times so they cant run too quick
	return temp1, temp2   # sends bother varibles back
	pass      	
try:
	while True:   				     # i want this running all the time should take data every 5 minutes 
		light = rc_time(pin_to_circuit)      # photoesenor code to sense light 
		light = 10000 - light                # 10000-light make number easier to deal with
		lcd.clear()                          # make sure lcd screen is cleared
		temp1, temp2 = temper()              # Call to the def above
		lcd.message("temp1 %.2f" %(temp1))   # Display temperature for senors 1 two decimal places
		time.sleep(5)                        # Allows user to see what is displayed 5 seconds
		lcd.clear()                          # make sure it is clear between displays
		lcd.message("temp2 %.2f" %(temp2))   # Display temperature for senors 1 two decimal places
		time.sleep(5)                        # Allows user to see what is displayed 5 seconds
		lcd.clear()                          # make sure lcd screen is cleared
		if light < 4000:                     # if value of light is getting less than 4000 means the light is off in the room
			lcd.clear()                  # make sure lcd screen is cleared
			lcd.message("Light is OFF")  # Will display: Light is OFF
			time.sleep(5)                # Allows user to see what is displayed
			GPIO.output(port,1) 	     # set port/pin value to 1/GPIO.HIGH/True     
		if light > 4000:                     # if value ofl ight is greater than 4000 this means it is getting full light lights are on i nthe room              
			lcd.message("Light is ON")   # lcd display will display: Light is ON
			time.sleep(5)                # Allows user to see what is displayed 5 seconds
			lcd.clear()                  # make sure lcd screen is cleared
			if temp1 > 80 and temp2 > 80:# if the temperature of both sensors are above 80 
				lcd.clear()          # make sure lcd screen is cleared    
				lcd.message("Temperature is over 80F") # Will display: Temperature is over 80F"
				time.sleep(2)        # Allows user to see what is displayed 2 seconds
				lcd.clear()          # make sure lcd screen is cleared
				lcd.message("Fans are ON")  # Will display: Fans are ON"
				time.sleep(5)        # Allows user to see what is displayed 5 seconds
				lcd.clear()          # make sure lcd screen is cleared
				GPIO.output(port,0)  # set port/pin value to 0/GPIO.LOW/False  
			if temp1 < 80 and temp2 < 80:# if the temperature of both sensors are under 80    
				lcd.message("Temperature is under 80F" )   # Will display: Temperature is under 80F"
				time.sleep(2)        # Allows user to see what is displayed 2 seconds
				lcd.clear()          # make sure lcd screen is cleared
				lcd.message("Fans are OFF")
 				time.sleep(5)        # Allows user to see what is displayed 5 seconds
				lcd.clear()          # make sure lcd screen is cleared
				GPIO.output(port,1)  # set port/pin value to 1/GPIO.HIGH/True   
		time.sleep(300)                      # sleep for 5 minutes
except KeyboardInterrupt:        
	pass
finally:
	GPIO.cleanup()                                # cleans up gpio stuff