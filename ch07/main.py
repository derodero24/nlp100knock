''' 第7章: データベース
artist.json.gzは，オープンな音楽データベースMusicBrainzの中で，アーティストに関するものをJSON形式に変換し，gzip形式で圧縮したファイルである．このファイルには，1アーティストに関する情報が1行にJSON形式で格納されている．JSON形式の概要は以下の通りである．（info.csv, info.jpg参照）
artist.json.gzのデータをKey-Value-Store (KVS) およびドキュメント志向型データベースに格納・検索することを考える．KVSとしては，LevelDB，Redis，KyotoCabinet等を用いよ．ドキュメント志向型データベースとして，MongoDBを採用したが，CouchDBやRethinkDB等を用いてもよい．
'''
import leveldb


def main():
    ''' 60. KVSの構築
    Key-Value-Store (KVS) を用い，アーティスト名（name）から活動場所（area）を
    検索するためのデータベースを構築せよ．
    '''
    import gzip
    import json

    # データベース読み込み（無ければ新規作成）
    db = leveldb.LevelDB('music_db')

    with gzip.open('artist.json.gz', 'r') as data_file:
        for line in data_file:
            data_json = json.loads(line)
            key = f'{data_json["name"]}_{str(data_json["id"])}'
            value = data_json.get('area', '')
            db.Put(key.encode(), value.encode())

def main():
    ''' 61. KVSの検索
    60で構築したデータベースを用い，特定の（指定された）アーティストの活動場所を取得せよ．
    '''
    import re
    db = leveldb.LevelDB('music_db')
    # clue = input('アーティスト名を入力してください--> ')
    pattern = re.compile(r'^(.*)_(\d+)$')

    clue = '嵐'

    for key, value in db.RangeIter(key_from=(clue + '_').encode()):

        # keyをnameとidに戻す
        match = pattern.match(key.decode())
        name = match.group(1)
        id = match.group(2)

        # 異なるアーティストになったら終了
        if name != clue:
            break

        # 活動場所のチェック、表示
        area = value.decode()
        if area != '':
            print('{}(id:{})の活動場所:{}'.format(name, id, area))
        else:
            print('{}(id:{})の活動場所は登録されていません'.format(name, id))
        hit = True

    if not hit:
        print('{}は登録されていません'.format(clue))


    ''' 62. KVS内の反復処理
    60で構築したデータベースを用い，活動場所が「Japan」となっているアーティスト数を求めよ．
    '''

    ''' 63. オブジェクトを値に格納したKVS
    KVSを用い，アーティスト名（name）からタグと被タグ数（タグ付けされた回数）のリストを検索するためのデータベースを構築せよ．さらに，ここで構築したデータベースを用い，アーティスト名からタグと被タグ数を検索せよ．
    '''

    ''' 64. MongoDBの構築
    アーティスト情報（artist.json.gz）をデータベースに登録せよ．さらに，次のフィールドでインデックスを作成せよ: name, aliases.name, tags.value, rating.value
    '''

    ''' 65. MongoDBの検索
    MongoDBのインタラクティブシェルを用いて，"Queen"というアーティストに関する情報を取得せよ．さらに，これと同様の処理を行うプログラムを実装せよ．
    '''

    ''' 66. 検索件数の取得
    MongoDBのインタラクティブシェルを用いて，活動場所が「Japan」となっているアーティスト数を求めよ．
    '''

    ''' 67. 複数のドキュメントの取得
    特定の（指定した）別名を持つアーティストを検索せよ．
    '''

    ''' 68. ソート
    "dance"というタグを付与されたアーティストの中でレーティングの投票数が多いアーティスト・トップ10を求めよ．
    '''

    ''' 69. Webアプリケーションの作成
    ユーザから入力された検索条件に合致するアーティストの情報を表示するWebアプリケーションを作成せよ．アーティスト名，アーティストの別名，タグ等で検索条件を指定し，アーティスト情報のリストをレーティングの高い順などで整列して表示せよ．
    '''


if __name__ == '__main__':
    main()
