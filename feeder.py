import RPi.GPIO as GPIO
import time
import sys
import datetime
import pyrebase

GPIO.setwarnings(False)

#config firebase
config = {
    "apiKey": "AIzaSyCTJfwqKPU41I7G2BKc1hkS1Hzty6CkyDc",
    "authDomain": "auto-feeder-7efce.firebaseapp.com",
    "databaseURL": "https://auto-feeder-7efce-default-rtdb.firebaseio.com",
    "storageBucket": "auto-feeder-7efce.appspot.com"
    }

firebase = pyrebase.initialize_app(config)

#define variables for motor
delay = 0.008

coil_A_1_pin = 17
coil_A_2_pin = 27
coil_B_1_pin = 22
coil_B_2_pin = 23

en_a = 21
en_b = 20

#variable for switch button
button = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)
GPIO.setup(en_a, GPIO.OUT)
GPIO.setup(en_b, GPIO.OUT)

GPIO.output(en_a,True)
GPIO.output(en_b,True)

#setup button
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def setstep(w1, w2, w3, w4):
    GPIO.output(coil_A_1_pin, w1)
    GPIO.output(coil_A_2_pin, w2)
    GPIO.output(coil_B_1_pin, w3)
    GPIO.output(coil_B_2_pin, w4)
    
def run_motor(steps):
    for i in range(0, steps):
        setstep(1,0,1,0)
        time.sleep(delay)
        setstep(0,1,1,0)
        time.sleep(delay)
        setstep(0,1,0,1)
        time.sleep(delay)
        setstep(1,0,0,1)
        time.sleep(delay)
                     
while True:
    try:
             
        #button switch
        button_state = GPIO.input(button)
        steps = 100 # 100 by default, because we cannot control speed from App
        if button_state == 0:
            #save time
            time_now = datetime.datetime.now()
            time_stamp = time_now.strftime('%b %d, %Y %I:%M:%S %p [Manual]')
            database.update({"time_save": time_stamp})
            run_motor(steps)
            time.sleep(1)

        database = firebase.database()
        #get feeding mode in firebase to determine the steps
        feed_mode = database.child("feed_mode").get().val()
        if feed_mode == 1:
            steps = 50
        elif feed_mode ==2:
            steps = 100
        else:
            steps = 150

        #check if feed is enable from firebase
        feed_en = database.child("feed_en").get().val()
        
        if feed_en == True:
            run_motor(steps)
            #disable feed signal in firebase
            database.update({"feed_en": False})
         
           
    except KeyboardInterrupt:
        #check_input = input("press 's' to stop:")
        #if check_input == 's':
        GPIO.cleanup
        sys.exit(0)