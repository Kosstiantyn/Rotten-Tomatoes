import requests
import pandas as pd
import sqlite3
from bs4 import BeautifulSoup

url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
db_name = "Rotten Tomatoes' Top 25.db"
table_name = "Top_25"
csv_path = "D:\\code\\python\\python_co\\rotten_tomatoes_project\\top_25.csv"
dataframe = pd.DataFrame(columns=["Film", "Year", "Rotten Tomatoes' Top 100"])
count = 0

html_page = requests.get(url).text
data = BeautifulSoup(html_page, "html.parser")

tables = data.find_all("tbody")
rows = tables[0].find_all("tr")

data_dict = {}
for row in rows:
   if count < 26:
      col = row.find_all("td")
      if len(col) != 0: 
         data_dict = {
				"Film": col[1].contents[0],
				"Year": col[2].contents[0],
				"Rotten Tomatoes' Top 100": col[3].contents[0],
			}
      dataframe1 = pd.DataFrame(data_dict, index=[0])
      dataframe = pd.concat([dataframe1, dataframe], ignore_index=True)
      count += 1
   else:
      break
   
print(dataframe)

dataframe.to_csv(csv_path)

conn = sqlite3.connect(db_name)
dataframe.to_sql(table_name, conn, if_exists="replace", index=False)
conn.close()
