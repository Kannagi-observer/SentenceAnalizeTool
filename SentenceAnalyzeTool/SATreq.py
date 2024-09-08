import requests as req
from requests.exceptions import ConnectionError
import json
import csv


def analyze(sentence , filename = "" , ext = "csv"):
    data = { "sentence" : sentence }
    post_data = json.dumps(data)
    
    try:
        response = req.post("http://127.0.0.1:8000/analyze" , data = post_data , timeout = (3.0 , 7.0)).json()
        #response = req.post("http://sakanadayo.f5.si/analyze" , data = post_data , timeout = (3.0 , 7.0)).json() #jsonファイルからlistに戻す際に三次元配列になっている
        uuid = response.pop(-1) #uuidを取得してファイル作成をサーバー側で行うのもあり

        result = []
        for i in range(len(response[0])):
            result.append(response[0][i])
        
        if(filename == ''):
            return result
            
        else:
            name = filename + "." + ext
            
            try:
                with open(name , mode = 'x' , encoding = 'utf-8' , newline = '') as f:
                    writer = csv.writer(f , quoting = csv.QUOTE_NONNUMERIC)
                    for i in range(len(result)):
                        writer.writerow(result[i])
                        
            except FileExistsError as F:
                print(f"そのファイルは既に存在しています : {F}")
                
            finally:
                return result
        
    except req.exceptions.ConnectionError as e:
        print(f"接続に失敗しました : {e}")
        return None

def help():
    print("このライブラリは、SAT(SentenceAnalyzingTool)呼び出し用のライブラリです。")
    print("Pythonに移植されたMeCabが古いVerのPythonでしか動かないため、APIサーバー経由で文章解析プログラムを利用できるようにしました。")
    print("使用してるサーバーやプロキシがダウンしてる時は利用できないです、ごめんなさい。")
    print("---Includes---\n",sep = '')
    print("""analyze( "sentence" , ["filename"] , ["ext"] )\n""",sep = '')
    print("\tsentence...解析する文章、解析エンジンの関係で数値や半角カタカナを示す語を入れるとバグるときがあります(対策中)\n")
    print("\tfilename...ファイルで出力する場合の名前、名前を指定するとファイルでも出力されます\n")
    print("\text...出力されるファイルの形式、デフォルトはcsv\n")

