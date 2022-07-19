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
# TODO:   Add all of Feature Request, Create DB Transfer Script, and test Funconality, add name drop down, option for no store number add total gaylord and totes to the top of processing
# Add Statistics page
# for Ceo: All inventory
# for Gary: only Processed Info with issues
# stores both processed and unprocessed

warehouse_db = cluster["WAREHOUSE_MANAGEMENT_Test"]  # GOODWILL
Truck_Receiver_DB = warehouse_db["Truck_Receiver_DB"]

Processor_Review_DB = warehouse_db["Processor_Review_DB"]


Jewelry_DB = warehouse_db["Jewelry_DB"]
Jewelry_Review_DB = warehouse_db["Jewelry_Review_DB"]

Books_Media_DB = warehouse_db["Books_Media_DB"]
Book_Media_Review_DB = warehouse_db["Book_Media_Review_DB"]

Finished_DB = warehouse_db["Finished_DB"]

Finished_Jewlery_DB = warehouse_db["Finished_Jewlery_DB"]
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


def db_post(post, isJewlery, isBooks, isSGW):  # Receving Document
    if post['Storage_Type'] != '':
        if isJewlery == True and isBooks == False and isSGW == False:
            x = 0
            while x < int(post['Quantity']):
                post['_id'] = random.random()
                Jewelry_DB.insert_one(post)
                x += 1
        elif isJewlery == False and isBooks == True and isSGW == False:
            x = 0
            while x < int(post['Quantity']):
                post['_id'] = random.random()
                Books_Media_DB.insert_one(post)
                x += 1
        else:
            x = 0
            while x < int(post['Quantity']):
                post['_id'] = random.random()
                Truck_Receiver_DB.insert_one(post)
                x += 1
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
        if request.form['item_contents'] == 'Jewelry':
            db_post(post=data_post, isJewlery=True, isBooks=False, isSGW=False)
        elif request.form['item_contents'] == 'Books':
            db_post(post=data_post, isJewlery=False, isBooks=True, isSGW=False)
        else:
            db_post(post=data_post, isJewlery=False, isBooks=False, isSGW=True)

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
            PROCESSED_BY = request.form['processed_by']

            # Delete post
            delquery = {"_id": float(ID)}
            Truck_Receiver_DB.delete_one(delquery)
            # add post to rev data
            New_Post = {
                '_id': random.random(),
                'Storage_Type': STORAGE,
                'Date_Received': date_proc_format,
                'Date_Processed': DATE_PROSESSED,
                'MANIFEST_NUMBER': MANIFEST_NUMBER,
                'Store_Number': STORE_NUMBER,
                'Contents': CONTENTS,
                'Problems': PROBLEMS,
                'Processed_By': PROCESSED_BY,
            }
            Finished_DB.insert_one(New_Post)
            date_selected = DATE_RECEIVED
            cat_selected = CONTENTS
            store_selected = STORE_NUMBER
        else:
            cat_selected = request.form['storage_type']
            store_selected = request.form['store_number']
            storage_selected = request.form['storage_type_1']

        storage_selected = request.form['storage_type_1']
        if cat_selected != "" and store_selected != "":
            proc_query = {'Store_Number': store_selected, 'Storage_Type': storage_selected,
                          'Contents': cat_selected}
        elif cat_selected != "" or store_selected != "":
            if cat_selected != "":
                proc_query = {'Contents': cat_selected,
                              'Storage_Type': storage_selected, }
            else:
                proc_query = {'Store_Number': store_selected,
                              'Storage_Type': storage_selected, }

        proc_documents = Truck_Receiver_DB.find(proc_query)
        document_count = Truck_Receiver_DB.count_documents(proc_query)
        return template.render(data=proc_documents, total=document_count, type=storage_selected)
    return template.render()


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
            delquery = {"_id": float(ID)}
            Jewelry_DB.delete_one(delquery)
            # add post to rev data
            New_Post = {
                '_id': random.random(),
                'Storage_Type': STORAGE,
                'Date_Received': date_proc_format,
                'Date_Processed': DATE_PROSESSED,
                'MANIFEST_NUMBER': MANIFEST_NUMBER,
                'Store_Number': STORE_NUMBER,
                'Contents': CONTENTS,
                'Problems': PROBLEMS,
                'Processed_By': PROCESSED_BY,
                'Seal_Number': SEAL_NUMBER,

            }
            Finished_Jewlery_DB.insert_one(New_Post)
            date_selected = DATE_RECEIVED
            cat_selected = CONTENTS
            store_selected = STORE_NUMBER
        else:

            cat_selected = request.form['storage_type']
            store_selected = request.form['store_number']

        if cat_selected != "" and store_selected != "":
            proc_query = {
                'Store_Number': store_selected, 'Contents': cat_selected}
        elif cat_selected != "" or store_selected != "":
            if cat_selected != "":
                proc_query = {'Contents': cat_selected}
            else:
                proc_query = {'Store_Number': store_selected}

        proc_documents = Jewelry_DB.find(proc_query)
        document_count = Jewelry_DB.count_documents(proc_query)
        return template.render(data=proc_documents, total=document_count, type=storage_selected)
    return template.render()


############################################


@app.route('/books', methods=['POST', 'GET'])  # Reciving finished post
def books():
    template = jinja_env.get_template('books_main.html')
    return template.render(date=date_proc_format)


@app.route('/books_data', methods=['POST', 'GET'])  # Reciving finished post
def books_data():
    template = jinja_env.get_template('books_data.html')
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

            # Delete post
            delquery = {"_id": float(ID)}
            Books_Media_DB.delete_one(delquery)
            # add post to rev data
            New_Post = {
                '_id': random.random(),
                'Storage_Type': STORAGE,
                'Date_Received': date_proc_format,
                'Date_Processed': DATE_PROSESSED,
                'MANIFEST_NUMBER': MANIFEST_NUMBER,
                'Store_Number': STORE_NUMBER,
                'Contents': CONTENTS,
                'Problems': PROBLEMS,
                'Processed_By': PROCESSED_BY,
            }
            Finished_DB.insert_one(New_Post)
            date_selected = DATE_RECEIVED
            cat_selected = CONTENTS
            store_selected = STORE_NUMBER
        else:
            cat_selected = request.form['storage_type']
            store_selected = request.form['store_number']
            storage_selected = request.form['storage_type_1']

        storage_selected = request.form['storage_type_1']
        if cat_selected != "" and store_selected != "":
            proc_query = {'Store_Number': store_selected, 'Storage_Type': storage_selected,
                          'Contents': cat_selected}
        elif cat_selected != "" or store_selected != "":
            if cat_selected != "":
                proc_query = {'Contents': cat_selected,
                              'Storage_Type': storage_selected, }
            else:
                proc_query = {'Store_Number': store_selected,
                              'Storage_Type': storage_selected, }

        proc_documents = Books_Media_DB.find(proc_query)
        document_count = Books_Media_DB.count_documents(proc_query)
        return template.render(data=proc_documents, total=document_count, type=storage_selected)
    return template.render()


##########################################################
# Reciving finished post


@app.route('/view_jewlery_main', methods=['POST', 'GET'])
def view_jewlery_main():
    template = jinja_env.get_template('jewl_view_main.html')
    return template.render()


@app.route('/view_jewlery', methods=['POST', 'GET'])  # Reciving finished post
def view():
    if request.method == 'POST':
        date = request.form['date_select']
        REV_documents = Finished_Jewlery_DB.find()
    template = jinja_env.get_template('jewlery_view.html')
    return template.render(data=REV_documents)


@app.route('/view_sgw_main', methods=['POST', 'GET'])  # Reciving finished post
def view_sgw_main():
    template = jinja_env.get_template('view_sgw_main.html')
    return template.render()


@app.route('/view_sgw', methods=['POST', 'GET'])  # Reciving finished post
def view_sgw():
    if request.method == 'POST':
        date = request.form['date_select']
        REV_documents = Finished_DB.find()
    template = jinja_env.get_template('view_sgw.html')
    return template.render(data=REV_documents)


@app.route('/stats', methods=['POST', 'GET'])  # Reciving finished post
def stats():
    book_query = {"Contents": 'Books'}
    media_query = {"Contents": "Media"}
    sgw_query = {"Contents": "Collectables"}
    jewlery_query = {"Contents": "Jewelry"}

    total_not_added_to_spreadsheet_books = Finished_DB.count_documents({
        "Contents": "Books"})
    total_not_added_to_spreadsheet_media = Finished_DB.count_documents({
        "Contents": "Media"})
    total_not_added_to_spreadsheet_sgw = Finished_DB.count_documents(
        {"Contents": "Collectables"})
    total_not_added_to_spreadsheet_jewlery = Finished_Jewlery_DB.count_documents({
        "Contents": "Jewelry"})
    # Total Left to process
    total_books_gay = Books_Media_DB.count_documents(
        {"Contents": "Books", "Storage_Type": "Gaylord"})
    total_books_tote = Books_Media_DB.count_documents(
        {"Contents": "Books", "Storage_Type": "Tote"})
    total_media_gay = Books_Media_DB.count_documents(
        {"Contents": "Media", "Storage_Type": "Gaylord"})
    total_media_tote = Books_Media_DB.count_documents(
        {"Contents": "Media", "Storage_Type": "Tote"})
    total_sgw_gay = Truck_Receiver_DB.count_documents(
        {"Contents": "Collectables", "Storage_Type": "Gaylord"})
    total_sgw_tote = Truck_Receiver_DB.count_documents(
        {"Contents": "Collectables", "Storage_Type": "Tote"})
    total_jewlery_gay = Jewelry_DB.count_documents(
        {"Contents": "Jewelry", "Storage_Type": "Gaylord"})
    total_jewlery_tote = Jewelry_DB.count_documents(
        {"Contents": "Jewelry", "Storage_Type": "Tote"})
    # Processed But not submitted

    Total_to_process_gay = total_books_gay + \
        total_media_gay + total_sgw_gay + total_jewlery_gay
    Total_to_process_tote = total_books_tote + \
        total_media_tote + total_sgw_tote + total_jewlery_tote

    total_ready_for_logging = total_not_added_to_spreadsheet_books + total_not_added_to_spreadsheet_media + \
        total_not_added_to_spreadsheet_sgw + total_not_added_to_spreadsheet_jewlery

    template = jinja_env.get_template('count.html')
    return template.render(tgtp=Total_to_process_gay, tttp=Total_to_process_tote, trfl=total_ready_for_logging, sgwTGTP=total_sgw_gay, sgwTTTP=total_sgw_tote, sgwTRFL=total_not_added_to_spreadsheet_sgw,
                           jewlTGTP=total_jewlery_gay, jewlTTTP=total_jewlery_tote, jewlTRFL=total_not_added_to_spreadsheet_jewlery,
                           bookTGTP=total_books_gay, bookTTTP=total_books_tote, bookTRFL=total_not_added_to_spreadsheet_books,
                           medTGTP=total_media_gay, medTTTP=total_media_tote, medTRFL=total_not_added_to_spreadsheet_media)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=1028)

#   http://sponge.icarus.io/?date=(Date goes here in YYYY-MM-DD form)
