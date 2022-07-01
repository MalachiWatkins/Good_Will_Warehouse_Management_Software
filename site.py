import requests
from flask import Flask, render_template , flash, url_for
from flask import request
import os
import jinja2
import cgi
import webbrowser
from datetime import date
from pymongo import MongoClient
import pymongo
### Mong DB ###


warehouse_db = cluster["WAREHOUSE_MANAGEMENT"]
receiverCollection = warehouse_db["receiver"]

##############

#### Flask Stuff #####

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
images_dir = os.path.join(os.path.dirname(__file__), 'images')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))
app = Flask(__name__,
static_folder="/static")
app.secret_key = 'WEIRD!'
app._static_folder = "/templates"

#######################

#### Global Vars ####

today = date.today()
date_format = today.strftime("%m/%d/%Y")

######################


def rec_post(post): # Receving Document
    if post['Storage_Type'] != 'Storage Type':
        receiverCollection.insert_one(post)
    else:
        # DATA NOT SUBMITTED ROUTE GOES HERE
        null = 'null'
    return

@app.route('/') # Landing Page
def main():
    template = jinja_env.get_template('Main.html')
    return template.render()

@app.route('/rec', methods = ['POST', 'GET']) # Receving route
def rec():

    template = jinja_env.get_template('rec.html')

    if request.method == 'POST':
        QUANTITY = request.form['quant']
        STORAGE_TYPE = request.form['storage_type']
        STORE_NUMBER = request.form['store_number']
        ITEM_CONTENTS = request.form['item_contents']
        PROBLEM_FORM = request.form['problem_form']
        receiver_post = {
            'Quantity': QUANTITY,
            'Storage_Type': STORAGE_TYPE,
            'Date_Received': date_format,
            'Store_Number': STORE_NUMBER,
            'Contents': ITEM_CONTENTS,
            'Problems': PROBLEM_FORM,
            }
        rec_post(post=receiver_post)
        return template.render()
    return template.render()

@app.route('/rec_finished',methods = ['POST', 'GET']) # Reciving finished post
def rec_finished():
    template = jinja_env.get_template('rec_finished.html')
    return template.render()

if __name__ == '__main__':
        app.run(debug=True, host="0.0.0.0", port=80)

#   http://sponge.icarus.io/?date=(Date goes here in YYYY-MM-DD form)
