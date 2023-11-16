import json
import socket
import time

SERVER_ADDRESS = '10.20.16.80'
SERVER_PORT = 2000


def add_null_terminator_at_beginning(message_str):
    # Convert the JSON string to bytes
    message_bytes = bytes(message_str, 'utf-8')

    # Add null terminator at the beginning
    return b'\x00' + message_bytes


def add_null_terminator_at_end(message_str):
    # Convert the JSON string to bytes
    message_bytes = bytes(message_str, 'utf-8')

    # Add null terminator at the end
    return message_bytes + b'\x00'


def send_message_to_server(filename, add_at_end=True, sleep_duration=10):
    # Read message from JSON file
    message_str = read_message_from_file(filename)

    if add_at_end:
        data = add_null_terminator_at_end(message_str)
    else:
        data = add_null_terminator_at_beginning(message_str)

    # Create a socket and connect to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_ADDRESS, SERVER_PORT))

        # Send the message to the server
        s.sendall(data)

        # Receive the response from the server
        response = s.recv(1024).decode('utf-8')

        # Save the response to a JSON file
        output_filename = 'output_' + filename
        save_response_to_file({'result': response}, output_filename)

        print(f'Received response from server: {response}')

        # Keep the connection alive for the specified duration
        time.sleep(sleep_duration)


def read_message_from_file(filename):
    with open(filename, 'rt+') as file:
        return file.read()


def save_response_to_file(response, filename):
    with open(filename, 'w') as file:
        json.dump(response, file, indent=2)


def main():
    # Specify the list of input files
    # input_files = ['handshake.json', 'identify.json']

    # Send message with null terminator at the beginning
    send_message_to_server('handshake.json', add_at_end=False)
    # Send message with null terminator at the end
    send_message_to_server('identify.json', add_at_end=True)


if __name__ == "__main__":
    main()
