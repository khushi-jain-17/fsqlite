import sqlite3
from flask import Blueprint, request, jsonify


get_routes = Blueprint("get_routes", __name__)
# get_id_routes = Blueprint("get_id_routes", __name__)
# create_routes = Blueprint("create_routes", __name__)
# update_routes = Blueprint("update_routes", __name__)
# delete_routes = Blueprint("delete_routes",__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@get_routes.route('/', methods=['GET'])
def get_posts():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts")
    posts = cur.fetchall()
    p_lists = []
    for p in posts:
        p_lists.append({
            'id': p['id'], 'created': p['created'], 'title': p['title'], 'content': p['content']})
    return jsonify({'posts': p_lists})

@get_routes.route('/get/<int:id>',methods=['GET'])
def get_id(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("select * from posts where id=?",(id,))
    data = cur.fetchall()
    post = []
    for d in data:
        post.append({
            'id' : d['id'], 'created': d['created'], 'title': d['title'], 'content': d['content']})
    cur.close()
    conn.close()
    return jsonify({'posts': post})

@get_routes.route('/pcreate',methods=['POST'])
def create():
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    data = request.json 
    cur.execute("insert into posts(id,title,content) values(?,?,?)",(data['id'], data['title'],data['content']))
    conn.commit()
    conn.close()
    return jsonify(data)

@get_routes.route("/update/<int:id>", methods=['POST'])
def update(id):
    conn = get_db_connection()
    cur = conn.cursor()
    data = request.json
    title = data.get("title")
    content = data.get("content")
    cur.execute("update posts set title=?,content=? where id=?",
                (title, content, id,))
    conn.commit()
    cur.close()
    conn.close()
    return "updated"

@get_routes.route("/delete/<int:id>",methods=['DELETE'])
def delete(id):
    conn = get_db_connection()
    cur = conn.cursor()
    id = request.json.get("id")
    cur.execute("delete from posts where id=?",(id,))
    conn.commit()
    cur.close()
    conn.close()
    return {'message': 'post deleted successfully'}