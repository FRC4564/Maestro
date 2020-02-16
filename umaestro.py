import board
import busio
#
# umaestro.py - Pololu Maestro Servo Controller for CircuitPython
#
# Steven Jacobs -- Feb 2020
# https://github.com/FRC4564/Maestro/
#
# For detailed documentation see the full Python implementation in maestro.py.
#
class Controller:
    # Maestro must be set to UART mode under Serial Settings (see Pololu Maestro Control Center).
    # Tested with Feather M4 and Micro Maestro.  Because the Feather is a 3.3v device and the Feather
    # a 5v device, level shifting is required.  See umaestro.md for details.
    def __init__(self, tx=board.TX, rx=board.RX, baud=115200, device=b'\x0c'):
        self.uart = busio.UART(tx, rx, baudrate=baud)
        self.PololuCmd = b'\xaa' + device
        self.Targets = [0] * 24
        self.Mins = [0] * 24
        self.Maxs = [0] * 24

    # Clean up by releasing the UART pins
    def close(self):
        self.uart.deinit()

    # Send a Pololu command out the serial port
    def sendCmd(self, cmd):
        self.uart.write(self.PololuCmd)
        self.uart.write(cmd)

    # Set channels min and max value range.
    def setRange(self, chan, min, max):
        self.Mins[chan] = min
        self.Maxs[chan] = max

    # Return Minimum channel range value
    def getMin(self, chan):
        return self.Mins[chan]

    # Return Maximum channel range value
    def getMax(self, chan):
        return self.Maxs[chan]

    # Set channel to a specified target value in quarter-microseconds
    def setTarget(self, chan, target):
        if self.Mins[chan] > 0 and target < self.Mins[chan]:
            target = self.Mins[chan]
        if self.Maxs[chan] > 0 and target > self.Maxs[chan]:
            target = self.Maxs[chan]
        lsb = target & 0x7f #7 bits for least significant byte
        msb = (target >> 7) & 0x7f #shift 7 and take next 7 bits for msb
        cmd = b'\x04' + chr(chan) + chr(lsb) + chr(msb)
        self.sendCmd(cmd)
        self.Targets[chan] = target

    # Set speed of channel measured as quarter-microseconds/10milliseconds
    def setSpeed(self, chan, speed):
        lsb = speed & 0x7f #7 bits for least significant byte
        msb = (speed >> 7) & 0x7f #shift 7 and take next 7 bits for msb
        cmd = b'\x07' + chr(chan) + chr(lsb) + chr(msb)
        self.sendCmd(cmd)

    # Set acceleration of channel
    def setAccel(self, chan, accel):
        lsb = accel & 0x7f #7 bits for least significant byte
        msb = (accel >> 7) & 0x7f #shift 7 and take next 7 bits for msb
        cmd = b'\x09' + chr(chan) + chr(lsb) + chr(msb)
        self.sendCmd(cmd)

    # Get the current position of the specified channel
    def getPosition(self, chan):
        cmd = b'\x10' + chr(chan)
        self.sendCmd(cmd)
        lsb = ord(self.uart.read(1))
        msb = ord(self.uart.read(1))
        return (msb << 8) + lsb

    # Is servo still moving?
    def isMoving(self, chan):
        if self.Targets[chan] > 0:
            if self.getPosition(chan) != self.Targets[chan]:
                return True
        return False

    # Have all servo outputs reached their targets?
    def getMovingState(self):
        cmd = b'\x13'
        self.sendCmd(cmd)
        if self.uart.read(1) == b'\x00':
            return False
        else:
            return True

    # Run a Maestro Script subroutine.
    # Subroutines are numbered sequentially starting with 0. 
    # Code the subroutine to either REPEAT infinitely or end with QUIT (RETURN is not valid).
    def runScriptSub(self, subNumber):
        cmd = b'\x27' + chr(subNumber)
        # can pass a param with command 0x28
        # cmd = b'\x28' + chr(subNumber) + chr(lsb) + chr(msb)
        self.sendCmd(cmd)

    # Stop the current Maestro Script
    def stopScript(self):
        cmd = b'\x24'
        self.sendCmd(cmd)