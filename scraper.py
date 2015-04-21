from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import URLError
import re
from datetime import datetime, timedelta

categories = [] 
locations = [] 
output = '' 

def set_up_globals():

	try:
		config = {}
		exec(open('config.conf').read(), config)
		global locations
		locations = config['locations']
		global categories
		categories = config['categories']
		global output
		output = '{}.html'.format(datetime.now().strftime('%Y%m%d%H%M'))

	except Exception as e:
		exit()

def write_html(tag, text) :
	#simple function that makes html given tag and text as input
	with open(output, 'a', encoding='utf8') as f :

		#I am sorry about this but it will be fixed, later 
		if tag == 'a' :
			f.write('<a href="{}" target="_blank">Open the original post.</a>'.format(text))
		else:
			f.write('<{tag}>{text}</{tag}>'.format(tag = tag ,text = text))

def filter_by_date(ad_date) :
	# I just care about the new post for today.
	return datetime.now().date() == datetime.strptime(ad_date, '%Y-%m-%d %H:%M').date()

def get_posts(location, category) :

	url = ('https://' + location + '.craigslist.org/search/' + category)

	try:
		soup = BeautifulSoup(urlopen(url).read())
	except URLError :
		write_html('h4', 'INVALID {} or {}'.format(location.upper(), category.upper()))
		return
	# html = urlopen(url).read()
	

	#gets list of post ids
	posts = soup.find_all('p', {'class':'row'})

	full_category_name = soup.find('a', {'class':'reset'}).string
	write_html('h2', full_category_name)

	# if post is a new post then retrtive content
	for post in ( s for s in posts if filter_by_date(s.find('time')['datetime'])) :
		get_post('https://' + location + '.craigslist.org/' + category + '/' + post['data-pid'] + '.html')
	else:
		write_html('p', 'No more posts found.')
	
def get_post(url):
	try :
		soup = BeautifulSoup(urlopen(url).read())
		write_html('h3', soup.title.string)

		#get the content of the post
		post_content = str(soup.find('section', {'id':'postingbody'}).text)

		#remove repetions of <br> and [/br] at the end of the post
		post_content = re.sub(r'(<br>){2,}','', post_content, flags=re.IGNORECASE)
		post_content = re.sub(r'(</br>){2,}','', post_content, flags=re.IGNORECASE)

		#write html
		write_html('p', post_content)

		#get the reply email for the post, the info that I need are in another html page
		reply = soup.find('a', {'id':'replylink'})
		if reply is not None :
			reply_link = reply['href']
			reply_url = url[:url.find('.org/') + 4] + reply_link 
			reply_page = BeautifulSoup(urlopen(reply_url).read())
			reply_email = reply_page.find('div', {'class':'anonemail'}).string 
			write_html('p', 'Reply at: {}'.format(reply_email))
		
		write_html('a', url)
		write_html('hr','')
		
	except URLError as error:
		return
	
def main() :

	set_up_globals()

	for location in locations :
		write_html('h1',location)
		for category in categories :
			get_posts(location, category) 


if __name__ == '__main__':
	main()