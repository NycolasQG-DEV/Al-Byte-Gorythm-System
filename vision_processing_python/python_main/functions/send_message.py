def send_message(ser,message):
    ser.write((message + '\n').encode())  # send a serial message