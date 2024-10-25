import pandas as pd
import json
import requests
import argparse
from pathlib2 import Path
from datetime import date
import os, sys

def get_article(year, start, end, next_year):
    start = str(date(year, start, 1))
    end = str(date(next_year, end, 1))
    like = []
    tags = []
    title = []
    url = []
    body = []
    created_at = []
    print(start, end)
    headers = {
              "Authorization": "Bearer " + "", #Qiitaに登録して、APIトークンを取得してここに書き込む
              }
    params = {"page": "1",
              "per_page":"100" }
    request_url = "https://qiita.com/api/v2/items" + "?query=created:>=" + start + " created:<"+ end
    r = requests.get(request_url, params=params, headers=headers, timeout=15.0)
    if r.status_code==200:
        total_page = int(r.headers.get("Total-Count"))//100+1
        jsondatas = json.loads(r.text)
        for parpage in range(2, total_page):
            print("残りページ{}".format(total_page-parpage))
            for article in jsondatas:
                like.append(article["likes_count"]) #いいね数
                tags.append(article["tags"]) # 記事のタグ
                title.append(article["title"]) # 記事タイトル
                url.append(article["url"]) # 記事url
                body.append(article["body"]) # 記事の内容
                #created_at.append(article["group"].value()[0])
            headers["page"] = str(parpage)
            r = requests.get(request_url, params=params, headers=headers, timeout=15.0)
            if r.status_code != 200:
                break
            jsondatas = json.loads(r.text)

        print("記事の取得が完了しました")
        articles = {"title":title, "url":url, "body":body, "tags":tags, "like":like,}
        for i,j in articles.items():
            print(len(i),len(j))
        articles = pd.DataFrame(articles)
        articles.to_csv(filepath.joinpath(f"Qiita{year}{start}to{end}.csv"))
    else:
        print("記事を取得することができませんでした", r.status_code)
    return

def main(year, start, end):
    next_year = 0
    if start > end:
        next_year = args.year + 1
    else:
        next_year = year
    get_article(year, start, end, next_year)      
    return 

if __name__ == '__main__':
    filepath = Path("data/Qiita/")
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int, help="type start year",)
    parser.add_argument("start", type=int, help="type start manth")
    parser.add_argument("end", type=int, help="type end manth",)
    args = parser.parse_args()
    year = args.year
    start_month = args.start
    end_month = args.end   
    main(year, start_month, end_month)
    