from .. import db

class Authority(db.Model):
    __tablename__ = 'Authority'

    authority_key = db.Column(db.Integer, primary_key=True, autoincrement=True)
    authority_context = db.Column(db.String(100), nullable=False)

