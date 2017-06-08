import math
import time

from display import Color, DisplayDriver

framebuffer = DisplayDriver()

try:
	t1 = 0; t1dir = 1
	t2 = 0; t2dir = 1
	t3 = 0; t3dir = 1
	while True:
		t1 = (t1 + 0.3 * t1dir)
		if t1 > 20:
			t1dir = -1
		if t1 < -4:
			t1dir = 1
		t2 = (t2 + 0.2 * t2dir)
		if t2 > 20:
			t2dir = -1
		if t2 < -4:
			t2dir = 1
		t3 = (t3 + 3.14 / 45.0) % 6.28
		for x in range(framebuffer.width):
			for y in range(framebuffer.height):
				hue = 4.0 \
					  + math.sin(x / (19.0 + t1)) \
					  + math.sin(y / (9.0 + t2) + t3) \
					  + math.sin((x + y) / (25.0 + t1 + t2)) \
					  + math.sin(
							math.sqrt(
								x ** 2.0 + y ** 2.0
							) / 8.0
						)
				color = Color.from_hsv(hue * 360.0, 1.0, 0.25)
				framebuffer.set_pixel(x, y, color)

		framebuffer.present()
		time.sleep(5.0 / 1000.0)
except KeyboardInterrupt:
	pass

