from wtforms import Form, TextAreaField, validators, \
    SubmitField, BooleanField, StringField, PasswordField  # , ValidationError, SelectField, IntegerField
from wtforms.widgets import TextArea


class CodeForm(Form):
    code_text = TextAreaField('Enter Code Here:', [validators.DataRequired()], widget=TextArea(),
                              render_kw={'class': 'form-control', 'rows': 10, 'columns': 1000})
    code_submit = SubmitField('Submit Code')


class ResultForm(Form):
    result_text = TextAreaField('Code Result:', [validators.data_required()],
								render_kw={'readonly': True, 'class': 'form-control', 'rows': 10, 'columns': 50})


class LoginForm(Form):
    username = StringField('Username', validators=[validators.DataRequired()],
								render_kw={'class': 'form-control', 'required': True,'placeholder': "Username", 'autofocus': True})
    password = PasswordField('Password', validators=[validators.DataRequired()],
								render_kw={'class': 'form-control', 'required': True,'placeholder': "Password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In',render_kw={'class': 'btn btn-lg btn-primary btn-block'})


class SignupForm(Form):
    username = StringField('Username', validators=[validators.Length(min=2, max=100)],
								render_kw={'class': 'form-control', 'required': True,'placeholder': "Username", 'autofocus': True})
    password = PasswordField('Password', validators=[validators.Length(min=4, max=15)],
								render_kw={'class': 'form-control', 'required': True,'placeholder': "Password"})
    name = StringField('Name', validators=[validators.Length(min=2, max=100)],
								render_kw={'class': 'form-control', 'required': True,'placeholder': "Name"})
    email = StringField('Email', validators=[validators.Email()],
								render_kw={'class': 'form-control', 'required': True,'placeholder': "Email"})
    submit = SubmitField('Sign Up',render_kw={'class': 'btn btn-lg btn-primary btn-block'})
