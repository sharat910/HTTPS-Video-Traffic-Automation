from selenium import webdriver
from multiprocessing import Process
from youtube import Youtube
from facebook import Facebook
from netflix import Netflix
from logger import Logger

def youtube_process(logger):
	driver = webdriver.Chrome("./chromedriver")
	y = Youtube(driver,logger)
	y.random_play()

def facebook_process(logger):
	driver = webdriver.Chrome("./chromedriver")
	f = Facebook(driver,logger)
	f.random_play()

def netflix_process(logger):
	driver = webdriver.Chrome("./chromedriver")
	f = Netflix(driver,logger)
	f.random_play()

if __name__ == '__main__':
	logger = Logger('video_palo_alto_verification.csv')
	for i in range(1):
		p = Process(target=youtube_process,args = (logger,))
		p.start()
		# p2 = Process(target=facebook_process,args = (logger,))
		# p2.start()
		# p3 = Process(target=netflix_process,args = (logger,))
		# p3.start()