import random
import time

from display import DisplayDriver

ms = lambda: int(round(time.time() * 1000))

framebuffer = DisplayDriver()

target_fps = 30
delay = ms()
try:
	for x in range(16):
		for y in range(16):
			framebuffer.set_pixel_rgb(x, y, x, x, x)
	while True:
		start = ms()
		framebuffer.present()
		end = ms()

		if (end - start < 1000.0 / target_fps):
			time.sleep((1000.0 / target_fps - (end - start)) / 1000.0)
		if (ms() - delay) >= 1000:
			delay = ms()
			print('Current fps: {}'.format(1000 / (ms() - start)))
except KeyboardInterrupt:
	pass
