from flask import Flask, request, render_template, Response, send_file, redirect, url_for
import pymongo
import pandas as pd
import os
from threading import Thread
import time
import json

# Connect to MongoDB
MONGODB = pymongo.MongoClient('192.168.1.16', 27017)
DATABASE_IN_MONGODB = MONGODB["recruitment_crawler"]

data_employment = list()
data_greenjapan = list()
data_nextrikunabi = list()
data_tenshoku = list()
time_crawl1 = list()
time_crawl2 = list()
time_crawl3 = list()
time_crawl4 = list()

def load_mongodb():
    global data_employment
    global data_greenjapan
    global data_nextrikunabi
    global data_tenshoku
    global time_crawl1
    global time_crawl2
    global time_crawl3
    global time_crawl4

    while True:
        time_crawl1 = list(DATABASE_IN_MONGODB["crawlTime"].find({"item":"Employment"},{"_id":0}))
        time.sleep(2)
        data_employment = list(DATABASE_IN_MONGODB["employment"].find({},{"_id":0}))
        time.sleep(2)
        df = pd.DataFrame(data_employment)
        time.sleep(2)
        df.to_excel("excel_data/employment.xlsx")
        time.sleep(2)

        time_crawl2 = list(DATABASE_IN_MONGODB["crawlTime"].find({"item": "Greenjapan"}, {"_id": 0}))
        time.sleep(2)
        data_greenjapan = list(DATABASE_IN_MONGODB["greenjapan"].find({},{"_id":0}))
        time.sleep(2)
        df = pd.DataFrame(data_greenjapan)
        time.sleep(2)
        df.to_excel("excel_data/greenjapan.xlsx")
        time.sleep(2)

        time_crawl3 = list(DATABASE_IN_MONGODB["crawlTime"].find({"item": "Nextrikunabi"}, {"_id": 0}))
        time.sleep(2)
        data_nextrikunabi = list(DATABASE_IN_MONGODB["nextrikunabi"].find({},{"_id":0}))
        time.sleep(2)
        df = pd.DataFrame(data_nextrikunabi)
        time.sleep(2)
        df.to_excel("excel_data/nextrikunabi.xlsx")
        time.sleep(2)

        time_crawl4 = list(DATABASE_IN_MONGODB["crawlTime"].find({"item": "Tenshoku"}, {"_id": 0}))
        time.sleep(2)
        data_tenshoku = list(DATABASE_IN_MONGODB["tenshoku"].find({},{"_id":0}))
        time.sleep(2)
        df = pd.DataFrame(data_tenshoku)
        time.sleep(2)
        df.to_excel("excel_data/tenshoku.xlsx")
        time.sleep(600)

if __name__ == '__main__':
    t1 = Thread(target=load_mongodb)
    t1.start()

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def home():
    return render_template("item.html")

@app.route('/data_employment', methods=['POST','GET'])
def data_employment():
    global data_employment
    global time_crawl1

    def download():
        df = pd.DataFrame(data_employment)
        df.to_excel("excel_data/employment.xlsx")

        return send_file("./excel_data/employment.xlsx",
                        mimetype = 'text/xlsx',
                        attachment_filename = "employment.xlsx",
                        as_attachment = True)

    if request.method == 'POST':
        if request.form['button'] == 'download': return download()
    else:
        return render_template("data_employment.html", data_col = data_employment, time_col = time_crawl1)

@app.route('/data_greenjapan', methods=['POST','GET'])
def data_greenjapan():
    global data_greenjapan
    global time_crawl2

    def download():
        df = pd.DataFrame(data_greenjapan)
        df.to_excel("excel_data/greenjapan.xlsx") 

        return send_file("./excel_data/greenjapan.xlsx",
                        mimetype = 'text/xlsx',
                        attachment_filename = "greenjapan.xlsx",
                        as_attachment = True)

    if request.method == 'POST':
        if request.form['button'] == 'download': return download()
    else:
        return render_template("data_greenjapan.html", data_col = data_greenjapan,time_col = time_crawl2)

@app.route('/data_nextrikunabi', methods=['POST','GET'])
def data_nextrikunabi():
    global data_nextrikunabi
    global time_crawl3

    def download():
        df = pd.DataFrame(data_nextrikunabi)
        df.to_excel("excel_data/nextrikunabi.xlsx") 

        return send_file("./excel_data/nextrikunabi.xlsx",
                        mimetype = 'text/xlsx',
                        attachment_filename = "nextrikunabi.xlsx",
                        as_attachment = True)

    if request.method == 'POST':
        if request.form['button'] == 'download': return download()
    else:
        return render_template("data_nextrikunabi.html", data_col = data_nextrikunabi,time_col = time_crawl3)

@app.route('/data_tenshoku', methods=['POST','GET'])
def data_tenshoku():
    global data_tenshoku
    global time_crawl4

    def download():
        df = pd.DataFrame(data_tenshoku)
        df.to_excel("excel_data/tenshoku.xlsx") 

        return send_file("./excel_data/tenshoku.xlsx",
                        mimetype = 'text/xlsx',
                        attachment_filename = "tenshoku.xlsx",
                        as_attachment = True)

    if request.method == 'POST':
        if request.form['button'] == 'download': return download()
    else:
        return render_template("data_tenshoku.html", data_col = data_tenshoku,time_col = time_crawl4)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port="9999")