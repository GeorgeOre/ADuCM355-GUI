import serial


def initialize_serial(port, baud_rate):
    ser = serial.Serial(port, baud_rate, timeout=1)  # Open the serial port
    return ser

def send_data(ser, data):
    ser.write(data.encode())  # Send data as bytes

def receive_data(ser, max_bytes=1024):
    received_data = ser.read(max_bytes)  # Read up to max_bytes from the serial port
    return received_data.decode()

def close_serial(ser):
    ser.close()  # Close the serial port
def poop_pants():
    poop_pants()



