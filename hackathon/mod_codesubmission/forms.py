# codesubmission/forms.py

from wtforms import Form, TextAreaField, validators, SubmitField
from wtforms.widgets import TextArea


class CodeForm(Form):
    code_text = TextAreaField('Enter Code Here:', [validators.DataRequired()], widget=TextArea(),
                              render_kw={'class': 'form-control',
                                         'rows': 10,
                                         'style': "font-family:'Monaco'"})
    code_verify = SubmitField('Verify Code')
    code_submit = SubmitField('Submit Code')


class ResultForm(Form):
    result_text = TextAreaField('Code Result:', [validators.data_required()],
                                render_kw={'readonly': True,
                                           'class': 'form-control',
                                           'rows': 10,
                                           'style': "font-family:'Monaco'"})
