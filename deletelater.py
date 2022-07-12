# Proc Data and jewlery data



######## rev ##############################################################

    template = jinja_env.get_template('jewl_rev.html')
    REV_documents = Jewlery_Review.find()

        PROCESSED_BY = request.form['processed_by']
        SEAL_NUMBER = request.form['seal_number_form']

        post = {
            'Processed_By': PROCESSED_BY,
            'Seal_Number': SEAL_NUMBER,

        }
        if request.form["test"] == 'Undo Processing':

            delete_one = Jewlery_Review.delete_one(proc_query)
            Jewlery_Received.insert_one(post)

        else:
            proc_query = {"_id": float(ID)}
            delete_one = Jewlery_Review.delete_one(proc_query)
            Jewlery_Ready_For_Logging.insert_one(post)
