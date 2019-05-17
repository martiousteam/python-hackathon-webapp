# mod_authorization/forms.py

from wtforms import Form, validators, SubmitField, StringField, PasswordField, BooleanField

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
