import os
import re
import subprocess


def main():
    modalias_file = open('/sys/class/dmi/id/modalias', 'r')
    modalias_line = modalias_file.readlines()[0]
    modalias_file.close()

    manufacturer_i = re.search(':svn', modalias_line).span()
    model_i = re.search(':pn', modalias_line).span()
    end_i = re.search(':pvr', modalias_line).span()

    manufacturer = modalias_line[manufacturer_i[1]:model_i[0]]
    model = modalias_line[model_i[1]:end_i[0]]

    driver_string = str(subprocess.check_output(['udevadm', 'info', '-n', '/dev/iio:device0']))

    driver_end_i = re.search(':00/iio:device0', driver_string).span()
    
    driver = driver_string[driver_end_i[0]-8:driver_end_i[0]]

    modalias_string = 'sensor:modalias:acpi:{}*:dmi:*:svn{}*:pn{}:*'.format(driver, manufacturer, model)

    temp_matrix = '  ACCEL_MOUNT_MATRIX=0, -1, 0; -1, 0, 0; 0, 0, -1'

    file_contents = modalias_string + '\n' + temp_matrix + '\n'

    file_path = '/etc/udev/hwdb.d/60-sensor.hwdb'

    matrix_file = open(file_path, 'w')
    matrix_file.write(file_contents)
    matrix_file.close()

    '''
    sudo systemd-hwdb update
    sudo udevadm trigger -v -p DEVNAME=/dev/iio:device0
    sudo service iio-sensor-proxy restart
    '''

    return None


main()