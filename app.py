from flask import Flask, request, render_template, jsonify, session, redirect, url_for


app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

## mongodb 저장 경로 ##
db = client.dbsparta



@app.route('/', methods=['GET', 'POST'])
def home():
	""" Session control"""
	if not session.get('logged_in'):
		return render_template('index.html')
	else:
		if request.method == 'POST':
			username = request.form['username']
			return render_template('index.html', username)
		return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	"""Login Form"""
	if request.method == 'GET':
		return render_template('login.html')
	else:
		name = request.form['username']
		passwd = request.form['password']
		try:
			#유저네임으로 찾기
			#data = User.query.filter_by(username=name, password=passw).first()
			data = db.users.find_one({'name': name},{'_id': False})
			if data is not None:
				session['logged_in'] = True
				return redirect(url_for('home')) #home.html로 가기
			else:
				return 'Dont Login'
		except:
			return "Dont Login"


@app.route('/register/', methods=['GET', 'POST'])
def register():
	"""Register Form"""
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		# 테이블 생성
		doc = {
			"id": 1,
			"name": username,
			"passd": password
		}
		db.users.insert_one(doc)
		#new_user = User(, password=request.form['password'])
		new_user = doc
		db.session.add(new_user)
		db.session.commit()
		return render_template('login.html')
	return render_template('register.html')


@app.route('/logout')
def logout():
	"""Logout Form"""
	session['logged_in'] = False
	return redirect(url_for('home'))

#@app.route('/findpassd')
#def findpassd():




if __name__ == '__main__':
    app.run('0.0.0.0', port=5005, debug=True)
