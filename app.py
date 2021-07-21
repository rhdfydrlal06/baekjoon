from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///board.db"
# DB를 지정 + 파일명을 지정. 작대기 3개면 상대경로, 4개면 절대경로
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)
db.init_app(app)

from model import *

###CRUD 생성###
class Board(Resource):
    def get(self): # 게시판에 있는 글을 불러온다??
        data = request.get_json()

        article_search_result = article.query.all()
        articles = [{'글 번호' : arti.id, '글 내용' : arti.content} for arti in article_search_result]
        return jsonify(status="success", result=articles)

    def post(self): # 글 작성 (글 내용, 비밀번호)
        try:
            data = request.get_json()
            content = data.get('content')
            password = data.get('password')

            article_info = article(password, content)
            db.session.add(article_info)
            db.session.commit()

            return jsonify(status="success", article_info={'글 내용': content, '글 번호': article_info.id})
        except Exception as e:
            return jsonify(error=str(e))

    def delete(self):
        pass
    
    def put(self):
        pass

api.add_resource(Board, '/board')

if __name__ == '__main__':
    app.run(port=1234, debug=True)