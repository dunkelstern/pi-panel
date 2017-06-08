import sys
from PIL import Image
from display import Color, DisplayDriver

framebuffer = DisplayDriver()

im = Image.open(sys.argv[1])
rgb = im.convert('RGBA')
for y in range(16):
	for x in range(16):
		r,g,b,a = rgb.getpixel((x,y))
		c = Color.from_rgb(r, g, b)
		c.multiply(factor= 0.25 * a / 255.0)
		framebuffer.set_pixel(y, (15 - x), c)

framebuffer.present()

while True:
	pass
