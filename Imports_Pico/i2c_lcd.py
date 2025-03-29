import time
from machine import I2C

from lcd_api import LcdApi  # Ensure lcd_api.py is in the same folder

DEFAULT_I2C_ADDR = 0x27

MASK_RS = 0x01
MASK_RW = 0x02
MASK_E = 0x04
SHIFT_BACKLIGHT = 3
SHIFT_DATA = 4


class I2cLcd(LcdApi):
    """Implements a HD44780 character LCD connected via PCF8574 on I2C."""

    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.backlight = 1  # Backlight ON by default

        # Initialize LCD
        self.i2c.writeto(self.i2c_addr, bytearray([0]))
        time.sleep(0.02)  # Allow LCD time to power up

        # Send reset 3 times
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        time.sleep(0.005)
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        time.sleep(0.001)
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        time.sleep(0.001)

        # Put LCD into 4-bit mode
        self.hal_write_init_nibble(self.LCD_FUNCTION)
        time.sleep(0.001)

        LcdApi.__init__(self, num_lines, num_columns)

        cmd = self.LCD_FUNCTION
        if num_lines > 1:
            cmd |= self.LCD_FUNCTION_2LINES
        self.hal_write_command(cmd)

    def hal_write_init_nibble(self, nibble):
        """Writes an initialization nibble to the LCD."""
        byte = ((nibble >> 4) & 0x0F) << SHIFT_DATA
        self.i2c.writeto(self.i2c_addr, bytearray([byte | MASK_E]))
        self.i2c.writeto(self.i2c_addr, bytearray([byte]))

    def hal_backlight_on(self):
        """Turn backlight on."""
        self.backlight = 1
        self.i2c.writeto(self.i2c_addr, bytearray([1 << SHIFT_BACKLIGHT]))

    def hal_backlight_off(self):
        """Turn backlight off."""
        self.backlight = 0
        self.i2c.writeto(self.i2c_addr, bytearray([0]))

    def hal_sleep_us(self, usecs):
        """Sleep for some time (given in microseconds)."""
        time.sleep(usecs / 1_000_000)

    def hal_write_command(self, cmd):
        """Writes a command to the LCD."""
        self._write_byte(cmd, is_data=False)
        if cmd <= 3:
            time.sleep(0.005)  # Home and clear require longer delay

    def hal_write_data(self, data):
        """Writes data to the LCD."""
        self._write_byte(data, is_data=True)

    def _write_byte(self, value, is_data):
        """Writes a byte to the LCD, setting RS accordingly."""
        rs_bit = MASK_RS if is_data else 0
        byte = (rs_bit | (self.backlight << SHIFT_BACKLIGHT) | (((value >> 4) & 0x0F) << SHIFT_DATA))
        self.i2c.writeto(self.i2c_addr, bytearray([byte | MASK_E]))
        self.i2c.writeto(self.i2c_addr, bytearray([byte]))

        byte = (rs_bit | (self.backlight << SHIFT_BACKLIGHT) | ((value & 0x0F) << SHIFT_DATA))
        self.i2c.writeto(self.i2c_addr, bytearray([byte | MASK_E]))
        self.i2c.writeto(self.i2c_addr, bytearray([byte]))

