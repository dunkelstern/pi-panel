import random
import time

from display import Color, DisplayDriver

colors = [
	Color.from_rgb(255 , 0, 0),
	Color.from_rgb(255 , 128, 0),
	Color.from_rgb(255, 255, 0),
	Color.from_rgb(255, 255, 255),
	Color.from_rgb(0, 255, 255),
	Color.from_rgb(0, 0, 255),
	Color.from_rgb(0, 255, 0)
]
current_color = 0

framebuffer = DisplayDriver()
while True:
	framebuffer.fade()
	for y in range(16):
		for x in range(16):
			if int(random.uniform(0,500)) == 0:
				framebuffer.set_pixel(x, y, colors[current_color])
				current_color = (current_color + 1) % len(colors)
	framebuffer.present()
	time.sleep(20.0 / 1000.0) # 100 ms
