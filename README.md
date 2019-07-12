# alarmypi
Python based alarm system for raspberrypi

A collection of scripts for the implementation of an alarm system based on an RPI. It detects an open door or something with a laser and a lighting Sensor. The programm is written in Python, the webfrontend for steering the system contains html and php.

Wiring

I use the actual Raspberrypi GPIO Pin Numbers, have a look at the picture for BCM or WiringPI numbers.

    Port4: 5V
    Port6: Ground
    Port8: Status LED (Green, On/Off) (use as on/off variable)
    Port10: Status LED (Red)
    Port16: Light detector

Patching for my RJ45 breakout Board

Breakout – Pi – Function

    1 – Port 10 – Status Red
    2 – Port 8 – Status Green
    3 – Port 16 – Light Detector
    4
    5
    6
    7 – Port 4 – 5V
    8 – Port 6 – Ground

Installation:

The Project have multiple Folders:

html: This folder contains the webfrontend, you have to put it into your webservers root directory. Please make sure that you have php installed and running. For security reasons you should at least set a password authentification with htaccess or something. In addition to that i restrict the access to a seperate wifi net to which only certain devices known by mac address can connect.

core: This folder contains the detection program, the alert script and the logfile. You can put it anywhere you want.

cmk: This folder contains a local checkmk check, giving you a critical if the detection script doesen’t running. Put the „alarmsystemcheck“ file into /usr/lib/check_mk_agent/local/

How to use:

After the „installation“ you have to start the detection.py script. For productive use, you’ll have to find a way to autostart the script (rc.local, deamonize it…). If the detection script is running, it detects the falling and rising flank of the lightning sensor. If you have a lightning sensor including a potentiometer, you can adjust the sensitifity here. The detection script also set the pin for the status LED as an output.

In a standard configuration you can reach the webinterface at port 80 (http). Here you can enable/disable the system. A disabled system also detects and log rising and falling flanks, but doesen’t execute the alert.py script. So you can also track the activity when the system is disabled.

How it works:

Detection:

The detection script reads out the input on GPIO Pin 16. It can be High or Low. High means that the Laser is disconnected, the alert.py script will be executed (if the system is active (GPIO Pin 8 = 1)).

    if GPIO.input(23):

    if GPIO.input(14):

    print(‚%s: !ALARMSYSTEM ACTIVATED!‘ %currentDT )
    os.system(„python %s/alert.py“%pwd)

Controlwebsite:

The buttons on the index.html page trigger two php scripts, on.php and off.php. Both scripts write a different value (1,0) to GPIO Pin 8 (Status LED). Additionally the scripts change the file status.html, it will be overwritten with either status_on.html or status_off.html. That the user can recognize whether the alarm system is on or off, status.html is integrated as an iframe in index.html.

CMK:

The checkmk local check is executed by your checkmk-agent, but you can also execute it by yourself to see the output and understand the functionality. The script checks with pgrep if there is a process named „detection.py“. If there is one, the output is „OK- Script is running“, if not it’s „CRITICAL- Script is not Running“.

Please use some kind of security measures, not everyone needs to know if your alarm system is running or not.
