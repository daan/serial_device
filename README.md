# serial_device
helper code to deal with serial devices and line based communication.

```
uv add git+https://github.com/daan/serial_device
```

```
>>> from serial_device import *
>>> print_devices()
+--------------+------+------+---------+--------------+------------+
|     port     | vid  | pid  |  serial | manufacturer |  product   |
+--------------+------+------+---------+--------------+------------+
| /dev/ttyACM0 | 5824 | 1155 | 5350430 | Teensyduino  | USB Serial |
+--------------+------+------+---------+--------------+------------+
```




