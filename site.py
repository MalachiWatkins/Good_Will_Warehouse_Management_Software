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
import random
### Mong DB ###

warehouse_db = cluster["WAREHOUSE_MANAGEMENT"]
receiverCollection = warehouse_db["receiver"]

processorCollection = warehouse_db["processor"]
processor_revCollection = warehouse_db["processor_rev"]


jewleryCollection = warehouse_db["jewlery"]
jewlery_revCollection = warehouse_db["jewlery_rev"]


FINISHEDCollection = warehouse_db["FINISHED"]

Finished_JewlCollection = warehouse_db["FINISHED_JEWL"]
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
date_proc_format = str(today)
######################


def db_post(post, isJewlery):  # Receving Document
    if post['Storage_Type'] != '':
        if isJewlery == True:
            x=0
            while x < int(post['Quantity']):
                post['_id'] = random.random()
                jewleryCollection.insert_one(post)
                x+=1
        else:
            x=0
            while x < int(post['Quantity']):
                post['_id'] = random.random()
                receiverCollection.insert_one(post)
                x+=1
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
            '_id': random.random(),
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
        if request.form['summited'] == 'yes':
            ID = request.form['ID']
            STORAGE = request.form['STORAGE']
            CONTENTS = request.form['CONTENTS']
            DATE_RECEIVED = request.form['DATE_RECEIVED']
            STORE_NUMBER = request.form['STORE_NUMBER']
            MANIFEST_NUMBER = request.form['manifest_number_form']
            PROBLEMS = request.form['problem_form']
            DATE_PROSESSED = date_proc_format

            # Delete post
            delquery = { "_id": float(ID) }
            receiverCollection.delete_one(delquery)
            # add post to rev data
            New_Post = {
                '_id': random.random(),
                'Storage_Type': STORAGE,
                'Date_Received':date_proc_format,
                'Date_Processed': DATE_PROSESSED,
                'MANIFEST_NUMBER': MANIFEST_NUMBER,
                'Store_Number': STORE_NUMBER,
                'Contents': CONTENTS,
                'Problems': PROBLEMS,

            }
            processor_revCollection.insert_one(New_Post)
            date_selected = DATE_RECEIVED
            cat_selected = CONTENTS
            store_selected = STORE_NUMBER
        else:

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

        return template.render(data=proc_documents)
    return template.render()


@app.route('/proc_rev', methods=['POST', 'GET'])  # Reciving finished post
def proc_rev():
    template = jinja_env.get_template('proc_rev.html')
    REV_documents = processor_revCollection.find()
    if request.method == 'POST':
        ID = request.form['ID']
        STORAGE = request.form['STORAGE']
        CONTENTS = request.form['CONTENTS']
        DATE_RECEIVED = request.form['DATE_RECEIVED']
        STORE_NUMBER = request.form['STORE_NUMBER']
        MANIFEST_NUMBER = request.form['manifest_number_form']
        PROBLEMS = request.form['problem_form']
        DATE_PROSESSED = date_proc_format
        try:
            testing = request.form['test']
        except:
            testing = 'null'

        post = {
            '_id': random.random(),
            'Storage_Type': STORAGE,
            'Date_Received':date_proc_format,
            'Date_Processed': DATE_PROSESSED,
            'MANIFEST_NUMBER': MANIFEST_NUMBER,
            'Store_Number': STORE_NUMBER,
            'Contents': CONTENTS,
            'Problems': PROBLEMS,
        }
        if request.form["test"] == 'Undo Processing':
            proc_query = {"_id": float(ID)}
            delete_one = processor_revCollection.delete_one(proc_query)
            move = receiverCollection.insert_one(post)
            return template.render(data=REV_documents)
        else:
            proc_query = {"_id": float(ID)}
            delete_one = processor_revCollection.delete_one(proc_query)
            FINISHEDCollection.insert_one(post)
            return template.render(data=REV_documents)


    return template.render(data=REV_documents)




######################################################################
#################### Jewelry ########################################
######################################################################

@app.route('/jewl', methods=['POST', 'GET'])  # Reciving finished post
def jewl():
    template = jinja_env.get_template('jewl_main.html')
    return template.render(date=date_proc_format)


@app.route('/jewl_data', methods=['POST', 'GET'])  # Reciving finished post
def jewl_data():
    template = jinja_env.get_template('jewl_data.html')
    if request.method == 'POST':
        if request.form['summited'] == 'yes':
            ID = request.form['ID']
            STORAGE = request.form['STORAGE']
            CONTENTS = request.form['CONTENTS']
            DATE_RECEIVED = request.form['DATE_RECEIVED']
            STORE_NUMBER = request.form['STORE_NUMBER']
            MANIFEST_NUMBER = request.form['manifest_number_form']
            PROBLEMS = request.form['problem_form']
            DATE_PROSESSED = date_proc_format
            PROCESSED_BY = request.form['processed_by']
            SEAL_NUMBER = request.form['seal_number_form']
            # Delete post
            delquery = { "_id": float(ID) }
            jewleryCollection.delete_one(delquery)
            # add post to rev data
            New_Post = {
                '_id': random.random(),
                'Storage_Type': STORAGE,
                'Date_Received':date_proc_format,
                'Date_Processed': DATE_PROSESSED,
                'MANIFEST_NUMBER': MANIFEST_NUMBER,
                'Store_Number': STORE_NUMBER,
                'Contents': CONTENTS,
                'Problems': PROBLEMS,
                'Processed_By': PROCESSED_BY,
                'Seal_Number': SEAL_NUMBER,

            }
            jewlery_revCollection.insert_one(New_Post)
            date_selected = DATE_RECEIVED
            cat_selected = CONTENTS
            store_selected = STORE_NUMBER
        else:
                        delquery = { "_id": float(ID) }
                        jewleryCollection.delete_one(delquery)
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

        proc_documents = jewleryCollection.find(proc_query)

        return template.render(data=proc_documents)
    return template.render()


@app.route('/jewl_rev', methods=['POST', 'GET'])  # Reciving finished post
def jewl_rev():
    template = jinja_env.get_template('jewl_rev.html')
    REV_documents = jewlery_revCollection.find()
    if request.method == 'POST':
        ID = request.form['ID']
        STORAGE = request.form['STORAGE']
        CONTENTS = request.form['CONTENTS']
        DATE_RECEIVED = request.form['DATE_RECEIVED']
        STORE_NUMBER = request.form['STORE_NUMBER']
        MANIFEST_NUMBER = request.form['manifest_number_form']
        PROBLEMS = request.form['problem_form']
        DATE_PROSESSED = date_proc_format
        PROCESSED_BY = request.form['processed_by']
        SEAL_NUMBER = request.form['seal_number_form']
        try:
            testing = request.form['test']
        except:
            testing = 'null'

        post = {
            '_id': random.random(),
            'Storage_Type': STORAGE,
            'Date_Received':date_proc_format,
            'Date_Processed': DATE_PROSESSED,
            'MANIFEST_NUMBER': MANIFEST_NUMBER,
            'Store_Number': STORE_NUMBER,
            'Contents': CONTENTS,
            'Problems': PROBLEMS,
            'Processed_By': PROCESSED_BY,
            'Seal_Number': SEAL_NUMBER,

        }
        if request.form["test"] == 'Undo Processing':
            proc_query = {"_id": float(ID)}
            delete_one = jewlery_revCollection.delete_one(proc_query)
            jewleryCollection.insert_one(post)
            return template.render(data=REV_documents)
        else:
            proc_query = {"_id": float(ID)}
            delete_one = jewlery_revCollection.delete_one(proc_query)
            Finished_JewlCollection.insert_one(post)
            return template.render(data=REV_documents)


    return template.render(data=REV_documents)

@app.route('/view_jewlery_main', methods=['POST', 'GET'])  # Reciving finished post
def view_jewlery_main():
    template = jinja_env.get_template('jewl_view_main.html')
    return template.render()

@app.route('/view_jewlery', methods=['POST', 'GET'])  # Reciving finished post
def view():
    if request.method == 'POST':
        date = request.form['date_select']
        REV_documents = Finished_JewlCollection.find()
    template = jinja_env.get_template('jewlery_view.html')
    return template.render(data = REV_documents)

@app.route('/view_sgw_main', methods=['POST', 'GET'])  # Reciving finished post
def view_sgw_main():
    template = jinja_env.get_template('view_sgw_main.html')
    return template.render()

@app.route('/view_sgw', methods=['POST', 'GET'])  # Reciving finished post
def view_sgw():
    if request.method == 'POST':
        date = request.form['date_select']
        REV_documents = FINISHEDCollection.find()
    template = jinja_env.get_template('view_sgw.html')
    return template.render(data = REV_documents)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)

#   http://sponge.icarus.io/?date=(Date goes here in YYYY-MM-DD form)
