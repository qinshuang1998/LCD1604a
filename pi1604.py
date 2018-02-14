#!/usr/bin/env python
# -*- coding: UTF-8 -*- 
import time
import RPi.GPIO as GPIO

class LCD1604:

    def __init__(self):

        self.GPIO = GPIO
        # Define GPIO to LCD mapping
        self.LCD_RS = 14
        self.LCD_E  = 15
        self.LCD_D4 = 17
        self.LCD_D5 = 18
        self.LCD_D6 = 27
        self.LCD_D7 = 22
        self.LCD_A  = 12

        # Define some device constants
        self.LCD_WIDTH = 16    # Maximum characters per line
        self.LCD_CHR = True
        self.LCD_CMD = False

        self.LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
        self.LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
        self.LCD_LINE_3 = 0x90
        self.LCD_LINE_4 = 0xD0

        # Timing constants
        self.E_PULSE = 0.0005
        self.E_DELAY = 0.0005

        try:
            self.setup()
        except:
            print('ERROR!')
        finally:
            pass


    def cleanup(self):
        self.lcd_byte(0x01, self.LCD_CMD)
        self.lcd_string("Goodbye!",1)
        time.sleep(3)
        self.lcd_string("",1)
        self.lcd_string("",2)
        self.lcd_string("",3)
        self.lcd_string("",4)
        self.GPIO.output(self.LCD_A, False)
        self.GPIO.cleanup()

    def lcd_init(self):
      # Initialise display
      self.lcd_byte(0x33,self.LCD_CMD) # 110011 Initialise
      self.lcd_byte(0x32,self.LCD_CMD) # 110010 Initialise
      self.lcd_byte(0x06,self.LCD_CMD) # 000110 Cursor move direction
      self.lcd_byte(0x0C,self.LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
      self.lcd_byte(0x28,self.LCD_CMD) # 101000 Data length, number of lines, font size
      # lcd_byte(0x01,LCD_CMD) # 000001 Clear display
      self.lcd_clear() # Clear display
      time.sleep(self.E_DELAY)

    def lcd_clear(self):
      self.lcd_byte(0x01,self.LCD_CMD) # 000001 Clear display
      time.sleep(self.E_DELAY)

    def lcd_byte(self, bits, mode):
      # Send byte to data pins
      # bits = data
      # mode = True  for character
      #        False for command

      self.GPIO.output(self.LCD_RS, mode) # RS

      # High bits
      self.GPIO.output(self.LCD_D4, False)
      self.GPIO.output(self.LCD_D5, False)
      self.GPIO.output(self.LCD_D6, False)
      self.GPIO.output(self.LCD_D7, False)
      if bits&0x10==0x10:
        self.GPIO.output(self.LCD_D4, True)
      if bits&0x20==0x20:
        self.GPIO.output(self.LCD_D5, True)
      if bits&0x40==0x40:
        self.GPIO.output(self.LCD_D6, True)
      if bits&0x80==0x80:
        self.GPIO.output(self.LCD_D7, True)

      # Toggle 'Enable' pin
      self.lcd_toggle_enable()

      # Low bits
      self.GPIO.output(self.LCD_D4, False)
      self.GPIO.output(self.LCD_D5, False)
      self.GPIO.output(self.LCD_D6, False)
      self.GPIO.output(self.LCD_D7, False)
      if bits&0x01==0x01:
        self.GPIO.output(self.LCD_D4, True)
      if bits&0x02==0x02:
        self.GPIO.output(self.LCD_D5, True)
      if bits&0x04==0x04:
        self.GPIO.output(self.LCD_D6, True)
      if bits&0x08==0x08:
        self.GPIO.output(self.LCD_D7, True)

      # Toggle 'Enable' pin
      self.lcd_toggle_enable()

    def lcd_toggle_enable(self):
      # Toggle enable
      time.sleep(self.E_DELAY)
      self.GPIO.output(self.LCD_E, True)
      time.sleep(self.E_PULSE)
      self.GPIO.output(self.LCD_E, False)
      time.sleep(self.E_DELAY)

    def lcd_string(self, message, line):
      # Send string to display

      message = message.ljust(self.LCD_WIDTH," ")

      switch = {
                1: self.LCD_LINE_1,
				2: self.LCD_LINE_2,
				3: self.LCD_LINE_3,
				4: self.LCD_LINE_4
              }
      self.lcd_byte(switch[line], self.LCD_CMD)

      for i in range(self.LCD_WIDTH):
        self.lcd_byte(ord(message[i]),self.LCD_CHR)

    def setup(self):
      # Main program block
      self.GPIO.setwarnings(False)
      self.GPIO.setmode(self.GPIO.BCM)       # Use BCM GPIO numbers
      self.GPIO.setup(self.LCD_E, self.GPIO.OUT)  # E
      self.GPIO.setup(self.LCD_RS, self.GPIO.OUT) # RS
      self.GPIO.setup(self.LCD_D4, self.GPIO.OUT) # DB4
      self.GPIO.setup(self.LCD_D5, self.GPIO.OUT) # DB5
      self.GPIO.setup(self.LCD_D6, self.GPIO.OUT) # DB6
      self.GPIO.setup(self.LCD_D7, self.GPIO.OUT) # DB7
      self.GPIO.setup(self.LCD_A, self.GPIO.OUT)  # A
      self.GPIO.output(self.LCD_A, True)

      # Initialise display
      self.lcd_init()

    def create_char(self, location, pattern):
      location &= 0x7
      self.lcd_byte(0x40 | (location << 3), self.LCD_CMD)
      for i in range(8):
        self.lcd_byte(pattern[i], self.LCD_CHR)