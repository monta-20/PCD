# import pandas as pd
# import mysql.connector
# def connectdb():
#     # Connect to the MySQL database
#     cnx = mysql.connector.connect(host='localhost', user='root', password='RabiaRabia123',
#                                   database='pcd')
#     cursor = cnx.cursor()
#     return cnx , cursor
#
# def commitdb(cnx , cursor):
#     # Commit the changes and close the connection
#     cnx.commit()
#     cursor.close()
#     cnx.close()
#
# cnx,cursor = connectdb()
# cursor.execute("""UPDATE ab
#                 SET news = 'Some news for this date'
#                 WHERE date = '2023-03-30';
#                 """)
# commitdb(cnx , cursor)








# hists["CLX"].index.min()
stock = "CLX"
# importing libraries and packages
import snscrape.modules.twitter as sntwitter
import pandas
from tqdm.notebook import tqdm

# # Creating list to append tweet data
# tweets_list = []
# # Using TwitterSearchScraper to scrape data and append tweets to list
# for i, tweet in tqdm(
#     enumerate(
#         sntwitter.TwitterSearchScraper(
#             f"${stock} since:2019-11-04 until:2022-11-02"
#         ).get_items()
#     ),
#     total=12_000,
# ):  # declare a username
#     if i > 12_000:  # number of tweets you want to scrape
#         break
#     tweets_list.append(
#         [tweet.date, tweet.id, tweet.content, tweet.user.username]
#     )  # declare the attributes to be returned
# # Creating a dataframe from the tweets list above
# print(tweets_list)


scraper = sntwitter.TwitterSearchScraper("#python")

for tweet in scraper.get_items():
   break

print(tweet)

