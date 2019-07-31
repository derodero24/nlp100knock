''' 第5章: 係り受け解析
夏目漱石の小説『吾輩は猫である』の文章（neko.txt）をCaboChaを使って係り受け解析し，
その結果をneko.txt.cabochaというファイルに保存せよ．
このファイルを用いて，以下の問に対応するプログラムを実装せよ．
'''
import re


def prepare():
    ''' 準備 '''
    import CaboCha
    cabocha = CaboCha.Parser()
    with open('../ch04/neko.txt') as f1, open('neko.txt.cabocha', 'w') as f2:
        for line in f1:
            f2.write(cabocha.parse(line).toString(CaboCha.FORMAT_LATTICE))


class Morph():
    ''' Morphクラス '''

    def __init__(self, line):
        word_info = re.split(r'\t|,', line.rstrip())
        self.surface = word_info[0]
        self.base = word_info[7]
        self.pos = word_info[1]
        self.pos1 = word_info[2]

    def __str__(self):
        return f'surface[{self.surface}]\tbase[{self.base}]\tpos[{self.pos}]\tpos1[{self.pos1}]'


class Chunk():
    ''' Chunkクラス '''

    def __init__(self, idx):
        self.idx = idx
        self.morphs = []
        self.dst = None
        self.srcs = []

    def __str__(self):
        return f'[{self.idx}]{self.surface():5}\tdst[{self.dst}]\tsrcs{self.srcs}'

    def surface(self, replace=(None, 'XXX')):
        surface = ''
        for morph in self.morphs:
            if morph.pos == '記号':
                continue
            elif morph.pos == replace[0]:
                surface += replace[1]
            else:
                surface += morph.surface
        surface = re.sub(r'(%s)+' % replace[1], replace[1], surface)
        return surface

    def get_morphs(self, pos, pos1=None, surface=None):
        res = [m for m in self.morphs if m.pos == pos]
        if pos1:
            res = [m for m in res if m.pos1 == pos1]
        if surface:
            res = [m for m in res if m.surface == surface]
        return res


def morphs_gen():
    ''' Morphリスト ジェネレータ '''
    morphs = []
    with open('neko.txt.cabocha') as f:
        for line in f:
            if line == 'EOS\n':
                yield morphs
                morphs = []
                continue
            if line[0] == '*':
                continue
            morphs.append(Morph(line))


def chunks_gen():
    ''' Chunkリスト ジェネレータ '''
    chunks = {}
    with open('neko.txt.cabocha') as f:
        for line in f:
            if line == 'EOS\n':
                chunks = [chunks[i] for i in range(len(chunks))]
                yield chunks
                chunks = {}
                continue

            if line[0] == '*':
                info = line.split()
                idx = int(info[1])
                dst = int(info[2][:-1])

                chunks.setdefault(idx, Chunk(idx))
                chunks[idx].dst = dst

                if dst >= 0:
                    chunks.setdefault(dst, Chunk(dst))
                    chunks[dst].srcs.append(idx)
                continue

            morph = Morph(line)
            chunks[idx].morphs.append(morph)


def main():
    ''' 40. 係り受け解析結果の読み込み（形態素）
    形態素を表すクラスMorphを実装せよ．
    このクラスは表層形（surface），基本形（base），品詞（pos），品詞細分類1（pos1）を
    メンバ変数に持つこととする．さらに，CaboChaの解析結果（neko.txt.cabocha）を読み込み，
    各文をMorphオブジェクトのリストとして表現し，3文目の形態素列を表示せよ．
    '''
    for i, morphs in enumerate(morphs_gen()):
        if i == 2:
            for morph in morphs:
                print(morph)
            break


def main():
    ''' 41. 係り受け解析結果の読み込み（文節・係り受け）
    40に加えて，文節を表すクラスChunkを実装せよ．
    このクラスは形態素（Morphオブジェクト）のリスト（morphs），係り先文節インデックス番号（dst），
    係り元文節インデックス番号のリスト（srcs）をメンバ変数に持つこととする．さらに，
    入力テキストのCaboChaの解析結果を読み込み，１文をChunkオブジェクトのリストとして表現し，
    8文目の文節の文字列と係り先を表示せよ．第5章の残りの問題では，ここで作ったプログラムを活用せよ．
    '''
    for i, chunks in enumerate(chunks_gen()):
        if i == 7:
            for chunk in chunks:
                print(chunk)
            break


def main():
    ''' 42. 係り元と係り先の文節の表示
    係り元の文節と係り先の文節のテキストをタブ区切り形式ですべて抽出せよ．
    ただし，句読点などの記号は出力しないようにせよ．
    '''
    for i, chunks in enumerate(chunks_gen()):
        for chunk in chunks:
            surface = chunk.surface()
            if chunk.dst >= 0:
                dst_surface = chunks[chunk.dst].surface()
            else:
                dst_surface = ''
            print(f'{surface}\t{dst_surface}')


def main():
    ''' 43. 名詞を含む文節が動詞を含む文節に係るものを抽出
    名詞を含む文節が，動詞を含む文節に係るとき，これらをタブ区切り形式で抽出せよ．
    ただし，句読点などの記号は出力しないようにせよ．
    '''
    for i, chunks in enumerate(chunks_gen()):
        for chunk in chunks:
            if chunk.dst >= 0 and \
                chunk.get_morphs('名詞') and \
                    chunks[chunk.dst].get_morphs('動詞'):

                surface = chunk.surface()
                dst_surface = chunks[chunk.dst].surface()
                print(f'{surface}\t{dst_surface}')


def main():
    ''' 44. 係り受け木の可視化
    与えられた文の係り受け木を有向グラフとして可視化せよ．可視化には，係り受け木をDOT言語に変換し，
    Graphvizを用いるとよい．また，Pythonから有向グラフを直接的に可視化するには，pydotを使うとよい．
    '''
    import pydot

    for i, chunks in enumerate(chunks_gen()):
        if i != 6:
            continue

        edge_list = []
        for chunk in chunks:
            if chunk.dst < 0:
                continue
            surface = chunk.surface()
            dst_surface = chunks[chunk.dst].surface()
            edge_list.append((surface, dst_surface))
        break

    pydot.graph_from_edges(edge_list).write_png('44.png')


def main():
    ''' 45. 動詞の格パターンの抽出
    今回用いている文章をコーパスと見なし，日本語の述語が取りうる格を調査したい．
    動詞を述語，動詞に係っている文節の助詞を格と考え，述語と格をタブ区切り形式で出力せよ．
    ただし，出力は以下の仕様を満たすようにせよ．
    ・動詞を含む文節において，最左の動詞の基本形を述語とする
    ・述語に係る助詞を格とする
    ・述語に係る助詞（文節）が複数あるときは，すべての助詞をスペース区切りで辞書順に並べる
    「吾輩はここで始めて人間というものを見た」という例文（neko.txt.cabochaの8文目）を考える．
    この文は「始める」と「見る」の２つの動詞を含み，「始める」に係る文節は「ここで」，「見る」に
    係る文節は「吾輩は」と「ものを」と解析された場合は，次のような出力になるはずである．
    --------------------------------------------------------------------------------
    始める  で
    見る    は を
    --------------------------------------------------------------------------------
    このプログラムの出力をファイルに保存し，以下の事項をUNIXコマンドを用いて確認せよ．
    ・コーパス中で頻出する述語と格パターンの組み合わせ
    ・「する」「見る」「与える」という動詞の格パターン（コーパス中で出現頻度の高い順に並べよ）
    '''
    for i, chunks in enumerate(chunks_gen()):
        for chunk in chunks:
            verbs = chunk.get_morphs('動詞')
            if not verbs:
                continue
            base = verbs[0].base

            posts = []
            for src in chunk.srcs:
                for morph in chunks[src].get_morphs('助詞'):
                    posts.append(morph.surface)

            if posts:
                print(f'{base}\t{" ".join(sorted(posts))}')


def main():
    ''' 46. 動詞の格フレーム情報の抽出
    45のプログラムを改変し，述語と格パターンに続けて項（述語に係っている文節そのもの）を
    タブ区切り形式で出力せよ．45の仕様に加えて，以下の仕様を満たすようにせよ．
    ・項は述語に係っている文節の単語列とする（末尾の助詞を取り除く必要はない）
    ・述語に係る文節が複数あるときは，助詞と同一の基準・順序でスペース区切りで並べる
    「吾輩はここで始めて人間というものを見た」という例文（neko.txt.cabochaの8文目）を考える．
    この文は「始める」と「見る」の２つの動詞を含み，「始める」に係る文節は「ここで」，「見る」に
    係る文節は「吾輩は」と「ものを」と解析された場合は，次のような出力になるはずである．
    --------------------------------------------------------------------------------
    始める  で      ここで
    見る    は を   吾輩は ものを
    --------------------------------------------------------------------------------
    '''
    for i, chunks in enumerate(chunks_gen()):
        for chunk in chunks:
            verbs = chunk.get_morphs('動詞')
            if not verbs:
                continue
            base = verbs[0].base

            posts = []
            for src in chunk.srcs:
                for morph in chunks[src].get_morphs('助詞'):
                    posts.append((morph.surface, chunks[src].surface()))

            if posts:
                ports = list(zip(*sorted(posts)))
                print(f'{base}\t{" ".join(ports[0])}\t{" ".join(ports[1])}')


def main():
    ''' 47. 機能動詞構文のマイニング
    動詞のヲ格にサ変接続名詞が入っている場合のみに着目したい．
    46のプログラムを以下の仕様を満たすように改変せよ．
    ・「サ変接続名詞+を（助詞）」で構成される文節が動詞に係る場合のみを対象とする
    ・述語は「サ変接続名詞+を+動詞の基本形」とし，文節中に複数の動詞があるときは，最左の動詞を用いる
    ・述語に係る助詞（文節）が複数あるときは，すべての助詞をスペース区切りで辞書順に並べる
    ・述語に係る文節が複数ある場合は，すべての項をスペース区切りで並べる（助詞の並び順と揃えよ）
    例えば「別段くるにも及ばんさと、主人は手紙に返事をする。」という文から，
    以下の出力が得られるはずである．
    --------------------------------------------------------------------------------
    返事をする      と に は        及ばんさと 手紙に 主人は
    --------------------------------------------------------------------------------
    このプログラムの出力をファイルに保存し，以下の事項をUNIXコマンドを用いて確認せよ．
    ・コーパス中で頻出する述語（サ変接続名詞+を+動詞）
    ・コーパス中で頻出する述語と助詞パターン
    '''
    for i, chunks in enumerate(chunks_gen()):
        for chunk in chunks:
            verbs = chunk.get_morphs('動詞')
            if not verbs:
                continue
            base = verbs[0].base

            try:
                for src in chunk.srcs:
                    morphs = chunks[src].morphs
                    for j in range(len(morphs[:-1])):
                        m1, m2 = morphs[j:j + 2]
                        if m1.pos + m1.pos1 == '名詞サ変接続' and \
                                m2.surface + m2.pos == 'を助詞':
                            sequence = m1.surface + m2.surface + base
                            used_morph = m2
                            raise Exception
                continue
            except:
                print(sequence, end='')

            posts = []
            for src in chunk.srcs:
                for morph in chunks[src].get_morphs('助詞'):
                    if morph != used_morph:
                        posts.append((morph.surface, chunks[src].surface()))

            if posts:
                ports = list(zip(*sorted(posts)))
                print(f'\t{" ".join(ports[0])}\t{" ".join(ports[1])}')
            else:
                print()


def main():
    ''' 48. 名詞から根へのパスの抽出
    文中のすべての名詞を含む文節に対し，その文節から構文木の根に至るパスを抽出せよ．
    ただし，構文木上のパスは以下の仕様を満たすものとする．
    ・各文節は（表層形の）形態素列で表現する
    ・パスの開始文節から終了文節に至るまで，各文節の表現を"->"で連結する
    「吾輩はここで始めて人間というものを見た」という文（neko.txt.cabochaの8文目）から，
    次のような出力が得られるはずである．
    --------------------------------------------------------------------------------
    吾輩は -> 見た
    ここで -> 始めて -> 人間という -> ものを -> 見た
    人間という -> ものを -> 見た
    ものを -> 見た
    --------------------------------------------------------------------------------
    '''
    for i, chunks in enumerate(chunks_gen()):
        for chunk in chunks:
            if not chunk.get_morphs('名詞'):
                continue
            print(chunk.surface(), end='')

            dst = chunk.dst
            while dst != -1:
                print(' -> ' + chunks[dst].surface(), end='')
                dst = chunks[dst].dst
            print()


def main():
    ''' 49. 名詞間の係り受けパスの抽出
    文中のすべての名詞句のペアを結ぶ最短係り受けパスを抽出せよ．
    ただし，名詞句ペアの文節番号がiとj（i<j）のとき，係り受けパスは以下の仕様を満たすものとする．
    ・問題48と同様に，パスは開始文節から終了文節に至るまでの各文節の表現（表層形の形態素列）を
      "->"で連結して表現する
    ・文節iとjに含まれる名詞句はそれぞれ，XとYに置換する
    また，係り受けパスの形状は，以下の2通りが考えられる．
    ・文節iから構文木の根に至る経路上に文節jが存在する場合:
        文節iから文節jのパスを表示
    ・上記以外で，文節iと文節jから構文木の根に至る経路上で共通の文節kで交わる場合:
        文節iから文節kに至る直前のパスと文節jから文節kに至る直前までのパス，文節kの内容を"|"で連結して表示
    例えば，「吾輩はここで始めて人間というものを見た。」という文（neko.txt.cabochaの8文目）から，
    次のような出力が得られるはずである．
    --------------------------------------------------------------------------------
    Xは | Yで -> 始めて -> 人間という -> ものを | 見た
    Xは | Yという -> ものを | 見た
    Xは | Yを | 見た
    Xで -> 始めて -> Y
    Xで -> 始めて -> 人間という -> Y
    Xという -> Y
    --------------------------------------------------------------------------------
    '''
    for i, chunks in enumerate(chunks_gen()):
        noun_idx = [i for i, c in enumerate(chunks) if c.get_morphs('名詞')]

        if len(noun_idx) < 2:
            continue

        for i, idx1 in enumerate(noun_idx[:-1]):
            for idx2 in noun_idx[i + 1:]:
                flag = False
                path = chunks[idx1].surface(replace=('名詞', 'X'))
                dst = chunks[idx1].dst

                while not flag:
                    if dst == idx2:
                        path += ' -> Y'
                        flag = True
                    elif chunks[dst].dst == -1:
                        break
                    else:
                        path += f' -> {chunks[dst].surface()}'
                        dst = chunks[dst].dst
                else:
                    print(path)
                    continue

                path += f' | {chunks[idx2].surface(replace=("名詞", "Y"))}'
                dst = chunks[idx2].dst
                while chunks[dst].dst != -1:
                    path += f' -> {chunks[dst].surface()}'
                    dst = chunks[dst].dst

                path += f' | {chunks[dst].surface()}'

                print(path)


if __name__ == '__main__':
    # prepare()
    main()
