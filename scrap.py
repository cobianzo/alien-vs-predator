import argparse
import json
import os
import re
import sys
from urllib.request import Request, urlopen

import requests
from bs4 import BeautifulSoup

# adapted from http://stackoverflow.com/questions/20716842/python-download-images-from-google-image-search
# usage: 
# scrap.py -s='alien' -n=4 -d=/Users/alvaroblancocobian/Downloads/temp
def get_soup(url,header):
	return BeautifulSoup(urlopen(Request(url,headers=header)),'html.parser')


def main(args):
	parser = argparse.ArgumentParser(description='Scrape Google images')
	parser.add_argument('-s', '--search', default='bananas', type=str, help='search term')
	parser.add_argument('-n', '--num_images', default=10, type=int, help='num images to save')
	parser.add_argument('-d', '--directory', default='/Users/gene/Downloads/', type=str, help='save directory')
	args = parser.parse_args()
	query = args.search #raw_input(args.search)
	max_images = args.num_images
	save_directory = args.directory
	image_type="Action"
	# query= query.split()
	# query='+'.join(query)
	url="https://www.google.es/search?safe=active&hl=es&authuser=0&tbm=isch&sxsrf=ALeKk03_T7yyskPOfqJDfpYUn41hhlaTVA%3A1603989752947&source=hp&biw=1440&bih=699&ei=-PCaX6CaN-TBlwS5-amICA&q=alien&oq=alien&gs_lcp=CgNpbWcQAzIECCMQJzIFCAAQsQMyBQgAELEDMgUIABCxAzIICAAQsQMQgwEyBQgAELEDMgUIABCxAzIFCAAQsQMyBQgAELEDMggIABCxAxCDAToCCABQqAxY9w9g8BFoAHAAeACAAVqIAZIDkgEBNZgBAKABAaoBC2d3cy13aXotaW1n&sclient=img&ved=0ahUKEwig9se7n9rsAhXk4IUKHbl8CoEQ4dUDCAc&uact=5"
	header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
	soup = get_soup(url,header)
	ActualImages=[] # contains the link for Large original images, type of  image
	print(soup.html)
	for div in soup.find_all("div",{"class":"isv-r"}) :
		imgs = div.find_all('img')
		if len(imgs) :
			img = imgs[0]
			if img.has_attr('data-src') : 
				ActualImages.append(img['data-src'])
	# print(ActualImages)
	for i , url_img in enumerate( ActualImages[0:max_images]):
		try:
			req = Request(url_img, headers=header)
			response = urlopen(req)
			raw_img = urlopen(req).read()
			# if len(Type)==0:
			# The/Directory/img_i.jpg
			f = open(os.path.join(save_directory , "img" + "_"+ str(i)+".jpg"), 'wb')
			# else :
			# 	f = open(os.path.join(save_directory , "img" + "_"+ str(i)+"."+Type), 'wb')
			f.write(raw_img)
			f.close()
			print('\n\n\n')
			print(f)
			print('\n\n\n')
		except Exception as e:
			print("could not load : "+url_img)
			print(e)

if __name__ == '__main__':
    from sys import argv
    try:
        main(argv)
    except KeyboardInterrupt:
        pass
    sys.exit()
