import time
import datetime
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from helper import get_soup
from randomizer import Randomizer

class Youtube(object):
	"""docstring for Youtube"""
	def __init__(self,driver,logger):
		super(Youtube, self).__init__()
		self.driver=driver
		self.logger = logger
		self.r = Randomizer('youtube')
		self.recursion_depth = 5

	def get_random_channel(self):
		#tech_users = ["marquesbrownlee","duncan33303","unboxtherapy","LinusTechTips"]
		pydata = ["PyDataTV","jacobschwarz"]
		user = random.choice(pydata)
		y = "https://www.youtube.com/user/%s/videos" % user
		return y

	def get_time_in_sec(self,time_string):
		tup = map(int,time_string.split(':'))
		if len(tup) == 2:
			return tup[0]*60+tup[1]
		else:
			return tup[0]*3600 + tup[1]*60 + tup[2]

	def get_video_url_time_list(self):
		channel_url = self.get_random_channel()
		soup = get_soup(channel_url)
		try:
			vid_grid = soup.find('ul',id='channels-browse-content-grid')
			vid_panes = vid_grid.find_all('li')
		except:
			if self.recursion_depth == 0:
				return ["https://m.youtube.com/watch?v=2MpUj-Aua48"]
			self.get_video_url_time_list()

		urls_times = []
		youtube_prefix = "https://www.youtube.com"
		for li in vid_panes:
			a = li.find('a')
			if a is None:
				continue
			href = a['href']
			time_string= li.find('span',{'class':'video-time'}).get_text()
			url = youtube_prefix + href
			t = self.get_time_in_sec(time_string)
			urls_times.append((url,t))
		return urls_times

	def disable_autoplay(self,driver):
		xpath = '//*[@id="autoplay-checkbox"]'
		self.driver.find_element_by_xpath(xpath).click()
		return


	def get_quality_button(self):
		elems = self.driver.find_elements_by_class_name('ytp-menuitem')
		elems = [x for x in elems if x.get_attribute('aria-haspopup')=='true']
		for elem in elems:
			x = elem.find_element_by_class_name('ytp-menuitem-label').text
			if x == 'Quality':
				return elem


	def select_resolution(self,res_level):
		try:
			sb = self.driver.find_element_by_css_selector('.ytp-button.ytp-settings-button')
			sb.click()
			time.sleep(1)
			qual = self.get_quality_button()			
			actions = webdriver.ActionChains(self.driver)
			actions.move_to_element(qual)
			actions.click()
			for i in range(res_level+1):
				actions.send_keys(Keys.UP)
			actions.send_keys(Keys.RETURN)
			actions.perform()
		except:
			if self.recursion_depth == 0:
				self.random_play()
			self.logger.log("Youtube: Resolution selection Failed")
			self.recursion_depth -=1
			time.sleep(5)
			self.select_resolution(res_level)
		return

	def fetch_current_resolution(self):
		try:
			sb = self.driver.find_element_by_css_selector('.ytp-button.ytp-settings-button')
			sb.click()
			time.sleep(1)
			qual = self.get_quality_button()
			res = qual.find_element_by_class_name('ytp-menuitem-content').text
			print "Resolution:",res
			# res = self.driver.find_element_by_xpath('//*[@id="movie_player"]/div[21]/div/div/div[5]/div[2]/div/span').text
			sb = self.driver.find_element_by_css_selector('.ytp-button.ytp-settings-button')
			sb.click()
			return res
		except:
			if self.recursion_depth == 0:
				self.random_play()
			self.logger.log("Youtube: Resolution fetch Failed")
			self.recursion_depth -=1
			time.sleep(3)
			self.fetch_current_resolution()
		

	def check_ad(self):
		try:
			self.driver.find_element_by_class_name('videoAdUiBottomBar')
		except:
			return
		# Get ad time
		try:
			time_elem = self.driver.find_element_by_class_name('ytp-time-duration')
			ts = time_elem.text
			self.logger.write('YoutubeAd',ts,'Auto')
			self.logger.log("Youtube: Playing Ad with resolution Auto for %s" % ts)
			time.sleep(self.get_time_in_sec(ts))
		except:
			if self.recursion_depth < 0:
				self.random_play()
			time.sleep(2)
			self.recursion_depth -=1
			self.check_ad()
		


	def play_video(self,url,time_sec,res_level):	
		self.driver.get(url)
		time.sleep(3)
		self.check_ad()
		#self.disable_autoplay(self.driver)
		self.select_resolution(res_level)
		time.sleep(2)
		res = self.fetch_current_resolution()
		play_time = min(self.r.get_play_time(),time_sec)
		time_str = "%dm,%ds" % (play_time/60,play_time%60)		
		self.logger.write('Youtube',time_str,res)
		self.logger.log("Youtube: Playing video with resolution %s for %s" % (res,time_str))
		time.sleep(play_time)

	def random_play(self):
		self.urls_times = self.get_video_url_time_list()
		while 1:
			self.recursion_depth = 5
			if random.random() < 0.2:
				self.urls_times = self.get_video_url_time_list()
			url,time_sec = random.choice(self.urls_times)
			self.play_video(url,time_sec,self.r.get_resolution())
			self.driver.get('chrome://settings/')
			wait_time = self.r.get_wait_time()
			self.logger.log("Youtube: Waiting for %dm,%ds" % (wait_time/60,wait_time%60))
			time.sleep(wait_time)