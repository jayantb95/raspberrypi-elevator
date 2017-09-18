import RPi.GPIO as GPIO 
import time, Queue


 
GPIO.setmode(GPIO.BOARD)
#GPIO.cleanup()

#GPIO Setup for the buttons
BUTTON_ONE = 37
BUTTON_TWO = 35
BUTTON_THREE = 31
BUTTON_FOUR = 16
BUTTON_FIVE = 13
BUTTON_SIX = 7

#GPIO setup for the LEDs
LED_ONE = 38
LED_TWO = 36
LED_THREE = 32
LED_FOUR = 18
LED_FIVE = 15
LED_SIX = 11

#Buzzer
BUZZER_PIN = 40


GPIO.setup(BUTTON_ONE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_TWO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_THREE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_FOUR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_FIVE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_SIX, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(LED_ONE, GPIO.OUT) #Floor 1
GPIO.setup(LED_TWO, GPIO.OUT) #Floor 2
GPIO.setup(LED_THREE, GPIO.OUT) #Floor 3
GPIO.setup(LED_FOUR, GPIO.OUT) #Floor 4
GPIO.setup(LED_FIVE, GPIO.OUT) #Floor 5
GPIO.setup(LED_SIX, GPIO.OUT) #Floor 6

GPIO.setup(BUZZER_PIN, GPIO.OUT)

pwm_led1 = GPIO.PWM(LED_ONE, 500)
pwm_led2 = GPIO.PWM(LED_TWO, 500)
pwm_led3 = GPIO.PWM(LED_THREE, 500)
pwm_led4 = GPIO.PWM(LED_FOUR, 500)
pwm_led5 = GPIO.PWM(LED_FIVE, 500)
pwm_led6 = GPIO.PWM(LED_SIX, 500)

pwm_led1.start(0)
pwm_led2.start(0)
pwm_led3.start(0)
pwm_led4.start(0)
pwm_led5.start(0)
pwm_led6.start(0)

off = 0
odd = 20
even = 10

floorQ = Queue.Queue()


def updateLED(floorNumber):
    
    if floorNumber == 1:        
        pwm_led1.ChangeDutyCycle(odd)
        pwm_led2.ChangeDutyCycle(off)
        pwm_led3.ChangeDutyCycle(off)
        pwm_led4.ChangeDutyCycle(off)
        pwm_led5.ChangeDutyCycle(off)
        pwm_led6.ChangeDutyCycle(off)
    
    elif floorNumber == 2:
        pwm_led1.ChangeDutyCycle(off)
        pwm_led2.ChangeDutyCycle(even)
        pwm_led3.ChangeDutyCycle(off)
        pwm_led4.ChangeDutyCycle(off)
        pwm_led5.ChangeDutyCycle(off)
        pwm_led6.ChangeDutyCycle(off)
    
    elif floorNumber == 3:
        pwm_led1.ChangeDutyCycle(off)
        pwm_led2.ChangeDutyCycle(off)
        pwm_led3.ChangeDutyCycle(odd)
        pwm_led4.ChangeDutyCycle(off)
        pwm_led5.ChangeDutyCycle(off)
        pwm_led6.ChangeDutyCycle(off)
    
    elif floorNumber == 4:
        pwm_led1.ChangeDutyCycle(off)
        pwm_led2.ChangeDutyCycle(off)
        pwm_led3.ChangeDutyCycle(off)
        pwm_led4.ChangeDutyCycle(even)
        pwm_led5.ChangeDutyCycle(off)
        pwm_led6.ChangeDutyCycle(off)
    
    elif floorNumber == 5:
        pwm_led1.ChangeDutyCycle(off)
        pwm_led2.ChangeDutyCycle(off)
        pwm_led3.ChangeDutyCycle(off)
        pwm_led4.ChangeDutyCycle(off)
        pwm_led5.ChangeDutyCycle(odd)
        pwm_led6.ChangeDutyCycle(off)
        
    elif floorNumber == 6:
        pwm_led1.ChangeDutyCycle(off)
        pwm_led2.ChangeDutyCycle(off)
        pwm_led3.ChangeDutyCycle(off)
        pwm_led4.ChangeDutyCycle(off)
        pwm_led5.ChangeDutyCycle(off)
        pwm_led6.ChangeDutyCycle(even)

def runBuzzer():
    p = GPIO.PWM(BUZZER_PIN, 100)
    period = 1.0 / 400     #the period (sec/cyc) is the inverse of the frequency (cyc/sec)
    delay = period / 2     #calcuate the time for half of the wave
    cycles = int(1 * 400)  #the number of waves to produce is the duration(in seconds) times the frequency

    for num in range(cycles):
        GPIO.output(BUZZER_PIN, True)
        time.sleep(delay)
        GPIO.output(BUZZER_PIN, False)
        time.sleep(delay)    

 
def switchfloor(floor, currentFloor):
    
    while currentFloor != floor :
        
        if currentFloor < floor:
            currentFloor += 1
            time.sleep(2)
            print(currentFloor)
            updateLED(currentFloor)
        
        if currentFloor > floor:
            currentFloor -= 1
            time.sleep(2)
            print(currentFloor)
            updateLED(currentFloor)
            
   
    if currentFloor == floor:
	     runBuzzer()

    return currentFloor
    

#Initialize floor values upon startup 
currentFloor = 1    
updateLED(currentFloor)


try:
    while True:
        input_state_one = GPIO.input(BUTTON_ONE)
        input_state_two = GPIO.input(BUTTON_TWO)
        input_state_three = GPIO.input(BUTTON_THREE)
        input_state_four = GPIO.input(BUTTON_FOUR)
        input_state_five = GPIO.input(BUTTON_FIVE)
        input_state_six = GPIO.input(BUTTON_SIX)
        
        if input_state_one == False:
            floorQ.put(1)
            time.sleep(0.2)
     
        if input_state_two == False:
            floorQ.put(2)
            time.sleep(0.2)
     
        if input_state_three == False:
            floorQ.put(3)
            time.sleep(0.2)
            
        if input_state_four == False:
            floorQ.put(4)
            time.sleep(0.2)
            
        if input_state_five == False:
            floorQ.put(5)
            time.sleep(0.2)
            
        if input_state_six == False:
            floorQ.put(6)
            time.sleep(0.2)        
         
        while not floorQ.empty():
            currentFloor = switchfloor(floorQ.get(), currentFloor)
            
except KeyboardInterrupt:
    GPIO.cleanup()
finally:
    GPIO.cleanup()