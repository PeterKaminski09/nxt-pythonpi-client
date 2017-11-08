from socketIO_client import SocketIO
from nxt.bluesock import BlueSock
from nxt.motor import Motor, PORT_A, PORT_B, PORT_C
from nxt.sensor import Light, Sound, Touch, Ultrasonic
from nxt.sensor import PORT_1, PORT_2, PORT_3, PORT_4
import sys

socketIO = SocketIO('http://robocode-server.herokuapp.com', 80)
mac_addresses = []
ports = {
    1: PORT_1,
    2: PORT_2,
    3: PORT_3,
    4: PORT_4,
    'A': PORT_A,
    'B': PORT_B,
    'C': PORT_C
}

### MOTOR ###
def execute_motor(command, brick):
    if 'brake' not in command or 'power' not in command or 'revolutions' not in command or 'port' not in command:
          return
    #Execute the command
    port = ports[command['port']]
    m = Motor(brick, port)
    m.turn(command['power'], command['revolutions'] * 360, command['brake'])


### SENSORS ###
def execute_touch(command, brick):
    if 'condition' not in command or 'port' not in command:
          return
          
    condition = command['condition']
          
    if 'touch' not in condition or 'notouch' not in condition or 'while' not in condition or 'if' not in condition or 'else' not in condition:
          return

    port = ports[command['port']]
    touch = condition['touch']
    notouch = condition['notouch']
    isWhile = condition['while']
    ifCommands = condition['if']
    elseCommands = condition['else']
    t = Touch(brick, port)

    #Run a while loop
    if isWhile and touch:
          while t.get_sample():
              execute_commands(ifCommands, brick)
    elif isWhile and notouch:
          while not t.get_sample():
              execute_commands(ifCommands, brick)
          
    #else if the sensor is touched
    elif touch and t.get_sample():
          #Run a check for the touch condition
          execute_commands(ifCommands, brick)
    elif touch and not t.get_sample():
          execute_commands(elseCommands, brick)

    #else if the sensor is not touched
    elif notouch and not t.get_sample():
          execute_commands(ifCommands, brick)
    elif notouch and t.get_sample():
          execute_commands(elseCommands, brick)
    
def execute_light():
    print('execute light')

def execute_ultrasonic():
    print('execute ultrasonic')


def execute_sound():
    print('execute sound')

functions = {
    "motor": execute_motor,
    "touch": execute_touch,
    "light": execute_light,
    "ultrasonic": execute_ultrasonic,
    "sound": execute_sound
}
    

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
            execute_commands(params['commands'], brick)
            sock.close()
            print('finished code')
        else:
            print("issue connecting to nxt to run code")
    socketIO.emit('finished program')



def execute_commands(commands, brick):
    #For each command, execute which type of command it is
    for command in commands:
        functions[command['type']](command, brick)
    

          
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
    print('registering nxts: ')
    print(mac_addresses)
    socketIO.emit('register nxts', {"addresses": mac_addresses})
    socketIO.wait()

if __name__ == '__main__':
    main()


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

