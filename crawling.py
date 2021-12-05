#제목, 내용, 링크 txt파일 구현
#html파일저장 파일 구현
from datetime import datetime, timedelta
from urllib.parse import quote_plus,unquote
from bs4 import BeautifulSoup
from selenium import webdriver
#from selenium.webdriver.support.ui import WebDriverWait

#파일이름 정해주는함수
def convertFilename(orgnStr):
    restrictChars = "|\\\\?*<\":>/"
    regExpr = "[" + restrictChars + "]+"

    # 파일명으로 사용 불가능한 특수문자 제거
    tmpStr = orgnStr.replace(regExpr, "")
    tmpStr = orgnStr.replace("/", "_")

    # 공백문자 "_"로 치환
    return tmpStr.replace(" ", "_")


#링크 클릭 후 html문서 txt파일에 저장함수
def Click_Pages(nodeHref, nodeTitle):
        driver.get(nodeHref)    
        driver.implicitly_wait(3)
        clickHtml = driver.page_source
        fileName = nodeTitle + '.html'
        fileName = convertFilename(fileName)
        html_file = open('/home/seny/crawling_href/' + fileName, 'w')
        html_file.write(clickHtml)
        html_file.close()

#첫번째 페이지 제외하고 n째 페이지 html문서 txt저장함수
def Click_PagesN(nodeHref, nodeTitle):
    driverN.get(nodeHref)
    driverN.implicitly_wait(3)
    clickHtml = driverN.page_source

    fileName = nodeTitle + '.html'
    fileName = convertFilename(fileName)
    html_file = open('/home/seny/crawling_href/' + fileName, 'w')
    html_file.write(clickHtml)
    html_file.close()

    
#페이지 제목,내용,링크 crawling날짜.txt파일로 저장함수
def Save_info(dList):
    InfoFile = convertFilename(date)
    f = open('crawling{}.txt'.format(InfoFile), 'w', encoding="UTF-8")
    i = 0
    for i in range (0,len(dList)) :
        f.write(dList[i]['nodeTitle'] + '\n' + dList[i]['nodeText'] + '\n' + dList[i]['nodeHref'] + '\n')
        i += 1




baseUrl = 'https://www.google.com/search?q='
t = datetime.today() - timedelta(1) #어제날짜
date = str(t.month) + '/' + str(t.day) + '/' + str(t.year)
dateurl = '&tbs=cdr:1,cd_min:' + date + ',cd_max:' + date
plusUrl = input('검색어 입력 : ')

url = baseUrl + quote_plus(plusUrl) + dateurl #https://www.google.com/search?q=%EC%9D%B4%EC%84%B8%EC%9D%80&tbs=cdr:1,cd_min:11/21/2021,cd_max:11/21/2021


options = webdriver.ChromeOptions()
options.add_argument('headless') #웹드라이버가 자동으로 브라우저를 제어하는 것을 칭을 열고 닫지 않으면서 가상으로 진행
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
driver = webdriver.Chrome(executable_path='/home/seny/chromedriver', options=options)
driver.get(url)
driver.implicitly_wait(3) #자바스크립트 돌아가는 시간

html = driver.page_source
soup = BeautifulSoup(html, features="html.parser")


driverN = webdriver.Chrome(executable_path='/home/seny/chromedriver', options=options) #두 번째 페이지부터 n페이지까지 쓰이는 드라이버
nxtPageHref = None #그 다음 페이지 링크
pageList = []
nxtPage = " " #isspace()확인 하려면 공백한자리 필요
dList = [] #크롤링 검색 (제목, 내용, 링크)set 저장 list

#쳣페이지에서 다음 페이지들 href리스트에 저장
aList = soup.select('a.fl') 
for node in aList:
    if node.attrs['href'].startswith("/search?q=") is True: #href가 "/search?q="로 시작 한다면 다음 페이지로 넘어가는 태그
        pageList.append(node.attrs['href']) #페이지 소스일 경우 모두 리스트에 저장


while True:

    
    #첫번째 페이지 제외한 n페이지
    if nxtPage.isspace() is False:
        list = soupN.select('div.g')
        IsFirstPage = False
        
    else: #첫 페이지
        list = soup.select('div.g')
        IsFirstPage = True
    
    
    #페이지 크롤링
    
    for i in list:
        data = {} #dict
        try: #가끔 나오는 nonetype반환에러 막기
            nodeTitle = i.select_one('h3.LC20lb').text #제목
        except AttributeError as e:
            nodeTitle = ''
            
        try:
            nodeText = i.select_one('div.IsZvec').text #내용
        except AttributeError as e:
            nodeText = ''
            
        try:
            nodeHref = unquote(i.a.attrs['href']) #주소
        except AttributeError as e:
            nodeHref = ''
        
        data['nodeTitle'] = nodeTitle
        data['nodeText'] = nodeText
        data['nodeHref'] = nodeHref
        dList.append(data)#dictionary list 저장
        
        #html페이지 별도 폴더에 저장
        if IsFirstPage is False:
            Click_PagesN(nodeHref, nodeTitle)
        else:
            Click_Pages(nodeHref, nodeTitle)
    
    
        
    if len(pageList)!= 0: #저장해둔 다음페이지리스트 로드
        nxtPage = 'https://www.google.com' + pageList[0]
        del pageList[0] #주소 저장한 후 해당 주소 리스트에서 삭제
        driverN.get(nxtPage)
        driverN.implicitly_wait(3) #자바스크립트 돌아가는 시간
        htmlN = driverN.page_source
        soupN = BeautifulSoup(htmlN, features="html.parser")
    
    else: #다음페이지 없으면 while문 break
        break


Save_info(dList)
    

driver.close()
driverN.close()
