import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from helper import get_soup
from randomizer import Randomizer
from logger import Logger

class Netflix(object):
	"""docstring for Netflix"""
	def __init__(self,driver,logger):
		super(Netflix, self).__init__()
		self.driver = driver
		self.r = Randomizer('netflix')
		self.logger = logger

	def login(self):
		try:
			self.driver.get("https://www.netflix.com/browse")
			user,password = open("credentials.txt","r").read().splitlines()
			user_xp = '//*[@id="appMountPoint"]/div/div[2]/div/div/form[1]/label/input'
			self.driver.find_element_by_xpath(user_xp).send_keys(user)
			pass_xp = '//*[@id="appMountPoint"]/div/div[2]/div/div/form[1]/div[1]/label/input'
			self.driver.find_element_by_xpath(pass_xp).send_keys(password)
			sign_xp = '//*[@id="appMountPoint"]/div/div[2]/div/div/form[1]/button'
			self.driver.find_element_by_xpath(sign_xp).click()
			hassan_xp = '//*[@id="appMountPoint"]/div/div/div[2]/div/div/ul/li[3]/div/a/div/div'
			self.driver.find_element_by_xpath(hassan_xp).click()
		except:
			self.logger.log("Netflix: Login Failed")
			time.sleep(2)
			self.login()
		time.sleep(4)

	def play_random_video(self): 
		self.driver.get("https://www.netflix.com/browse")
		time.sleep(3)
		pane_num = random.randint(1,4)
		vid_num = random.randint(1,4)
		vid_xp = '//*[@id="title-card-%d-%d"]/div/div[1]' % (pane_num,vid_num)
		try:
			self.driver.find_element_by_xpath(vid_xp).click()
			time.sleep(2)
			div = self.driver.find_element_by_class_name('jawBone')
			a_tag = div.find_elements_by_tag_name('a')[1]
			a_tag.click()
		except:
			self.logger.log("Netflix: Video playing Failed")
			self.driver.get("https://www.netflix.com/browse")
			time.sleep(3)
			self.play_random_video()
		play_time = self.r.get_play_time()
		time_str = "%dm,%ds" % (play_time/60,play_time%60)		
		self.logger.write('Netflix',time_str,'Auto')
		self.logger.log("Netflix: Playing video with resolution Auto for %s" % time_str)
		time.sleep(play_time)


	def random_play(self):
		self.login()
		while 1:
			self.play_random_video()
			wait_time = self.r.get_wait_time()
			self.driver.get("chrome://settings/")
			self.logger.log("Netflix: Waiting for %dm,%ds" % (wait_time/60,wait_time%60))
			time.sleep(wait_time)