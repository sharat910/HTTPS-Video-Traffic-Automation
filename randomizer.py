import random

class Randomizer(object):
	"""docstring for Randomizer"""
	def __init__(self,videosource):
		super(Randomizer, self).__init__()
		if videosource == 'youtube':
			self.play_time_range = 300,900
			self.wait_time_range = 70,120
			self.res_range = 2,7
		elif videosource == 'facebook':
			self.play_time_range = 40,150
			self.wait_time_range = 40,100
		elif videosource == 'netflix':
			self.play_time_range = 300,900
			self.wait_time_range = 70,120
		else:
			raise 'Error: Incorrect video source'
	
	def get_play_time(self):
		return random.randint(*self.play_time_range)

	def get_wait_time(self):
		return random.randint(*self.wait_time_range)

	def get_resolution(self):
		return random.randint(*self.res_range)
