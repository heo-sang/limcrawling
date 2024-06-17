import mysql.connector
import dotenv 
import os

def create_database_and_table():
  dotenv.read_dotenv()
  try:
    # MySQL 서버에 연결
    mysql_connection = mysql.connector.connect(
      host=os.getenv('DATABASE_HOST'),
      user=os.getenv('DATABASE_USER'),
      password=os.getenv('DATABASE_PASSWORD'),
    )
    if mysql_connection.is_connected():
      cursor = mysql_connection.cursor()
      # 데이터베이스가 존재하지 않으면 생성
      cursor.execute("CREATE DATABASE IF NOT EXISTS limbuild")
      cursor.execute("USE limbuild")
      # 테이블이 존재하지 않으면 생성
      create_table_queries = [
            """
            CREATE TABLE IF NOT EXISTS special_keywords (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS basic_keywords (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS affiliation (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            )
            """
      ]

      for query in create_table_queries:
        cursor.execute(query)
      mysql_connection.commit()
  except mysql.connector.Error as e:
      print(f"Error: {e}")
  finally:
    # 연결 닫기
    if 'connection' in locals() and mysql_connection.is_connected():
      cursor.close()
      mysql_connection.close()

create_database_and_table()
