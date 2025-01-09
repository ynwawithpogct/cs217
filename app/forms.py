from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, ValidationError

# class violationForm(FlaskForm):
#     loivipham = StringField('loivipham', validators=[DataRequired()])
#     phuongTien = StringField('phuongTien', validators=[DataRequired()])
#     chiTietLoi = StringField('chiTietLoi', validators=[DataRequired()])
#     submit = SubmitField('Submit')

# Validator tùy chỉnh
def at_least_one_required(form, field):
    # Kiểm tra nếu tất cả các trường đều trống
    if not (form.loivipham.data or form.phuongTien.data or form.chiTietLoi.data):
        raise ValidationError("At least one field must be filled.")

class violationForm(FlaskForm):
    loivipham = StringField('loivipham', validators=[at_least_one_required])
    phuongTien = StringField('phuongTien', validators=[at_least_one_required])
    chiTietLoi = StringField('chiTietLoi', validators=[at_least_one_required])
    submit = SubmitField('Tìm các lỗi thỏa điều kiện')
    
class nextForm(FlaskForm):
    next = SubmitField('Next')
    
class backForm(FlaskForm):
    back = SubmitField('Back')
    
class homeForm(FlaskForm):
    home = SubmitField('Home')

class searchForm(FlaskForm):
    search = SubmitField('Tìm Kiếm Các Lỗi')
    
class queryForm(FlaskForm):
    query = SubmitField('Thêm các lỗi')
    
class clearQuerry(FlaskForm):
    clear = SubmitField('Clear')