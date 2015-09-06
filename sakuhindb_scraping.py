#coding:utf-8

from BeautifulSoup import BeautifulSoup
# import sys
import urllib2
# import unicodedata
# import re
# import codecs


def ExtractUrl():
	url = "http://sakuhindb.com/jmanga/HUNTERXHUNTER/"
	html = urllib2.urlopen(url)
	soup = BeautifulSoup(html)
	url_list = []
	url_list.append(url + "1.html#sort_review")
	page_num = soup.findAll("ul",{"id":"pagination-flickr"})#対象コミックの前ページ数
	for i in soup.findAll("ul",{"id":"pagination-flickr"}):
		for link in i.findAll("a"):
			url_list.append("http://sakuhindb.com" + link.get("href"))
	return url_list


def ExtractReview(all_url):
	review_text = []
	html = urllib2.urlopen(all_url[0])
	soup = BeautifulSoup(html)
	for each_review in soup.findAll(itemprop = "reviewBody"):#.get_text()
		review_text.append(each_review.text)
	return review_text


def main():
	extract_url = ExtractUrl()#対象作品の全レビューページ
	extract_review = ExtractReview(extract_url)
	for i in extract_review:
		print i
    

	

if __name__ == "__main__":
    main()
