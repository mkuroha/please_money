import psycopg2

"""
How To Use
$ python manage_db.py -f c
$ python manage_db.py -f d -t payment
$ python manage_db.py -f i -t bank
"""


def create_db():
    """
    DB作成
    """
    conn = psycopg2.connect("dbname=please_money host=localhost user=postgres password=kurochan0917")
    cur = conn.cursor()
    
    # テーブルの作成
    # クレカ使用状況
    cur.execute("CREATE TABLE payment (id serial PRIMARY KEY, time timestamp, company_name varchar, cost integer, usage varchar, payment_type varchar)")
    # 銀行残高情報
    cur.execute("CREATE TABLE bank (id serial PRIMARY KEY, time timestamp, value integer, usage varchar)")
    
    conn.commit()  # 書き込みみたいな
    cur.close()
    conn.close()


def drop_table(table_name):
    """
    テーブルの削除
    """
    conn = psycopg2.connect("dbname=please_money host=localhost user=postgres password=kurochan0917")
    cur = conn.cursor()
    
    cur.execute("DROP TABLE %s;", (table_name, ))  # テーブルを削除


def initialize_db(table_name):
    """
    初期化
    """
    conn = psycopg2.connect("dbname=please_money host=localhost user=postgres password=kurochan0917")
    cur = conn.cursor()
    
    cur.execute("truncate %s;", (table_name,)) # 初期化（テーブルは残す）
    

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        prog='Please Money', # プログラム名
        usage='DB management', # プログラムの利用方法
        description='description', # 引数のヘルプの前に表示
        epilog='end', # 引数のヘルプの後で表示
        add_help=True, # -h/–help オプションの追加
    )
    parser.add_argument("-f", 'function')
    parser.add_argument("-t", 'table_name')
    args = parser.parse_args()
    
    if args.function=="c":
        create_db()
    elif args.function=="d":
        if args.table_name:
            drop_table(args.table_name)
        else:
            print("table_nameを指定してください")
    elif args.function=="i":
        if args.table_name:
            initialize_db(args.table_name)
        else:
            print("table_nameを指定してください")
    else:
        print("functionはc,d,i")