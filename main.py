"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""
import os
from flask import Flask, render_template, request, redirect, send_file
from so_job import get_so_job
from wwr_job import get_wwr_job
from rok_job import get_rok_job
from save_job import save_job_csv

os.system("clear")
USER_AGENT = os.environ['USER_AGENT']
FONT_KIT = os.environ['FONT_KIT']

app = Flask("chocotScrapper")
db = {}

@app.route("/")
def home():
  db_keys = db.keys()
  return render_template(
    "home.html", 
    font_kit=FONT_KIT,
    searched_keys=db_keys, 
    keys_len=len(db_keys)
  )

@app.route("/report")
def report():
  word = request.args.get("word")
  if word:
    word = word.lower().strip()
    from_db = db.get(word)
    if from_db:
      jobs = from_db
    else:
      so_jobs = get_so_job(word)
      wwr_jobs = get_wwr_job(word)
      rok_jobs = get_rok_job(word, USER_AGENT)
      jobs = so_jobs + wwr_jobs + rok_jobs
      db[word] = jobs
  else:
    return redirect("/")
  return render_template(
    "report.html", 
    search_word=word, 
    job_num=len(jobs), 
    jobs=jobs, 
    font_kit=FONT_KIT
  )

@app.route("/export")
def export():
  try:
    word = request.args.get("word")
    if not word:
      raise Exception()
    word = word.lower().strip()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_job_csv(jobs, f"jobs_{word}")
    return send_file(
      f"jobs_{word}.csv", 
      mimetype='text/csv', 
      attachment_filename=f'jobs_{word}.csv', 
      as_attachment=True
    )
  except:
    return redirect("/")

app.run(host="0.0.0.0")