#!/usr/bin/env python3

from konf import Konf
from os import system
from time import sleep
from transitions import Machine
import datetime

def parse_config(filename):
	k = Konf(filename)
	field_formats = {'lock command' : str, 'time to sleep': int, 'sleep length': int}
	return {name : k(name, format) for name, format in field_formats.items()}

class SleepyLocker(Machine):
	states = ['asleep', 'awake']

	def __init__(self, config):
		Machine.__init__(self, states=self.states, initial='awake', queued = True)
		self.add_transition('check', '*', 'asleep', conditions = 'is_sleepy_time')
		self.add_transition('check', '*', 'awake', unless = 'is_sleepy_time')

		self.lock_command = config['lock command']
		self.sleepy_start = datetime.time(hour = config['time to sleep'])
		self.sleepy_end = datetime.time(hour = config['time to sleep'] + config['sleep length'])
	
	def on_enter_asleep(self):
		system(self.lock_command)
		#print('asleep')
		sleep(3)
		self.check()

	def on_enter_awake(self):
		#print('awake')
		sleep(10)
		self.check()

	def is_sleepy_time(self):
		return self.sleepy_start <= datetime.datetime.now().time() <= self.sleepy_end


k = SleepyLocker(parse_config('config.yml'))
k.check();

