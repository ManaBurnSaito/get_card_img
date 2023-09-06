
# MTG 画像収集プログラム
マジック ザ・ギャザリングのリミテッド用画像を楽に収集するためのプログラム

クエリパラメーターのexpansionを変更することで楽にカード画像を収集することができます。
expansionに記載するのはセットの略号です。ex.MOM等

# クエリパラメータ
params = {
    "expansion": "WOE",
    "format": "PremierDraft",
    "start_data": "2019-01-01",
    "end_data": "2030-01-01"
}

同時にカード名：カード画像名が記載されたTSVファイルが生成されます。


収集した画像名のスペースは_に変換されます。
カード名：Tough Cookie　→ 画像名:Tough_Cookie

![2023111100383](https://github.com/ManaBurnSaito/get_card_img/assets/139425458/feb5f4c9-6901-4033-b2ff-cd619d51d323)
