import sqlite3

DATABASE = 'database.db'

def create_table():
    con = sqlite3.connect(DATABASE)
    
    # 製造記録テーブルの作成
    con.execute("""
        CREATE TABLE IF NOT EXISTS ProductMaster (
            ProductNo TEXT PRIMARY KEY,
            MethodID INTEGER,
            resultA1 TEXT,
            resultA2 TEXT,
            resultA3 TEXT,
            resultB1 TEXT,
            resultB2 TEXT,
            resultB3 TEXT,
            FOREIGN KEY (MethodID) REFERENCES MethodMaster(MethodID)
        )
    """)
   

    # 製造方法テーブルの作成
    con.execute("""
        CREATE TABLE IF NOT EXISTS MethodMaster (
            MethodID INTEGER PRIMARY KEY,
            Process TEXT,
            condition1 TEXT,
            condition2 TEXT,
            condition3 TEXT
        )
    """)

   

    # 表示文字テーブルの作成
    con.execute("""
        CREATE TABLE IF NOT EXISTS ProcessText (
            Process TEXT PRIMARY KEY,
            Text1 TEXT,
            Text2 TEXT,
            Text3 TEXT
        )
    """)

    # コミットして接続を閉じる
    con.commit()
    con.close()

def INS_table():
    # データベースに接続
    con = sqlite3.connect(DATABASE)
    
    # 製造記録にデータを挿入
    Product_Ins = """
    INSERT INTO ProductMaster (ProductNo, MethodID) 
    VALUES ('001', 1), ('002', 2);
    """
    con.execute(Product_Ins)
   
    # 製造方法にデータを挿入
    Method_Ins = """
    INSERT INTO MethodMaster (MethodID, Process, condition1, condition2, condition3) 
    VALUES 
        (1, 'A', 'ConAa', 'ConAb', 'ConAc'),
        (2, 'A', 'ConAd', 'ConAe', 'ConAf');
    """
    con.execute(Method_Ins)
    
    # 表示文字にデータを挿入
    ProcessText_Ins = """
    INSERT INTO ProcessText (Process, Text1, Text2, Text3) 
    VALUES 
        ('A', 'Text A1', 'Text A2', 'Text A3');
    """
    con.execute(ProcessText_Ins)

    # コミットして接続を閉じる
    con.commit()
    con.close()