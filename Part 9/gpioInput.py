### The majority of this code is based on the Adafruit tutorial "Analog Inputs for Raspberry Pi Using the MCP3008"
### https://learn.adafruit.com/reading-a-analog-in-and-controlling-audio-volume-with-the-raspberry-pi/script

import RPi.GPIO as GPIO

class GpioInput():
	GPIO.setmode(GPIO.BCM)

	windowWidth = 0

	SPICLK = 11
	SPIMISO = 9
	SPIMOSI = 10
	SPICS = 8

	BUTTON = 7

	GPIO.setup(SPIMOSI, GPIO.OUT)
	GPIO.setup(SPIMISO, GPIO.IN)
	GPIO.setup(SPICLK, GPIO.OUT)
	GPIO.setup(SPICS, GPIO.OUT)

	GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	potentiometer_adc = 0
	last_read = 0
	tolerance = 5

	def __init__(self, windowWidth):
		self.windowWidth = windowWidth

	def readButton(self):
		return GPIO.input(self.BUTTON) == False

	def getPotPosition(self):
		trim_pot = self.readadc(self.potentiometer_adc, self.SPICLK, self.SPIMOSI, self.SPIMISO, self.SPICS)
		if (abs(trim_pot - self.last_read) > self.tolerance):
			position = trim_pot
			self.last_read = trim_pot
		else:
			position = self.last_read

		position = position * self.windowWidth / 1023.0

		return position

	def readadc(self, adcnum, clockpin, mosipin, misopin, cspin):
		if ((adcnum > 7) or (adcnum < 0)):
			return -1
		GPIO.output(cspin, True)

		GPIO.output(clockpin, False)  
		GPIO.output(cspin, False)    

		commandout = adcnum
		commandout |= 0x18  
		commandout <<= 3    
		for i in range(5):
			if (commandout & 0x80):
				GPIO.output(mosipin, True)
			else:
				GPIO.output(mosipin, False)
			commandout <<= 1
			GPIO.output(clockpin, True)
			GPIO.output(clockpin, False)

		adcout = 0
		for i in range(12):
			GPIO.output(clockpin, True)
			GPIO.output(clockpin, False)
			adcout <<= 1
			if (GPIO.input(misopin)):
				adcout |= 0x1

		GPIO.output(cspin, True)

		adcout >>= 1
		return adcout