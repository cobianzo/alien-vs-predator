# This script works ok on its own, as long as the interpreter includes the dependencies.
# Scraps the 
# adapted from http://stackoverflow.com/questions/20716842/python-download-images-from-google-image-search
# usage:  
# > 	python3 scrap.py -s='alien' -n=4 -sk=0 -d=/Users/alvaroblancocobian/Downloads/temp 


# %%
import argparse
import json
import os
import re
import sys
from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup
from helpers import get_download_path

# %%
def get_soup(url,header):
	return BeautifulSoup(urlopen(Request(url,headers=header)),'html.parser')

# %%
def main(args):
	# %%
	# arguments cleanup
	parser = argparse.ArgumentParser(description='Scrape Google images')
	parser.add_argument('-s', '--search', default='bananas', type=str, help='search term')
	parser.add_argument('-n', '--num_images', default=10, type=int, help='num images to save')
	parser.add_argument('-sk', '--skip', default=0, type=int, help='num imgs to skip before accepting')
	parser.add_argument('-p', '--prefix', default='img', type=str, help='prefix string for every image file')
	parser.add_argument('-d', '--directory', default='/Users/gene/Downloads/', type=str, help='save directory')
	args 			= parser.parse_args()
	max_images 		= args.num_images
	skip_imgs 		= args.skip
	save_directory 	= args.directory
	prefix 			= args.prefix
	# TODO: if not args.directory use `get_download_path()`
	query 	= args.search #raw_input(args.search)
	query	= query.split()
	query	='+'.join(query)
	url		="https://www.google.es/search?safe=active&hl=es&authuser=0&tbm=isch&sxsrf=ALeKk03_T7yyskPOfqJDfpYUn41hhlaTVA%3A1603989752947&source=hp&biw=1440&bih=699&ei=-PCaX6CaN-TBlwS5-amICA&q="+query+"&oq=alien&gs_lcp=CgNpbWcQAzIECCMQJzIFCAAQsQMyBQgAELEDMgUIABCxAzIICAAQsQMQgwEyBQgAELEDMgUIABCxAzIFCAAQsQMyBQgAELEDMggIABCxAxCDAToCCABQqAxY9w9g8BFoAHAAeACAAVqIAZIDkgEBNZgBAKABAaoBC2d3cy13aXotaW1n&sclient=img&ved=0ahUKEwig9se7n9rsAhXk4IUKHbl8CoEQ4dUDCAc&uact=5"
	header	={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

	soup 	= get_soup(url,header)

	ActualImages=[] # contains the link of the preview img
	# print(soup.html)

	# Iteration html nodes, saving every image url
	for div in soup.find_all("div",{"class":"isv-r"}) : # div.isv-r is the container of the thumbnail
		imgs = div.find_all('img')
		if len(imgs) :
			img = imgs[0]
			if img.has_attr('data-src') : 
				ActualImages.append(img['data-src'])

	# iteration every image url, saving in computer
	for i , url_img in enumerate( ActualImages[0:max_images]):
		if ( i < skip_imgs ):
			continue
		try:
			req = Request(url_img, headers=header)
			response = urlopen(req)
			raw_img = urlopen(req).read()
			# if len(Type)==0:
			# The/Directory/img_i.jpg
			f = open(os.path.join(save_directory , prefix + "_"+ str(i)+".jpg"), 'wb')
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

# %%
if __name__ == '__main__':
    from sys import argv
    try:
        main(argv)
    except KeyboardInterrupt:
        pass
    sys.exit()

