''' 第8章: 機械学習
本章では，Bo Pang氏とLillian Lee氏が公開しているMovie Review Dataの
sentence polarity dataset v1.0を用い，文を肯定的（ポジティブ）もしくは
否定的（ネガティブ）に分類するタスク（極性分析）に取り組む．
'''
import pickle

import numpy as np
from nltk.corpus import stopwords

stop_words = stopwords.words('english') + ['--']


def is_stopword(s):
    return s.lower() in stop_words


def main():
    ''' 70. データの入手・整形
    文に関する極性分析の正解データを用い，以下の要領で正解データ（sentiment.txt）を作成せよ．
    1.rt-polarity.posの各行の先頭に"+1 "という文字列を追加する
      （極性ラベル"+1"とスペースに続けて肯定的な文の内容が続く）
    2.rt-polarity.negの各行の先頭に"-1 "という文字列を追加する
      （極性ラベル"-1"とスペースに続けて否定的な文の内容が続く）
    3.上述1と2の内容を結合（concatenate）し，行をランダムに並び替える
    sentiment.txtを作成したら，正例（肯定的な文）の数と負例（否定的な文）の数を確認せよ．
    '''
    import random
    file_pos = 'rt-polaritydata/rt-polarity.pos'
    file_neg = 'rt-polaritydata/rt-polarity.neg'
    file_res = 'sentiment.txt'
    # 読み込み
    result = []
    with open(file_pos) as f_pos, open(file_neg) as f_neg:
        result += [f'+1 {line}' for line in f_pos]
        result += [f'-1 {line}' for line in f_neg]
        random.shuffle(result)
    # 書き出し
    with open(file_res, 'w') as f:
        print(*result, file=f, sep='')
    # カウント
    with open(file_res) as f:
        text = f.read()
        pos, neg = text.count('+1 '), text.count('-1 ')
        print(f'pos:{pos}, neg:{neg}')


def main():
    ''' 71. ストップワード
    英語のストップワードのリスト（ストップリスト）を適当に作成せよ．さらに，引数に与えられた単語（文字列）がストップリストに含まれている場合は真，それ以外は偽を返す関数を実装せよ．さらに，その関数に対するテストを記述せよ．
    '''
    print(is_stopword('hello'))
    print(is_stopword('can'))


def main():
    ''' 72. 素性抽出
    極性分析に有用そうな素性を各自で設計し，学習データから素性を抽出せよ．素性としては，レビューからストップワードを除去し，各単語をステミング処理したものが最低限のベースラインとなるであろう．
    '''
    import snowballstemmer
    from collections import Counter
    from contractions import expandContractions
    stemmer = snowballstemmer.stemmer('english')
    counter = Counter()
    data = []
    # 読み込み
    with open('sentiment.txt') as f:
        for line in f:
            label, text = line[:2], line[3:]
            text = expandContractions(text)
            words = [w for w in text.split() if not is_stopword(w)]
            words = [w for w in words if (len(w) > 1) or (w in ['!', '?'])]
            words = [stemmer.stemWord(w) for w in words]
            counter.update(words)
            data += [(label, words)]
    # 6回以上出現するワード
    features = [w for w, c in counter.items() if c > 5]
    # 書き出し
    with open('features.txt', 'w') as f:
        for i, w in enumerate(features):
            print(w, file=f)
    with open('data.txt', 'w') as f:
        for label, words in data:
            words = [features.index(w) for w in words if w in features]
            label = 1 if label == '+1' else 0
            print(label, *words, file=f)


def main():
    ''' 73. 学習
    72で抽出した素性を用いて，ロジスティック回帰モデルを学習せよ．
    '''
    from sklearn.linear_model import LogisticRegression

    with open('data.txt') as f:
        X, y = [], []
        for line in f:
            data = [int(w) for w in line.split()]
            y.append(data[0])
            x = np.zeros(3187)
            x[data[1:]] = 1
            X.append(x)

    model = LogisticRegression(random_state=0)
    model.fit(X, y)

    with open('model.pkl', mode='wb') as f:
        pickle.dump(model, f)


def main():
    ''' 74. 予測
    73で学習したロジスティック回帰モデルを用い，与えられた文の極性ラベル（正例なら"+1"，負例なら"-1"）と，その予測確率を計算するプログラムを実装せよ．
    '''
    with open('model.pkl', mode='rb') as f:
        model = pickle.load(f)

    correct = 0
    with open('data.txt') as f:
        for i, line in enumerate(f):
            data = [int(w) for w in line.split()]
            y = data[0]
            x = np.zeros(3187)
            x[data[1:]] = 1

            pred = model.predict([x])
            if pred[0] == y:
                correct += 1
    print(f'accuracy:{correct/(i+1)}')


def main():
    ''' 75. 素性の重み
    73で学習したロジスティック回帰モデルの中で，重みの高い素性トップ10と，重みの低い素性トップ10を確認せよ．
    '''
    with open('features.txt') as f:
        features = f.read().split()

    with open('model.pkl', mode='rb') as f:
        model = pickle.load(f)

    a = model.get_params()
    print(a)

    ''' 76. ラベル付け
    学習データに対してロジスティック回帰モデルを適用し，正解のラベル，予測されたラベル，予測確率をタブ区切り形式で出力せよ．
    '''

    ''' 77. 正解率の計測
    76の出力を受け取り，予測の正解率，正例に関する適合率，再現率，F1スコアを求めるプログラムを作成せよ．
    '''

    ''' 78. 5分割交差検定
    76-77の実験では，学習に用いた事例を評価にも用いたため，正当な評価とは言えない．すなわち，分類器が訓練事例を丸暗記する際の性能を評価しており，モデルの汎化性能を測定していない．そこで，5分割交差検定により，極性分類の正解率，適合率，再現率，F1スコアを求めよ．
    '''

    ''' 79. 適合率-再現率グラフの描画
    ロジスティック回帰モデルの分類の閾値を変化させることで，適合率-再現率グラフを描画せよ．
    '''


if __name__ == '__main__':
    main()
