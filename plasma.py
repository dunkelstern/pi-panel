import math
import time

from display import Color, DisplayDriver
ms = lambda: int(round(time.time() * 1000))

framebuffer = DisplayDriver()

sinus = [math.sin(i * 3.1415 / 180.0) for i in range(360)]

target_fps = 30
delay = ms()
try:
	t1 = 0; t1dir = 1
	t2 = 0; t2dir = 1
	t3 = 0; t3dir = 1
	while True:
		start = ms()
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
					  + sinus[int((x / (19.0 + t1)) / 3.1415 * 180) % 360] \
					  + sinus[int((y / (9.0 + t2) + t3) / 3.1415 * 180) % 360] \
					  + sinus[int(((x + y) / (25.0 + t1 + t2)) / 3.1415 * 180) % 360] \
					  + sinus[
							int((math.sqrt(
								x ** 2.0 + y ** 2.0
							) / 8.0) / 3.1415 * 180) % 360
						]
				framebuffer.set_pixel_hsv(x, y, hue * 360.0, 1.0, 0.25)

		framebuffer.present()
		end = ms()

		if (end - start < 1000.0 / target_fps):
			time.sleep((1000.0 / target_fps - (end - start)) / 1000.0)
		if (ms() - delay) >= 1000:
			delay = ms()
			print('Current fps: {}'.format(1000 / (ms() - start)))
except KeyboardInterrupt:
	pass

