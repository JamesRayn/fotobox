#!/bin/bash

echo "Enabling Camera"
#yes, 0=on, 1=off
sudo raspi-config nonint do_camera 0

echo "Updating System"
sudo apt update
yes | sudo apt dist-upgrade

echo "Installing prerequirements"
yes | sudo apt install openbox xorg lightdm python3 python3-picamera2 python3-opengl python3-pyqt5 python3-pyqt5.qtwebkit python3-rpi.gpio unclutter
# no more python3-picamera 
# Suggested tools: sxiv tmux vim usbmount x11vnc git //note unclutter-xfixes unclutter-startup

echo "Installing Fotobox"
#git clone https://github.com/adlerweb/fotobox.git /home/pi/fotobox

echo "Configuring autostart"
mkdir -p ~/.config/openbox
echo "xset s noblank" >> ~/.config/openbox/autostart
echo "xset s off" >> ~/.config/openbox/autostart
echo "xset -dpms" >> ~/.config/openbox/autostart
echo "sudo renice 19 -u www-data" >> ~/.config/openbox/autostart
echo "cd ~/fotobox/ ; python3 fotobox.py | tee fotobox.log" >> ~/.config/openbox/autostart
echo "cd ~/fotobox/ ; python3 fotobox.py | tee fotobox.log" >> ~/.config/openbox/autostart
echo "cd ~/fotobox/ ; python3 fotobox.py | tee fotobox.log" >> ~/.config/openbox/autostart
echo "cd ~/fotobox/ ; python3 fotobox.py | tee fotobox.log" >> ~/.config/openbox/autostart
echo "cd ~/fotobox/ ; python3 fotobox.py | tee fotobox.log" >> ~/.config/openbox/autostart
# GUI-Boot with autologin
sudo raspi-config nonint do_boot_behaviour B4

echo "Syncing..."
sudo sync

echo "Reboot..."
sudo reboot