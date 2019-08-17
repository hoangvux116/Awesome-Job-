import requests
import sqlite3
import time
import os

URL = 'https://api.github.com/repos/awesome-jobs/vietnam/issues?page={}'
DATABASE = 'job_data.db'
SQL_FILE = os.path.join(os.path.abspath('.'), DATABASE)


def awesome_job_crawl():
    page = 1
    ses = requests.Session()
    resp = ses.get(URL.format(page))
    if resp.status_code == 200:
        # Write your logic here
        data = resp.json()
    else:
        resp.raise_for_status()  # raise an exception for error codes (4xx or 5xx)
    # CREATE new datasheet to store data   
    if os.path.exists(SQL_FILE):
        try:
            os.remove(SQL_FILE)
        except Exception as e:
            raise Exception(e) 
    while data:
        conn = sqlite3.connect(SQL_FILE)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS data_jobs
        (job_id integer, publisher text, Titles text, Descriptions text, Date_of_Post text, URLs text)''')
        # INSERT record to table:
        for job in data:
            cur.execute('INSERT INTO data_jobs VALUES (?, ?, ?, ?, ?, ?)',
                        (job['id'],
                        job['user']['login'],
                        job['title'],
                        job['body'],
                        job['updated_at'][:10],
                        job['html_url']))
        conn.commit()
        page += 1
        ses = requests.Session()
        resp = ses.get(URL.format(page))
        data = resp.json()
        time.sleep(1)
    conn.close()


def main():
    awesome_job_crawl()


if __name__ == "__main__":
    main()
