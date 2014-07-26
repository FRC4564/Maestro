maestro.py
==========

This Python class supports Pololu's Maestro servo controller over USB serial. Great for use with the Raspberry Pi.

The class includes methods to control servos (position, speed, acceleration), read servo position, and start/stop Maestro scripts.  See Pololu's on-line documentation to learn about the full capabilities of this nifty micro-controller.

Pololu's Maestro Windows installer sets up the Maestro Control Center, used to configure, test and program the controller.  Be sure the Maestro is configured for "USB Dual Port" serial mode.  I believe the controller is setup in this mode by default by default, so it shouldn't be necessary to use the Control Center application.

You'll need to have the 'pyserial' Python module installed to use maestro.py.

For Linux, download pyserial-2.7.tar.gz from http://sourceforge.net/projects/pyserial/files/pyserial/

    wget http://sourceforge.net/projects/pyserial/files/pyserial/2.7/pyserial-2.7.tar.gz

 and then install

    tar –zxf pyserial-2.7.tar.gz
    cd pyserial-2.7
    sudo python setup.py install


Example usage of maestro.py:

    import maestro.py
    servo = maestro.Controller()
    servo.setAccel(0,4)      #set servo 0 acceleration to 4
    servo.setTarget(0,6000)  #set servo to move to center position
    servo.close

