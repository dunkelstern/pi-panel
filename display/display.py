import random
import RPIO
from spi import *
import time
import numpy as np

from .color import Color, hsv_to_rgb
	

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
		self.spi.speed = 500000

		RPIO.setmode(RPIO.BOARD)
		RPIO.setup(11, RPIO.OUT)

		self.frame_buffer = np.zeros((self.width, self.height, 3), dtype=np.uint8)
		self.clear()
		self.reset()
		self.present()
		time.sleep(20.0 / 1000.0) # 20 ms

	def __del__(self):
		for i in range(64):
			self.fade()
			self.present()
			time.sleep(10.0 / 1000.0) # 20 ms
		RPIO.cleanup()
	
	def reset(self):
		""" Reset the arduino, use periodically to avoid sync errors """

		RPIO.output(11, RPIO.HIGH)
		time.sleep(1.0 / 1000.0)
		RPIO.output(11, RPIO.LOW)
		time.sleep(20.0 / 1000.0)
	
	def clear(self):
		""" Clear the matrix to black color """
		self.frame_buffer = np.zeros((self.width, self.height, 3), dtype=np.uint8)

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
		return Color.from_rgb(*tuple(self.frame_buffer[x][y]))

	def set_pixel(self, x, y, color):
		"""
		Set pixel color of pixel at given x and y coordinates
		
		:param int x: X coordinate of pixel to set
		:param int y: Y coordinate of pixel to set
		:param Color color: color to set the pixel to
		:raises ValueError: if the coordinate is out of bounds
		"""

		if x > self.width or x < 0:
			raise ValueError('x coordinate has to be >= 0 and < width ({})'.format(self.width))
		if y > self.height or y < 0:
			raise ValueError('y coordinate has to be >= 0 and < height ({})'.format(self.height))
		index = (y * self.width + x) * 3
		c = color.rgb
		self.frame_buffer[x][y] = c
	
	def set_pixel_rgb(self, x, y, r, g, b):
		"""
		Set pixel color of pixel at given x and y coordinates
		
		:param int x: X coordinate of pixel to set
		:param int y: Y coordinate of pixel to set
		:param int r: red component 0-255
		:param int g: green component 0-255
		:param int b: blue component 0-255
		:raises ValueError: if the coordinate is out of bounds
		"""

		if x > self.width or x < 0:
			raise ValueError('x coordinate has to be >= 0 and < width ({})'.format(self.width))
		if y > self.height or y < 0:
			raise ValueError('y coordinate has to be >= 0 and < height ({})'.format(self.height))
		self.frame_buffer[x][y] = (r, g, b)	

	def set_pixel_hsv(self, x, y, h, s, v):
		"""
		Set pixel color of pixel at given x and y coordinates
		
		:param int x: X coordinate of pixel to set
		:param int y: Y coordinate of pixel to set
		:param int h: hue component 0-360
		:param int s: saturation component 0.0-1.0
		:param int v: value component 0.0-1.0
		:raises ValueError: if the coordinate is out of bounds
		"""

		if x > self.width or x < 0:
			raise ValueError('x coordinate has to be >= 0 and < width ({})'.format(self.width))
		if y > self.height or y < 0:
			raise ValueError('y coordinate has to be >= 0 and < height ({})'.format(self.height))
		self.frame_buffer[x][y] = hsv_to_rgb(h, s, v)

	def fill(self, color):
		"""
		Fill complete framebuffer with color

		:param Color color: the color to fill
		"""

		self.frame_buffer = np.repeat(color.rgb, (self.width, self.height))
	
	def fade(self, speed=1.2):
		"""
		Fade out framebuffer a bit

		:param float speed: the speed with which to fade. 1.0 would keep the buffer stable,
			values above 1.0 fade to black, below 1.0 fade to white
		"""

		self.frame_buffer /= speed

	def present(self):
		""" Present the framebuffer """
		self.spi.write(np.ravel(self.frame_buffer))

if __name__ == "__main__":
	driver = DisplayDriver()
	driver.fill(Color.from_rgb(16, 16, 16))
	driver.present()

