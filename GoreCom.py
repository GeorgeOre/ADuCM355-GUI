import time
import serial


def initialize_serial(port, baud_rate):
    ser = serial.Serial(port, baud_rate, timeout=1)  # Open the serial port
    return ser

def send_data(ser, data):
    ser.write(data.encode())  # Send data as bytes

def receive_data(ser, max_bytes=1024):
    received_data = ser.read(max_bytes)  # Read up to max_bytes from the serial port
    return received_data.decode()

def receive_data2(ser, voltage_data, current_data, total_input):
    # Set the timeout to 12 seconds
    timeout = time.time() + 12

    try:
        while True:
            if time.time() > timeout:
                break
            data = ser.readline().decode('utf-8').strip()
            total_input += data

            # Check if the line contains numerical data
            if ',' in data and '[' not in data:
                parts = data.split(',')
                x_value = float(parts[0])
                y_value = float(parts[1])
                voltage_data.append(x_value)
                current_data.append(y_value)
    finally:
        return total_input

def close_serial(ser):
    ser.close()  # Close the serial port
def poop_pants():
    poop_pants()



