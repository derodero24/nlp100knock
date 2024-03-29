''' 第2章: UNIXコマンドの基礎
hightemp.txtは，日本の最高気温の記録を「都道府県」「地点」「℃」「日」の
タブ区切り形式で格納したファイルである．以下の処理を行うプログラムを作成し，
hightemp.txtを入力ファイルとして実行せよ．さらに，同様の処理をUNIXコマンドでも実行し，
プログラムの実行結果を確認せよ．
'''


def main():
    ''' 10. 行数のカウント
    行数をカウントせよ．確認にはwcコマンドを用いよ．
    '''
    with open('hightemp.txt', 'r') as f:
        print(len(f.readlines()))


def main():
    ''' 11. タブをスペースに置換
    タブ1文字につきスペース1文字に置換せよ．確認にはsedコマンド，trコマンド，
    もしくはexpandコマンドを用いよ．
    '''
    with open('hightemp.txt', 'r') as f:
        print(f.read().replace('\t', ' '))


def main():
    ''' 12. 1列目をcol1.txtに，2列目をcol2.txtに保存
    各行の1列目だけを抜き出したものをcol1.txtに，2列目だけを抜き出したものをcol2.txtとして
    ファイルに保存せよ．確認にはcutコマンドを用いよ．
    '''
    with open('hightemp.txt', 'r') as f, open('col1.txt', 'w') as f1, open('col2.txt', 'w') as f2:
        cols = [l.split('\t')[:2] for l in f]
        f1.write('\n'.join(c for c, _ in cols))
        f2.write('\n'.join(c for _, c in cols))


def main():
    ''' 13. col1.txtとcol2.txtをマージ
    12で作ったcol1.txtとcol2.txtを結合し，元のファイルの1列目と2列目をタブ区切りで並べた
    テキストファイルを作成せよ．確認にはpasteコマンドを用いよ．
    '''
    with open('col1.txt', 'r') as f1, open('col2.txt', 'r') as f2, open('marge.txt', 'w') as f3:
        for line1, line2 in zip(f1, f2):
            f3.write(f'{line1.strip()}\t{line2.strip()}\n')


def main():
    ''' 14. 先頭からN行を出力
    自然数Nをコマンドライン引数などの手段で受け取り，入力のうち先頭のN行だけを表示せよ．
    確認にはheadコマンドを用いよ．
    '''
    n = 5
    with open('hightemp.txt', 'r') as f:
        {print(l.strip()) for l in f.readlines()[:n]}


def main():
    ''' 15. 末尾のN行を出力
    自然数Nをコマンドライン引数などの手段で受け取り，入力のうち末尾のN行だけを表示せよ．
    確認にはtailコマンドを用いよ．
    '''
    n = 5
    with open('hightemp.txt', 'r') as f:
        {print(l, end='') for l in f.readlines()[-n:]}


def main():
    ''' 16. ファイルをN分割する
    自然数Nをコマンドライン引数などの手段で受け取り，入力のファイルを行単位でN分割せよ．
    同様の処理をsplitコマンドで実現せよ．
    '''
    n = 5
    with open('hightemp.txt', 'r') as f:
        for i, line in enumerate(f):
            print(line, end=('' if (i + 1) % n else '\n'))


def main():
    ''' 17. １列目の文字列の異なり
    1列目の文字列の種類（異なる文字列の集合）を求めよ．確認にはsort, uniqコマンドを用いよ．
    '''
    with open('hightemp.txt', 'r') as f:
        kens = {l.split('\t')[0] for l in f}
    {print(ken) for ken in kens}


def main():
    ''' 18. 各行を3コラム目の数値の降順にソート
    各行を3コラム目の数値の逆順で整列せよ（注意: 各行の内容は変更せずに並び替えよ）．
    確認にはsortコマンドを用いよ（この問題はコマンドで実行した時の結果と合わなくてもよい）．
    '''
    with open('hightemp.txt', 'r') as f:
        lines = f.readlines()
    lines.sort(key=lambda l: float(l.split('\t')[2]), reverse=True)
    [print(line, end='') for line in lines]


def main():
    ''' 19. 各行の1コラム目の文字列の出現頻度を求め，出現頻度の高い順に並べる
    各行の1列目の文字列の出現頻度を求め，その高い順に並べて表示せよ．
    確認にはcut, uniq, sortコマンドを用いよ．
    '''
    from itertools import groupby
    from operator import itemgetter
    with open('hightemp.txt', 'r') as f:
        kens = sorted([line.split('\t')[0] for line in f])
    res = [(ken, sum(True for _ in group)) for ken, group in groupby(kens)]
    res.sort(key=itemgetter(1), reverse=True)
    {print(ken, num) for ken, num in res}


if __name__ == '__main__':
    main()
