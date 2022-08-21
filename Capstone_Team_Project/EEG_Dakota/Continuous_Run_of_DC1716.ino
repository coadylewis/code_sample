@endverbatim

http://www.linear.com/product/LTC2473

http://www.linear.com/product/LTC2473#demoboards


Copyright 2018(c) Analog Devices, Inc.

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
 - Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
 - Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in
   the documentation and/or other materials provided with the
   distribution.
 - Neither the name of Analog Devices, Inc. nor the names of its
   contributors may be used to endorse or promote products derived
   from this software without specific prior written permission.
 - The use of this software may or may not infringe the patent rights
   of one or more patent holders.  This license does not release you
   from the requirement that you obtain separate licenses from these
   patent holders to use this software.
 - Use of the software either in source or binary form, must be run
   on or directly connected to an Analog Devices Inc. component.

THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES "AS IS" AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, NON-INFRINGEMENT,
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL ANALOG DEVICES BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, INTELLECTUAL PROPERTY RIGHTS, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

#include <Arduino.h>
#include <stdint.h>
#include "Linduino.h"
#include "LT_SPI.h"
#include <SPI.h>
#include "UserInterface.h"
#include "LT_I2C.h"
#include "QuikEval_EEPROM.h"
#include "LTC2473.h"
#include "LTC24XX_general.h"

// Global variables
static float LTC2473_vref = 1.25;                   //!< The nominal reference voltage
static uint8_t i2c_address = LTC2473_I2C_ADDRESS;   //!< I2C address in 7 bit format for part
static uint16_t timeout = 300;                      //!< The timeout in microseconds


void setup() {
//  uint8_t demo_board_connected; // Set to 1 if the board is connected
//  char demo_name[]="DC1716";    // Demo Board Name stored in QuikEval EEPROM
  quikeval_I2C_init();          // Configure the EEPROM I2C port for 100kHz
  quikeval_I2C_connect();       // Connect I2C to main data port
  Serial.begin(115200);         // Initialize the serial port to the PC
}

void loop() {
  int32_t adc_code = 0;     // The LTC2473 code
  float adc_voltage;        // The LTC2473 voltage
  uint8_t ack = 0;          // Acknowledge bit
  int16_t user_command;     // The user input command
  
  ack |= LTC2473_read(i2c_address, &adc_code, timeout);  // Throws out reading
  delay(100);
  ack |= LTC2473_read(i2c_address, &adc_code, timeout);  // Reads the ADC
  
  if(!ack)
  {
    adc_voltage = LTC2473_code_to_voltage(adc_code, LTC2473_vref);
    Serial.print(abs(adc_voltage), 2);
    //Serial.write(abs(adc_voltage));
    //Serial.print('\n');
    delay(100);
  }
  else 
  {
    Serial.println(F("Device NAK'd, please check I2C address"));
    return 1;
  }
  return(0);

}
