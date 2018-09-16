#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

# GPIO
TRIG = 23 
ECHO = 24
RED = 26
AMBER = 19
GREEN = 13


# Calibration
OVERFILL = 30
EMPTY = 23
FULL = 6

def init():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(TRIG,GPIO.OUT)
  GPIO.setup(ECHO,GPIO.IN)

  GPIO.setup(RED,GPIO.OUT)
  GPIO.setup(AMBER,GPIO.OUT)
  GPIO.setup(GREEN,GPIO.OUT)

  GPIO.output(RED, False)
  GPIO.output(AMBER, False)
  GPIO.output(GREEN, False)
  

def get_distance():
  GPIO.output(TRIG, False)
  time.sleep(1)
  
  GPIO.output(TRIG, True)
  time.sleep(0.00001)
  GPIO.output(TRIG, False)
  
  count = 0
  limit = 60
  pulse_start = time.time()
  while GPIO.input(ECHO)==0:
    pulse_start = time.time()
    count += 1
    if count > limit:
      raise Exception('Ping Exception')
  
  count = 0
  pulse_end = time.time()
  while GPIO.input(ECHO)==1:
    pulse_end = time.time()
    count += 1
    if count > limit:
      raise Exception('Pong Exception')
  
  pulse_duration = pulse_end - pulse_start
  
  distance = pulse_duration * 17150
  
  distance = round(distance, 2)
  return distance

def get_average( distance_list, precision=0 ):
  size = len(distance_list)
  total = 0
  for i in range(0, size):
    total += distance_list[i]

  average = total / size
  return round(average, precision)

def set_red():
  GPIO.output(RED, True)
  GPIO.output(AMBER, False)
  GPIO.output(GREEN, False)

def set_amber():
  GPIO.output(RED, False)
  GPIO.output(AMBER, True)
  GPIO.output(GREEN, False)

def set_green():
  GPIO.output(RED, False)
  GPIO.output(AMBER, False)
  GPIO.output(GREEN, True)

def set_overfill():
  GPIO.output(RED, True)
  GPIO.output(AMBER, True)
  GPIO.output(GREEN, True)

def set_lights( distance ):
  level_range = EMPTY - FULL
  level_umid = (level_range * 0.3) + FULL
  level_lmid = EMPTY - (level_range * 0.3)

  if distance < level_umid:
    set_green()
    return

  if distance < level_lmid:
    set_amber()
    return

  if distance > OVERFILL:
    set_overfill()
    return 

  set_red()
  

def main():
  distance_list = []
  rolling_width = 5

  while True:
    try:
      distance = get_distance() 
      distance_list.insert(0, distance)
      distance_list = distance_list[:rolling_width]
      average = get_average(distance_list)
      print average
      set_lights(average)
    except Exception as error:
      print error
      

init()  
main()
  
