from flask import Flask, render_template, request
import json
import numpy as np 
import pandas as pd 
import os
import random
import copy

path_ratings="BX-Book-Ratings.csv"
path_books="BX-Books.csv"

app = Flask("Book Recommendations")

def load_data():
    df_ratings=pd.read_csv(path_ratings, on_bad_lines="warn", delimiter=";", encoding = "ISO-8859-1")
    df_ratings.dropna()
    df_ratings['ISBN'] = df_ratings['ISBN'].str.replace('[^\d]', '', regex=True)

    df_ratings = df_ratings.loc[df_ratings.duplicated(subset='User-ID', keep=False), :]

    df_books=pd.read_csv(path_books, on_bad_lines="skip", delimiter=";", encoding = "ISO-8859-1", dtype={"ISBN": "string", "Year-Of-Publication": "string"})
    df_books.dropna()
    df_books['ISBN'] = df_books['ISBN'].str.replace('[^\d]', '', regex=True)
    df_books = df_books.drop_duplicates(subset='ISBN')
    df_books_shorter = df_books.drop(['Publisher','Image-URL-S','Image-URL-M','Image-URL-L','Year-Of-Publication'],axis=1)
    return df_ratings, df_books_shorter

def full_name(isbn):
    book_name = df_books_shorter[df_books_shorter['ISBN']==isbn]['Book-Title']
    book_author = df_books_shorter[df_books_shorter['ISBN']==isbn]['Book-Author']
    if ((book_name.empty) or (book_author.empty)):
        return "", ""
    else:
        return book_name.iloc[0], book_author.iloc[0]

def build_dictionary_both(df_ratings):
    users = {}
    books = {}
    for index, row in df_ratings.iterrows():
        user = row['User-ID']
        isbn = row['ISBN']
        if (user in users.keys()):
            users[user].append(isbn)
        else:
            users[user] = [isbn]
        if (isbn in books.keys()):
            books[isbn].append(user)
        else:
            books[isbn] = [user]
    return books, users
    
def recomm_dict_without_ratings(books, users, isbn):
    videli_taky = {}
    if isbn in books.keys():
        videli_to = books[isbn]
        for user in videli_to:
            if user in users.keys():
                for book in users[user]:
                    if book != isbn:
                        if (book in videli_taky.keys()):
                            videli_taky[book] += 1
                        else: 
                            videli_taky[book] = 1
    else:    
        print("Insufficient data for a reliable recommendation. Your taste is unique.")
                    
    return videli_taky


def formulate_recom(isbn, both_books, both_users, df_books_shorter):
    recommend = recomm_dict_without_ratings(both_books, both_users, isbn)
    sorted_recom = sorted(recommend.items(), key=lambda x:x[1], reverse=True)

    max_recom = 5    # or 20, or...
    reasonable_amount = 5 # don't accept less people having seen this
    if sorted_recom:
        list_outputs = "We recommend: "
        i = 0
        for item in sorted_recom:
            isbn = item[0]
            pocet_lidi = item[1]
            if ((int(pocet_lidi) >= reasonable_amount) and (i < max_recom)):
                bname, bauthor = full_name(isbn)
                if (bname and bauthor):
                    list_outputs = list_outputs + bname + " by " + bauthor + ", "
                    i+=1
        list_outputs = list_outputs[:-2]
    else:
        list_outputs = "Insufficient data for a reliable recommendation. Your taste is unique."

    return list_outputs


@app.route("/RecommendBooks")
def RecommendBooks():
    ISBN = request.args.get('ISBN')
    list_outputs = formulate_recom(ISBN, both_books, both_users, df_books_shorter)
    return list_outputs

@app.route("/")
def renderIndexPage():
    return render_template("index.html")

df_ratings, df_books_shorter = load_data()
both_books, both_users = build_dictionary_both(df_ratings)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

#    df_ratings, df_books_shorter = load_data()
#    both_books, both_users = build_dictionary_both(df_ratings)

