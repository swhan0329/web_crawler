from incruit import get_whole_jobs as get_incruit_jobs
from flask import Flask, render_template, request, redirect, send_file
from save import save_to_file
app = Flask("SuperScrapper")
db = {}

@app.route("/")
def home():
    return render_template("potato.html")

@app.route("/report")
def report():
    word = request.args.get('word')
    if word:
        word = word.lower()
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs = get_incruit_jobs(word)
            db[word] = jobs
    else:
        redirect("/")
    return render_template("report.html",searchingBy=word,
                           resultsNumber=len(jobs),jobs=jobs)

@app.route("/export")
def export():
    try:
        word = request.args.get('word')
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs)
        return send_file("jobs.csv")
    except:
        return redirect("/")

app.run(host="127.0.0.1")