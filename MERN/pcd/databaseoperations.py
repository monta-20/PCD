import pandas as pd
import mysql.connector
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import featureEnginnering as fe
import constants as ct
import pymysql
def connectdb():
    user = 'root'
    password = 'root123'
    host = 'localhost'
    database = 'pcd'
    connection = pymysql.connect(user=user, password=password, host=host, database=database)
    return connection
def commitdb(engine):
    # Commit the changes and close the connection
    engine.dispose()
def PutInDatabase(name):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(f'../investing data/{name}.csv')
    df = df.rename(
        columns={'Date': 'date', 'Dernier': 'close', 'Ouv.': 'open', ' Plus Haut': 'high', 'Plus Bas': 'low', 'Vol.': 'vol',
                 'Variation %': 'change'})
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
    # df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    # Define a list of column names to convert
    cols_to_convert = ['close', 'open' , 'high' , 'low']
    def convert_to_float(s):
        return float(s.replace(",", "."))
    # Apply the function to all elements in the DataFrame
    df[cols_to_convert] = df[cols_to_convert].applymap(convert_to_float)

    # Connect to the MySQL database
    cnx = mysql.connector.connect(host='localhost', user='root', password='root123',
                                  database='pcd')
    cursor = cnx.cursor()

    cursor.execute(f"DROP TABLE IF EXISTS {name}")

    cursor.execute(f"""create table {name}(
                    date date,
                    close float,
                    open float,
                    high float ,
                    low float
                    )""")

    # Insert the data into the MySQL table
    for row in df.itertuples():
        cursor.execute(f"INSERT INTO {name}  (date, close, open , high , low ) VALUES (%s, %s, %s , %s, %s )",
                       (row.date, row.close, row.open , row.high , row.low ))
    # Commit the changes and close the connection
    cnx.commit()
    cursor.close()
    cnx.close()
def Update(companyName, process ,updateName):
    deferred = process.crawl(updateName, companyName=companyName, process=process )
    # deferred.addBoth(lambda _: process.stop())
def UpdateAll(updateName , callback = None):
    process = CrawlerProcess(get_project_settings())
    for name in ct.allTableNames:
        Update(name, process, updateName)
    process.start()
    if callback:
        callback()
# UpdateAll(ct.updateNames[1])

def CollectNews(companyName, process):
    deferred = process.crawl("collectnews", companyName=companyName, process=process )
    # deferred.addCallback(lambda _: process.stop())
def CollectNewsAll():
    process = CrawlerProcess(get_project_settings())
    for name in ct.companyNames:
        CollectNews(name, process)
    process.start()
def NewsToVector(name, connection, nlp , days):
    if (days > 0 ):
        query = f"""SELECT *
                    FROM {name}
                    WHERE date >= (
                        SELECT MAX(date) - INTERVAL {days} DAY
                        FROM {name}
                    )
                    ORDER BY date Desc;
                """
    else:
        query = f"SELECT * FROM {name};"

    # Fetch data from the database
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [i[0] for i in cursor.description]

    df = pd.DataFrame(data, columns=columns)
    df['date'] = pd.to_datetime(df['date'])
    df['news_vectors'] = df['news'].apply(lambda new: fe.news_to_vector(new, nlp))

    # Update the table
    with connection.cursor() as cursor:
        for index, row in df.iterrows():
            update_query = f"UPDATE {name} SET news_vectors = '{row['news_vectors']}' WHERE date = '{row['date']}';"
            cursor.execute(update_query)
            connection.commit()
def NewsToVectorAll(days = 0):
    connection = connectdb()
    nlp = fe.LoadSpacyModel()
    for name in ct.companyNames:
        NewsToVector(name, connection, nlp , days)
    connection.close()
NewsToVectorAll(20)



























# def CollectNewsAll(companyNames):
#     process = CrawlerProcess(get_project_settings())
#     deferred = process.crawl(CollectNews, companyNames=companyNames)
#     deferred.addBoth(lambda _: process.stop())
#     process.start()
#
# CollectNewsAll(ct.companyNames)





# cnx,cursor = connectdb()
# # # for name in ct.companyNames :
# cursor.execute(f"""Select * from ab;""")
#
# data = cursor.fetchall()
# columns = [i[0] for i in cursor.description ]
# df = pd.DataFrame(data , columns = columns )
# df.to_csv( "E:", index=False)
# #
# # query = f"""SELECT news FROM biat
# #             where news is not Null
# #             ORDER BY date DESC; """
# # cursor.execute(query)
# # news_list = [[item for item in news[0].split("***") if item ] for news in cursor.fetchall()]
# # print(news_list)
# # print(sum(news_list, []))
# commitdb(cnx , cursor)


# process = CrawlerProcess(get_project_settings())
#
# CollectNews("USDTND", process)
# process.start()

# SELECT pcd.ab.* , pcd.dt.close AS dt
# FROM pcd.ab
# RIGHT JOIN pcd.dt
# ON pcd.dt.date = pcd.ab.date
# where pcd.ab.date IS NOT NULL
# ;


#
# DROP TABLE IF EXISTS DT;
# CREATE TABLE DT AS
# SELECT * FROM USD_TND2
# UNION
# SELECT * FROM USD_TND;