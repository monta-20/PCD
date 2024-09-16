# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
import pandas as pd
from .items import PcdItem
from scrapy.exceptions import DropItem

SEPARATING_UNIT="***"

class DBConnection:

    def __init__(self):
        self.connectdb()

    def connectdb(self):
        # Connect to the MySQL database
        self.cnx = mysql.connector.connect(host='localhost', user='root', password='root123', database='pcd')
        self.cursor = self.cnx.cursor()

    def closedb(self):
        self.cnx.commit()
        self.cursor.close()
        self.cnx.close()

class PcdPipeline:
    def __init__(self):
        self.db = DBConnection()


    def insert(self , item):
        df = pd.DataFrame.from_dict(dict(item))
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
        cols_to_convert = ['close', 'open', 'high', 'low']

        def convert_to_float(s):
            return float(s.replace(",", "."))

        # Apply the function to all elements in the DataFrame
        df[cols_to_convert] = df[cols_to_convert].applymap(convert_to_float)
        print(df)

        query = f"""INSERT INTO {item.get('companyName')} (date, close, open, high, low) 
        VALUES (%s, %s, %s, %s, %s) as v
        ON DUPLICATE KEY UPDATE close=v.close, open=v.open, high=v.high, low=v.low"""
        data = []
        for index, row in df.iterrows():
            data.append((row['date'], row['close'], row['open'], row['high'], row['low']))
        self.db.cursor.executemany(query, data)
        self.db.closedb()
    def process_item(self, item, spider):
        if isinstance(item, PcdItem):
            self.insert(item)
        else:
            # Drop the item if it's not a PcdItem
            raise DropItem()
        return item

class NewsPipeline:
    def __init__(self):
        self.db = DBConnection()

    def insert(self, item):
        df = pd.DataFrame.from_dict(dict(item))
        # Define a function to extract the date part
        def extract_date(datetime_str):
            return datetime_str.split()[0]

        # Apply the function to the 'date' column
        df['date'] = df['date'].apply(extract_date)
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y')

        print( df)
        query = f"""INSERT INTO {item.get('companyName')} (date, news) 
               VALUES (%s, %s) as v
               ON DUPLICATE KEY UPDATE news = IF(COALESCE({item.get('companyName')}.news, '') LIKE CONCAT('%', v.news, '%'), {item.get('companyName')}.news, CONCAT(COALESCE({item.get('companyName')}.news, ''), '{SEPARATING_UNIT}', v.news))"""
        data = []
        for index, row in df.iterrows():
            data.append((row['date'], row['news']))
        self.db.cursor.executemany(query, data)
        self.db.closedb()



    def process_item(self, item, spider):

        self.db = DBConnection()
        self.insert(item)

        return item
