# %%
import os
import sys
import requests
import json
import pandas as pd
from pandas import json_normalize


#変更する箇所
SET1 = "WOE" #DLしたいセット
SET2 = "WOT" #追加するセット。ない場合は""にして空を入れる。
LANG = "en" #"jp" 言語

# ベースのURL
base_url = "https://api.scryfall.com/cards/search"

# クエリパラメータ
params = {
    #"format": "csv",
    "q": f"lang:{LANG} set:{SET1}+{SET2}"
}

# %%
def main():
    mk_dir_img()
    df_list = get_df(base_url, params)
    get_image_uris(df_list)
    get_list_tsv(df_list)


def mk_dir_img() -> None:
    """プログラムがある場所に移動と同フォルダ内にimgフォルダの作成"""
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))  # カレントリディレクト移動、ファイルと同じ場所へ
    if not os.path.exists('img'):
        os.mkdir('img')


def get_df(base_url: str, params: dict[str, ...]) -> list:
    """JSONデータの取得"""

    # クエリを結合してリクエストを送信
    response = requests.get(base_url, params=params)

    # レスポンスを処理
    if response.status_code == 200:
        # レスポンスの内容を取得
        json_data = json.loads(response.text)
        data = json_data['data']
        
        while json_data['has_more'] == True:
            response = requests.get(json_data['next_page'])
            if response.status_code == 200:
                json_data = json.loads(response.text)
                data += json_data['data']

        normalized_data = pd.json_normalize(data)
        normalized_data.to_csv(f"{SET1}_fall.tsv", sep='\t', index=True)
        normalized_data.to_csv(f"{SET1}_fall.csv", index=True)
        return data

    else:
        print(f"Request failed with status code {response.status_code}")
        sys.exit()


def get_list_tsv(df:list) -> None:
    """JSONデータからカード名と画像名のtsv作成"""

    with open(f"Aname_list.tsv", 'w') as f:
        f.write(f'name\timg\n')
        for i in df:
            name = i['name'].split('//')[0]
            new_name = name.replace(' ', '_') + '.png'
            f.write(f'{name}\t{new_name}\n')


def get_image_uris(df:list) -> None:
    """JSON→リストのimage_urisをアンパックしてimgをDL"""
    
    for i in df:
        response = requests.get(i['image_uris']['png'])
        name = i['name'].split('//')[0]

        if response.status_code == 200:
            new_name = name.replace(' ', '_') + '.png'
            with open(os.path.join("images",new_name), 'wb') as file:
                    file.write(response.content)
            print(f'Image {name} downloaded and saved as {new_name}.')

        else:
            # エラーハンドリング
            print(f'Failed to download image {name} with status code {response.status_code}')


if __name__ == "__main__":
    main()
# %%
