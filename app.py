from flask import Flask, request, render_template, jsonify
import gridfs

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

## mongodb 저장 경로 ##
db = client.dbsparta


@app.route("/")
def main():
    #db 이미지 저장
    doc = {
        'id': '온도',
        'img_url': 'https://raw.githubusercontent.com/maino77/SparataWeather/99c4709d7a883d6fb7915ce8dc9733dfd6988297/img/extra_1.png',
    }
    db.photo.insert_one(doc)
    return render_template('index.html')


@app.route("/showPhoto", methods=['GET'])
def show():
    #온도 조건 받는 부분 추가 ondo = request.args.get('')
    clothes = list(db.photo.find({'id': '온도'}, {'_id': False}))
    return jsonify({'all_clothes': clothes})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5005, debug=True)
