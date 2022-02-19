import datetime # 유효기간
import hashlib # 문자열 해싱(암호화)설정

import jwt

#로그아웃 기능구현
from flask_jwt_extended import get_jti

# session : 로그인 구현 해주는 딕셔너리. 사람들마다 다른 세션부여해줌.
from flask import url_for, session, Flask, render_template, request, redirect

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
## mongoDB 저장 경로
db = client.dbmaking

""" 파일명: users"""
"""name = db.users.find_one({'name':'name'})
print(users['name']"""

app = Flask(__name__)
SECRET_KEY  = 'chick@chick!_74123@!'

@app.route('/', methods=['GET', 'POST'])
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('index.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for('login', msg="로그인시간이 만료되었어요"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('login', msg="로그인 정보가 없어요!"))


""""회원가입 Register Form"""
# 회원정보 받아오기 (id / pw)
# 회원정보 비밀번호는 해시로 암호화하여 db저장
@app.route('/resister', methods=[ 'POST'])
def resister():
    if request.method == 'POST';
        return render_template("resister.html")
    else:
        # 회원정보 생성
        ## id / pw 각각 지정
        id_receive = request.form['id_give']
        pw_receive = request.form['pw_give']
        re_pw = request.form['re_pw']  # 비밀번호 확인

        if id_receive == "":
            flash('이메일을 입력해주세요!')
            return render_template('login.html')
        elif pw_receive == "":
            flash('비밀번호를 입력해주세요!')
            return render_template('login.html')

        # 비밀번호 암호화
        pw_protect = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

        ## 회원정보 저장하기 (딕셔너리 만든 후 저장)
        doc = {
            'id':id_receive,
            'pw':pw_protect,
        }

        new_user = db.users.insert_one(doc)
        flash('회원가입이 완료되었어요~')
        return render_template("login.html")

         '''if new_user is None:
            # 회원정보가 등록되어있지않는 경우 (새유저 없다면 = 미등록 -> 로그인창 이동 및 회원가입 완료)
            return render_template('login.html', 'msg':'회원가입이 완료되었어요')
           # 회원정보가 등록되어있는 경우 (새유저가 있다면 = 기등록 -> 로그인창으로 이동)
            else:
            return jsonify({'result':'success', 'msg':'이미 회원가입이 되어있어요!'})
            return render_template('login.html')'''

'''로그인 API'''
@app.route('/login') ### 요기는 다시 보자 ㅠ 헷갈령
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


# id/pw 받아 맞춰본 후, 토큰 만들어서 발급하기!
@app.route('/sign_in', methods=['POST'])  #-> 메소드 확인하기
def sign_in():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # pw 암호화하기 (hashlib 필요 - 설치가 따로 안되고 자동 import가 됐음)
    pw_protect = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id와 pw를 가지고 해당 유저 찾아주기
    result = db.users.find_one({'id': id_receive, 'pw':pw_protect})

    # id/pw 찾으면  jmt 토큰 발급하여 로그인 성공 (값이 있는 경우)
        if result is not None:
        # jmt 토큰 = payload 및 secret key 필요
        # 시크릿키 있어야 토큰 디코딩(풀기)을 하여 payload 값 확인
        # payload를 풀어야 userid 값 확인
        # exp로 유효기간 설정 = 만료시간 지나면, 시크릿키로 토큰 풀 시 만료되었을 때 에러발생
        payload = {
            'id': id_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60) # 로그인 1시간 유지!
        }
        # jwt 암호화
        token = jwt.encode(payload, SECRET_KEY, algorithm='H5256').decode('uft-8')
        # session 지정
        session['login'] = True
        # token 값 주기!
        return jsonify({'result': 'success', 'token':token})

    # 찾지 못하면 뜨는 내용(값이 없는 경우)
    else:
        return jsonify({'result':'fail', 'msg': '가입하지 않은 아이디이거나, 비밀번호가 일치하지 않습니다!'})


'''로그아웃'''
@app.route('/logout', methods=['POST'])
def logout():
    session['login']= False
    return redirect(url_for('home', msg='로그아웃 되었어요!'))


'''비밀번호 찾기'''
@app.route('/findpw', methods=['GET', 'POST'])
def findpw():
    # ID(이메일)로 PW 찾기
    if id_receive = request.form['id_give']
        find_id = db.users.find_one({'id': id_receive})
        find_pw = find_id['pw']
        return jsonify({'msg':'비밀번호 :'find_pw})

    # PW로 ID(이메일)찾기
    else pw_receive = requests.form('pw_give')
        find_pw = db.users.find_one({'pw':pw_receive})
        find_id = find_pw
        return jsonify({'msg':'이메일(ID) :'find_id})

@app.route('/comment', methods=['GET'])
# 로그인된 사용자만 이야기 남길 수 있도록 #
@check_for_token # token 없거나 만료되면 끝!
def user_only():
    if mytoken = False
        return render_template('index.html')
    else
        return render_template('comment.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)