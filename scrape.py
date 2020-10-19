import os
import re
import bs4
import time
import requests
import pprint

def load(url):
    res = requests.get(url)
    res.raise_for_status()

    return res.text

def pickup_tag(html, find_tag):
    soup = bs4.BeautifulSoup(str(html), 'html.parser')
    paragraphs = soup.find_all(find_tag)

    return paragraphs

def parse(html):
    soup = bs4.BeautifulSoup(str(html), 'html.parser')
    # htmlタグの排除
    kashi_row = soup.getText()
    kashi_row = kashi_row.replace('\n', '')
    kashi_row = kashi_row.replace('　', '')

    # 英数字の排除
    kashi_row = re.sub(r'[a-zA-Z0-9]', '', kashi_row)
    # 記号の排除
    kashi_row = re.sub(r'[ ＜＞♪`‘’“”・…_！？!-/:-@[-`{-~]', '', kashi_row)
    # 注意書きの排除
    kashi = re.sub(r'注意：.+', '', kashi_row)

    return kashi

def main():
    with open('yonedu_kashi.txt', 'a') as f:

        # アーティストページ(米津玄師)のアドレス
        url = 'https://www.uta-net.com/artist/12795/'

        # 曲ページの先頭アドレス
        base_url = 'https://www.uta-net.com'

        # ページの取得
        html = load(url)

        # 曲ごとのurlを格納
        musics_url = []
        # 歌詞を格納
        kashis = ''

        """ 曲のurlを取得 """
        # td要素の取り出し
        for td in pickup_tag(html, 'td'):
            # a要素の取り出し
            for a in pickup_tag(td, 'a'):
                # href属性にsongを含むか
                if 'song' in a.get('href'): 
                    # urlを配列に追加
                    musics_url.append(base_url + a.get('href'))


        """ 歌詞の取得 """
        for i, page in enumerate(musics_url):
            print('{}曲目:{}'.format(i + 1, page))
            html = load(page)
            for div in pickup_tag(html, 'div'):
                # id検索がうまく行えなかった為、一度strにキャスト
                div = str(div)
                # 歌詞が格納されているdiv要素か
                if r'itemprop="text"' in div:
                    # 不要なデータを取り除く
                    kashi = parse(div)
                    print(kashi, end = '\n\n')
                    # 歌詞を１つにまとめる
                    kashis += kashi + '\n'

                    # １秒待機
                    time.sleep(1)
                    break
        # 歌詞の書き込み
        f.write(kashis)

if __name__ == '__main__':
    main()
