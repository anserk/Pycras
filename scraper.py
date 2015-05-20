from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import URLError
import re
from datetime import datetime, timedelta
from Post import Post

def get_globals():

	try:
		config = {}
		exec(open('config.conf').read(), config)
		locations = config['locations']
		categories = config['categories']
		# output = '{}.html'.format(datetime.now().strftime('%Y%m%d%H%M'))
		return (locations, categories)

	except Exception as e:
		raise

def filter_by_date(ad_date):
	# I just care about the new posts of today.
	return datetime.now().date() == datetime.strptime(ad_date, '%Y-%m-%d %H:%M').date()

def get_posts(location, category):

	posts = []

	url = ('https://' + location + '.craigslist.org/search/' + category)
	try:
		soup = BeautifulSoup(urlopen(url).read())
	except URLError :
		raise

	#gets list of post ids
	ids = soup.find_all('p', class_= 'row')

	#remove nearby posts and old ones
	ids = (post for post in ids if filter_by_date(post.time['datetime']))
	ids = (post for post in ids if post.a['href'][0]=='/')

	for post in ids:
		posts.append(Post(post['data-pid'], location, category, date = post.time['datetime']))

	return posts 

def make_html(locations, categories, posts):
	from jinja2 import Environment, PackageLoader
	env = Environment(loader=PackageLoader('scraper', 'templates'))
	template = env.get_template('template.html')
	html_output = template.render(locations= locations, categories= categories, posts= posts)
	output_destination = '{}.html'.format(datetime.now().strftime('%Y%m%d%H%M'))

	with open(output_destination,'wb') as output:
		output.write(bytes(html_output, 'UTF-8'))

	
def main():

	locations, categories = get_globals()
	posts = []

	for location in locations :
		for category in categories :
			posts.extend(get_posts(location, category)) 

	#make ouput
	make_html(locations,categories,posts)

if __name__ == '__main__':
	main()
	# p = Post('51', 'asheville', 'sad')
	# print(p)