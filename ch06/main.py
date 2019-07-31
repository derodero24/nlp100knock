''' 第6章: 英語テキストの処理
英語のテキスト（nlp.txt）に対して，以下の処理を実行せよ．
'''
import xml.etree.ElementTree as ET

import regex as re


def main():
    ''' 50. 文区切り
    (. or ; or : or ? or !) → 空白文字 → 英大文字
    というパターンを文の区切りと見なし，入力された文書を1行1文の形式で出力せよ．
    '''
    pattern = re.compile(r'\s*(.+?([\.|;|:|\?|!](?=\s[A-Z])|$))', re.MULTILINE)
    with open('nlp.txt') as f:
        for i, m in enumerate(pattern.finditer(f.read())):
            print(f'{i+1:2}  {m.group(1)}')


def main():
    ''' 51. 単語の切り出し
    空白を単語の区切りとみなし，50の出力を入力として受け取り，1行1単語の形式で出力せよ．
    ただし，文の終端では空行を出力せよ．
    '''
    pattern = re.compile(r'\s*(.+?([\.|;|:|\?|!](?=\s[A-Z])|$))', re.MULTILINE)
    with open('nlp.txt') as f:
        for m in pattern.finditer(f.read()):
            line = m.group(1)  # 50の出力
            for word in line.split(' '):
                print(word.rstrip('.,;:?!'))
            print()


def main():
    ''' 52. ステミング
    51の出力を入力として受け取り，Porterのステミングアルゴリズムを適用し，単語と語幹をタブ区切り形式で出力せよ． Pythonでは，Porterのステミングアルゴリズムの実装としてstemmingモジュールを利用するとよい．
    '''
    import snowballstemmer
    stemmer = snowballstemmer.stemmer('english')

    pattern = re.compile(r'\s*(.+?([\.|;|:|\?|!](?=\s[A-Z])|$))', re.MULTILINE)
    with open('nlp.txt') as f:
        for m in pattern.finditer(f.read()):
            line = m.group(1)  # 50の出力
            for word in line.split(' '):
                word = word.rstrip('.,;:?!')  # 51の出力
                print(f'{word:10}\t{stemmer.stemWord(word)}')
            print()


def main():
    ''' 53. Tokenization
    Stanford Core NLPを用い，入力テキストの解析結果をXML形式で得よ．
    また，このXMLファイルを読み込み，入力テキストを1行1単語の形式で出力せよ．
    '''
    tree = ET.parse('nlp.txt.xml')
    for word in tree.iter('word'):
        print(word.text)


def main():
    ''' 54. 品詞タグ付け
    Stanford Core NLPの解析結果XMLを読み込み，単語，レンマ，品詞をタブ区切り形式で出力せよ．
    '''
    tree = ET.parse('nlp.txt.xml')
    for token in tree.iter('token'):
        word = token.findtext('word')
        lemma = token.findtext('lemma')
        pos = token.findtext('POS')
        print(f'{word}\t{lemma}\t{pos}')


def main():
    ''' 55. 固有表現抽出
    入力文中の人名をすべて抜き出せ．
    '''
    tree = ET.parse('nlp.txt.xml')
    for token in tree.iterfind('.//token[NER="PERSON"]'):
        print(token.findtext('word'))


def main():
    ''' 56. 共参照解析
    Stanford Core NLPの共参照解析の結果に基づき，文中の参照表現（mention）を代表参照表現（representative mention）に置換せよ．ただし，置換するときは，「代表参照表現（参照表現）」のように，元の参照表現が分かるように配慮せよ．
    '''
    tree = ET.parse('nlp.txt.xml')

    # 置換置換候補を収集
    replace_dict = {}
    for conf in tree.iterfind('.//coreference/coreference'):
        rep_text = conf.findtext('.//text')
        for mention in conf.iterfind('.//mention'):
            # 代表は無視
            if mention.get('representative'):
                continue
            # 代表以外は置換候補に追加
            sent = int(mention.findtext('sentence'))
            start = int(mention.findtext('start'))
            end = int(mention.findtext('end'))
            # 先勝ち
            replace_dict.setdefault((sent, start), (end, rep_text))

    # 置換しながら出力
    rest = 0
    for sent in tree.iterfind('.//sentences/sentence'):
        sent_id = int(sent.get('id'))
        for token in sent.iterfind('./tokens/token'):
            token_id = int(token.get('id'))

            if (sent_id, token_id) in replace_dict and rest == 0:
                end, rep_text = replace_dict[(sent_id, token_id)]
                print(f'[{rep_text}] (', end='')
                rest = end - token_id

            print(token.findtext('word'), end='')

            if rest != 0:
                rest -= 1
                if rest == 0:
                    print(')', end='')

            print(' ', end='')
        print()


def main():
    ''' 57. 係り受け解析
    Stanford Core NLPの係り受け解析の結果（collapsed-dependencies）を有向グラフとして可視化せよ．可視化には，係り受け木をDOT言語に変換し，Graphvizを用いるとよい．
    また，Pythonから有向グラフを直接的に可視化するには，pydotを使うとよい．
    '''
    import pydot

    tree = ET.parse('nlp.txt.xml')
    for i, sent in enumerate(tree.iterfind('.//sentences/sentence')):
        sent_id = sent.get('id')
        edges = []

        for dep in sent.iterfind('./dependencies[@type="collapsed-dependencies"]/dep'):
            # 句読点はスキップ
            if dep.get('type') == 'punct':
                continue

            gvr = dep.find('./governor')
            dpt = dep.find('./dependent')
            edges.append(((gvr.get('idx'), gvr.text),
                          (dpt.get('idx'), dpt.text)))\

        pydot.graph_from_edges(edges).write_png(f'57_{sent_id}.png')

        if i == 2:
            break


def main():
    ''' 58. タプルの抽出
    Stanford Core NLPの係り受け解析の結果（collapsed-dependencies）に基づき，「主語 述語 目的語」の組をタブ区切り形式で出力せよ．ただし，主語，述語，目的語の定義は以下を参考にせよ．
    ・述語: nsubj関係とdobj関係の子（dependant）を持つ単語
    ・主語: 述語からnsubj関係にある子（dependent）
    ・目的語: 述語からdobj関係にある子（dependent）
    '''
    tree = ET.parse('nlp.txt.xml')

    for sent in tree.iterfind('.//sentences/sentence'):
        dep_dict = {}
        for dep in sent.iterfind('./dependencies[@type="collapsed-dependencies"]/dep'):
            dep_type = dep.get('type')
            if dep_type == 'nsubj' or dep_type == 'dobj':

                govr = dep.find('./governor')
                idx = govr.get('idx')
                dep_dict.setdefault(idx, {'pred': govr.text,
                                          'nsubj': None, 'dobj': None})
                dep_dict[idx][dep_type] = dep.findtext('./dependent')

        for key, val in dep_dict.items():
            if all(v for v in val.values()):
                print(f'{val["nsubj"]}\t{val["pred"]}\t{val["dobj"]}')


def main():
    ''' 59. S式の解析
    Stanford Core NLPの句構造解析の結果（S式）を読み込み，文中のすべての名詞句（NP）を表示せよ．入れ子になっている名詞句もすべて表示すること．
    '''
    pat_1 = re.compile(r'(?<a>\((?:[^()]+|(?&a))*\))')
    pat_2 = re.compile(r'\(.+? ([^()]+?)\)')

    tree = ET.parse('nlp.txt.xml')
    for parse in tree.iter('parse'):
        for capture in pat_1.search(parse.text).captures('a'):

            if capture[1:3] != 'NP':
                continue

            for match in pat_2.finditer(capture):
                print(match.group(1), end=' ')
            print()


if __name__ == '__main__':
    main()
