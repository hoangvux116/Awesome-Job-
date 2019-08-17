from flask import Flask, render_template, url_for, Markup
import markdown
import sqlite3
from get_data import get_data
from get_data import get_id
from crawl import awesome_job_crawl
import os

app = Flask(__name__)
DATABASE = 'job_data.db'
SQL_FILE = os.path.join(os.path.abspath('.'), DATABASE)

conn = sqlite3.connect(SQL_FILE, check_same_thread=False)
c = conn.cursor()

@app.route("/")
def home():
    data = c.execute("SELECT * FROM data_jobs;").fetchall()
    jobs = get_data()
    return render_template("job_home.html", jobs=jobs, num_of_result=len(data))


@app.route("/jobs/<int:input_id>")
def job_info(input_id):
    title, body = get_id(input_id)
    job_descr = Markup(markdown.markdown(body))
    job_title = title[(title.find('-') + 1):]
    company_name = title[:(title.find('-') - 1)]
    return render_template("job_description.html", company_name=company_name, job_title=job_title, job_descrip=job_descr)


if __name__ == "__main__":
	app.run(debug=True)
