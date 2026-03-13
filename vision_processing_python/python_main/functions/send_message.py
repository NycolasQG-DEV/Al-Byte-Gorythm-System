def send_message(ser,message):
    ser.write((message + '\n').encode())  # Adiciona uma nova linha e envia a mensagem