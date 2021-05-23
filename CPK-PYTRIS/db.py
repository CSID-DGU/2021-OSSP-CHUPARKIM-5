import os
import sys
import logging
import requests
import base64
import pymysql

host = "cpk.cq4jonxrld9g.us-east-2.rds.amazonaws.com"
port = 3306
username = "cpk"
database = "cpk"
password = "bananana"

def main():
    conn, cursor = connect_RDS(host, port, username, password, database)

    query = "INSERT INTO artist_genres (artist_id, genre) VALUE ('2345', 'rock')"
    cursor.execute(query)
    conn.commit()
    
    conn.close()

def connect_RDS(host, port, username, password, database):
    try:
        conn = pymysql.connect(host, user=username, passwd=password, db=database, port=port, use_unicode=True, charset='utf8')
        cursor = conn.cursor()
    except:
        logging.error("RDS에 연결X")
        sys.exit(1)
    return conn, cursor

if __name__ == "__main__":
    main()
