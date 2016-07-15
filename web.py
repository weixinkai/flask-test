# coding: utf8
import sqlite3
from flask import Flask, g, url_for, render_template, redirect, request
from math import ceil

ITEM_NUM_PER_PAGE = 30
#create
app = Flask(__name__)

@app.before_request
def before_request():
    g.db = sqlite3.connect('data.db')

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
@app.route('/<int:page>')
def show_items(page=1):
    order = get_order()
    max_page = count_page()
    cur = g.db.execute('''SELECT DISTINCT * FROM collection
                          ORDER BY date '''+ order + ' LIMIT ? OFFSET ?',
                          (ITEM_NUM_PER_PAGE, ITEM_NUM_PER_PAGE * (page - 1), ))
    items = [dict(title=row[0], date=row[1], url=row[2])
             for row in cur.fetchall()]
    return render_template('show.html', items=items,
                           current_page = page, max_page=max_page)

@app.route('/goto',methods=['POST', 'GET'])
def goto():
    if request.method == 'POST':
        page = request.form['target_page']
        return redirect(url_for('show_items', page=page))
    return redirect(url_for('index'))

def count_page():
    cur = g.db.execute('SELECT count(DISTINCT url) FROM collection')
    return ceil(cur.fetchone()[0] / ITEM_NUM_PER_PAGE)

def get_order():
    order = request.args.get('order', 'DESC')
    return order if order in ['DESC', 'ASC'] else 'DESC'

if __name__ == '__main__':
    app.run()
