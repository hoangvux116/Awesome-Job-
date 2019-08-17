import sqlite3

DATABASE = 'job_data.db'

def get_data():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    data = cur.execute("SELECT * FROM data_jobs;").fetchall()
    conn.commit()
    conn.close()
    for row in data:
        # job = {}
        # Tao dict chua TITLE, PUBLISHED va UPDATE AT:
        job_id, publisher, title, _, date, _ = row
        # job['publisher'] = publisher
        # job['title'] = title
        # job['date'] = date
        yield job_id, title, publisher, date

def get_id(job_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    data = cur.execute("SELECT * FROM data_jobs WHERE job_id=?", (job_id,)).fetchone()
    conn.commit()
    conn.close()
    _, _, title, job_description, _, _ = data
    return title, job_description