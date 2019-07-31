''' 第3章: 正規表現
Wikipediaの記事を以下のフォーマットで書き出したファイルjawiki-country.json.gzがある．
・1行に1記事の情報がJSON形式で格納される
・各行には記事名が"title"キーに，記事本文が"text"キーの辞書オブジェクトに格納され，
  そのオブジェクトがJSON形式で書き出される
・ファイル全体はgzipで圧縮される
以下の処理を行うプログラムを作成せよ．
'''
import gzip
import json
import re
from pprint import pprint


def json_data(*titles):
    ''' 記事ジェネレータ '''
    with gzip.open('jawiki-country.json.gz', 'rt') as f:
        for line in f:
            article = json.loads(line)
            if titles:
                if article['title'] in titles:
                    yield article
            else:
                yield article


def info2dict(article):
    ''' 基本情報を辞書化 '''
    from collections import OrderedDict
    # re.DOTALL '.'に改行も含める
    info = re.search(r'^\{\{基礎情報.*?\}\}$', article, re.MULTILINE + re.DOTALL)
    if info:
        # print(info.group())
        info_dict = OrderedDict()
        # a(?=b) 肯定的先読み(直後にbがあるa, bは含まない)
        data = re.finditer(r'\|\s*(.*?) ?= ?(.*?)(?:(?=\n\|)|(?=\|\n)|(?=\n\})|(?=\}\}$))',
                           info.group(), re.DOTALL)
        for match in data:
            field, value = match.groups()
            info_dict[field] = value
        return info_dict


def main():
    ''' 20. JSONデータの読み込み
    Wikipedia記事のJSONファイルを読み込み，「イギリス」に関する記事本文を表示せよ．
    問題21-29では，ここで抽出した記事本文に対して実行せよ．
    '''
    for article in json_data():
        if article['title'] == 'イギリス':
            print(article['text'])
            break


def main():
    ''' 21. カテゴリ名を含む行を抽出
    記事中でカテゴリ名を宣言している行を抽出せよ．
    '''
    pattern = re.compile(r'^\[\[Category:.*\]\].*$', re.MULTILINE)
    for article in json_data():
        print(f'----- {article["title"]} -----')
        categories = pattern.finditer(article['text'])
        {print(c.group()) for c in categories}
        print()


def main():
    ''' 22. カテゴリ名の抽出
    記事のカテゴリ名を（行単位ではなく名前で）抽出せよ．
    '''
    # () キャプチャ対象, (?:) キャプチャ対象外, .*? 最短一致
    pattern = re.compile(r'^\[\[Category:(.*?)(?:\|.*)?\]\].*$', re.MULTILINE)
    for article in json_data():
        print(f'----- {article["title"]} -----')
        categories = pattern.finditer(article['text'])
        {print(c.group(1)) for c in categories}
        print()


def main():
    ''' 23. セクション構造
    記事中に含まれるセクション名とそのレベル（例えば"== セクション名 =="なら1）を表示せよ．
    '''
    # "={2,}" 2個以上の'=', "\1" 1番目のキャプチャ対象と同じ内容, "\s" 空白文字[ \t\n\r\f]
    pattern = re.compile(r'^(={2,})\s*(.+?)\s*\1$', re.MULTILINE)
    for article in json_data():
        print(f'------ {article["title"]} -----')
        for match in pattern.finditer(article['text']):
            level = len(match.group(1)) - 1
            name = match.group(2)
            print(f'{"  " * (level - 1)}{level}.{name}')
        print()


def main():
    ''' 24. ファイル参照の抽出
    記事から参照されているメディアファイルをすべて抜き出せ．
    '''
    pattern = re.compile(r'(?:File|ファイル):(.*?)\|', re.MULTILINE)
    for article in json_data():
        print(f'----- {article["title"]} -----')
        files = pattern.finditer(article['text'])
        {print(f.group(1)) for f in files}
        print()


def main():
    ''' 25. テンプレートの抽出
    記事中に含まれる「基礎情報」テンプレートのフィールド名と値を抽出し，辞書オブジェクトとして格納せよ．
    '''
    for article in json_data('イギリス', 'カナダ', '南オセチア'):
        print(f'----- {article["title"]} -----')
        d = info2dict(article['text'])
        pprint(d)


def main():
    ''' 26. 強調マークアップの除去
    25の処理時に，テンプレートの値からMediaWikiの強調マークアップ（弱い強調，強調，強い強調のすべて）
    を除去してテキストに変換せよ（参考: マークアップ早見表）．
    '''
    emphasis_p = re.compile(r'(\'{2,5})(.+?)\1')
    for article in json_data('イギリス', 'カナダ', '南オセチア'):
        print(f'----- {article["title"]} -----')
        d = info2dict(article['text'])
        if not d:
            continue
        for key in d.keys():
            for match in emphasis_p.finditer(d[key]):
                print(match.group(), match.group(2))
                d[key] = d[key].replace(match.group(), match.group(2))
        # pprint(d)


def main():
    ''' 27. 内部リンクの除去
    26の処理に加えて，テンプレートの値からMediaWikiの内部リンクマークアップを除去し，
    テキストに変換せよ（参考: マークアップ早見表）．
    '''
    emphasis_p = re.compile(r'(\'{2,5})(.+?)\1')
    # (?<!a)b 否定的後読み（直前にaがないb, aは含まない）
    # b(?!a) 否定的先読み(直後にaがないb, aは含まない)
    link_p = re.compile(
        r'(?<!#REDIRECT )\[\[(?!Category)(?:[^|]*\|)??([^|]+?)\]\]')
    for article in json_data('イギリス', 'カナダ', '南オセチア'):
        print(f'----- {article["title"]} -----')
        d = info2dict(article['text'])
        if not d:
            continue
        for key in d.keys():
            d[key] = emphasis_p.sub(r'\2', d[key])  # 26
            # 27
            for match in link_p.finditer(d[key]):
                print(match.group(), match.group(1))
                d[key] = d[key].replace(match.group(), match.group(1))
        # pprint(d)


def main():
    ''' 28. MediaWikiマークアップの除去
    27の処理に加えて，テンプレートの値からMediaWikiマークアップを可能な限り除去し，
    国の基本情報を整形せよ．
    '''
    import html
    emphasis_p = re.compile(r'(\'{2,5})(.+?)\1')
    boxbrackets_p = re.compile(r'\[\[(?:[^|]*\|)*?([^|]+?)\]\]')
    braces_p = re.compile(r'\{\{(?:[^|]*\|)*?([^|]+?)\}\}')
    link_p = re.compile(r'\[(http[^\s]*?\s)?(.*?)\]')
    tag_p = re.compile(r'<.*?>')

    for article in json_data('イギリス', 'カナダ', '南オセチア', 'ドイツ', 'ソマリア'):
        # for article in json_data():
        print(f'----- {article["title"]} -----')
        d = info2dict(article['text'])
        if not d:
            continue
        for key in d.keys():
            d[key] = emphasis_p.sub(r'\2', d[key])  # 26（強調）
            # [[?|?|...|?]]
            for match in boxbrackets_p.finditer(d[key]):
                # print(match.group(), match.group(1))
                d[key] = d[key].replace(match.group(), match.group(1))
            # {{?|?|...|?}}
            for match in braces_p.finditer(d[key]):
                # print(match.group(), match.group(1))
                d[key] = d[key].replace(match.group(), match.group(1))
            # 外部リンク [http...], [http... xxx]
            for match in link_p.finditer(d[key]):
                # print(match.group())
                # print(len(match.groups()), match.groups())
                d[key] = d[key].replace(match.group(), match.group(2).strip())
            # タグ
            for match in tag_p.finditer(d[key]):
                # print(match.group())
                d[key] = d[key].replace(match.group(), '')
            # 文字参照
            d[key] = html.unescape(d[key])
        pprint(d)


def main():
    ''' 29. 国旗画像のURLを取得する
    テンプレートの内容を利用し，国旗画像のURLを取得せよ．
    （ヒント: MediaWiki APIのimageinfoを呼び出して，ファイル参照をURLに変換すればよい）
    '''
    import requests
    import json
    # for article in json_data('イギリス', 'カナダ', '南オセチア', 'ドイツ', 'ソマリア'):
    for article in json_data():
        print(f'----- {article["title"]} -----')
        d = info2dict(article['text'])
        if not d or not '国旗画像' in d.keys():
            continue
        flag = re.search(r'([^\|]+)(\|.*)?', d['国旗画像']).group(1)
        print(flag)
        url = 'https://www.mediawiki.org/w/api.php?' \
            + 'action=query' \
            + '&titles=File:' + flag \
            + '&format=json' \
            + '&prop=imageinfo' \
            + '&iiprop=url'
        res = json.loads(requests.get(url).text)
        print(res['query']['pages'].popitem()[1]['imageinfo'][0]['url'])


if __name__ == '__main__':
    main()
