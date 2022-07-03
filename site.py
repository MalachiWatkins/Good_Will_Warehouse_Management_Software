import requests
from flask import Flask, render_template, flash, url_for
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
processorCollection = warehouse_db["processor"]
processor_revCollection = warehouse_db["processor_rev"]
jewleryCollection = warehouse_db["jewlery"]
FINISHEDCollection = warehouse_db["FINISHED"]

### Add another route for view all and edit ####
##############

#### Flask Stuff #####

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
images_dir = os.path.join(os.path.dirname(__file__), 'images')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
app = Flask(__name__,
            static_folder="/static")
app.secret_key = 'WEIRD!'
app._static_folder = "/templates"

#######################

#### Global Vars ####

today = date.today()
date_format = today.strftime("%Y-%m-%d")
date_proc_format = today
######################


def db_post(post, isJewlery):  # Receving Document
    if post['Storage_Type'] != '':
        if isJewlery == True:
            jewleryCollection.insert_one(post)
        else:
            receiverCollection.insert_one(post)
    else:
        # DATA NOT SUBMITTED ROUTE GOES HERE
        null = 'null'
    return


@app.route('/')  # Landing Page
def main():
    template = jinja_env.get_template('Main.html')
    return template.render()


######################################################################
################## receiver ##########################################
######################################################################

@app.route('/rec', methods=['POST', 'GET'])  # Receving route
def rec():

    template = jinja_env.get_template('rec.html')

    if request.method == 'POST':
        QUANTITY = request.form['quant']
        STORAGE_TYPE = request.form['storage_type']
        STORE_NUMBER = request.form['store_number']
        ITEM_CONTENTS = request.form['item_contents']
        PROBLEM_FORM = request.form['problem_form']
        data_post = {
            'Quantity': QUANTITY,
            'Storage_Type': STORAGE_TYPE,
            'Date_Received': date_format,
            'Store_Number': STORE_NUMBER,
            'Contents': ITEM_CONTENTS,
            'Problems': PROBLEM_FORM,
        }
        if request.form['item_contents'] != 'Jewelry':
            db_post(post=data_post, isJewlery=False)
        else:
            db_post(post=data_post, isJewlery=True)

    return template.render()


@app.route('/rec_finished', methods=['POST', 'GET'])  # Reciving finished post
def rec_finished():
    template = jinja_env.get_template('rec_finished.html')
    return template.render()

######################################################################
#################### Processor #######################################
######################################################################


@app.route('/proc', methods=['POST', 'GET'])  # Reciving finished post
def proc_main():
    template = jinja_env.get_template('proc_main.html')
    return template.render(date=date_proc_format)


@app.route('/proc_data', methods=['POST', 'GET'])  # Reciving finished post
def proc_data():
    template = jinja_env.get_template('proc_data.html')
    if request.method == 'POST':
        date_selected = request.form['date_select']
        cat_selected = request.form['storage_type']
        store_selected = request.form['store_number']
        if cat_selected != "" and store_selected != "":
            proc_query = {"Date_Received": date_selected,
                          'Store_Number': store_selected, 'Contents': cat_selected}
        elif cat_selected != "" or store_selected != "":
            if cat_selected != "":
                proc_query = {"Date_Received": date_selected,
                              'Contents': cat_selected}
            else:
                proc_query = {"Date_Received": date_selected,
                              'Store_Number': store_selected}

        else:
            proc_query = {"Date_Received": date_selected}

        proc_documents = receiverCollection.find(proc_query)

        doc_list = []

        for doc in proc_documents:
            print(doc)
            x = 0
            quant_int = int(doc['Quantity'])
            while x < quant_int:
                doc_list.append(doc)
                x += 1
        print(doc_list)
        return template.render(data=doc_list)
    return template.render()


@app.route('/proc_rev', methods=['POST', 'GET'])  # Reciving finished post
def proc_rev():
    template = jinja_env.get_template('proc_rev.html')
    return template.render()


@app.route('/proc_finished', methods=['POST', 'GET'])  # Reciving finished post
def proc_finished():
    template = jinja_env.get_template('proc_finished.html')
    return template.render()

######################################################################
#################### Jewelry ########################################
######################################################################


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)

#   http://sponge.icarus.io/?date=(Date goes here in YYYY-MM-DD form)
