#!/bin/bash
# Script to start FluidSynth & aconnect
echo Attempting to start FluidSynth
amixer cset numid=3 1
sudo fluidsynth -si -a alsa -m alsa_seq /usr/share/sounds/sf2/FluidR3_GM.sf2 &
sleep 5
sudo pkill fluidsynth
amixer cset numid=3 1
sudo fluidsynth -si -f /home/pi/config.txt -a alsa -m alsa_seq /usr/share/sounds/sf2/FluidR3_GM.sf2 &
sleep 10
aconnect 20:0 128:0