import random
import time

from display import Color, DisplayDriver

ms = lambda: int(round(time.time() * 1000))

colors = [
	(255 , 0, 0),
	(255 , 128, 0),
	(255, 255, 0),
	(255, 255, 255),
	(0, 255, 255),
	(0, 0, 255),
	(0, 255, 0)
]
current_color = 0

framebuffer = DisplayDriver()

target_fps = 30
delay = ms()
try:
	while True:
		start = ms()
		framebuffer.fade()
		x, y = random.uniform(0,16), random.uniform(0,16)
		framebuffer.set_pixel_rgb(x, y, *colors[current_color])
		current_color = (current_color + 1) % len(colors)
		framebuffer.present()
		end = ms()

		if (end - start < 1000.0 / target_fps):
			time.sleep((1000.0 / target_fps - (end - start)) / 1000.0)
		if (ms() - delay) >= 1000:
			delay = ms()
			print('Current fps: {}'.format(1000 / (ms() - start)))

except KeyboardInterrupt:
	pass
