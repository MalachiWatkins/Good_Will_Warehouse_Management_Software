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
user = warehouse_db["User"]
Receiver = warehouse_db["Receiver"]

Processor_Review = warehouse_db["Processor_Review"]

Books_Media_Received = warehouse_db["Books_Media_Received"]
Books_Media_Review = warehouse_db["Books_Media_Review"]

Jewlery_Received = warehouse_db["Jewlery_Received"]
Jewlery_Review = warehouse_db["Jewlery_Review"]


Ready_For_Logging = warehouse_db["Ready_For_Logging"]
Jewlery_Ready_For_Logging = warehouse_db["Jewlery_Ready_For_Logging"]

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


#### Chooses Jewelry Collection if submitted is jewlery ###
def db_post(post, isJewlery,isBooks_Media):
    if post['Storage_Type'] != '':
        if isJewlery == True:
            x=0
            while x < int(post['Quantity']):
                post['_id'] = random.random()
                Jewlery_Received.insert_one(post)
                x+=1
        elif isBooks_Media == True:
            print(32)
            x=0
            while x < int(post['Quantity']):
                post['_id'] = random.random()
                Books_Media_Received.insert_one(post)
                x+=1
        else:
            x=0
            while x < int(post['Quantity']):
                post['_id'] = random.random()
                Receiver.insert_one(post)
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
        if request.form['item_contents'] == 'Jewlery':
            db_post(post=data_post, isJewlery=f, isBooks_Media=False)
            print('JEwl')
        elif request.form['item_contents'] == 'Books' or request.form['item_contents'] == 'Media':
            print('Books')
            db_post(post=data_post, isJewlery=False, isBooks_Media=True)
        else:
            db_post(post=data_post, isJewlery=False, isBooks_Media=False)

    return template.render()


@app.route('/rec_finished', methods=['POST', 'GET'])  # Reciving finished post
def rec_finished():
    template = jinja_env.get_template('rec_finished.html')
    return template.render()

######################################################################
#################### Processor #######################################
######################################################################
@app.route('/proc', methods=['POST', 'GET'])  # Main Processor View
def proc():
    template = jinja_env.get_template('processor_main.html')
    return template.render(date=date_proc_format)

@app.route('/processing', methods=['POST', 'GET'])  # Processing Data Viewing
def processing():
    Template = ['data.html']
    Document_Data = []
    Item_Cat = []
    if request.method == 'POST':
        cat_selected = request.form['storage_type']
        def data(collection,Review_Collection):
            if request.form['summited'] == 'yes': ### Checks if data is Submitted and sends it to review
                ##### Gets form Data and creates a post with it #####
                ID = request.form['ID']
                STORAGE = request.form['storage_type']
                CONTENTS = request.form['CONTENTS']
                DATE_RECEIVED = request.form['DATE_RECEIVED']
                STORE_NUMBER = request.form['STORE_NUMBER']
                MANIFEST_NUMBER = request.form['manifest_number_form']
                PROBLEMS = request.form['problem_form']
                DATE_PROSESSED = date_proc_format

                PROCESSED_BY = request.form['processed_by']
                SEAL_NUMBER = request.form['seal_number_form']


                delquery = { "_id": float(ID) }

                # Deletes Post and addes it to the Review collecion for viewing with a new ID
                collection.delete_one(delquery)

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

                Review_Collection.insert_one(New_Post)

                date_selected = DATE_RECEIVED
                contents = CONTENTS
                store_selected = STORE_NUMBER
            else: ### If request method was not post ###
                date_selected = request.form['date_select']#####
                cat_selected = request.form['storage_type']####   # Gets filters from main view #
                store_selected = request.form['store_number']###
            date_fiter = request.form['date_filter']
            if date_fiter == 'Dont use Date':
                if store_selected == '':
                    Queryed_Document = collection.find()
                    Document_Data.append(Queryed_Document)
                    print(Document_Data)
                else:
                    Query == {'Store_Number': store_selected}
                    Queryed_Document = collection.find(Query)
                    Document_Data.append(Queryed_Document)
                    print(Document_Data)
            else:
                if store_selected == '':
                    Query = {'Date_Received': date_selected}
                    Queryed_Document = collection.find(Query)
                    Document_Data.append(Queryed_Document)
                    print(Document_Data)
                else:
                    Query = {'Date_Received': date_selected,'Store_Number': store_selected }
                    Queryed_Document = collection.find(Query)
                    Document_Data.append(Queryed_Document)
                    print(Document_Data)
            return

        if cat_selected == 'Jewelry':
            Selected_collect = Jewlery_Received
            Selected_Review = Jewlery_Review
        elif cat_selected == 'Books' or cat_selected == 'Media':
            Selected_collect = Books_Media_Received
            Selected_Review = Books_Media_Review
        else:
            Selected_collect = Receiver
            Selected_Review = Processor_Review
        data(collection=Selected_collect,Review_Collection=Selected_Review)

        template = jinja_env.get_template(Template[0])
        return template.render(data=Document_Data[0])
    template = jinja_env.get_template(Template[0])
    return template.render(data=Document_Data)



@app.route('/rev', methods=['POST', 'GET'])  #  Processing Data Reviewing
def rev():
    contents = request.form['ye']  # Will not work with anything but test I have no Clue why lol
    if contents == 'Collectables':
        collecion_selected = Receiver.find()
        Review_Documents = Processor_Review.find()
    elif contents == 'Books':
        collecion_selected = Books_Media_Received.find()
        Review_Documents = Books_Media_Review.find()
    elif contents == 'Media':
        collecion_selected = Books_Media_Received.find()
        Review_Documents = Books_Media_Review.find()
    else:
        collecion_selected = Jewlery_Received.find()
        Review_Documents = Jewlery_Review.find()

    template = jinja_env.get_template('review.html')
    def review(collection,Review_Collection):
        if request.method == 'POST':
            print(request.form["test"])
            contents = request.form['CONTENTS']  # Will not work with anything but test I have no Clue why lol
            if contents == 'Collectables':
                collecion_selected = Receiver.find()
                Review_Documents = Processor_Review.find()
            elif contents == 'Books':
                collecion_selected = Books_Media_Received.find()
                Review_Documents = Books_Media_Review.find()
            elif contents == 'Media':
                collecion_selected = Books_Media_Received.find()
                Review_Documents = Books_Media_Review.find()
            else:
                collecion_selected = Jewlery_Received.find()
                Review_Documents = Jewlery_Review.find()

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

            if request.form["ye"] == 'Undo Processing':
                proc_query = {"_id": float(ID)}
                delete_one = Review_Collection.delete_one(proc_query)
                move = collection.insert_one(post)

                return template.render(data=Review_Documents)
            else:
                proc_query = {"_id": float(ID)}
                delete_one = Review_Collection.delete_one(proc_query)
                Ready_For_Logging.insert_one(post)
                return template.render(data=Review_Documents)


        review(collection=collecion_selected,Review_Collection=Review_Documents)
    return template.render(data=Review_Documents)




######################################################################
#################### Jewelry ########################################
######################################################################

@app.route('/view_jewlery_main', methods=['POST', 'GET'])  # Reciving finished post
def view_jewlery_main():
    template = jinja_env.get_template('jewl_view_main.html')
    return template.render()

@app.route('/view_jewlery', methods=['POST', 'GET'])  # Reciving finished post
def view():
    if request.method == 'POST':
        date = request.form['date_select']
        REV_documents = Jewlery_Ready_For_Logging.find()
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
        REV_documents = Ready_For_Logging.find()
    template = jinja_env.get_template('view_sgw.html')
    return template.render(data = REV_documents)

@app.route('/stats', methods=['POST', 'GET'])  # Reciving finished post
def stats():
    book_query = {"Contents": 'Books'}
    media_query = {"Contents": "Media"}
    sgw_query = {"Contents": "Collectables"}
    jewlery_query = {"Contents": "Jewelry"}

    total_not_added_to_spreadsheet_books = Ready_For_Logging.count_documents({"Contents": "Books"})
    total_not_added_to_spreadsheet_media = Ready_For_Logging.count_documents({"Contents": "Media"})
    total_not_added_to_spreadsheet_sgw = Ready_For_Logging.count_documents({"Contents": "Collectables"})
    total_not_added_to_spreadsheet_jewlery = Jewlery_Ready_For_Logging.count_documents({"Contents": "Jewelry"})
    ## Total Left to process
    total_books_gay = Receiver.count_documents({"Contents": "Books", "Storage_Type":"Gaylord"})
    total_books_tote = Receiver.count_documents({"Contents": "Books", "Storage_Type":"Tote"})
    total_media_gay = Receiver.count_documents({"Contents": "Media", "Storage_Type":"Gaylord"})
    total_media_tote = Receiver.count_documents({"Contents": "Media", "Storage_Type":"Tote"})
    total_sgw_gay = Receiver.count_documents({"Contents": "Collectables", "Storage_Type":"Gaylord"})
    total_sgw_tote = Receiver.count_documents({"Contents": "Collectables", "Storage_Type":"Tote"})
    total_jewlery_gay = Jewlery_Received.count_documents({"Contents": "Jewelry", "Storage_Type":"Gaylord"})
    total_jewlery_tote = Jewlery_Received.count_documents({"Contents": "Jewelry", "Storage_Type":"Tote"})
    ### Processed But not submitted
    toat_review_books = Processor_Review.count_documents({"Contents": "Books"})
    toat_review_media = Processor_Review.count_documents({"Contents": "Media"})
    toat_review_jewlery = Jewlery_Review.count_documents({"Contents": "Jewelry"})
    toat_review_sgw = Processor_Review.count_documents({"Contents": "Collectables"})

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
