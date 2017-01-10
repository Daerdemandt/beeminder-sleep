#!/usr/bin/env python3

from konf import Konf
from os import system
from time import sleep
from transitions import Machine

def parse_config(filename):
	k = Konf(filename)
	field_formats = {'lock command' : str, 'time to sleep': int, 'sleep length': int}
	return {name : k(name, format) for name, format in field_formats.items()}

config = parse_config('config.yml')

def is_sleepy_time():
	return False

class SleepyLocker(Machine):
	states = ['asleep', 'awake']

	def __init__(self, config):
		Machine.__init__(self, states=self.states, initial='awake', queued = True)
		self.add_transition('check', 'awake', 'asleep', conditions = 'is_sleepy_time')
		self.add_transition('check', 'asleep', 'awake', unless = 'is_sleepy_time')
		self.lock_command = config['lock command']
	
	def on_enter_asleep(self):
		#system(self.lock_command)
		print('asleep')
		sleep(1)
		self.check()

	def on_enter_awake(self):
		print('awake')
		sleep(1)
		self.check()

	def is_sleepy_time(self):
		return self.state == 'awake'


k = SleepyLocker(parse_config('config.yml'))
#k.lock();
k.check();

