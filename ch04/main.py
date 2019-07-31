''' 第4章: 形態素解析
夏目漱石の小説『吾輩は猫である』の文章（neko.txt）をMeCabを使って形態素解析し，
その結果をneko.txt.mecabというファイルに保存せよ．このファイルを用いて，
以下の問に対応するプログラムを実装せよ．
なお，問題37, 38, 39はmatplotlibもしくはGnuplotを用いるとよい．
'''
import re
from collections import Counter

import matplotlib.pyplot as plt


def prepare():
    ''' 準備 '''
    import MeCab
    mecab = MeCab.Tagger()
    with open('neko.txt') as f1, open('neko.txt.mecab', 'w') as f2:
        f2.write(mecab.parse(f1.read()))


def sequence_gen():
    ''' 情報を一文ずつ取得 '''
    with open('neko.txt.mecab') as f:
        sequence = []
        for line in f:
            if line == 'EOS\n':
                yield sequence
                break
            word_info = re.split(r'\t|,', line.rstrip())
            sequence.append({'surface': word_info[0],
                             'base': word_info[7],
                             'pos': word_info[1],
                             'pos1': word_info[2]})
            if word_info[2] == '句点':
                yield sequence
                sequence = []


def main():
    ''' 30. 形態素解析結果の読み込み
    形態素解析結果（neko.txt.mecab）を読み込むプログラムを実装せよ．
    ただし，各形態素は表層形（surface），基本形（base），品詞（pos），品詞細分類1（pos1）を
    キーとするマッピング型に格納し，1文を形態素（マッピング型）のリストとして表現せよ．
    第4章の残りの問題では，ここで作ったプログラムを活用せよ．
    '''
    for sequence in sequence_gen():
        print(sequence)


def main():
    ''' 31. 動詞
    動詞の表層形をすべて抽出せよ．
    '''
    for sequence in sequence_gen():
        for word in sequence:
            if word['pos'] == '動詞':
                print(word['surface'])


def main():
    ''' 32. 動詞の原形
    動詞の原形をすべて抽出せよ．
    '''
    for sequence in sequence_gen():
        for word in sequence:
            if word['pos'] == '動詞':
                print(word['base'])


def main():
    ''' 33. サ変名詞
    サ変接続の名詞をすべて抽出せよ．
    '''
    for sequence in sequence_gen():
        for word in sequence:
            if word['pos'] + word['pos1'] == '名詞サ変接続':
                print(word['surface'], word)


# def main():
#     ''' 34. 「AのB」
#     2つの名詞が「の」で連結されている名詞句を抽出せよ．
#     '''
#     pattern = re.compile('S(?:&S)+')
#     for seq in sequence_gen():
#         encode_str = ''
#         for w in seq:
#             if w['surface'] == 'の':
#                 encode_str += '&'
#             elif w['pos'] == '名詞':
#                 encode_str += 'S'
#             else:
#                 encode_str += '?'
#         for m in pattern.finditer(encode_str):
#             print(''.join(w['surface'] for w in seq[m.start():m.end()]))
#
#
# def main():
#     ''' 35. 名詞の連接
#     名詞の連接（連続して出現する名詞）を最長一致で抽出せよ．
#     '''
#     pattern = re.compile('SS+')
#     for seq in sequence_gen():
#         encode_str = ''.join('S' if w['pos'] == '名詞' else '?' for w in seq)
#         for m in pattern.finditer(encode_str):
#             print(''.join(w['surface'] for w in seq[m.start():m.end()]))
#
#
# def main():
#     ''' 36. 単語の出現頻度
#     文章中に出現する単語とその出現頻度を求め，出現頻度の高い順に並べよ．
#     '''
#     counter = Counter(w['surface'] for seq in sequence_gen() for w in seq)
#     {print(word, num) for word, num in counter.most_common()}
#
#
# def main():
#     ''' 37. 頻度上位10語
#     出現頻度が高い10語とその出現頻度をグラフ（例えば棒グラフなど）で表示せよ．
#     '''
#     counter = Counter(w['surface'] for seq in sequence_gen() for w in seq)
#     for word, num in counter.most_common(10):
#         plt.bar(word, num)
#     plt.grid(axis='y')
#     plt.xlabel('単語')
#     plt.ylabel('出現頻度')
#     plt.show()
#
#
# def main():
#     ''' 38. ヒストグラム
#     単語の出現頻度のヒストグラム
#     （横軸に出現頻度，縦軸に出現頻度をとる単語の種類数を棒グラフで表したもの）を描け．
#     '''
#     counter = Counter(w['surface'] for seq in sequence_gen() for w in seq)
#     plt.hist([n for w, n in counter.most_common()], bins=19, range=(1, 20))
#     plt.xlim(xmin=1, xmax=20)
#     plt.grid(axis='y')
#     plt.xlabel('出現頻度')
#     plt.ylabel('単語の種類数')
#     plt.show()
#
#
# def main():
#     ''' 39. Zipfの法則
#     単語の出現頻度順位を横軸，その出現頻度を縦軸として，両対数グラフをプロットせよ．
#     '''
#     counter = Counter(w['surface'] for seq in sequence_gen() for w in seq)
#     counts = [n for w, n in counter.most_common()]
#     plt.loglog(range(1, len(counts) + 1),  counts)
#     plt.xlabel('出現度順位')
#     plt.ylabel('出現頻度')
#     plt.show()


if __name__ == '__main__':
    main()
