# %%
import os
import sys
import requests
import json
import pandas as pd
from pandas import json_normalize


# ベースのURL
base_url = "https://www.17lands.com/card_ratings/data"

# クエリパラメータ
params = {
    "expansion": "WOE",
    "format": "PremierDraft",
    "start_data": "2019-01-01",
    "end_data": "2030-01-01"
}

# %%
def main():
    mk_dir_img()
    data = get_df(base_url, params)
    get_img(data)
    get_list_tsv(data)


def mk_dir_img() -> None:
    """プログラムがある場所に移動と同フォルダ内にimgフォルダの作成"""
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))  # カレントリディレクト移動、ファイルと同じ場所へ
    if not os.path.exists('img'):
        os.mkdir('img')


def get_df(base_url: str, params: dict[str, ...]) -> pd.DataFrame:
    """JSONデータの取得"""

    # クエリを結合してリクエストを送信
    response = requests.get(base_url, params=params)

    # レスポンスを処理
    if response.status_code == 200:
        # レスポンスの内容を取得
        json_data = json.loads(response.text)
        df = json_normalize(json_data)
        return df

    else:
        print(f"Request failed with status code {response.status_code}")
        sys.exit()


def get_list_tsv(df:pd.DataFrame) -> None:
    """JSONデータからカード名と画像名のtsv作成"""

    with open(f"name_list.tsv", 'w') as f:
        f.write(f'name\timg\n')
        for index, row in df.iterrows():
            name = row['name']
            img = name.replace(' ', '_') + '.jpg'
            f.write(f'{name}\t{img}\n')


def get_img(df:pd.DataFrame) -> None:
    """JSONデータのurlカラムから画像のＤＬ"""

    for index, row in df.iterrows():
        url = row['url']
        name = row['name']
        response = requests.get(url)

        if response.status_code == 200:
            new_name = name.replace(' ', '_') + '.jpg'
            with open(os.path.join("img",new_name), 'wb') as file:
                    file.write(response.content)
            print(f'Image {name} downloaded and saved as {new_name}.')

        else:
            # エラーハンドリング
            print(f'Failed to download image {name} with status code {response.status_code}')

if __name__ == "__main__":
    main()


