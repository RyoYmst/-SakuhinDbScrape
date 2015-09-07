#coding:utf-8

from BeautifulSoup import BeautifulSoup
import urllib2
import urllib
import re
import codecs


def GetReviewNum(soup):
	data = []
	for i in soup.findAll("td",{"class":"center"}):
		data.append(i)
	return data[2].text

def GetTitle(soup):
	for i in soup.findAll("h1"):
		return i.find(itemprop = "name").text

def ExtractUrl():
	url = "http://sakuhindb.com/jmanga/HUNTERXHUNTER/"
	html = urllib2.urlopen(url)
	soup = BeautifulSoup(html)
	title = GetTitle(soup)
	review_num = GetReviewNum(soup)

	url_data = []
	url_data.append(url + "1.html#sort_review")
	page_num = soup.findAll("ul",{"id":"pagination-flickr"})#対象コミックの前ページ数
	for i in soup.findAll("ul",{"id":"pagination-flickr"}):
		for link in i.findAll("a"):
			url_data.append("http://sakuhindb.com" + link.get("href"))
	return url_data,title,review_num

def ExtractReview(all_url):
	review_text = []
	for i in range(0,1):
	# for i in range(0,len(all_url)):
		# print i
		html = urllib2.urlopen(all_url[i])
		soup = BeautifulSoup(html)
		for each_review in soup.findAll(itemprop = "reviewBody"):#.get_text()
			review_text.append(each_review.text)
	return review_text

def Output(title,review_num,review):
	print review
	write_data = codecs.open("masterthesis_review/"+ title +".txt","w","utf-8")
	write_data.write(review_num)
	for i in review:
		write_data.write(i)
	write_data.close()

def main():
	extract_url = ExtractUrl()#対象作品の全レビューページ
	extract_review = ExtractReview(extract_url[0])	
	Output(extract_url[1],extract_url[2],extract_review)
	
	



	

if __name__ == "__main__":
    main()
