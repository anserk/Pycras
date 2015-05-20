from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import URLError
import re
from datetime import datetime, timedelta

class Post(object) :
	
	def __init__(self, post_id, location, category, title='', content='', email='', date='', status = 0):

		self.post_id = post_id
		self.url = ('https://{}.craigslist.org/{}/{}.html').format(location, category, post_id)
		self.location = location
		self.category = category
		self.title = title
		self.content = content
		self.email = email
		self.date = date
		self.status = status

		self.get_post()
		
	def get_post(self):

		# print(self.url)
		try:
			soup = BeautifulSoup(urlopen(self.url).read())
			self.title = soup.title.string

			#get the content of the post
			post_content = str(soup.find(id='postingbody')) #section', {'id':'postingbody'}).text)

			#remove repetions of <br> and [/br] at the end of the post
			post_content = re.sub(r'(<br>){2,}','', post_content, flags=re.IGNORECASE)
			post_content = re.sub(r'(</br>){2,}','', post_content, flags=re.IGNORECASE)
			self.content = post_content

			#get the reply email for the post, the info that I need are in another html page
			reply = soup.find(id='replylink')#'a', {'id':'replylink'})
			if reply is not None :
				reply_link = reply['href']
				reply_url = self.url[:self.url.find('.org/') + 4] + reply_link 
				reply_page = BeautifulSoup(urlopen(reply_url).read())
				self.email = reply_page.find('div', class_='anonemail').string # {'class':'anonemail'}).string 
				# self.email = format(reply_email)

		except URLError as error:
			# print(error)
			pass

	def get_location(self):
		return self.location

	def get_category(self):
		return self.category

	def get_title(self):
		return self.title

	def get_body(self):
		return self.content

	def get_email(self):
		return self.email

	def get_date(self):
		return self.date

	def __str__(self):
		return 'Title:{title}. Date:{date}. Email:{email}. Location:{location}. Category:{category}'.format(title= self.title, date= self.date, email= self.email, location= self.location, category= self.category)
