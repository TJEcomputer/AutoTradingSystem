
# 모듈 import
import multiprocessing
import time
import urllib.request
import urllib.parse
import datetime
import os
from bs4 import BeautifulSoup
from web import csvcsv
from web import log_recorder

#종목 리스트 가져오기
logger = log_recorder.recorder_time("popo")
def code_list():
    code_num = []
    code_li = csvcsv.csv_reader("code.csv")
    for i in range(1,len(code_li)):
        code_num.append(code_li[i][0])
    return code_num

#종목 리스트 생성
code_li = code_list()

#
def get_link(code):
    web_url = "https://finance.naver.com/item/sise_day.nhn?code="+str(code)+"&page=1"
    with urllib.request.urlopen(web_url) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        tt = soup.find("table",{'class':'Nnavi'}).find_all("a")
        link = str(tt[-1]["href"])
        ln_li = link.split('=')
        last_page = int(ln_li[-1]) + 1
    return last_page

def check_data(code):
    date_data = []
    if os.path.isfile("../DB/CSV/"+code + ".csv"):
        daily_data_list = csvcsv.csv_reader(code + ".csv")

        for daily_data in daily_data_list:
            date_data.append(daily_data[0])
        return date_data
    else:
        date_data = []
        return date_data

#웹 크롤링
def get_data(code):
    # 파일에 컬럼명 입력 명령
    # col = ["date","close","prev","start","high","low","volume"]
    # csvcsv.csv_writer_w("20200820\\"+code+".csv", col)

    #마지막 페이지 수
    # get_link
    # web_url = "https://finance.naver.com/item/sise_day.nhn?code="+str(code)+"&page=1"
    # with urllib.request.urlopen(web_url) as response:
    #     html = response.read()
    #     soup = BeautifulSoup(html, 'html.parser')
    #     tt = soup.find("table",{'class':'Nnavi'}).find_all("a")
    #     link = str(tt[-1]["href"])
    #     ln_li = link.split('=')
    #     last_page = int(ln_li[-1])+1

    # get_link() 메소드로 각 종목 마지막 페이지 return
    last_page = get_link(code)
    start = datetime.datetime.now()
    nt_st = start.strftime("%H:%M:%S")
    logger.info(str(code) + " 시작 " + nt_st)
    date_data = check_data(str(code))
    for i in range(1,last_page):
        start = datetime.datetime.now()
        nt_st = start.strftime("%H:%M:%S")
        print(str(code) + " 시작 " + nt_st + " - " + str(i)+"  page")
        web_url = "https://finance.naver.com/item/sise_day.nhn?code="+str(code)+"&page="+str(i)
        with urllib.request.urlopen(web_url) as response:
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            tt = soup.find_all('span')
            del tt[0]
            lplp = []
            for i in range(len(tt)):
                chch = str(tt[i].get_text()).strip()
                lplp.append(chch)

            for i in range(1,10):

                lplp1 = lplp[:7]
                del lplp[0:7]
                # 기존에 저장되어 있는 데이터셋에 데이터가 없으면 기록
                if str(lplp1[0]) in date_data:
                    print("데이터가 있습니다.")
                else:
                    csvcsv.csv_writer_a(code+".csv",lplp1)
    nt_st = start.strftime("%H:%M:%S")
    logger.info(code + " 완료 " + nt_st)

if __name__ == "__main__":
    start = time.time()
    pool =multiprocessing.Pool(processes=6) #최대 8개
    pool.map(get_data, code_li)
    pool.close()
    pool.join()
    end = time.time()
    spent = end - start
    logger.info("Update Code complete" + " - " + str(spent) + " secs")
    logger.info("크롤링 완료")

    # date = check_data("000020")
    # print(date)