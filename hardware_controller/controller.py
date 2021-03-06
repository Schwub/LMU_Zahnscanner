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
            self.connection.write('S10\n')
            self.read_response()
            self.positionTable += 1

    def move_plane_right(self, steps):
        for i in range(steps):
            self.connection.write('S11\n')
            self.read_response()
            self.positionTable -= 1

    def move_rocker_back(self, steps):
        for i in range(steps):
            self.connection.write('S20\n')
            self.read_response()
            self.positionRocker -= 1

    def move_rocker_front(self, steps):
        for i in range(steps):
            if self.rockerLimitSwitch:
                break
            self.connection.write('S21\n')
            self.read_response()
            self.positionRocker += 1

    def turn_table_clockwise(self, steps):
        for i in range(steps):
            if self.tableLimitSwitch:
                break
            self.connection.write('S30\n')
            self.read_response()
            self.positionTable += 1

    def turn_table_counterclockwise(self, steps):
        for i in range(steps):
            self.connection.write('S31\n')
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
    controller = Controller('/dev/ttyUSB0', 57600)
    controller.move_plane_left(10)
    controller.move_plane_right(10)
    time.sleep(2)
    controller.move_rocker_back(100)
    controller.move_rocker_front(100)
    time.sleep(2)
    controller.turn_table_clockwise(10)
    controller.turn_table_counterclockwise(10)
    time.sleep(2)
    controller.right_laser_on()
    controller.left_laser_on()
    time.sleep(2)
    controller.left_laser_off()
    controller.right_laser_off()
    time.sleep(2)
