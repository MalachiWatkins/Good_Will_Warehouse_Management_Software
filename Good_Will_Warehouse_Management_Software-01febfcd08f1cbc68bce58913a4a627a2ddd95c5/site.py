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

@app.route('/stats', methods=['POST', 'GET'])  # Reciving finished post
def stats():
    book_query = {"Contents": 'Books'}
    media_query = {"Contents": "Media"}
    sgw_query = {"Contents": "Collectables"}
    jewlery_query = {"Contents": "Jewelry"}

    total_not_added_to_spreadsheet_books = FINISHEDCollection.count_documents({"Contents": "Books"})
    total_not_added_to_spreadsheet_media = FINISHEDCollection.count_documents({"Contents": "Media"})
    total_not_added_to_spreadsheet_sgw = FINISHEDCollection.count_documents({"Contents": "Collectables"})
    total_not_added_to_spreadsheet_jewlery = Finished_JewlCollection.count_documents({"Contents": "Jewelry"})
    ## Total Left to process
    total_books_gay = receiverCollection.count_documents({"Contents": "Books", "Storage_Type":"Gaylord"})
    total_books_tote = receiverCollection.count_documents({"Contents": "Books", "Storage_Type":"Tote"})
    total_media_gay = receiverCollection.count_documents({"Contents": "Media", "Storage_Type":"Gaylord"})
    total_media_tote = receiverCollection.count_documents({"Contents": "Media", "Storage_Type":"Tote"})
    total_sgw_gay = receiverCollection.count_documents({"Contents": "Collectables", "Storage_Type":"Gaylord"})
    total_sgw_tote = receiverCollection.count_documents({"Contents": "Collectables", "Storage_Type":"Tote"})
    total_jewlery_gay = jewleryCollection.count_documents({"Contents": "Jewelry", "Storage_Type":"Gaylord"})
    total_jewlery_tote = jewleryCollection.count_documents({"Contents": "Jewelry", "Storage_Type":"Tote"})
    ### Processed But not submitted
    toat_review_books = processor_revCollection.count_documents({"Contents": "Books"})
    toat_review_media = processor_revCollection.count_documents({"Contents": "Media"})
    toat_review_jewlery = jewlery_revCollection.count_documents({"Contents": "Jewelry"})
    toat_review_sgw = processor_revCollection.count_documents({"Contents": "Collectables"})

    Total_to_process_gay = total_books_gay + total_media_gay + total_sgw_gay + total_jewlery_gay
    Total_to_process_tote =  total_books_tote + total_media_tote + total_sgw_tote + total_jewlery_tote
    total_to_review = toat_review_books + toat_review_media + toat_review_jewlery + toat_review_sgw
    total_ready_for_logging = total_not_added_to_spreadsheet_books + total_not_added_to_spreadsheet_media + total_not_added_to_spreadsheet_sgw + total_not_added_to_spreadsheet_jewlery

    template = jinja_env.get_template('count.html')
    return template.render(tgtp=Total_to_process_gay, tttp=Total_to_process_tote , ttr=total_to_review, trfl=total_ready_for_logging, sgwTGTP = total_sgw_gay, sgwTTTP = total_sgw_tote, sgwTTR = toat_review_sgw, sgwTRFL=total_not_added_to_spreadsheet_sgw,
    jewlTGTP=total_jewlery_gay, jewlTTTP=total_jewlery_tote,jewlTTR=toat_review_jewlery, jewlTRFL=total_not_added_to_spreadsheet_jewlery,
    bookTGTP=total_books_gay,bookTTTP=total_books_tote, bookTTR=toat_review_books,bookTRFL=total_not_added_to_spreadsheet_books,
    medTGTP=total_media_gay,medTTTP=total_media_tote, medTTR= toat_review_media, medTRFL=total_not_added_to_spreadsheet_media)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=1024)

#   http://sponge.icarus.io/?date=(Date goes here in YYYY-MM-DD form)