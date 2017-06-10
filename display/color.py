import math
import colorsys

def hsv_to_rgb(h, s, v):
	r, g, b = colorsys.hsv_to_rgb(h / 360.0, s, v)
	return int(r * 255.0), int(g * 255.0), int(b * 255.0)

def rgb_to_hsv(r, g, b):
	r, g, b = r / 255.0, g / 255.0, b / 255.0
	h, s, v = colorsys.rgb_to_hsv(r, g, b)
	return h * 360.0, s, v

class Color(object):
	"""
	The ``Color`` class is a convenience class to convert between RGB and HSV color
	"""

	def __init__(self):
		self._rgb = None
		self._hsv = None

	@classmethod
	def from_rgb(cls, r, g, b):
		"""
		Create a color from rgb values

		:param int r: 0-255 red value
		:param int g: 0-255 green value
		:param int b: 0-255 blue value
		:return: new ``Color`` instance with color values set
		"""

		c = cls()
		c.rgb = (r, g, b)
		return c

	@classmethod
	def from_hsv(cls, h, s, v):
		"""
		Create a color from hsv values

		:param float h: 0-360 hue value
		:param float s: 0-1 saturation value
		:param float v: 0-1 brightness value
		:return: new ``Color`` instance with color values set
		"""

		c = cls()
		c.hsv = (h, s, v)
		return c

	@property
	def rgb(self):
		"""
		RGB version of the color

		:return: three-tuple (r, g, b)
		"""
		if self._rgb is None:
			self._rgb = hsv_to_rgb(*self._hsv)
		return self._rgb
	
	@rgb.setter
	def rgb(self, rgb):
		"""
		Set rgb version of the color

		:param tuple rgb: three tuple (r, g, b)
		"""

		self._rgb = rgb
		self._hsv = None

	@property
	def hsv(self):
		"""
		HSV version of the color

		:return: three-tuple (h, s, v)
		"""
		if self._hsv is None:
			self._hsv = rgb_to_hsv(**self._rgb)
		return self._hsv
	
	@hsv.setter
	def hsv(self, hsv):
		"""
		Set hsv version of the color

		:param tuple hsv: three tuple (h, s, v)
		"""

		self._hsv = hsv
		self._rgb = None
	
	def multiply(self, factor=0.5):
		"""
		Multiply RGB version by factor

		:param float factor: 1.0 keeps color the same, values < 1.0 darken, > 1.0 lighten
		"""

		self._rgb = (
			min(int(self.rgb[0] * factor), 255),
			min(int(self.rgb[1] * factor), 255),
			min(int(self.rgb[2] * factor), 255)
		)
		self._hsv = None

	def hue_shift(self, distance=5):
		"""
		Shift the hue of the color

		:param float distance: the distance to shift
		"""

		self._hsv = ((self.hsv[0] + distance) % 360, self.hsv[1], self.hsv[2])
		self._rgb = None

