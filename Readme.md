# Pi-Panel

This is the Pi-Panel repository to make a Raspberry Pi talk to an Arduino to drive a WS2812B LED Matrix.

## Raspberry Pi part

This part runs on the Raspberry Pi and uses Python3 to generate a frame to send to the Arduino.

Just run one of the Demos (`plasma.py`, `sparkle.py` or `picture.py`) to see it working.

The Python side of the panel driver resides in `display` and is composed of two files, one `Color` helper class to calculate with colors (RGB/HSV conversion, color modification) and the `DisplayDriver` class that does the not so heavy lifting.

## Arduino part

Just flash the sketch in the `arduino` subdir.

TODO: Wiring schema
TODO: Fork spi library to make it work under python 3
TODO: Setup instructions for python venv
