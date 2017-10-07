from socketIO_client import SocketIO
from nxt.bluesock import BlueSock
import sys

socketIO = SocketIO('http://robocode-server.herokuapp.com', 80)
mac_addresses = []

### Socket Handlers ###
def on_connect(*args):
    print('connected to the server')

def on_execute_code (*args):
    print('executing commands')
    if len(args) == 0:
        print('didnt get enough arguments')
        return

    params = args[0]
    if 'commands' in params and 'address' in params:
        sock = BlueSock(params['address'])
        if sock:
            brick = sock.connect()
            brick.play_tone_and_wait(440, 1000)
            sock.close()
            print('finished code')
        else:
            print("issue connecting to nxt to run code")
    socketIO.emit('finished program')


### Main ### 
def main():
    #Read in the mac addresses that we'll need to send code to
    file = open("mac_addresses.txt", "r")
    global mac_addresses 
    mac_addresses += file.readlines()
    mac_addresses = [x.strip() for x in mac_addresses]
    
    #Open a socket connection with the server
    socketIO.on('connect', on_connect)
    socketIO.on('execute code', on_execute_code)
    socketIO.emit('register nxts', {"addresses": mac_addresses})
    socketIO.wait()

if __name__ == '__main__':
    main()

### Helper functions ###
def ping_server_with_mac(mac_address):
        
        brick = sock.connect()
        for command in body["commands"]:
                print(command)
                run_command_on_brick(brick, command)     
        sock.close()
        
def run_command_on_brick(brick, command):
        if command["type"] == "sound":
                print("trying to run the command")
                freq = 475
                duration = 1000
                if 'freq' in command:
                        freq = command["freq"]
                if 'duration' in command:
                        duration = command["duration"]
                brick.play_tone_and_wait(freq,duration)
        else:
                print("command not run")

