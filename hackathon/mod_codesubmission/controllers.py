# codesubmission/controllers.py


from flask import request, render_template,  redirect, url_for, Blueprint, flash
from flask_login import login_required, current_user
from datetime import datetime

from hackathon.mod_codesubmission.forms import CodeForm, ResultForm
from hackathon.mod_codesubmission.exec_untrusted_basic import exec_untrusted
from hackathon.mod_authorization.models import User
from hackathon.mod_codesubmission.models import Competition, Participant, CodeSubmission, ProblemStatement

from hackathon import db, app

mod_codesubmission = Blueprint('codesubmission', __name__, url_prefix='/codesubmission')


@mod_codesubmission.route('/participanthome/', methods=['GET', 'POST'])
@login_required
def participanthome():
    competitions = Competition.query.filter(Competition.participants.any(id = current_user.id)).all()
    return render_template('codesubmission/participanthome.html', competitions=competitions)


@mod_codesubmission.route('/attemptproblem/<int:competition_id>', methods=['GET', 'POST'])
@login_required
def attemptproblem(competition_id):
    problem_list = ProblemStatement.query.filter(ProblemStatement.competition_id==competition_id).all()
    return render_template('codesubmission/problemlist.html', problem_list=problem_list)


@mod_codesubmission.route('/reviewcode/<int:problem_statement_id>,<int:competition_id>', methods=['GET', 'POST'])
@login_required
def reviewcode(problem_statement_id, competition_id):
    code_form = CodeForm(request.form)
    result_form = ResultForm(request.form)
    result_text = ""
    
    app.logger.info(request.method)
    # app.logger.info(app.config['SQLALCHEMY_DATABASE_URI'])

    if request.method == 'POST' and code_form.validate() and code_form.code_verify.data:
        code_str = code_form.code_text.data
        result_text = exec_untrusted(code_str)
        result_form.result_text.data = result_text['result']

    if request.method == 'POST' and code_form.validate() and code_form.code_submit.data:
        code_str = code_form.code_text.data
        result_text = exec_untrusted(code_str)

        if result_text['outcome']:
            submission = CodeSubmission(user_id=current_user.id,
                                        competition_id=competition_id,
                                        problem_statement_id = problem_statement_id,
                                        date_submitted=datetime.utcnow(),
                                        code_text=code_str,
                                        result_text=str(exec_untrusted(code_str)))
            db.session.add(submission)
            db.session.commit()
            flash("Code Submitted Successfully", "success")
            return redirect(url_for('home'))
        else:
            flash("Correct the code before submitting!", "danger")

    return render_template('codesubmission/codereview.html', code_form=code_form, result_form=result_form)
