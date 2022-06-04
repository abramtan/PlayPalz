# -*- coding:utf-8 -*-
import LCD_1in44
import LCD_Config

import RPi.GPIO as GPIO

import time
from time import sleep

import datetime
import random
from PIL import Image,ImageDraw,ImageFont,ImageColor

import subprocess
import os
from pygame import mixer

import board
import neopixel
import smbus

KEY_UP_PIN     = 17 
KEY_DOWN_PIN   = 6
KEY_LEFT_PIN   = 26
KEY_RIGHT_PIN  = 5z
KEY_PRESS_PIN  = 13

#init GPIO dont uncomment
GPIO.setmode(GPIO.BCM) 
GPIO.cleanup()
GPIO.setup(KEY_UP_PIN,      GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Input with pull-up
GPIO.setup(KEY_DOWN_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_LEFT_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_RIGHT_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY_PRESS_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up

# 240x240 display with hardware SPI:
disp = LCD_1in44.LCD()
Lcd_ScanDir = LCD_1in44.SCAN_DIR_DFT  #SCAN_DIR_DFT = D2U_L2R
disp.LCD_Init(Lcd_ScanDir)
disp.LCD_Clear()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = 128
height = 128
image = Image.new('RGB', (width, height))

font = ImageFont.load_default()
font2 = ImageFont.truetype('An.ttf',15)
font3 = ImageFont.truetype('An.ttf',35)
font4 = ImageFont.truetype('An.ttf',15)
font5 = ImageFont.truetype('An.ttf',28)

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)
disp.LCD_ShowImage(image,0,0)

now_page_1_hor = 5
now_page_1_ver = 5
now_page_2 = 4
now_page_c=15
current_page=7
high=0
low=0
high_l=0
high_r=0
high_u=0
high_d=0
low_l=0
low_r=0
low_u=0
low_d=0
completed_c1=0 #0 means complete
completed_c2=0
completed_c3=0
s_c1=0
s_c2=0
s_c3=0
points_c1=0
points_c2=0
points_c3=0
points=0
col_sel_q=0
col_sel_p=0
col_sel_r=0
col_sel_t=0
col_c1=0
col_c2=0
col_c3=0
col_b_c=0
col_d=0
col_b=0
num_pixels=16
x=1
pixels = neopixel.NeoPixel(board.D12, 16)

find_things = ["mimosa plant", "snails", "leaves"]
thing = random.choice(find_things)

mixer.init()

retro_sound=mixer.Sound('retro_game_jingle.wav')
button_click=mixer.Sound('button_click.wav')

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

y=0

bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

def main_menu_display():

    global col_sel_q
    global col_sel_p
    global col_sel_r
    global col_sel_t

    draw.rectangle((0,0,128,128), outline=0, fill=0)

    draw.rectangle((5,5,59,59), outline=100, fill='#ffd9ea')
    draw.rectangle((69,5,123,59), outline=100, fill='#ffeda2')
    draw.rectangle((5,69,59,123), outline=100, fill='#b7ffb1')
    draw.rectangle((69,69,123,123), outline=100, fill='#95f2ff')

    draw.text((16,23),"Quest", font=font2, fill=col_sel_q)
    draw.text((78,23), "Points", font=font2, fill=col_sel_p)
    draw.text((9,87), "Rewards", font=font2, fill=col_sel_r)
    draw.text((84,87), "Time", font=font2, fill=col_sel_t)

def page_manage():

    global current_page

    if current_page==0:
        main_menu()
    elif current_page==1:
        menu_challenges()
    elif current_page==2:
        menu_points()
    elif current_page==3:
        menu_characters()
    elif current_page==4: #for challenge1
        challenge_1()
    elif current_page==5:
        challenge_2()
    elif current_page==6:
        challenge_3()
    elif current_page==7:
        time_now()
    elif current_page==8:
        led_blnk()

def input():
    global high
    global low

    if GPIO.input(KEY_PRESS_PIN)==0:
        high=1
        low=0
        if mixer.get_busy():
            hello = "hello"
        else:
            button_click.play()
    else:
        low=1

def input_l():
    global high_l
    global low_l

    if GPIO.input(KEY_LEFT_PIN)==0:
        high_l=1
        low_l=0
        if mixer.get_busy():
            hello = "hello"
        else:
            button_click.play()
    else:
        low_l=1

def input_r():

    global high_r
    global low_r

    if GPIO.input(KEY_RIGHT_PIN)==0:
        high_r=1
        low_r=0
        if mixer.get_busy():
            hello = "hello"
        else:
            button_click.play()
    else:
        low_r=1

def input_u():
    global high_u
    global low_u

    if GPIO.input(KEY_UP_PIN)==0:
        high_u=1
        low_u=0
        if mixer.get_busy():
            hello = "hello"
        else:
            button_click.play()
    else:
        low_u=1

def input_d():
    global high_d
    global low_d

    if GPIO.input(KEY_DOWN_PIN)==0:
        high_d=1
        low_d=0
        if mixer.get_busy():
            hello = "hello"
        else:
            button_click.play()
    else:
        low_d=1


def time_now():

    global current_page
    global high

    draw.rectangle((0,0,128,128), outline=0, fill=0)

    e=datetime.datetime.now()
    f=e.strftime("%Y-%m-%d")
    g=e.strftime("%H:%M:%S")
    draw.text((35,30), str(f), font=font4, fill=255)
    draw.text((20,50), str(g), font=font5, fill=255)

    input()
    if high==1 and low==1:
        current_page=0
        high=0

def led_blnk():

    global current_page
    global high
    global x
    global num_pixels
    global pixels

    draw.rectangle((0,0,128,128), outline=0, fill='#ffd9ea')

    draw.text((15,30),"Search for your", font=font4, fill=0)
    draw.text((15,50),"teammate", font=font4, fill=0)

    pixels[5] = (1,1,1)
    pixels[7] = (1,1,1)
    pixels[13] = (1,1,1)
    time.sleep(0.1)
    pixels.fill((0,0,0))
    time.sleep(0.1)

    input()
    if high==1 and low==1:
        current_page=1
        high=0
        pixels.fill((0,0,0))

def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

MPU_Init()

def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value

def imu_stuff():

    global y
    	
	#Read Accelerometer raw value
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)
	
	#Read Gyroscope raw value
    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_YOUT_H)
    gyro_z = read_raw_data(GYRO_ZOUT_H)
	
	#Full scale range +/- 250 degree/C as per sensitivity scale factor
    Ax = acc_x/16384.0
    Ay = acc_y/16384.0
    Az = acc_z/16384.0
	
    Gx = gyro_x/131.0
    Gy = gyro_y/131.0
    Gz = gyro_z/131.0
	
#    print(Gx)
#    print(Gy)
#    print(Gz)
 
    if Gx > 50 or Gy > 50 or Gz > 50:
        print('Challenge Complete')
        print(y)
        y = y + 1



def main_menu():

    global now_page_1_hor
    global now_page_1_ver
    global now_page_2
    global current_page
    global high
    global low
    global high_u
    global low_u
    global high_d
    global low_d
    global high_r
    global low_r
    global high_l
    global low_l
    global col_sel_q
    global col_sel_p
    global col_sel_r
    global col_sel_t

    main_menu_display()

    input_u()
    if high_u==1 and low_u==1: # button is released 
        #if now_page_1_ver==69:
            #now_page_1_ver -= 64
            #draw.rectangle((now_page_1_hor,now_page_1_ver,now_page_1_hor+54,now_page_1_ver+54), outline=255, fill='#f9f4e3')
        hello = "hello"
        if now_page_1_hor==5:
            col_sel_q=255
            col_sel_p=0
        elif now_page_1_hor==69:
            col_sel_p=255
            col_sel_q=0
            #else:
                #draw.rectangle((now_page_1_hor,5,now_page_1_hor+54,59), outline=255)
        col_sel_r=0
        col_sel_t=0
        now_page_1_ver=5
        high_u=0
    
    input_l()
    if high_l==1 and low_l==1: # button is released
        #if now_page_1_hor>5:
            #now_page_1_hor -= 64
            #draw.rectangle((now_page_1_hor,now_page_1_ver,now_page_1_hor+54,now_page_1_ver+54), outline=255)
        #else:
            #draw.rectangle((5,now_page_1_ver,59,now_page_1_ver+54), outline=255)
        hello = "hello"
        if now_page_1_ver==5:
            col_sel_q=255
            col_sel_r=0
        elif now_page_1_ver==69:
            col_sel_q=0
            col_sel_r=255
        col_sel_p=0
        col_sel_t=0
        now_page_1_hor=5
        high_l=0
    
    input_r()
    if high_r==1 and low_r==1: # button is released
        #if now_page_1_hor<69:
            #now_page_1_hor += 64
            #draw.rectangle((now_page_1_hor,now_page_1_ver,now_page_1_hor+54,now_page_1_ver+54), outline=255)
        #else:
            #draw.rectangle((69,now_page_1_ver,123,now_page_1_ver+54), outline=255)
        hello = "hello"
        if now_page_1_ver==5:
            col_sel_p=255
            col_sel_t=0
        elif now_page_1_ver==69:
            col_sel_p=0
            col_sel_t=255
        col_sel_q=0
        col_sel_r=0
        now_page_1_hor=69
        high_r=0
        
    input_d()
    if high_d==1 and low_d==1: # button is released
        #if now_page_1_ver<69:
            #now_page_1_ver += 64
            #draw.rectangle((now_page_1_hor,now_page_1_ver,now_page_1_hor+54,now_page_1_ver+54), outline=255)
        #else:
            #draw.rectangle((now_page_1_hor,69,now_page_1_hor+54,123), outline=255)
        hello = "hello"
        if now_page_1_hor==5:
            col_sel_r=255
            col_sel_t=0
        elif now_page_1_hor==69:
            col_sel_r=0
            col_sel_t=255
        col_sel_q=0
        col_sel_p=0
        now_page_1_ver=69
        high_d=0
        
    input()
    if high==1 and low==1:
    #if GPIO.input(KEY_PRESS_PIN) == 0: # button is released

        if col_sel_q==255:
            current_page=8
            high=0

        if col_sel_p==255:
            current_page=2
            high=0
                
        if col_sel_r==255:
            current_page=3
            high=0

        if col_sel_t==255:
            current_page=7
            high=0

def menu_challenges():

    global now_page_2
    global current_page
    global high
    global low
    global high_u
    global low_u
    global high_d
    global low_d
    global col_c1
    global col_c2
    global col_c3
    global col_b_c

    draw.rectangle((0,0,128,128), outline=0, fill=0)

    draw.rectangle((10,4,118,28), outline=100, fill='#ffd9ea')
    draw.rectangle((10,36,118,60), outline=100, fill='#ffd9ea')
    draw.rectangle((10,68,118,92), outline=100, fill='#ffd9ea')
    draw.rectangle((10,100,118,124), outline=100, fill='#ffd9ea')

    draw.text((15,6),"Challenge 1", font=font2, fill=col_c1)
    draw.text((15,38),"Challenge 2", font=font2, fill=col_c2)
    draw.text((15,70),"Challenge 3", font=font2, fill=col_c3)
    draw.text((15,102),"Back", font=font2, fill=col_b_c)

    input_u()
    if high_u==1 and low_u==1:
        #if now_page_2>4:
            #now_page_2 -= 32
            #draw.rectangle((10,now_page_2,118,now_page_2+24),outline=255)
    #col_ 
        #else:
            #draw.rectangle((10,4,118,28), outline=255)
        if now_page_2==4:
            col_c1=255
            col_c2=0
            col_c3=0
            col_b_c=0
        elif now_page_2==36:
            col_c1=255
            col_c2=0
            col_c3=0
            col_b_c=0
            now_page_2=4
        elif now_page_2==68:
            col_c1=0
            col_c2=255
            col_c3=0
            col_b_c=0
            now_page_2=36
        elif now_page_2==100:
            col_c1=0
            col_c2=0
            col_c3=255
            col_b_c=0
            now_page_2=68
        high_u=0

    input_d()
    if high_d==1 and low_d==1:
        #if now_page_2<100:
            #now_page_2 += 32
            #draw.rectangle((10,now_page_2,118,now_page_2+24), outline=255)
        #else:
            #draw.rectangle((10,100,118,124), outline=255)
    #high_d=0
        if now_page_2==4:
            col_c1=0
            col_c2=255
            col_c3=0
            col_b_c=0
            now_page_2=36
        elif now_page_2==36:
            col_c1=0
            col_c2=0
            col_c3=255
            col_b_c=0
            now_page_2=68
        elif now_page_2==68:
            col_c1=0
            col_c2=0
            col_c3=0
            col_b_c=255
            now_page_2=100
        elif now_page_2==100:
            col_c1=0
            col_c2=0
            col_c3=0
            col_b_c=255
        high_d=0

        #if GPIO.input(KEY_PRESS_PIN) == 0 and now_page_2==100:
    input()
    if high==1 and low==1:
        if now_page_2==4:
            current_page = 4
            high=0
        elif now_page_2==36:
            current_page=5
            high=0
        elif now_page_2==68:
            current_page=6
            high=0
        elif now_page_2==100:
            current_page=0
            high=0

def challenges_display():

    #global now_page_c
    #global col_b
    #global col_d
    global high_r
    global high_l
    global low_r
    global low_l

    draw.rectangle((15,85,59,108), outline=0)
    draw.rectangle((69,85,113,108), outline=0)

    draw.text((21,87),"Shake", font=font2, fill=0)
    draw.text((79,87),"Back", font=font2, fill=255)

    #input_l()
    #if high_l==1 and low_l==1:
        #if now_page_c==69:
            #now_page_c=15
        #col_d=255
        #col_b=0
        #high_l=0

    #input_r()
    #if high_r==1 and low_r==1:
        #if now_page_c==15:
            #now_page_c=69
        #col_d=0
        #col_b=255
        #high_r=0


def challenge_1():

    global high
    global low
    global current_page
    global completed_c1
    global now_page_c
    global s_c1
    global y

    imu_stuff()

    draw.rectangle((0,0,128,128), outline=0, fill='#ffeda2')

    draw.text((15,20),"Slide with your", font=font4, fill=0)
    draw.text((15,45),"teammate", font=font4, fill=0)

    challenges_display()

    if y==3:
        completed_c1=1
        if mixer.get_busy():
            hello = "hello"
            #retro_sound.stop()
        else:
            print(s_c1)
            if s_c1==0:
                retro_sound.play()
                s_c1=1
                print(s_c1)

    input()
    if high==1 and low==1:
        #if now_page_c==69:
        current_page=1
        high=0

def challenge_2():

    global high
    global low
    global current_page
    global completed_c2
    global now_page_c
    global s_c2

    draw.rectangle((0,0,128,128), outline=0, fill='#ffeda2')

    draw.text((15,20),"High five your", font=font4, fill=0)
    draw.text((15,45),"teammate", font=font4, fill=0)

    challenges_display()

    input()
    if high==1 and low==1:

        if now_page_c==15:
            completed_c2=1
            if mixer.get_busy():
                hello="hello"
            else:
                if s_c2==0:
                    retro_sound.play()
                    s_c2=1
        elif now_page_c==69:
            current_page=1
        high=0

def challenge_3():
	
    global high
    global low
    global current_page
    global completed_c3
    global now_page_c
    global thing
    global s_c3

    draw.rectangle((0,0,128,128), outline=0, fill='#ffeda2')

    draw.text((15,20), "Find:", font=font4, fill=0)
    draw.text((15,45), str(thing) , font=font4, fill=0)

    challenges_display()

    input()
    if high==1 and low==1:

        if now_page_c==15:
            completed_c3=1
            if mixer.get_busy():
                 hello="hello"
            else:
                if s_c3==0:
                    retro_sound.play()
                    s_c2=1
        elif now_page_c==69:
            current_page=1
        high=0


def menu_points():

    global points
    global current_page
    global high
    global low
    global points_c1
    global points_c2
    global points_c3
    global completed_c1
    global completed_c2
    global completed_c3

    p_disp=62

    if completed_c1==1:
        points_c1=100
    if completed_c2==1:
        points_c2=100
    if completed_c3==1:
        points_c3=100

    points=points_c1+points_c2+points_c3

    if points==0:
        p_disp=62
    else:
        p_disp=42

    draw.rectangle((0,0,128,128), outline=0, fill='#ffeda2')

    draw.text((p_disp,42), str(points), font=font3, fill=255)

    #if GPIO.input(KEY_LEFT_PIN) == 0:
    input()
    if high==1 and low==1:
        current_page=0
        high=0

def menu_characters():

    global current_page
    global high
    global low

    draw.rectangle((0,0,128,128), outline=0, fill=0)

    image=Image.open('qr.png')
    disp.LCD_ShowImage(image,0,0)

    #if GPIO.input(KEY_LEFT_PIN) == 0:
    input()
    if high==1 and low==1:
        current_page=0
        high=0

try:
    while 1:
        page_manage()
        disp.LCD_ShowImage(image,0,0)


except:
    GPIO.cleanup()

