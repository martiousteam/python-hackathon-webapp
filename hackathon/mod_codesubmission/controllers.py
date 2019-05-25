# codesubmission/controllers.py


from flask import request, render_template,  redirect, url_for, Blueprint
from flask_login import login_required

from hackathon.mod_codesubmission.forms import CodeForm, ResultForm
from hackathon.mod_codesubmission.exec_untrusted_basic import exec_untrusted

from hackathon import db, app

mod_codesubmission = Blueprint('codesubmission', __name__, url_prefix='/codesubmission')


@mod_codesubmission.route('/reviewcode/', methods=['GET', 'POST'])
@login_required
def reviewcode():
    code_form = CodeForm(request.form)
    result_form = ResultForm(request.form)
    
    app.logger.info(request.method)
    # app.logger.info(app.config['SQLALCHEMY_DATABASE_URI'])

    if request.method == 'POST' and code_form.validate() and code_form.code_verify.data:
        code_str = code_form.code_text.data
        result_text = exec_untrusted(code_str)
        result_form.result_text.data = result_text

    if request.method == 'POST' and code_form.validate() and code_form.code_submit.data:
        pass

    return render_template('codesubmission/codereview.html', code_form=code_form, result_form=result_form)
