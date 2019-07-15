# codesubmission/controllers.py


from flask import request, render_template,  redirect, url_for, Blueprint, flash
from flask_login import login_required, current_user
from datetime import datetime

from hackathon.mod_codesubmission.forms import CodeForm
from hackathon.mod_codesubmission.exec_untrusted_basic import exec_untrusted
from hackathon.mod_authorization.models import User
from hackathon.mod_codesubmission.models import Competition, Participant, CodeSubmission,ProblemStatement, ParticipantProblemStatement


from hackathon import db, app
from sqlalchemy.sql import text

mod_codesubmission = Blueprint('codesubmission', __name__, url_prefix='/codesubmission')


# This is a testing route to test different ORM options
@mod_codesubmission.route('/testcodesubmissionmodule/')
@login_required
def testcodesubmissionmodule():
    current_participant = Participant.get_by_user(current_user)
    current_participants_competitions = current_participant.competitions
   
    first_competition = Competition.query.filter_by(id="2").first()
    first_competition_participants = first_competition.participants
    
    # Himanshu - help solve this. How to select all problemstatements linked to participant but also belong to first_competition
    # This line does not work.....
    # current_participants_problemstatements = current_participant.problemstatements.query(competition=first_competition).all()
    
    return render_template('codesubmission/testcodesubmissionmodule.html',current_participant=current_participant
                    ,current_participants_competitions=current_participants_competitions
                    ,first_competition=first_competition
                    ,first_competition_participants=first_competition_participants
                    ,current_participants_problemstatements=current_participants_problemstatements)


@mod_codesubmission.route('/participanthome/', methods=['GET', 'POST'])
@login_required
def participanthome():
    current_participant = Participant.get_by_user(current_user)
    current_participants_competitions = current_participant.competitions
    
    if (len(current_participants_competitions) == 0):
        flash("You are not registered for any competition!", "danger")
    
    return render_template('codesubmission/participanthome.html', competitions=current_participants_competitions)


@mod_codesubmission.route('/myteam/')
@login_required
def myteam():
    current_participant = Participant.get_by_user(current_user)
    custom_sql = """
                    SELECT participant.name, participant.team_name, problemstatement.problem_summary, IFNULL(codesubmission.is_correct,0) as is_correct
                    from participant
                        inner join participant_problemstatement
                        on participant_problemstatement.participant_id = participant.id
                        inner join problemstatement
                        on problemstatement.id = participant_problemstatement.problemstatement_id
                        LEFT JOIN codesubmission
                        on codesubmission.problemstatement_id = problemstatement.id
                        AND codesubmission.participant_id = participant.id
                        AND codesubmission.is_correct = 1
                    WHERE team_name IN (SELECT p.team_name from participant p where p.id = :id)
                    order by participant.name, problemstatement.problem_summary
                 """
    teammember_list = db.engine.execute(text(custom_sql),{"id":current_participant.id})
    
    return render_template('codesubmission/myteam.html', teammember_list=teammember_list)


@mod_codesubmission.route('/listmyproblems/<int:competition_id>', methods=['GET', 'POST'])
@login_required
def listmyproblems(competition_id):
    current_participant = Participant.get_by_user(current_user)
    problem_list = current_participant.problemstatements
    # current_participant.problemstatements.query.filter(competition_id==competition_id)
    # ProblemStatement.query.filter(ProblemStatement.competition_id==competition_id).all()
    if (len(problem_list) == 0):
        flash("You are not registered for any competition!", "danger")
    return render_template('codesubmission/listmyproblems.html', problem_list=problem_list)


@mod_codesubmission.route('/reviewcode/<int:problem_statement_id>,<int:competition_id>', methods=['GET', 'POST'])
@login_required
def reviewcode(problem_statement_id, competition_id):
    current_participant = Participant.get_by_user(current_user)
    participant_problemstatement = ParticipantProblemStatement.query.filter_by(participant_id=current_participant.id\
                                            ,problemstatement_id=problem_statement_id).first()
    
    if (participant_problemstatement is None):
        flash("You are not registered for the competition (problem) you are trying to attempt!", "danger")
        return redirect(url_for('home'))
    
    code_form = CodeForm(request.form)
        
    # app.logger.info(request.method)
    # app.logger.info(app.config['SQLALCHEMY_DATABASE_URI'])

    if request.method == 'POST' and code_form.validate() and code_form.code_verify.data:
        
        code_text_input = code_form.code_text.data
        result_text = exec_untrusted(code_text_input)
        
        if not result_text['outcome']:
            flash('Your code failed to execute!','danger')
        
        code_form.result_text.data = result_text['result']

    elif request.method == 'POST' and code_form.validate() and code_form.code_submit.data:
        
        code_text_input = code_form.code_text.data
        result_text_input = code_form.result_text.data
        
        # print("(result_text_input '{}')".format(result_text_input))
        
        if result_text_input != '':
            
            result_text = exec_untrusted(code_text_input)

            if result_text['outcome']:
                expected_problem_answer = ProblemStatement.query.filter_by(id=problem_statement_id).first().problem_answer
                is_correct = False
                
                if(expected_problem_answer == result_text['result']):
                    is_correct = True
                
                submission = CodeSubmission(participant_id=current_participant.id,
                                            competition_id=competition_id,
                                            problemstatement_id = problem_statement_id,
                                            code_text=code_text_input,
                                            result_text=result_text['result'],
                                            is_correct=is_correct)
                
                db.session.add(submission)
                db.session.commit()
                
                if(is_correct):
                    flash('Congratulations, code submitted successfully! Try other problems or help your colleagues now...', 'success')
                    return redirect(url_for('home'))
                else:
                    flash('Unfortunately the output generated by your code is not correct, try again...', 'danger')
            
            else:
                flash('Correct the code before submitting! Use "Verify Code" button to test the code output.', 'danger')
        
        else:
            flash('Click "Verify Code" button to test the code before submitting.', 'danger')
        
    return render_template('codesubmission/reviewcode.html', code_form=code_form, participant_problemstatement=participant_problemstatement)
