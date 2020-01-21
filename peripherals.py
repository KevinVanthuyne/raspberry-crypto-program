import i2c_lcd
import RPi.GPIO as GPIO
import _thread
import time

class Peripherals:
    """ Handles displaying info to the screen in pages
        and the buttons to navigate between pages """

    def __init__(self):
        # the lcd screen
        self.screen = i2c_lcd.lcd()

        # the 3 buttons
        self.middle_clicks = 0  # used for exiting application
        left_button = 19    # BCM pin of the left button
        middle_button = 13  # BCM pin of the middle button
        right_button = 6    # BCM pin of the right button

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(left_button, GPIO.IN, pull_up_down=GPIO.PUD_UP) # left
        GPIO.setup(middle_button, GPIO.IN, pull_up_down=GPIO.PUD_UP) # middle
        GPIO.setup(right_button, GPIO.IN, pull_up_down=GPIO.PUD_UP) # right

        # when a button is pressed, the callback method is called in a seperate thread
        GPIO.add_event_detect(left_button, GPIO.FALLING, callback=self.left_button_press, bouncetime=300)
        GPIO.add_event_detect(right_button, GPIO.FALLING, callback=self.right_button_press, bouncetime=300)
        GPIO.add_event_detect(middle_button, GPIO.FALLING, callback=self.middle_button_press, bouncetime=300)

        # what page is displayed at the moment
        self.index = 0

        # content to display on each page
        self.pages = []

    def left_button_press(self, channel):
        # decrease index to go to the previous page
        if self.index > 0:
            self.index -= 1
        # when on the first page, go to the last page
        else:
            self.index = len(self.pages) - 1
        self.update_screen()
        # reset amount of middle clicks
        self.middle_clicks = 0

    def right_button_press(self, channel):
        # increase index to go to the next page
        if self.index < len(self.pages) - 1:
            self.index += 1
        # when on the last page, go back to the first page
        else:
            self.index = 0
        self.update_screen()
        # reset amount of middle clicks
        self.middle_clicks = 0

    def middle_button_press(self, channel):
        # quit application when middle button is pressed 3 times in a row
        if self.middle_clicks >= 2:
            self.screen.lcd_clear()
            print("Cleared screen")
            _thread.interrupt_main()

        self.middle_clicks += 1

    def update_screen(self):
        self.screen.lcd_clear()
        i = 1

        # display all 4 lines of the current page
        for line in self.pages[self.index]:
            self.screen.lcd_display_string(line, i)
            i += 1

    def add_page(self, line1=None, line2=None, line3=None, line4=None):
        page = ['', '', '', '']

        if line1:
            page[0] = line1
        if line2:
            page[1] = line2
        if line3:
            page[2] = line3
        if line4:
            page[3] = line4

        self.pages.append(page)
        self.update_screen()


if __name__ == '__main__':
    try:
        p = Peripherals()
        p.update_screen()
        p.add_page(line3="Test")

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped")
