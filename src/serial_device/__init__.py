import sys
import glob
import serial
import serial.tools.list_ports
import prettytable

# non blocking
class SerialDevice:
    def __init__(self):
        self._line = ""

    def open(self, p, baud=115200):
        print(f"opening port {p} with baudrate {baud}")
        try:
            self.ser = serial.Serial(port=p, baudrate=baud, timeout=0, xonxoff=False)
        except:
            print("Error opening serial port {}".format(p))
            sys.exit()
        # self.handle_response()

    def close(self):
        self.ser.close()

    def readline(self):
        if self.ser.in_waiting != 0:
            c = self.ser.read()
            if c == b"\n":
                s = self._line
                self._line = ""
                return s
            else:
                self._line += c.decode("utf-8")

    def readline_bytes(self):
        if self.ser.in_waiting != 0:
            c = self.ser.read()
            if c == b"\n":
                s = self._line
                if s[-1] == "\r":
                    s = s[:-1]
                self._line = ""
                return s
            else:
                self._line += c.decode()

    def write(self, str):
        self.ser.write(str.encode())


class Printer(SerialDevice):
    def home(self):
        self.send_gcode("G28")

    def move(self, x, y, z, speed=200):
        self.send_gcode(f"G0 X{x:.3f} Y{y:.3f} Z{z:.3f} F{speed}")

    def send_gcode(self, gcode):
        gcode += "\n"
        # print("sending gcode", gcode.encode())
        self.ser.write(gcode.encode())

    def wait_for_ok(self):
        while True:
            s = self.readline()
            if s != None:
                if s == "ok":
                    return


# USB_VENDOR_DICT
usbvid = {9114: "Adafruit", 10161: "Ultimachine", 1027: "FTDI"}


def print_ports():
    for p in serial.tools.list_ports.comports():
        vid = str(p.vid)
        if p.vid in usbvid:
            vid += f" {usbvid[p.vid]}"
        print(f"{p.device} vid:{vid} pid:{p.pid} {p.description}")


def enumerate_ports():
    return [p.device for p in serial.tools.list_ports.comports()]


def get_ports_with_vid(vid):
    return [p.device for p in serial.tools.list_ports.comports() if p.vid == vid]


def print_devices():
    table = prettytable.PrettyTable()
    table.field_names = ["port", "vid", "pid", "serial", "manufacturer", "product"]
    for p in serial.tools.list_ports.comports():
        if p.vid == None or p.pid == None:
            continue
        vid = str(p.vid)
        if p.vid in usbvid:
            vid += f" {usbvid[p.vid]}"
        table.add_row( [p.device, vid, p.pid, p.serial_number, p.manufacturer, p.product] )
        print(p.manufacturer, p.serial_number, p.product)
    print(table)

   


if __name__ == "__main__":
    print_ports()
    print(enumerate_ports())
    print(get_ports_with_vid(9114))
