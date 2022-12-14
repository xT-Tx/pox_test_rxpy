#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 11:13:22 2022

@author: nanjiang
"""

from pox.core import core
from pox.datapaths import do_launch
from pox.datapaths import SwitchLaunchedEvent

from pox.datapaths.pcap_switch import PCapSwitch
import reactivex
from reactivex import operators
from reactivex.scheduler import ThreadPoolScheduler
import random
import time
import multiprocessing

_switches = {}

def sleep_randomly(value):
    time.sleep(random.randint(1, 5)*0.5)
    return value
optimal_thread_count = multiprocessing.cpu_count()
pool_scheduler = ThreadPoolScheduler(optimal_thread_count-1)

class MultipleSwitchesTest (object):
    def __init__ (self):
      core.addListeners(self)
        
def launch (address = '127.0.0.1', port = 6633, max_retry_delay = 16,
    dpid = None, ports = '', extra = None, ctl_port = None,
    __INSTANCE__ = None):

  _ports = ports.strip()
  
  """
  Launch switches
  """
  def up (event):
    sw_list = ["S11", "S12", "S13", "S14", "S15"]
    for sw in sw_list:
        source = reactivex.of(sw).pipe(
            operators.map(lambda s: sleep_randomly(s)), 
            operators.subscribe_on(pool_scheduler)
            )
        source.subscribe(
            on_next = lambda i: action(i)
            )
        
  def action(state):
    ports = [p for p in _ports.split(",") if p]
    dpid = state[1:] # strip off 'S': "11", "12", "13"...
    sw = do_launch(PCapSwitch, address, port, max_retry_delay, dpid,
                    ports=ports, extra_args=extra,
                    magic_virtual_port_names = True)
    _switches[state] = sw
    
    core.raiseEvent(SwitchLaunchedEvent(), dpid)
      
  
  core.addListenerByName("UpEvent", up)
