from app import db
from sqlalchemy.schema import CreateTable


class Info(db.Model):
    __tablename__ = 'user_info'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=20))
    stu_id = db.Column(db.String(length=8))
    department = db.Column(db.Integer)
    photo = db.Column(db.LargeBinary(length=4096))
    keep_private = db.Column(db.Integer)
    score = db.Column(db.Integer)



if __name__ == '__main__':
    print(CreateTable(Global.__table__))

