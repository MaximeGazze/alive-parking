import RPi.GPIO as GPIO
import time

class LCD():
    def __init__(
            self,
            LCD_RS = 7,
            LCD_E = 8,
            LCD_D4 = 25,
            LCD_D5 = 24,
            LCD_D6 = 23,
            LCD_D7 = 18,
            LCD_CHARS = 16,
            lines = [0x80, 0xC0],
    ):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        self.LCD_RS = LCD_RS
        self.LCD_E = LCD_E
        self.LCD_D4 = LCD_D4
        self.LCD_D5 = LCD_D5
        self.LCD_D6 = LCD_D6
        self.LCD_D7 = LCD_D7
        self.LCD_CHARS = LCD_CHARS
        self.lines = lines

        GPIO.setup(LCD_E, GPIO.OUT)
        GPIO.setup(LCD_RS, GPIO.OUT)
        GPIO.setup(LCD_D4, GPIO.OUT)
        GPIO.setup(LCD_D5, GPIO.OUT)
        GPIO.setup(LCD_D6, GPIO.OUT)
        GPIO.setup(LCD_D7, GPIO.OUT)

        self.lcd_write(0x33, False) # Initialize
        self.lcd_write(0x32, False) # Set to 4-bit mode
        self.lcd_write(0x06, False) # Cursor move direction
        self.lcd_write(0x0C, False) # Turn cursor off
        self.lcd_write(0x28, False) # 2 line display
        self.lcd_write(0x01, False) # Clear display
        # time.sleep(0.0005) # Delay to allow commands to process

    def lcd_write(self, bits, mode):
        GPIO.output(self.LCD_RS, mode)

        GPIO.output(self.LCD_D4, False)
        GPIO.output(self.LCD_D5, False)
        GPIO.output(self.LCD_D6, False)
        GPIO.output(self.LCD_D7, False)
        if bits&0x10==0x10:
            GPIO.output(self.LCD_D4, True)
        if bits&0x20==0x20:
            GPIO.output(self.LCD_D5, True)
        if bits&0x40==0x40:
            GPIO.output(self.LCD_D6, True)
        if bits&0x80==0x80:
            GPIO.output(self.LCD_D7, True)

        self.lcd_toggle_enable()

        GPIO.output(self.LCD_D4, False)
        GPIO.output(self.LCD_D5, False)
        GPIO.output(self.LCD_D6, False)
        GPIO.output(self.LCD_D7, False)
        if bits&0x01==0x01:
            GPIO.output(self.LCD_D4, True)
        if bits&0x02==0x02:
            GPIO.output(self.LCD_D5, True)
        if bits&0x04==0x04:
            GPIO.output(self.LCD_D6, True)
        if bits&0x08==0x08:
            GPIO.output(self.LCD_D7, True)

        self.lcd_toggle_enable()

    def lcd_toggle_enable(self):
        # time.sleep(0.0005)
        GPIO.output(self.LCD_E, True)
        time.sleep(0.0005)
        GPIO.output(self.LCD_E, False)
        # time.sleep(0.0005)

    def text(self, message, line):
        line = self.lines[line]
        message = message.ljust(self.LCD_CHARS," ")
        self.lcd_write(line, False)
        for i in range(self.LCD_CHARS):
            self.lcd_write(ord(message[i]),True)

    def clear(self):
        self.lcd_write(0x01, False)
