from .. import db
from .authority import Authority

class User_group(db.Model):
    __tablename__ = 'UserGroup'

    user_group_key = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_group_name = db.Column(db.String(50), nullable=False)
    group_authority = db.Column(db.Integer, nullable=False)

    authority_relationship = db.ForeignKey(group_authority, Authority.authority_key)
