import sqlite3

def create_connection():
    # this method of connecting might cause a problem later, I tried getcwd but that didnt
    # work, I tried exact path, but that will cause problems with different systems.
    conn = sqlite3.connect(r'../spc/spcapi_calls_and_sorted_data.db', isolation_level=None)
    return conn


def cursor():
    conn = create_connection()
    return conn.cursor()


def create_table(artist_name):
    create_table_sql = f"""CREATE TABLE a{artist_name}_Songs(
                            page_number integer PRIMARY KEY, 
                            api_data text,
                            date_time text
                        );"""
    cursor().execute(create_table_sql)


def create_api_data(artist_name, api_data_and_datetime):
    sql = f"""INSERT INTO a{artist_name}_Songs (api_data, date_time) VALUES(?, ?)"""
    cursor().executemany(sql, api_data_and_datetime)


def delete_table(artist_name):
    cursor().execute(f"""DROP TABLE IF EXISTS a{artist_name}_Songs""")


def select_data_from_table(artist_name, data_to_select, table_suffix):
    cur = cursor()
    cur.execute(f"""SELECT {data_to_select} from a{artist_name}_{table_suffix}""")
    return cur.fetchall()
