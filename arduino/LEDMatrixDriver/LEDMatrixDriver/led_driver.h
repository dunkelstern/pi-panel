#include <avr/io.h>
#include <inttypes.h>
#include <avr/interrupt.h>
#include <util/delay_basic.h>
#include <avr/sfr_defs.h>

#ifndef LED_MATRIX_PORT
#define LED_MATRIX_PORT PORTD
#endif

#ifndef LED_MATRIX_DDR
#define LED_MATRIX_DDR DDRD
#endif

#ifndef LED_MATRIX_PIN
#define LED_MATRIX_PIN 0
#endif

#ifndef LED_MATRIX_WIDTH
#define LED_MATRIX_WIDTH 16
#endif

#ifndef LED_MATRIX_HEIGHT
#define LED_MATRIX_HEIGHT 16
#endif

unsigned char framebuffer[LED_MATRIX_WIDTH * LED_MATRIX_HEIGHT * 3];

#if !(F_CPU == 8000000 || F_CPU == 16000000 || F_CPU == 20000000)
#error "On an AVR, this version of the LED driver only supports 8, 16 and 20 MHz."
#endif

// This function clocks out the framebuffer bytes to the specified PORT and PIN
static void __attribute__((aligned(16))) presentFramebuffer(void) {
	uint16_t remaining = LED_MATRIX_HEIGHT * LED_MATRIX_WIDTH;
	unsigned char *fbpos = framebuffer;
		
	LED_MATRIX_PORT &= ~(1 << (LED_MATRIX_PIN)); // pull pin low
	LED_MATRIX_DDR |= (1 << (LED_MATRIX_PIN)); // set as output pin
	cli(); // disable interrupts as the timing in the following loop is important
	

	// send the bits to the led matrix
	// this code is lifted from the pololu led driver
	while (remaining--) {
		
		// attention WS2811 have GRB ordering, so we initially skip the red byte and start with green
		asm volatile(
		"ld __tmp_reg__, %a0+\n"         // Advance pointer from red to green.
		"ld __tmp_reg__, %a0\n"          // Read the green component and leave the pointer pointing to green.
		"rcall send_led_strip_byte%=\n"  // Send green component.
		"ld __tmp_reg__, -%a0\n"         // Read the red component and leave the pointer at red.
		"rcall send_led_strip_byte%=\n"  // Send red component.
		"ld __tmp_reg__, %a0+\n"         // Advance pointer from red to green.
		"ld __tmp_reg__, %a0+\n"         // Advance pointer from green to blue.
		"ld __tmp_reg__, %a0+\n"         // Read the blue component and leave the pointer on the next color's red.
		"rcall send_led_strip_byte%=\n"  // Send blue component.
		"rjmp led_strip_asm_end%=\n"     // Jump past the assembly subroutines.

		// send_led_strip_byte subroutine:  Sends a byte to the LED strip.
		"send_led_strip_byte%=:\n"
		"rcall send_led_strip_bit%=\n"  // Send most-significant bit (bit 7).
		"rcall send_led_strip_bit%=\n"
		"rcall send_led_strip_bit%=\n"
		"rcall send_led_strip_bit%=\n"
		"rcall send_led_strip_bit%=\n"
		"rcall send_led_strip_bit%=\n"
		"rcall send_led_strip_bit%=\n"
		"rcall send_led_strip_bit%=\n"  // Send least-significant bit (bit 0).
		"ret\n"

		// send_led_strip_bit subroutine:  Sends single bit to the LED strip by driving the data line
		// high for some time.  The amount of time the line is high depends on whether the bit is 0 or 1,
		// but this function always takes the same time (2 us).
		"send_led_strip_bit%=:\n"
		#if F_CPU == 8000000
		"rol __tmp_reg__\n"                      // Rotate left through carry.
		#endif
		"sbi %2, %3\n"                           // Drive the line high.
		#if F_CPU != 8000000
		"rol __tmp_reg__\n"                      // Rotate left through carry.
		#endif

		#if F_CPU == 16000000
		"nop\n" "nop\n"
		#elif F_CPU == 20000000
		"nop\n" "nop\n" "nop\n" "nop\n"
		#endif

		"brcs .+2\n" "cbi %2, %3\n"              // If the bit to send is 0, drive the line low now.

		#if F_CPU == 8000000
		"nop\n" "nop\n"
		#elif F_CPU == 16000000
		"nop\n" "nop\n" "nop\n" "nop\n" "nop\n"
		#elif F_CPU == 20000000
		"nop\n" "nop\n" "nop\n" "nop\n" "nop\n"
		"nop\n" "nop\n"
		#endif

		"brcc .+2\n" "cbi %2, %3\n"              // If the bit to send is 1, drive the line low now.

		"ret\n"
		"led_strip_asm_end%=: "
		: "=b" (fbpos)
		: "0" (fbpos),                                         // %a0 points to the next color to display
		"I" ((unsigned char)(_SFR_IO_ADDR(LED_MATRIX_PORT))),  // %2 is the port register (e.g. PORTC)
		"I" ((unsigned char)(LED_MATRIX_PIN))                  // %3 is the pin number (0-7)
		);
	}
	sei(); // re-enable interrupts
	
	// wait 80 us to latch the color
	#if F_CPU == 8000000
	_delay_loop_2(160);
	#elif F_CPU == 16000000
	_delay_loop_2(320);
	#elif F_CPU == 20000000
	_delay_loop_2(400);
	#endif
}