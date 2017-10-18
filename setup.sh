sudo apt-get update
sudo apt-get install bluetooth bluez blueman python-lightblue python-bluez
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
cp -rf /usr/lib/python2.7/dist-packages/bluetooth venv/lib/python2.7/site-packages/
cp -rf /usr/lib/python2.7/dist-packages/lightblue venv/lib/python2.7/site-packages/
cd ~/Downloads
wget https://github.com/Eelviny/nxt-python/archive/v2.2.2.tar.gz
tar xzf nxt-python-2.2.2.tar.gz
cd nxt-python-2.2.2
python setup.py install
cd
mkdir automated-pylog
sudo crontab -l > mycron
echo "@reboot sh /home/pi/nxt-pythonpi-client/start.sh >/home/pi/automated-pylog/cronlog 2>&1" >> mycron
sudo crontab mycron
echo "Restart required...restarting now"
shutdown -r
