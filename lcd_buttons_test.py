import i2c_lcd
import time
import RPi.GPIO as GPIO
import _thread
import peripherals

left_button = 19
middle_button = 13
right_button = 6

def left_button_press(channel):
    global index
    if index > 0:
        index -= 1
    else:
        index = len(pages) - 1
    refresh_screen()

def right_button_press(channel):
    global index
    global pages
    if index < len(pages) - 1:
        index += 1
    else:
        index = 0
    refresh_screen()

def middle_button_press(channel):
    global pages
    global index
    if pages[index] == 'Quit':
        _thread.interrupt_main()

def refresh_screen():
    global pages
    global index
    screen.lcd_clear()
    screen.lcd_display_string("Pagina:", 1)
    screen.lcd_display_string(pages[index], 2)

try:
    screen = i2c_lcd.lcd()

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(left_button, GPIO.IN, pull_up_down=GPIO.PUD_UP) # left
    GPIO.setup(middle_button, GPIO.IN, pull_up_down=GPIO.PUD_UP) # middle
    GPIO.setup(right_button, GPIO.IN, pull_up_down=GPIO.PUD_UP) # right

    GPIO.add_event_detect(left_button, GPIO.FALLING, callback=left_button_press, bouncetime=200) # bouncetime = x ms
    GPIO.add_event_detect(right_button, GPIO.FALLING, callback=right_button_press, bouncetime=200)
    GPIO.add_event_detect(middle_button, GPIO.FALLING, callback=middle_button_press, bouncetime=200)

    index = 0
    pages = ["1. Bitcoin", "2. Stellar", "3. RippleCoin", "Quit"]

    refresh_screen()

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopped")
    screen.lcd_clear()
