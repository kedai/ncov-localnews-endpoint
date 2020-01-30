from flask import Flask, request, jsonify, make_response
#from memcache import Client
from flaskext.mysql import MySQL
import json, os

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = os.environ.get("USER")
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get("PASS")
app.config['MYSQL_DATABASE_DB'] = os.environ.get("DB")
app.config['MYSQL_DATABASE_HOST'] = os.environ.get("HOST")
mysql.init_app(app)
 
@app.route("/get_articles")
def get_articles():
    cursor = mysql.connect().cursor()
    cursor.execute("select * from newsapi_local order by addedOn desc limit 10")
    r = [dict((cursor.description[i][0], value)
           for i, value in enumerate(row)) for row in cursor.fetchall()]
    resp = make_response(jsonify({'recs': r}))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['SameSite'] = 'Secure'
    return resp

@app.route("/get_articles/<lng>")
def get_article_lng(lng):
    cursor = mysql.connect().cursor()
    cursor.execute('select * from newsapi_local where language = "{}" order by addedOn desc limit 10'.format(lng))
    r = [dict((cursor.description[i][0], value)
           for i, value in enumerate(row)) for row in cursor.fetchall()]
    resp = make_response(jsonify({'recs': r}))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['SameSite'] = 'Secure'
    return resp

if __name__ == "__main__":
    app.run(debug=True)

