import os
from datetime import datetime, timedelta
from urllib.parse import quote_plus,unquote
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

#파일이름 정해주는 함수
def convertFilename(orgnStr):
    restrictChars = "|\\\\?*<\":>/"
    regExpr = "[" + restrictChars + "]+"

    # 파일명으로 사용 불가능한 특수문자 제거
    tmpStr = orgnStr.replace(regExpr, "")
    tmpStr = orgnStr.replace("/", "_")

    # 공백문자 "_"로 치환
    return tmpStr.replace(" ", "_")


#링크 클릭 후 html파일 저장하는 함수
def Click_Pages(nodeHref, nodeTitle):
    try: #가끔씩 뜨는 페이지 커넥션 타임아웃에러 처리
        driver.get(nodeHref)
        driver.set_page_load_timeout(10)
        
    except TimeoutException:
        print(nodeTitle + "페이지 로드 실패 ")
        driver.back() #페이지 로드 실패 경우 전페이지로 돌아가기
    else:   
        clickHtml = driver.page_source
        fileName = nodeTitle + '.html'
        fileName = convertFilename(fileName)
        if not os.path.exists("crawling_html"): #크롤링html페이지들 저장할 폴더 없으면 만들기
            os.mkdir("crawling_html")
        html_file = open("./crawling_html/" + fileName, 'w')
        html_file.write(clickHtml)
        html_file.close()

    
#페이지 제목,내용,링크 txt파일 저장하는 함수
def Save_info(dList):
    InfoFile = convertFilename(date)
    topic = convertFilename(plusUrl)
    f = open('crawling{}.txt'.format(topic + InfoFile), 'w', encoding="UTF-8") #txt파일명을 "검색어 + 날짜"로 지정
    i = 0
    for i in range (0,len(dList)) :
        f.write(str(i+1) + ". " + dList[i]['nodeTitle'] + '\n' + dList[i]['nodeText'] + '\n' + dList[i]['nodeHref'] + '\n\n')
        i += 1




baseUrl = 'https://www.google.com/search?q='
t = datetime.today() - timedelta(1) #어제날짜
date = str(t.month) + '/' + str(t.day) + '/' + str(t.year)
dateurl = '&tbs=cdr:1,cd_min:' + date + ',cd_max:' + date
plusUrl = input('검색어 입력 : ')

url = baseUrl + quote_plus(plusUrl) + dateurl


options = webdriver.ChromeOptions()
options.add_argument('headless') #웹드라이버가 자동으로 브라우저를 제어하는 것을 칭을 열고 닫지 않으면서 가상으로 진행
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
driver = webdriver.Chrome(executable_path='/home/seny/chromedriver', options=options)
driver.get(url)
driver.implicitly_wait(3) #자바스크립트 돌아가는 시간
html = driver.page_source
soup = BeautifulSoup(html, features="html.parser")

#driver.execute_script("window.open();")
#driver.close() #활성화된 창만 닫음, selenium서비스가 메모리에 아직 상주, 재활용 가능
#위 코드 실행 시 모든 브라우저가 닫히므로 셀레니움 이용불가

pageList = [] #다음페이지들 링크 담아둘 리스트
dList = [] #크롤링 검색 (제목, 내용, 링크)set 저장 list

#쳣페이지에서 다음 페이지들 href리스트에 저장
aList = soup.select('a.fl') 
for node in aList:
    if node.attrs['href'].startswith("/search?q=") is True: #href가 "/search?q="로 시작 한다면 다음 페이지로 넘어가는 태그
        pageList.append(node.attrs['href']) #페이지 소스일 경우 모두 리스트에 저장


while True:
        
    #페이지 크롤링
    list = soup.select('div.g')
    
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
        except AttributeError as e: #링크가 none타입으로 나오는 경우 건너뜀
            continue
        
        data['nodeTitle'] = nodeTitle
        data['nodeText'] = nodeText
        data['nodeHref'] = nodeHref
        dList.append(data)#dictionary list 저장
        
        
    #다음페이지리스트 로드
    if len(pageList)!= 0: 
        nxtPage = 'https://www.google.com' + pageList[0]
        del pageList[0] #주소 저장한 후 해당 주소 리스트에서 삭제
        driver.get(nxtPage)
        driver.implicitly_wait(3) #자바스크립트 돌아가는 시간
        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")
        #driver.close() #탭 닫기
        #driver.execute_script("window.open();") #새창 열어놓고
    
    else: #다음페이지 없으면 while문 break
        break

#제목내용링크 txt파일에 저장
Save_info(dList)
#html페이지 별도 폴더에 저장
for page in range(0, len(dList)):
    Click_Pages(dList[page]['nodeHref'], dList[page]['nodeTitle'])
    

driver.quit()
