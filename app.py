from flask import Flask, request, render_template, jsonify, session, redirect, url_for


app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

## mongodb 저장 경로 ##
db = client.dbsparta



@app.route('/')
def home():
	##로그인 기능이 들어오면 수정되어야할 부분
	return render_template('comment.html')


###### 코멘트 API  생성 ########
@app.route('/weather/comment', methods=['POST'])
def write_comment():
	local_receive = request.form['local_give']
	talk_receive = request.form['talk_give']
	date_receive = request.form['date_give']


	doc = {
		'local': local_receive,
		'talk': talk_receive,
		'date' : date_receive

	}
	db.album.insert_one(doc)
	return jsonify({'msg': '이 요청은 코멘트 POST'})


@app.route('/weather/comment', methods=['GET'])
def show_comment():
	comments = list(db.album.find({}, {'_id':False}))
	return jsonify({'all_comments': comments})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5005, debug=True)
