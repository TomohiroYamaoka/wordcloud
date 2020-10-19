from bs4 import BeautifulSoup
import urllib3

url = "http://www.nikkei.com/"

http = urllib3.PoolManager()
r = http.request('GET', url)

soup = BeautifulSoup(r.data, 'html.parser')

# タイトル要素を取得する → <title>経済、株価、ビジネス、政治のニュース:日経電子版</title>
title_tag = soup.title

# 要素の文字列を取得する → 経済、株価、ビジネス、政治のニュース:日経電子版
title = title_tag.string

# タイトル要素を出力
print(title_tag)

# タイトルを文字列を出力
print(title)