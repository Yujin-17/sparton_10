from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

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
    login_name = request.form['name_give']
    login_pwd = request.form['pwd_give']
    match_name = db.info.find_one({'name': login_name})
    match_pwd = db.info.find_one({'pwd': login_pwd})

    if login_name == match_name and login_pwd == match_pwd:
        return jsonify({'msg': '로그인 되었습니다.'})
    else:
        return jsonify({'msg2': '닉네임 또는 비밀번호가 일치하지 않습니다'})


@app.route("/sign", methods=["POST"])
def sign_post():
    user_name = request.form['name_give']
    user_pwd = request.form['pwd_give']
    user_pwd_re = request.form['pwd_re_give']
    user_list = list(db.info.find({},{'_id':False}))['name']

    if (user_name in user_list) or (user_pwd != user_pwd_re):
        return jsonify({'msg': '닉네임 중복 또는 비밀번호가 일치하지 않습니다'})
    else:
        doc = {
            'name': user_name,
            'pwd': user_pwd
        }
        db.info.insert_one(doc)

        return jsonify({'msg':'가입이 완료 되었습니다'})


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
