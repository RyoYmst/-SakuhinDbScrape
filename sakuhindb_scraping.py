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

def ExtractData(all_url,image_url):
	data = []


	for url,image in zip(all_url,image_url)[6:7]:
		each_comic_data = {}
		html = urllib2.urlopen(url)
		soup = BeautifulSoup(html)
		title = GetTitle(soup)
		print title
		review_num = GetReviewNum(soup)
		each_comic_url = []
		
		each_comic_url.append(url + "1.html#sort_review")
		page_num = soup.findAll("ul",{"id":"pagination-flickr"})#対象コミックの前ページ数
		try:
			urllib.urlretrieve(image,"../masterthesis_image/" + title + ".jpg")#画像抽出//画質荒すぎて使えない
		except IOError:
			print "例外検出"

		for i in soup.findAll("ul",{"id":"pagination-flickr"}):
			for link in i.findAll("a"):
				each_comic_url.append("http://sakuhindb.com" + link.get("href"))
		each_comic_data["title"] = title
		each_comic_data["review_num"] = review_num
		each_comic_data["url"] = each_comic_url[:-1]#最後の値は次のページのURLなので無視
		data.append(each_comic_data)

	return data

def ExtractReview(data):
	all_review_text = []
	for each_comic_data in data:
		each_review_text = []
		for each_comic_url in each_comic_data["url"]:
			print each_comic_url
		 	html = urllib2.urlopen(each_comic_url)
			soup = BeautifulSoup(html)
			for each_review in soup.findAll(itemprop = "reviewBody"):#.get_text()
				#print each_review.text
				each_review_text.append(each_review.text)
		all_review_text.append(each_review_text)
	return all_review_text


def Output(data,reviews):
	for i,each_comic_data,each_comic_review in zip(range(0,len(data)),data,reviews):
		try:
			write_data = codecs.open("../masterthesis_review/"+ data[i]["title"] +".txt","w","utf-8")
			write_data.write(each_comic_data["review_num"]) 
			for text in each_comic_review:
				write_data.write(text)
			write_data.close()
		except IOError:
			print "例外検出"

def main():
	link_url = []
	image_url = []
	url = "http://sakuhindb.com/anime/j_manga_popular.html"
	html = urllib2.urlopen(url)
	soup = BeautifulSoup(html)
	
	for each_comic_data in soup.findAll("tr",{"class":"va_top"}):
		url_data  = each_comic_data.find("a")["href"]
		link_url.append("http://sakuhindb.com" + url_data)
	for each_comic_image in soup.findAll("span",{"class":"like_link"}):
		images = each_comic_image.findAll("img")
		for image in images:
			image_url.append(image["src"])

	extract_data = ExtractData(link_url,image_url)#対象作品の全レビューページ
	extract_review = ExtractReview(extract_data)
	Output(extract_data,extract_review)


if __name__ == "__main__":
    main()
