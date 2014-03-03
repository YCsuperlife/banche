#coding=utf-8

from bottle import route, run, template, post, request
import sqlite3 as db
import json

# DB API
def init_db():
    con = db.connect('user.db')
    cur = con.cursor()
    try:
        cur.execute('create table user (name varchar(100), lon varchar(100), lat varchar(100), addr varchar(100), comment varchar(500))')
    except:
        print('table existed')
        pass

def get_user_list():
    con = db.connect('user.db')
    cur = con.cursor()

    cur.execute("select name,lon,lat,addr,comment from user")
    return cur.fetchall()

def update_user(name, lon, lat, addr,comment):
    con = db.connect('user.db')
    cur = con.cursor()

    # 看看用户存在不
    cur.execute("select * from user where name='%s'" % (name))
    if len(cur.fetchall()) > 0:
        cur.execute("update user set lon='%s',lat='%s',addr='%s',comment='%s' where name='%s'" % (lon, lat, addr, comment, name))
    else:
        cur.execute("insert into user values('%s','%s','%s','%s','%s')"%(name,lon,lat,addr,comment))
    con.commit()


@route('/')
def index():
    init_db()
    return template('index.html')

@route('/result')
def result():
    init_db()
    return template('result.html')

@post('/api/adduser')
def api_adduser():
    name = request.forms.get('name')
    lon = request.forms.get('lon')
    lat = request.forms.get('lat')
    addr = request.forms.get('address')
    comment = request.forms.get('comment')

    update_user(name,lon,lat,addr,comment)
    return "上传成功"

@route('/api/list')
def api_list():
    ret = json.dumps(get_user_list())
    return ret

if __name__=="__main__":
    run(host="0.0.0.0", port=8080)
