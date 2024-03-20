import RPi.GPIO as GPIO
import time

# Set GPIO mode and pin for IR sensor
GPIO.setmode(GPIO.BOARD)
IR_PIN = 11
GPIO.setup(IR_PIN, GPIO.IN)

# Initialize variables
egg_count = 0
debounce_delay = 0.3  # Debounce delay in seconds
last_detection_time = time.time()

try:
    while True:
        # Check if IR sensor is triggered
        if GPIO.input(IR_PIN) == GPIO.LOW:
            # Perform debounce
            if time.time() - last_detection_time > debounce_delay:
                egg_count += 1
                print("Egg detected! Total eggs counted:", egg_count)
                last_detection_time = time.time()

        # You can add additional logic here, such as saving the count to a file or database.

        time.sleep(0.1)  # Sleep to reduce CPU usage

except KeyboardInterrupt:
    GPIO.cleanup()  # Clean up GPIO on CTRL+C exit
