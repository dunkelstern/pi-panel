import random
import RPIO
from spi import *
import time

from .color import Color
	

class DisplayDriver(object):
	"""
	The ``DisplayDriver`` class holds a frame buffer to send to the Arduino which
	in turn sends the bits to the LED matrix.

	There are some convenience functions like ``clear()``, ``fill()``, and ``fade()``
	"""

	def __init__(self, spi_device="/dev/spidev0.0", width=16, height=16):
		"""
		Initialize display driver

		:param str spi_device: the SPI device instance to use, optional, defaults to ``/dev/spidev0.0``
		:param int width: width of the framebuffer, defaults to 16
		:param int height: height of the framebuffer, defaults to 16
		"""

		self.width = width
		self.height = height

		self.spi = SPI('/dev/spidev0.0')
		self.spi.mode = SPI.MODE_0
		self.spi.bits_per_word = 8
		self.spi.speed = 450000

		RPIO.setmode(RPIO.BOARD)
		RPIO.setup(11, RPIO.OUT)

		self.frame_buffer = []
		self.clear()
		self.reset()
		self.present()
		time.sleep(20.0 / 1000.0) # 20 ms

	def __del__(self):
		for i in range(64):
			self.fade()
			self.present()
			time.sleep(20.0 / 1000.0) # 20 ms
		RPIO.cleanup()
	
	def reset(self):
		""" Reset the arduino, use periodically to avoid sync errors """

		RPIO.output(11, RPIO.HIGH)
		time.sleep(1.0 / 1000.0)
		RPIO.output(11, RPIO.LOW)
		time.sleep(20.0 / 1000.0)
	
	def clear(self):
		""" Clear the matrix to black color """
		self.frame_buffer = [0 for _ in range(self.width*self.height*3)]

	def get_pixel(self, x, y):
		"""
		Get pixel color of pixel at given x and y coordinates
		
		:param int x: X coordinate of pixel to get
		:param int y: Y coordinate of pixel to get
		:return: ``Color`` instance for the pixel
		:raises ValueError: if the coordinate is out of bounds
		"""

		if x > self.width or x < 0:
			raise ValueError('x coordinate has to be >= 0 and < width ({})'.format(self.width))
		if y > self.height or y < 0:
			raise ValueError('y coordinate has to be >= 0 and < height ({})'.format(self.height))
		index = (y * self.width + x) * 3
		return Color.from_rgb(self.frame_buffer[index], self.frame_buffer[index + 1], self.frame_buffer[index + 2])

	def set_pixel(self, x, y, color):
		"""
		Set pixel color of pixel at given x and y coordinates
		
		:param int x: X coordinate of pixel to set
		:param int y: Y coordinate of pixel to set
		:param Color color: color to set the pixel to
		:raises ValueError: if the coordinate is out of bounds
		"""

		if x > self.width:
			raise ValueError('x coordinate has to be smaller than width ({})'.format(self.width))
		if y > self.height:
			raise ValueError('y coordinate has to be smaller than height ({})'.format(self.height))
		index = (y * self.width + x) * 3
		c = color.rgb
		self.frame_buffer[index] = c[0]
		self.frame_buffer[index + 1] = c[1]
		self.frame_buffer[index + 2] = c[2]

	def fill(self, color):
		"""
		Fill complete framebuffer with color

		:param Color color: the color to fill
		"""

		c = color.rgb
		for i in range(self.width * self.height):
			index = i * 3
			self.frame_buffer[index] = c[0]
			self.frame_buffer[index + 1] = c[1]
			self.frame_buffer[index + 2] = c[2]
	
	def fade(self, speed=1.2):
		"""
		Fade out framebuffer a bit

		:param float speed: the speed with which to fade. 1.0 would keep the buffer stable,
			values above 1.0 fade to black, below 1.0 fade to white
		"""

		for i in range(self.width * self.height * 3):
			self.frame_buffer[i] = int(self.frame_buffer[i] / speed)

	def present(self):
		""" Present the framebuffer """
		self.spi.write(self.frame_buffer)

if __name__ == "__main__":
	driver = DisplayDriver()
	driver.fill(Color.from_rgb(16, 16, 16))
	driver.present()

