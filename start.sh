#!/bin/bash
open_venv () {
  . /home/pi/Desktop/client-setup/venv/bin/activate
}

cd /home/pi/Desktop/client-setup
open_venv
python client.py
