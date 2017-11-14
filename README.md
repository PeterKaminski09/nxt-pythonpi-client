# NXT + Rasberry Pi + iPad

This is the Raspberry pi python client code for the project. It should be downloaded and run on the Raspberry Pi.

The Raspberry Pi server code can be found [here](https://github.com/PeterKaminski09/nxt-js-server)

## How to use

1. Clone the repository and run the setup.sh script. You'll need to accept and enter Y when prompted for one of the downloads, and then the raspberry pi will restart.

2. Once it's restarted, modify the nxt_beep.py file to add the MAC address of the NXT you're trying to test. Make sure the NXT is connected to the Bluetooth of the Pi.

3. Finally, run the postsetup.sh script to finalize the setup and you should hear your NXT play a sound to confirm that the setup was successful.

More detailed instructions can be found [here](https://docs.google.com/document/d/1wYHb94qGpXc_Zqt9wM6cyfQtsu9Hmcr0uXfuJewzkoo/edit?usp=sharing)
