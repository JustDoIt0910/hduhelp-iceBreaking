from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, SelectField, SubmitField, FileField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    name = StringField(label="姓名", validators=[DataRequired("请输入姓名")],
                       render_kw={"placeholder": "请输入姓名",
                                  "class": "name-input"})
    stu_id = StringField(label="学号", validators=[DataRequired("请输入学号"),
                                                 Length(min=8, max=8, message="学号应为8位")],
                         render_kw={"placeholder": "请输入学号",
                                    "class": "stu-id-input"})
    department = SelectField(label="部门", validators=[DataRequired("请选择部门")],
                             choices=[(1, "部门1"), (2, "部门2"), (3, "部门3"), (4, "部门4")],
                             render_kw={"class": "department-input"},
                             default=1, coerce=int)
    submit = SubmitField(label="登录", render_kw={"class": "btn-submit"})


class UploadForm(FlaskForm):
    image = FileField(label="上传头像", validators=[FileRequired(),
                                                FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    submit = SubmitField(label="上传", render_kw={"class": "btn-submit"})
