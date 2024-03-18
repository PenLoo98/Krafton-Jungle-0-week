import random
import requests

from bs4 import BeautifulSoup
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbjungle                      # 'dbjungle'라는 이름의 db를 만듭니다.


def insert_all():
    # URL을 읽어서 HTML를 받아오고,
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://movie.daum.net/ranking/boxoffice/yearly', headers=headers)

    # HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
    soup = BeautifulSoup(data.text, 'html.parser')

    # select를 이용해서, li들을 불러오기
    movies = soup.select('#daumWrap > #daumContent > #cMain > #mArticle > .inner_article > .g_comp > #morColl > .coll_cont > .mg_cont > ol > li')
    print(len(movies))

    # movies (li들) 의 반복문을 돌리기
    for movie in movies:
        # 영화 제목 추출
        tag_element = movie.select_one('div.wrap_cont > div.info_tit > a')
        if not tag_element:
            continue
        title = movie.select_one('div.wrap_cont > div.info_tit > a').text.replace(' ','')


        # 영화 개봉 년도/월/일을 추출하기
        tag_element = movie.select_one('div.wrap_cont > dl.dl_comm > dd.cont')
        if not tag_element:
            continue
        open_date = movie.select_one('div.wrap_cont > dl.dl_comm > dd.cont').text
        open_date_split = open_date.split(".")
        open_year = open_date_split[0]
        open_month = open_date_split[1]
        open_day = open_date_split[2]


        # 누적 관객수를 얻어낸다. "783,567명" 과 같은 형태가 된다.
        tag_element = movie.select('div.wrap_cont > dl.dl_comm > dt.tit_base')
        if not tag_element:
            continue
        for row in tag_element:
            if(row.text=="누적"):
                if(movie.select('div.wrap_cont > dl.dl_comm > dd.cont')[1].text):
                    viewers = movie.select('div.wrap_cont > dl.dl_comm > dd.cont')[1].text
                else:
                    viewers = "미 집계"
        

        # 영화 포스터 이미지 URL 을 추출한다.
        tag_element = movie.select_one('div.wrap_thumb > a > .thumb_img')
        if not tag_element:
            continue
        poster_url = tag_element["data-original-src"]
        if not poster_url:
            continue


        # 영화 정보 URL 을 추출한다.
        tag_element = movie.select_one('div.wrap_thumb > a')
        if not tag_element:
            continue
        info_url = 'https://search.daum.net/search' + tag_element['href']
        if not info_url:
            continue

        # # 존재하지 않는 영화인 경우만 추가한다.
        # found = list(db.movies.find({'title': title}))
        # if found:
        #     continue

        # 좋아요를 random 으로 정한다 [0, 100)
        likes = random.randrange(0, 100)

        doc = {
            'title': title,
            'open_year': open_year,
            'open_month': open_month,
            'open_day': open_day,
            'viewers': viewers,
            'poster_url': poster_url,
            'info_url': info_url,
            'likes': likes,
            'trashed': False,
        }
        db.movies.insert_one(doc)
        print('완료: ', title, open_year, open_month, open_day, viewers, poster_url, info_url)


if __name__ == '__main__':
    # 기존의 movies 콜렉션을 삭제하기
    db.movies.drop()

    # 영화 사이트를 scraping 해서 db 에 채우기
    insert_all()