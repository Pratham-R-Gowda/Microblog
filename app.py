import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    client = MongoClient("mongodb+srv://microblogproject:vscodeflaskmb_99@cluster0.1zgro.mongodb.net/")
    app.db = client.microblogproject
    entries=[]

    @app.route("/", methods=["GET","POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            format_date = datetime.datetime.today().strftime("%d-%m-%Y")
            app.db.entries.insert_one({"content": entry_content, "date": format_date})

        entries_with_date = [
            (
                entry["content"], 
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%d-%m-%Y").strftime("%b %d")

            )
            for entry in app.db.entries.find({})
        ]    
        return render_template("homepage.html", entries = entries_with_date)
    return app

 

