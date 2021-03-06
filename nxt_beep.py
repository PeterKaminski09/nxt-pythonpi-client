# Program to make NXT brick beep using NXT Python with Bluetooth socket
#
# Simon D. Levy  CSCI 250   Washington and Lee University    April 2011

# Change this ID to match the one on your brick.  You can find the ID by doing Settings / NXT Version.  
# You will have to put a colon between each pair of digits.
ID = '00:16:53:1B:E4:30'
# This is all we need to import for the beep, but you'll need more for motors, sensors, etc.
from nxt.bluesock import BlueSock

# Create socket to NXT brick
sock = 	BlueSock(ID)

# On success, socket is non-empty
if sock:

   # Connect to brick
   brick = sock.connect()

   # Play tone A above middle C for 1000 msec
   brick.play_tone_and_wait(440, 1000)
   brick.play_tone_and_wait(440, 250)
   brick.play_tone_and_wait(440, 500)
   # Close socket
   sock.close()

# Failure
else:
   print 'No NXT bricks found'

