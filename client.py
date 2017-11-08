from socketIO_client import SocketIO
from nxt.bluesock import BlueSock
from nxt.motor import Motor, PORT_A, PORT_B, PORT_C
from nxt.sensor import Light, Sound, Touch, Ultrasonic
from nxt.sensor import PORT_1, PORT_2, PORT_3, PORT_4
import sys

# Global variables
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


# Function which determines the output of the conditional statement based on the given sensor
def compute_check(cond, sensor):
    if 'gt' not in cond or 'gte' not in cond or 'lt' not in cond or 'lte' not in cond or 'e' not in cond or 'ne' not in cond or 'check' not in cond:
        return

    gt = cond['gt']
    gte = cond['gte']
    lt = cond['lt']
    lte = cond['lte']
    e = cond['e']
    ne = cond['ne']
    check = cond['check']

    print(sensor.get_sample())
    if gt:
        return sensor.get_sample() > check
    elif gte:
        return sensor.get_sample() >= check
    elif lt:
        return sensor.get_sample() < check
    elif lte:
        return sensor.get_sample() <= check
    elif e:
        return sensor.get_sample() == check
    else:
        return sensor.get_sample() != check

### MOTOR ###
def execute_motor(command, brick):
    if 'brake' not in command or 'power' not in command or 'revolutions' not in command or 'port' not in command:
          return
    #Execute the command
    port = ports[command['port']]
    m = Motor(brick, port)
    m.turn(command['power'], command['revolutions'] * 360, command['brake'])


### TOUCH SENSOR ###
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

### LIGHT SENSORS ###
def execute_light(command, brick):
    if 'port' not in command or 'condition' not in command:
        return
    
    port = ports[command['port']]
    cond = command['condition']
    light = Light(brick, port)
    comparison = compute_check(cond, light)

    # Dont execute any malformed commands
    if comparison == None or 'while' not in cond or 'if' not in cond or 'else' not in cond:
        return
    
    isWhile = cond['while']
    ifCommands = cond['if']
    elseCommands = cond['else']

    if isWhile and comparison:
        while compute_check(cond, light):
            execute_commands(ifCommands, brick)
    elif not isWhile and comparison:
        execute_commands(ifCommands, brick)
    elif not isWhile and not comparison:
        execute_commands(elseCommands, brick)
    
    

### ULTRASONIC SENSOR ###
def execute_ultrasonic(command, brick):
    if 'port' not in command or 'condition' not in command:
        return

    port = ports[command['port']]
    cond = command['condition']
    ultrasonic = Ultrasonic(brick, port)
    comparison = compute_check(cond, ultrasonic)

    # Dont execute any malformed commands
    if comparison == None or 'while' not in cond or 'if' not in cond or 'else' not in cond:
        return
    
    isWhile = cond['while']
    ifCommands = cond['if']
    elseCommands = cond['else']

    if isWhile and comparison:
        while compute_check(cond, ultrasonic):
            execute_commands(ifCommands, brick)
    elif not isWhile and comparison:
        execute_commands(ifCommands, brick)
    elif not isWhile and not comparison:
        execute_commands(elseCommands, brick)

### SOUND SENSOR ###
def execute_sound(command, brick):
    if 'port' not in command or 'condition' not in command:
        return

    port = ports[command['port']]
    cond = command['condition']
    sound = Sound(brick, port)
    comparison = compute_check(cond, sound)

    # Dont execute any malformed commands
    if comparison == None or 'while' not in cond or 'if' not in cond or 'else' not in cond:
        return
    
    isWhile = cond['while']
    ifCommands = cond['if']
    elseCommands = cond['else']

    if isWhile and comparison:
        while compute_check(cond, sound):
            execute_commands(ifCommands, brick)
    elif not isWhile and comparison:
        execute_commands(ifCommands, brick)
    elif not isWhile and not comparison:
        execute_commands(elseCommands, brick)


### Play a sound ###
def play_sound(command, brick):
    
    if 'file' in command:
        file = command['file'].encode('ascii', 'ignore')
        brick.play_sound_file(False, file + '.rso')
        return
    if 'freq' not in command and 'duration' not in command:
        return
    freq = command['freq']
    duration = command['duration']
    brick.play_tone_and_wait(freq,duration)
    

functions = {
    "motor": execute_motor,
    "touch": execute_touch,
    "light": execute_light,
    "ultrasonic": execute_ultrasonic,
    "sound": execute_sound,
    "playsound": play_sound
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
            try:
                execute_commands(params['commands'], brick)
            except:
                print("Error thrown executing commands")
            sock.close()
            print('finished code')
        else:
            print("issue connecting to nxt to run code")
    socketIO.emit('finished program')



def execute_commands(commands, brick):
    #For each command, execute which type of command it is
    for command in commands:
        if 'type' in command:
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

