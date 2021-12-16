from bs4 import BeautifulSoup
import os

#html페이지들 list에 저장
dirPath = "/home/seny/crawling_github/crawling/crawling_html"
fileList = os.listdir(dirPath)


pageData = open("/home/seny/crawling_github/crawling/crawling_html/" + fileList[0], 'rt', encoding="utf-8").read()
soup = BeautifulSoup(pageData, features="html.parser")

data = []

for tag in soup.find_all('p'): #어떤 태그를 검색할 것인가....
    data.append(tag.get_text())

print(data)

'''
for page in fileList: 
    pageData = open(page, 'rt', encoding="utf-8").read()
    soup = BeautifulSoup(pageData, features="html.parser") #html을 soup객체로! 태그 추출 용이하도록
    
    
'''