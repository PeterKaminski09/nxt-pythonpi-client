#!/bin/bash
open_venv () {
  . /home/pi/nxt-pythonpi-client/venv/bin/activate
}

cd /home/pi/nxt-pythonpi-client
open_venv
python client.py
