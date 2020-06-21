#!/usr/bin/env python3

''' Icom IC-9700 Time Synchronization
    This program sets the clock of the Icom IC-7300 radio to the current time
    of the computer.  See "User Configurations" section below for program  
    options that must be set.  This script requires the pyserial module.  Add 
    this dependency with the `py -m pip install pyserial` command.
    
    Copyright (C) 2020  Claus Niesen
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''    
    
import serial
import time

### User Configurations ###
#
# Baud rate for the CI-V interface of the Icom IC-7300.
#baudrate = 9600
baudrate = 115200
#
# Serial port of the computer on which the CI-V interface of the radio is connected.
#serialport = '/dev/ttyUSB0'  # for Linux
#serialport = 'COM3'          # for Windows
serialport = 'COM6' 
#
# Swap the CLOCK and UTC times of the Icom IC-7300. 
#swapclock = False  # display local time on CLOCK
#swapclock = True  # display UTC time on CLOCK (the UTC display will show local time)
swapclock = True
 
#
### end of user configurations ###

preamble = 'FEFEA2E01A05'
setDateCommand = '0179'
setTimeCommand = '0180'
setUtcOffsetCommand = '0184'
postamble = 'FD'
responseOk = 'FEFEE0A2FBFD'

ser = serial.Serial(serialport, baudrate)
ser.timeout = 5

if (swapclock):
    def getTime():
        return time.gmtime()
else: 
    def getTime():
        return time.localtime()
        
def sendCommand(command, data):
    command = preamble + command + data + postamble
    ser.write(bytes.fromhex(command))
    ser.read_until(bytes.fromhex(postamble)) # the send command (why, oh why?)
    response = ser.read_until(bytes.fromhex(postamble)) 
    if (response != bytes.fromhex(responseOk)):
        exit('Error: Command ' + command + ' did not receive OK from radio.')
        
print('Setting Icom clock to', getTime().tm_zone, '. This may take up to 1 minute to complete.')

# Set UTC offset on radio
if(time.localtime().tm_gmtoff < 0):
    offsetData = time.strftime('%H%M', time.gmtime(time.localtime().tm_gmtoff * -1))
    if (swapclock):
        offsetData += '00'
    else:
        offsetData += '01'
else :
    offsetData = time.strftime('%H%M', time.gmtime(time.localtime().tm_gmtoff))
    if (swapclock):
        offsetData += '01'
    else:
        offsetData += '00'
sendCommand(setUtcOffsetCommand, offsetData)

# Set date on radio
dateData = time.strftime('%Y%m%d', getTime())
sendCommand(setDateCommand, dateData)

# Set time on radio (top of minute)
while(time.localtime().tm_sec != 0):
    pass
timeData = time.strftime('%H%M', getTime())
sendCommand(setTimeCommand, timeData)

ser.close()
