import serial
import time


class Controller:
    positionPlain = 0
    positionRocker = 0
    positionTable = 0
    rockerLimitSwitch = False
    tableLimitSwitch = False
    device = None
    baudrate = None
    connection = None

    def __init__(self, device, baudrate):
        self.device = device
        self.baudrate = baudrate
        self.connection = serial.Serial(self.device, self.baudrate, timeout=1)
        time.sleep(1)
        print self.connection

    def right_laser_on(self):
        self.connection.write('L11\n')

    def right_laser_off(self):
        self.connection.write('L10\n')

    def left_laser_on(self):
        self.connection.write('L21\n')

    def left_laser_off(self):
        self.connection.write('L20\n')

    def move_plane_left(self, steps):
        for i in range(steps):
            if self.tableLimitSwitch:
                break
            self.connection.write('S10\n')
            self.read_response()
            self.positionTable += 1

    def move_plane_right(self, steps):
        for i in range(steps):
            self.connection.write('S11\n')
            self.read_response()
            self.positionTable -= 1

    def read_response(self):
        while True:
            data = self.connection.readline()
            if data == "ES11\r\n":
                self.tableLimitSwitch = True
            if data == "ES10\r\n":
                self.tableLimitSwitch = False
            print data
            if data == "0\r\n":
                break



if __name__ == '__main__':
    controller = Controller('/dev/ttyACM0', 9600)
    controller.move_plane_left(500)
    controller.move_plane_right(500)
    controller.right_laser_on()
    controller.left_laser_on()
    time.sleep(1)
    controller.left_laser_off()
    controller.right_laser_off()
    time.sleep(1)
