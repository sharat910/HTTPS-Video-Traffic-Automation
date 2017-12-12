import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from helper import get_soup
from randomizer import Randomizer

class Facebook(object):
	"""docstring for Facebook"""
	def __init__(self,driver,logger):
		super(Facebook, self).__init__()
		self.driver = driver
		self.int_to_res = {1:'240p',2:'360p',3:'480p',4:'720p'}
		self.r = Randomizer('facebook')
		self.logger = logger
		self.error_count = 0

	def get_random_url(self):
		prefix = 'https://www.facebook.com/facebook/videos/'
		vid_ids = ['10155484162461729/','10155656407651729/','10155278547321729/',
		'10154835146021729/','10154729016861729/','10154553970951729/','10154249775416729/']
		return prefix + random.choice(vid_ids)

	# def select_resolution(self,res):
	# 	xp = '//*[@id="u_0_d"]/div/div[2]/div/div/div[3]/div[3]/button'
	# 	elem = self.driver.find_element_by_xpath(xp)
	# 	actions = webdriver.ActionChains(self.driver)
	# 	actions.move_to_element(elem)
	# 	xpath = '//*[@id="u_0_d"]/div/div[2]/div/div/div[3]/div[3]/div/div/div[1]/a[%d]' % (6-res)
	# 	res_elem = self.driver.find_element_by_xpath(xpath)
	# 	# res_elem.click()
	# 	actions.move_to_element(res_elem)
	# 	actions.click()
	# 	actions.perform()

	def get_video_length(self):
		time.sleep(1)
		xp = '//*[@id="u_0_d"]/div/div[2]/div/div/div[2]/div/div/div'
		try:
			elem = self.driver.find_element_by_xpath(xp)
			val = elem.get_attribute("aria-valuemax")
		except:
			self.logger.log("Facebook: Video length fetch failed")
			val=9999
		return int(float(val))

	def play_video(self,url):
		try:
			self.driver.get(url)
			try:
				time.sleep(4)
				self.driver.find_element_by_id('u_0_7').click()
			except:
				pass
			time.sleep(1)
			self.driver.find_element_by_id('u_0_f').click()			
		except:
			self.logger.log("Facebook: Video playing Failed")
			if self.recursion_depth == 0:
				self.random_play()
			self.recursion_depth -= 1
			time.sleep(2)
			self.play_video(self.get_random_url())
		time.sleep(1)
		#self.select_resolution(res)
		vid_len = self.get_video_length()
		rn_pl_tm = self.r.get_play_time()
		play_time = min(vid_len,rn_pl_tm)
		time_str = "%dm,%ds" % (play_time/60,play_time%60)		
		self.logger.write('Facebook',time_str,'Auto')
		self.logger.log("Facebook: Playing video with resolution Auto for %s" % time_str)
		time.sleep(play_time)

	def random_play(self):
		while 1:
			self.recursion_depth = 5		
			url = self.get_random_url()
			#res = self.r.get_resolution()
			self.play_video(url)
			self.driver.get('chrome://settings/')
			wait_time = self.r.get_wait_time()
			self.logger.log("Facebook: Waiting for %dm,%ds" % (wait_time/60,wait_time%60))
			time.sleep(wait_time)