# Bob Smith Charanga
# 2016-09
# theremin.py
"""MIDI based theremin using a Raspberry Pi and a sonar HC-SR04 as pitch control"""
"""based on code from derickdeleon.com"""

import RPi.GPIO as GPIO
import ZeroSeg.led as led
import pygame
import pygame.midi
import time



#display related methods

device = led.sevensegment(cascaded=2)

def writeKey(keyID = 0):
    print('writeKey',keyID)
    keyArray = [0x00000C,0x0000Db,0x00000D,0x0000Eb,0x00000E,0x00000F,0x00009b,0x000009,0x0000Ab,0x00000A,0x0000Bb,0x00000B,0x00000C,0x000DDD]
    device.write_number(deviceId=1, value=keyArray[keyID], base=16, leftJustify=False)
   

def writeMIDIPatch(midP = 0):
    #device.letter(device, 4, int(midP / 100))     # Tens
    
    counter = 8
    for i in str(midP):
        device.letter(1, counter, i)     # Tens
        counter = counter -1

def writeNote(noP = 0):
    #device.letter(device, 4, int(midP / 100))     # Tens
    
    counter = 5
    for i in str(noP):
        device.letter(1, counter, i)     # Tens
        counter = counter -1





# Distance Related Methods
def prepare(GPIO_ECHO, GPIO_TRIGGER):
    """ Initialize the Raspberry Pi GPIO  """
    # Set pins as output and input
    print(""" Initialize the Raspberry Pi GPIO  """)
    GPIO.setup(GPIO_TRIGGER,GPIO.OUT)    # Trigger
    GPIO.setup(GPIO_ECHO,GPIO.IN)        # Echo
    # Set trigger to False (Low)
    GPIO.output(GPIO_TRIGGER, False)

    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(button3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(button4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(fswitch1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(fswitch2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # Allow module to settle
    time.sleep(0.5)

def get_distance(GPIO_ECHO, GPIO_TRIGGER):
    """ get the distance from the sensor, echo - the input from sensor """
    # Send 10us pulse to trigger
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()
    # Taking time
    while GPIO.input(GPIO_ECHO)==0:
        start = time.time()
    while GPIO.input(GPIO_ECHO)==1:
        stop = time.time()
    # Calculate pulse length
    elapsed = stop-start
    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = elapsed * 34300
    # That was the distance there and back so halve the value
    distance = distance / 2

    return round(distance,2)

def get_switch(GPI_BUTTON):
    """ get the state on any switch """

    input_state = GPIO.input(GPI_BUTTON)
    #print('Button Checked',GPI_BUTTON,input_state)
    if input_state == False:
        print('Button Pressed',GPI_BUTTON,input_state)
        return True
    return False


def conf_midi():
    """ Initialize MIDI component """
    
    pygame.init()
    pygame.midi.init()
    port = 0
    global midiOutput   # It is used in other methods
    midiOutput = pygame.midi.Output(port, 9)
    set_instrument(1)
    #print_device_info()

def set_instrument(inst):
    print("set_instrument",inst)
    midiOutput.set_instrument(inst)

def play_midi(note, b4note, volume):
    """ Play a new MIDI note and turn off the last one """
    # use the last note to compare
    
    if (note != b4note):
        """ To-Do: smoother transitions between notes, use pitch bend. """
        

        midiOutput.note_off(b4note,volume,channel)

        
        midiOutput.note_on(note,volume,channel)
        print(note,channel)
    # help to not consume all resources
    time.sleep(.2)

def get_note(dist=0):
    """ Compute the note based on the distance measurements, get percentages of each scale and compare """
    # Config
    # you can play with these settings

    #scale =         [-1, -5, 60,  60, -5 ,62, 62, -5, 64, 64, -5, 67, 67, -5, 69, 69, -5, 72, -5, -1]
    #distances =     [38, 29, 28,  24, 21, 21, 19, 17, 16, 13, 12, 11,  9,  7,  6,  5,  3,  2,  1,  0]
    
    '''scale =         [-1, -5,  60, -5 , 62, -5, 64, -5,  67, -5,  69, -5, 72, -5, -1]
    distances =     [40, 35,  24, 21,  19, 17, 13, 10,   9,  7,    5,  4,  2,  .5,  0]'''
    
    
    scale =         [-1, -5,  60, -5 ,      67, -5,  69, -5, 72, -5, -1]
    distances =     [40, 35,  21, 18,       16,  9,    6,  4,  2,  .5,  0]

    for index in range(len(distances)):
        if dist>distances[index]:            
           
            return int(scale[index])



'''

    offset = 0

    minDist = 3    # Distance Scale
    maxDist = 30
    octaves = 1
    minNote = 48   # c4 middle c
    maxNote = minNote + 12*octaves
    #print("dist",dist)
                
    if dist>38:
        return int(-1)

    if dist>27:
        return int(60+offset)


    if dist>20:
        return int(62+offset)
    if dist>15:
        return int(64+offset)
    if dist>10:
        return int(67+offset)
    if dist>5:
        return int(69+offset)
    if dist>3:
        return int(72+offset)
     
    return int(-1)
    
    # Percentage formula
    fup = (dist - minDist)*(maxNote-minNote)
    fdown = (maxDist - minDist)
    note = minNote + fup/fdown
    """ To-do: Add in scales """
   
    return int(note)
    '''
# MAIN
GPIO.setwarnings(False)
# The pin number is the actual pin number
GPIO.setmode(GPIO.BCM)
# Set up the GPIO channels
trigger = 23
echo = 24
button = 12
button1 = 21 #button 1 on device controls midi
button2 = 20 #button 2 on device controls key
button3 = 19
button4 = 4

fswitch1 = 17
fswitch2 = 26
# channel is to swap between 9 and 0 if 9 we are in drum mode if 0 instrument mode
channel =9
prepare(echo, trigger)
note = 0
conf_midi()
volume = 127
instrument = 1
offset=-21
device.clear()
delay = .5
writeKey(13)
time.sleep(delay)
writeMIDIPatch(instrument)
lastDistance = 0
offCounter = 0

try:
    while True:
        """ to-do this is broke """

        b4note = note
        # get distance
        d = get_distance(echo, trigger)
        # calculate note
        '''
        if abs(d-lastDistance)>500:
            print "weirdRange",d
            offCounter = offCounter+1;
            if offCounter<3:
                d=lastDistance
            else:
                offCounter=0'''
        '''d = lastDistance + (d-lastDistance)/1.1
        print d , lastDistance
        lastDistance = d'''
        
        note = get_note(d)
        if note>0:
            note = note+offset

        switch = get_switch(button)
        switch1 = get_switch(button1)
        switch2 = get_switch(button2)
        switch3 = get_switch(button3)
        switch4 = get_switch(button4)
        switch5 = get_switch(fswitch1)
        switch6 = get_switch(fswitch2)

        #print("switches",switch,switch1,switch2,switch3,switch4,switch5,switch6)
       
        # to-do, take a number of sample notes and average them, or any other statistical function. eg. Play just minor notes, ponderate average, etc. 
        # play the note

       

            
        bright = 10

        volume = 80
        if switch:

            volume = 110
            bright = 15
        if  switch3:
             note = 60+offset
        #print("note",note)
            
        if note != -5:
            
            play_midi(note, b4note, volume)
           
            if note!=-1:

                device.brightness(bright)
                writeNote(note)
            else:
                device.brightness(6)
        if note == -5:
            note = b4note





        if switch1:
            print ("Button 1 pressed",offset)
            
            offset = offset +1
            if offset>12:
                offset = 0
            
            elif offset<0:
                offset=0


            if offset==12:
                writeKey(offset+1)
                writeMIDIPatch(instrument)
                channel=9
                print "DRUMS setting standard offset to be hand clap"
                offset=-21
            else:
                print"NotDrums"
                channel=0
                writeKey(offset)
                writeMIDIPatch(instrument)
            
            time.sleep(0.4)
            
        if switch2:
            print "Button 2 pressed"
            instrument = instrument +1
            if instrument>=128:
                instrument = 1
            set_instrument(instrument)
            writeKey(offset)
            writeMIDIPatch(instrument)
     
     
       
      
        
           
                

except KeyboardInterrupt:

    GPIO.cleanup()
    del midiOutput
    pygame.midi.quit()
GPIO.cleanup()
pygame.midi.quit()
