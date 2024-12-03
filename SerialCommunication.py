import serial
import time

# Connect to Arduino

print("Connected to Arduino!")

def send_data(board,word):

    try:
        # Iterate over generated values
        board.write(f"{word}\n".encode())

    except KeyboardInterrupt:
        print("\nExiting program...")


