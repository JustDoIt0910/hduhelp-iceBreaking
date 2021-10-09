from flask import Flask, render_template, request, redirect, url_for, jsonify
from form import LoginForm, UploadForm
from flask_sqlalchemy import SQLAlchemy
from flask import flash
import random
import os


app = Flask(__name__)
app.config.update(SECRET_KEY=os.getenv('SECRET_STRING'),
                  SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL') + '/photo?charset=utf8')
db = SQLAlchemy(app)
from database import Info

login_info = {'name': '', 'stu_id': '', 'department': 1}
choices = [None] * 4
correct = ()
with open('static/img/default.jpg', 'rb') as f:
    default_avatar = f.read()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_info['name'] = request.form.get('name')
        login_info['stu_id'] = request.form.get('stu_id')
        login_info['department'] = int(request.form.get('department'))
        stu = Info.query.filter(Info.stu_id == login_info['stu_id']).first()
        if stu is None:
            new_user = Info(name=login_info['name'], stu_id=login_info['stu_id'],
                            department=int(login_info['department']))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            print(stu.name, login_info['name'])
            print(stu.department, login_info['department'])
            if stu.name == login_info['name'] and stu.department == login_info['department']:
                print('redirect')
                return redirect(url_for('index'))
            else:
                flash('登陆信息有误，请检查信息')
                return redirect(url_for('login'))
    else:
        return render_template('login.html', form=form)


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if login_info['name'] == '':
        return redirect(url_for('login'))
    form = UploadForm()
    if form.validate_on_submit():
        # 得到上传图片的二进制文件
        image = form.image.data
        image = image.read()
        # 存储到数据库中
        check = request.form.getlist('kp')
        kp = 0 if len(check) == 0 else 1
        stu = Info.query.filter(Info.stu_id == login_info['stu_id']).first()
        if stu is None:
            info = Info(name=login_info['name'], stu_id=login_info['stu_id'],
                        department=int(login_info['department']), photo=image,
                        keep_private=kp, score=0)
            db.session.add(info)
        else:
            stu.photo = image
            stu.keep_private = kp
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('upload.html', form=form)


@app.route('/userinfo/<string:query>')
def get_user_info(query):
    if query == 'avatar':
        people = Info.query.filter(Info.name == login_info['stu_id']).first()
        if people is None or people.photo is None:
            return default_avatar
        else:
            return people.photo
    elif query == 'info':
        return jsonify(login_info) if login_info['name'] != '' else jsonify({})


@app.route('/index/play/<string:query>')
def game(query):
    global correct, choices
    print(Info.query.count())
    if query == 'options':
        correct = ()
        choices = [None] * 4
        available_photo = Info.query.filter(Info.photo is not None).filter(Info.keep_private == 0).all()
        print(available_photo)
        if len(available_photo) == 0:
            return jsonify({})
        c1 = available_photo[random.randint(0, len(available_photo) - 1)]
        print(c1)
        available_stu = Info.query.filter(Info.stu_id != c1.stu_id).all()
        print(available_stu)
        stu_num = len(available_stu) + 1
        if stu_num < 4:
            positions = [i for i in range(stu_num)]
            random.shuffle(positions)
            choices[positions[0]] = c1
            correct = (positions[0], c1.stu_id)
            for i in range(1, stu_num):
                choices[positions[i]] = available_stu[i - 1]
        else:
            positions = [0, 1, 2, 3]
            random.shuffle(positions)
            choices[positions[0]] = c1
            correct = (positions[0], c1.stu_id)
            choice_index = random.sample(range(0, len(available_stu)), 3)
            for i in range(1, 4):
                choices[positions[i]] = available_stu[choice_index[i - 1]]
        res = {}
        for i, p in enumerate(choices):
            if p is not None:
                res['op' + str(i + 1)] = p.name
        return jsonify(res)
    elif query == 'photo':
        print(correct)
        return Info.query.filter(Info.stu_id == correct[1]).first().photo
    elif query == 'validate':
        select = int(request.args.get('select')[2])
        return jsonify(success=(choices[select - 1].stu_id == correct[1]), ans=select, iscorrect=correct[0] + 1)


if __name__ == '__main__':
    app.run()
