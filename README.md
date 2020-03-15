Icom IC-7300 Time Synchronization
================================

Python3 script to set the clock of the Icom IC-7300 radio to the current time of the computer. 
 
 
User Configurations
-------------------
The script in the Set_IC7300_time.py file contains a user configuration section that needs to be set correctly.
 
**baudrate** - specifies the baud rate for the CI-V interface of the Icom IC-7300.   
   Example: `baudrate = 115200` 
 
**serialport** - specifies the serial port of the computer on which the CI-V interface of the radio is connected.  
    Windows example: `serialport = 'COM3'`  
    Linux example: `serialport = '/dev/ttyUSB0'` 
   
**swapclock** - specifies if the CLOCK and UTC times of the Icom IC-7300 should be swapped. 
    `swapclock = False` keeps the CLOCK at local time and UTC time as UTC.
    `swapclock = True` makes the CLOCK to display UTC time while the UTC time is actually the local time.  Some users prefere to see the UTC time on the top right of the Icom IC-7300 and this setting will do that.

   
Running on Windows
------------------
Install the latest version of [Python3](https://www.python.org/downloads/) and add the pyserial module by executing the `py -m pip install pyserial` command from the command line.  Make sure the user configurations have been correctly set (see above).  Now the script can be run with the `py Set_IC7300_time.py` command.


Running on Linux / OSX
----------------------
Install the latest version of Python3 (e.g. `sudo apt install python3`) and pyserial (i.e. `sudo apt install python3-serial`). Make the script executable (i.e. `chmod +x Set_IC7300_time.py` and set the user configurations in the script (see above).  Now the script can be run (i.e. `python3 Set_IC7300_time.py`).


History
-------

The Icom IC-7300 has the chronic habbit of loosing the current time.  It's apparently an issue with the internal clock battery.

Kevin created the first version of this script to set the time in June 2019 that syncs the clock.  A video overview of this script can be seen at https://youtu.be/GhuI-vrCBhs .

Claus did a complete rewrite of the script in March 2020, adding date and UTC offset syncing as well.