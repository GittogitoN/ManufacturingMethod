from flaskr import app
from flask import render_template,request,redirect,url_for
import sqlite3
DATABASE='database.db'

def get_db_data(product_no=None, process=None):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # 条件をselectする
        select_condition = """
        SELECT condition1, condition2, condition3 
        FROM MethodMaster 
        WHERE Process = ? AND MethodID = (
            SELECT MethodID 
            FROM ProductMaster 
            WHERE ProductNo = ?
        );
        """
        cursor.execute(select_condition, (process, product_no))  # SQL文とパラメータを渡す
        conditions = cursor.fetchall()  # [(condition1, condition2, condition3), ...]

        # 項目をselectする
        select_text = """
        SELECT Text1, Text2, Text3
        FROM ProcessText 
        WHERE Process = ?;
        """
        cursor.execute(select_text, (process,))  # SQL文とパラメータを渡す
        texts = cursor.fetchall()  # [(Text1, Text2, Text3), ...]
        conn.close()
        return conditions,texts

    except sqlite3.Error as e:
        print(f"SQLite Error: {e}")
        return {'conditions_texts': []}  # エラー時は空のリストを返す

# メインページ（製品番号でフィルタリング）
@app.route('/', methods=['GET', 'POST'])
def index():
    # URLのクエリパラメータから製品番号とプロセスを取得
    product_no = request.args.get('product_no')  # 製品番号を取得
    process = request.args.get('process', 'A')  # processパラメータを取得、デフォルトは 'A'

    # 製品番号とプロセスに基づいてデータを取得
    conditions,texts= get_db_data(product_no, process)
    x=len(texts[0])
    numbers = list(range(x))
   
    
    
    # HTMLに条件を渡してレンダリング
    return render_template('index.html', conditions=conditions, texts=texts,numbers=numbers,product_no=product_no)  # contextを展開して渡す

@app.route('/save_record', methods=['POST'])
def save_record():
    # フォームから送信されたデータを取得
    print(request.form)

    #値を取り出す
    resultA_keys = [key for key, value in request.form.items() if key.startswith('resultA')]
    resultA_vals = [value for key, value in request.form.items() if key.startswith('resultA')]
    product_no = request.form.get('product_no', '')

    #SQLを作成
    UPD_result1="UPDATE ProductMaster SET "
    UPD_result2=""
    # resultA_keys と resultA_vals を使って SET部分を動的に作成
    for i, key in enumerate(resultA_keys):
        UPD_result2 += f"{key} = '{resultA_vals[i]}',"

    # 最後のカンマを削除
    UPD_result2 = UPD_result2[:-1]

    # 最終的なUPDATE文を作成
    UPD_result = f"{UPD_result1} {UPD_result2} WHERE ProductNo = '{product_no}'"

    conn = sqlite3.connect(DATABASE)  # データベース名を適宜変更
    cursor = conn.cursor()
    cursor.execute(UPD_result)  # SQL文の実行
    conn.commit()  # 変更を保存
    conn.close()  # 接続を閉じる  


    return render_template('index.html')
