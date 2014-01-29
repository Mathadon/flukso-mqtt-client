#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Wouter Horré
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import paho.mqtt.client as paho
import time
import json
import sys

class Reading:

  def __init__(self, sensorid, type, timestamp, value, unit):
    self.sensorid = sensorid
    self.type = type
    self.timestamp = timestamp
    self.value = value
    self.unit = unit

def process_reading(reading):
  print("{} - {} ({}): {} {}".format(time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(reading.timestamp)), 
    reading.sensorid, reading.type, reading.value, reading.unit))

def on_message(client, userdata, msg):
  topicparts = msg.topic.split("/")
  p = json.loads(msg.payload.decode(encoding='UTF-8'))
  r = Reading(topicparts[2], topicparts[3], p[0], p[1], p[2])
  process_reading(r)


def on_connect(client, obj, rc):
  if rc == 0:
    print("Connected successfully.")
  client.subscribe("/sensor/+/+",0)


if __name__=="__main__":
  if len(sys.argv) < 2:
    print("Usage: {} <ip_of_flukso>".format(sys.argv[0]))
    exit(-1)
  client = paho.Client("test-client")
  client.on_connect = on_connect
  client.on_message = on_message
  client.connect(sys.argv[1])
  try:
    client.loop_forever()
  except KeyboardInterrupt:
    pass

