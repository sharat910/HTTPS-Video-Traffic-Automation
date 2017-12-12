import csv
import datetime

class Logger(object):
	"""docstring for Logger"""
	def __init__(self, filename):
		super(Logger, self).__init__()
		self.filename = filename
		file_handle = open(filename,"a",0)
		self.log_handle = open("%s.log" % filename.split(".")[0],"a",0)
		self.writer = csv.writer(file_handle, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
		self.writer.writerow(['Timestamp','Provider','Duration','Resolution'])

	def write(self,provider,duration,resolution):
		self.writer.writerow([str(datetime.datetime.now()),provider,duration,resolution])
	
	def log(self,message):
		self.log_handle.write("%s\t%s\n" % (str(datetime.datetime.now()),message))
		
if __name__ == '__main__':
	l = Logger("test.csv")
	for i in range(100):
		l.write('Youtube',"1m30s","720p")