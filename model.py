from app import db

class article(db.Model):

    __tablename__ = 'article'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password    = db.Column(db.String(20), nullable=False)
    content     = db.Column(db.Text, nullable=False)

    def __init__(self, password, content):
        self.password   = password
        self.content    = content