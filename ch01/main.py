# 第1章: 準備運動

def main():
    ''' 00. 文字列の逆順
    文字列"stressed"の文字を逆に（末尾から先頭に向かって）並べた文字列を得よ．
    '''
    s = 'stressed'
    print(s[-1::-1])


def main():
    ''' 01. 「パタトクカシーー」
    「パタトクカシーー」という文字列の1,3,5,7文字目を取り出して連結した文字列を得よ．
    '''
    s = 'パタトクカシーー'
    print(s[0::2])


def main():
    ''' 02. 「パトカー」＋「タクシー」＝「パタトクカシーー」
    「パトカー」＋「タクシー」の文字を先頭から交互に連結して文字列「パタトクカシーー」を得よ．
    '''
    s1, s2 = 'パトカー', 'タクシー'
    {print(s1 + s2, end='') for s1, s2 in zip(s1, s2)}


def main():
    ''' 03. 円周率
    "Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."
    という文を単語に分解し，各単語の（アルファベットの）文字数を先頭から出現順に並べたリストを作成せよ．
    '''
    s = 'Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics.'
    import re
    print([len(w) for w in re.split('[,. ]', s) if len(w)])


def main():
    ''' 04. 元素記号
    "Hi He Lied Because Boron Could Not Oxidize Fluorine.
    New Nations Might Also Sign Peace Security Clause. Arthur King Can."
    という文を単語に分解し，1, 5, 6, 7, 8, 9, 15, 16, 19番目の単語は先頭の1文字，
    それ以外の単語は先頭に2文字を取り出し，取り出した文字列から単語の位置
    （先頭から何番目の単語か）への連想配列（辞書型もしくはマップ型）を作成せよ．
    '''
    s = 'Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can.'
    import re
    ws = [w for w in re.split('[,. ]', s) if len(w)]
    dic = {}
    for i, w in enumerate(ws):
        c = 1 if i + 1 in (1, 5, 6, 7, 8, 9, 15, 16, 19) else 2
        dic.setdefault(w[:c], i + 1)
    print(dic)


def main():
    ''' 05. n-gram
    与えられたシーケンス（文字列やリストなど）からn-gramを作る関数を作成せよ．
    この関数を用い，"I am an NLPer"という文から単語bi-gram，文字bi-gramを得よ．
    '''
    def ngram(s, n):
        return [s[i:i + n] for i in range(len(s) - n + 1)]
    s = 'I am an NLPer'
    print('単語bi-gram:', ngram(s.split(), 2))
    print('文字bi-gram:', ngram(s, 2))


def main():
    ''' 06. 集合
    "paraparaparadise"と"paragraph"に含まれる文字bi-gramの集合を，
    それぞれ, XとYとして求め，XとYの和集合，積集合，差集合を求めよ．
    さらに，'se'というbi-gramがXおよびYに含まれるかどうかを調べよ．
    '''
    def ngram(s, n):
        return {s[i:i + n] for i in range(len(s) - n + 1)}
    X = ngram('paraparaparadise', 2)
    Y = ngram('paragraph', 2)
    print('和集合', X | Y)
    print('積集合', X & Y)
    print('差集合', X - Y | Y - X)
    print('"se" in X ->', 'se' in X)
    print('"se" in Y ->', 'se' in Y)


def main():
    ''' 07. テンプレートによる文生成
    引数x, y, zを受け取り「x時のyはz」という文字列を返す関数を実装せよ．
    さらに，x=12, y="気温", z=22.4として，実行結果を確認せよ．
    '''
    def template(x, y, z):
        return f'{x}時の{y}は{z}'
    print(template(12, '気温', 22.4))


def main():
    ''' 08. 暗号文
    与えられた文字列の各文字を，以下の仕様で変換する関数cipherを実装せよ．
    ・英小文字ならば(219 - 文字コード)の文字に置換
    ・その他の文字はそのまま出力
    この関数を用い，英語のメッセージを暗号化・復号化せよ．
    '''
    def cipher(input):
        output = ''.join(chr(219 - ord(c)) if c.islower() else c for c in input)
        print(output)
        return output
    cipher(cipher('This is secret.'))


def main():
    ''' 09. Typoglycemia
    スペースで区切られた単語列に対して，各単語の先頭と末尾の文字は残し，
    それ以外の文字の順序をランダムに並び替えるプログラムを作成せよ．
    ただし，長さが４以下の単語は並び替えないこととする．適当な英語の文
    （例えば"I couldn't believe that I could actually understand what I was reading :
    the phenomenal power of the human mind ."）を与え，その実行結果を確認せよ．
    '''
    import random
    def Typoglycemia(text):
        shuffled = []
        for w in text.split():
            if len(w) <= 4:
                shuffled.append(w)
            else:
                w_mid = ''.join(random.sample(w[1:-1], len(w) - 2))
                shuffled.append(w[0] + w_mid + w[-1])
        return ' '.join(shuffled)
    text = "I couldn't believe that I could actually understand what I was reading : the phenomenal power of the human mind ."
    print(Typoglycemia(text))


if __name__ == '__main__':
    main()
