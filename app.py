import datetime
import hashlib
from datetime import datetime, timedelta

import jwt
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.SECRET_KEY = '123'

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@Cluster0.mhvqxjc.mongodb.net/?retryWrites=true&w=majority')

db = client.dbsparta


@app.route('/')
def home():
    return render_template('login.html')

@app.route('/signup.html')
def test():
    return render_template('signup.html')


@app.route('/main.html')
def test2():
    return render_template('main.html')



@app.route("/login", methods=["POST"])
def login_post():
    login_name = request.form['username_give']
    login_pwd = request.form['password_give']

    pw_hash = hashlib.sha256(login_pwd.encode('utf-8')).hexdigest()  # 유저가 입력한 pw를 해쉬화
    result = db.info.find_one({'username': login_name, 'password': pw_hash})
    print(result)
    # 아이디와 유저가 입력한 해쉬화된 pw가 DB에 저장되어 있는 해쉬화된 pw와 일치하는지 확인
    if result is not None:  # 일치한다면
        payload = {
            'id': login_name,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 1)  # 로그인 1시간 유지 -> 해커 취약점 방지 로그인 시간 조정
        }
        # 유저 아이디와 유효기간을 담고 있는 payload 생성
        token = jwt.encode(payload, app.SECRET_KEY, algorithm='HS256')  # jwt기반 토큰 생성

        return jsonify({'result': 'success', 'mytoken': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route("/sign", methods=["POST"])
def sign_post():
    user_name = request.form['name_give']
    user_pwd = request.form['pwd_give']
    user_pwd_re = request.form['pwd_re_give']
# // todo
    password_hash = hashlib.sha256(user_pwd.encode('utf-8')).hexdigest()
    doc = {
        "username": user_name,  # 아이디
        "password": password_hash,  # 비밀번호
    }
    db.info.insert_one(doc)  # 유저가 입력한 아이디, pw DB에 저장
    return jsonify({'response': 'success'})

@app.route("/main", methods=["POST"])
def save_main():
    titles_receive = request.form['titles_give']
    descs_receive = request.form['descs_give']
    comments_receive = request.form['comments_give']
    print(titles_receive, descs_receive,comments_receive)
    doc = {
        'titles':titles_receive,
        'descs':descs_receive,
        'comments':comments_receive
    }
    db.show.insert_one(doc)
    return jsonify({'msg':  '저장 완료!'})

@app.route("/main", methods=["GET"])
def show_get():
    show_list = list(db.show.find({}, {'_id': False}))
    return jsonify({'show':show_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
