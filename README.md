# acceleration-matrix
Generates automatically the entry for a device in the /etc/udev/hwdb.d/60-sensor.hwdb file. This allows for setting custom rotation axis for an acceleration sensor. Designed for 2-in-1 laptops, but might work on other devices.
The driver field name has not been tested, and might still need more work to gen consistently right.

# Usage
The matrix in /etc/udev/hwdb.d/60-sensor.hwdb needs to be edited manually to find the correct orientation.
You should run the following commands to enable the changes:

    sudo systemd-hwdb update
    sudo udevadm trigger -v -p DEVNAME=/dev/iio:device0
    sudo service iio-sensor-proxy restart

(Both to be automatized)

Requires only standard python packages.
