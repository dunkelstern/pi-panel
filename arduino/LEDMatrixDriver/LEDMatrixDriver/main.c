/*
 * LEDMatrixDriver.c
 *
 * Created: 2017-06-10 18:39:11
 * Author : Johannes Schriewer
 */ 

#include <avr/io.h>

#define LED_MATRIX_PORT PORTD
#define LED_MATRIX_DDR DDRD
#define LED_MATRIX_PIN 2

#define LED_MATRIX_WIDTH 16
#define LED_MATRIX_HEIGHT 16

volatile uint16_t fb_pos = 0;
volatile uint8_t byte_pos = 0;
volatile int8_t fb_write_dir = 1;
volatile uint8_t ready = 0;

#include "led_driver.h"

int main(void);

int main(void) {
	// Setup SPI Slave mode
	DDRB |= (1 << 3); // MISO is output
	DDRB &= ~(1 << 2); // SS is input

	SPCR &= ~((1 << CPOL) | (1 << CPHA)); // SPI mode 0
	SPCR |= ((1 << SPE) | (1 << SPIE)); // enable SPI and SPI interrupt

	// enable reset pin interrupt
	EICRA |= (1 << ISC10) | (1 << ISC11);
	EIMSK |= (1 << INT1);

	// Initialize framebuffer with a default pattern
	for(uint8_t x = 0; x < LED_MATRIX_WIDTH; x++) {
		for(uint8_t y = 0; y < LED_MATRIX_HEIGHT; y++) {
			uint16_t index = 0;
			if (y & 0x01) {
				index = x + y * LED_MATRIX_WIDTH;
			} else {
				index = (LED_MATRIX_WIDTH - x - 1) + y * LED_MATRIX_WIDTH;
			}
			index *= 3;
			framebuffer[index] = x;
			framebuffer[index + 1] = 0;
			framebuffer[index + 2] = 0;
		}
	}
	presentFramebuffer();

    while (1) {
		if (ready) {
			presentFramebuffer();
			ready = 0;
		}
    }
}

// SPI recv interrupt
ISR (SPI_STC_vect) {
	// save byte to framebuffer
	framebuffer[(fb_pos * 3) + byte_pos] = SPDR;
	
	// advance framebuffer, the trick is this is written zig-zagging
	byte_pos++;
	if (byte_pos == 3) {
		byte_pos = 0;
		fb_pos += fb_write_dir;
	
	
		// if we write in increasing direction flip the direction when reaching next line
		if ((fb_write_dir == 1) && (fb_pos % LED_MATRIX_WIDTH == 0)) {
			// flip direction
			fb_write_dir = -1;

			// say we are at position 16, so we add 15 to be at 31 for next write
			fb_pos += LED_MATRIX_WIDTH - 1;
		} else 

		// if we write in decreasing direction flip the direction when reaching previous line
		if ((fb_write_dir == -1) && ((fb_pos + 1) % LED_MATRIX_WIDTH == 0)) {
			// flip direction
			fb_write_dir = 1;

			// let's say we are at position 15 so we add 17 to be at 32 next
			fb_pos += LED_MATRIX_WIDTH + 1;
		}
	
		// framebuffer is ready when we reach the end
		ready = (fb_pos >= (LED_MATRIX_WIDTH * LED_MATRIX_HEIGHT));
		if (ready) {
			fb_pos = 0;
			byte_pos = 0;
			fb_write_dir = 1;
		}
	}
}

// reset pin interrupt
ISR(INT1_vect) {
	cli();
	ready = 0;
	fb_pos = 0;
	byte_pos = 0;
	fb_write_dir = 1;
	sei();
}