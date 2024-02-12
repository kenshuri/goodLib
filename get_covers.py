import os
import glob
import pandas as pd
import urllib.request

# Get Goodreads export from https://www.goodreads.com/review/import
books_data = pd.read_csv('goodreads_library_export.csv')
books_data = books_data.rename(columns=str.lower)
books_data = books_data.rename(
    columns={
        "my rating": "my_rating",
        "average rating": "gr_rating"
    })
books_data["date_read"] = pd.to_datetime(books_data["date read"], format = '%Y/%m/%d')
books_data = books_data[books_data["date_read"] >= "2020-01-01"]
books_data["isbn"] = books_data["isbn"].str.replace('=', '')
books_data["isbn"] = books_data["isbn"].str.replace('"', '')
books_data = books_data[["title", "author", "date_read", "my_rating", "gr_rating", "isbn"]]
books_data = books_data.sort_values("date_read", ascending=False)

# Get covers from openlibrary
for index, row in books_data.iterrows():
    isbn = row['isbn']
    if isbn:
        urllib.request.urlretrieve(f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg", f"covers/{isbn}-cover.jpg")

# Delete "empty covers"
all_covers = glob.glob('covers/*.jpg')
for c in all_covers:
     c_stat = os.stat(c)
     if c_stat.st_size < 1000:
         os.remove(c)

# Youtube code along
