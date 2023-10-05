from __future__ import print_function

import os
import re
import json
from dateutil.parser import parse
import time
from facebook_scraper import get_posts
from operator import itemgetter

from frontend import write_html

with open('./ACCESS_TOKEN', 'r') as f:
	EMAIL = f.readline().split('"')[1]
	PASSWORD = f.readline().split('"')[1]

def get_feed(page_id):
	# check last update time
	try:
		old_data = json.load(open('docs/{}.json'.format(page_id), 'r'))
		last_post_time = parse(old_data[0]['time'])
	except FileNotFoundError:
		old_data = []
		last_post_time = parse("1950-01-01 12:05:06")

	# scrape the page
	print('scraping:', page_id)
	posts = []
	for post in get_posts(page_id, pages=10, credentials=(EMAIL,PASSWORD), timeout=15):
		json_object = json.loads(json.dumps(post, indent = 4, default=str))
		post_time = parse(json_object['time'])
		if (post_time > last_post_time):
			posts.append(post)
		else:
			break	
			
	posts.extend(old_data)
	with open('docs/{}.json'.format(page_id), 'w') as f:
		print(json.dumps(posts, indent = 4, default=str), file=f)
	return posts


def remove_duplicates(data):
	uniq_data = []
	for item in data:
		if item not in uniq_data:
			uniq_data.append(item)

	return uniq_data

def data_prettify(data):
	for item in data:
		date = parse(item['time'])
		item['real_date'] = date.strftime('%d-%m-%Y')
		item['real_time'] = date.strftime('%I:%M%p')
	return data


def get_aggregated_feed(pages):
	"""
	Aggregates feeds give a list of pages and their ids.

	Input: A list of tuples
	Output: Combined list of posts sorted by timestamp
	"""
	data = list()
	for page_name, _id in pages:
		page_data = get_feed(_id)
		for data_dict in page_data:
			data_dict['source'] = page_name
		data.extend(page_data)

	data.sort(key=itemgetter('timestamp'), reverse=True)
	return data


if __name__ == "__main__":
	# Great thanks to https://gist.github.com/abelsonlive/4212647
	news_pages = json.load(open("./pages.json"))
	# for_later = ['Cultural-IIT-Kharagpur']

	data = get_aggregated_feed(news_pages)
	data = remove_duplicates(data)
	data_prettify(data)
	with open('docs/feed.json', 'w') as f:
		print(json.dumps(data, indent = 4, default=str), file=f)

	write_html(data, 'docs/index.html')

	localtime = str(time.asctime( time.localtime(time.time()) ))
	stamp="			<font size=2 color=\"white\"><div align=\"right\"><b>Last updated: "+localtime+" IST</b></div></font>\n"
	fn=open("docs/index.html","r+")
	fo=open("docs/indext.html","w")
	while (True):
  		abc=fn.readline()
  		fo.write(abc)
  		if not abc: break
  		if (abc[:30]=="			<!Time stamp here>"):	fo.write(stamp)
fn.close()
fo.close()
os.system("mv docs/indext.html docs/index.html")