import math

class Color(object):
	"""
	The ``Color`` class is a convenience class to convert between RGB and HSV color
	"""

	def __init__(self):
		self._rgb = (0, 0, 0)
		self._hsv = (0, 0, 0)

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

		return self._rgb
	
	@rgb.setter
	def rgb(self, rgb):
		"""
		Set rgb version of the color

		:param tuple rgb: three tuple (r, g, b)
		"""

		self._rgb = rgb
		self._hsv = self.rgb_to_hsv()

	@property
	def hsv(self):
		"""
		HSV version of the color

		:return: three-tuple (h, s, v)
		"""

		return self._hsv
	
	@hsv.setter
	def hsv(self, hsv):
		"""
		Set hsv version of the color

		:param tuple hsv: three tuple (h, s, v)
		"""

		self._hsv = hsv
		self._rgb = self.hsv_to_rgb()
	
	def multiply(self, factor=0.5):
		"""
		Multiply RGB version by factor

		:param float factor: 1.0 keeps color the same, values < 1.0 darken, > 1.0 lighten
		"""

		self._rgb = (
			min(int(self._rgb[0] * factor), 255),
			min(int(self._rgb[1] * factor), 255),
			min(int(self._rgb[2] * factor), 255)
		)
		self._hsv = self.rgb_to_hsv()

	def hue_shift(self, distance=5):
		"""
		Shift the hue of the color

		:param float distance: the distance to shift
		"""

		self._hsv = ((self._hsv[0] + distance) % 360, self._hsv[1], self._hsv[2])
		self._rgb = self.hsv_to_rgb()

	def hsv_to_rgb(self):
		h = float(self._hsv[0])
		s = float(self._hsv[1])
		v = float(self._hsv[2])
		h60 = h / 60.0
		h60f = math.floor(h60)
		hi = int(h60f) % 6
		f = h60 - h60f
		p = v * (1 - s)
		q = v * (1 - f * s)
		t = v * (1 - (1 - f) * s)
		r, g, b = 0, 0, 0
		if hi == 0: r, g, b = v, t, p
		elif hi == 1: r, g, b = q, v, p
		elif hi == 2: r, g, b = p, v, t
		elif hi == 3: r, g, b = p, q, v
		elif hi == 4: r, g, b = t, p, v
		elif hi == 5: r, g, b = v, p, q
		r, g, b = int(r * 255), int(g * 255), int(b * 255)
		return r, g, b
    
	def rgb_to_hsv(self):
		r, g, b = self._rgb[0]/255.0, self._rgb[1]/255.0, self._rgb[2]/255.0
		mx = max(r, g, b)
		mn = min(r, g, b)
		df = mx-mn
		if mx == mn:
			h = 0
		elif mx == r:
			h = (60 * ((g-b)/df) + 360) % 360
		elif mx == g:
			h = (60 * ((b-r)/df) + 120) % 360
		elif mx == b:
			h = (60 * ((r-g)/df) + 240) % 360
		if mx == 0:
			s = 0
		else:
			s = df/mx
		v = mx
		return h, s, v

