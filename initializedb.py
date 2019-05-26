import sys
sys.path.insert(0,"/var/www/python/python-hackathon-webapp/")

from hackathon import db
from hackathon import app
from hackathon.mod_authorization.models import User
from hackathon.mod_codesubmission.models import Competition, ProblemStatement # Team, TeamParticipant


if __name__ == "__main__":
    # TBD - Change create_all to create database only if file does not exist.
    with app.test_request_context():
        db.init_app(app)
        db.create_all()

    # TBD - Change code to make sure record is inserted only if it does not exist.
    user1 = User(id=1,username='TestUser',email='martious@gmail.com',name='Test User',password='test',is_kerberos=False)
    user2 = User(id=2,username='himanshu',email='himanshu.shrotri@gmail.com',name='Himanshu Shrotri',password='test',is_kerberos=False)
    user3 = User(id=3,username='pratik',email='pratikajmera@gmail.com',name='Pratik Ajmera',password='test',is_kerberos=False)
    user4 = User(id=4,username='ajmera@INTRANET.MARTIOUS.COM',email='pratik.ajmera@martious.com',name='Pratik Ajmera',is_kerberos=True)
    db.session.add_all([user1,user2,user3,user4])

    competition1 = Competition(id=1,name='Martious Hackathon 1', description="Join in the world's most excieting Coding Competition @ Martious.com 1")
    competition2 = Competition(id=2,name='Martious Hackathon 2', description="Join in the world's most excieting Coding Competition @ Martious.com 2")
    competition1.competition_participants.append(user1)
    competition1.competition_participants.append(user2)
    competition1.competition_participants.append(user3)
    competition1.competition_participants.append(user4)
    competition2.competition_participants.append(user2)
    db.session.add(competition1)
    db.session.add(competition2)

    problemstatement1 = ProblemStatement(competition_id=1, problem_summary="Short Summary 1.1",
                                         problem_text="Sample Problem Test Goes Here 1")
    problemstatement2 = ProblemStatement(competition_id=1, problem_summary="Short Summary 1.2",
                                         problem_text="Sample Problem Test Goes Here 2")
    problemstatement3 = ProblemStatement(competition_id=2, problem_summary="Short Summary 2.1",
                                         problem_text="Sample Problem Test Goes Here 3")
    problemstatement4 = ProblemStatement(competition_id=2, problem_summary="Short Summary 2.2",
                                         problem_text="Sample Problem Test Goes Here 4")
    problemstatement5 = ProblemStatement(competition_id=2, problem_summary="Short Summary 2.3",
                                         problem_text="Sample Problem Test Goes Here 5")
    problemstatement6 = ProblemStatement(competition_id=2, problem_summary="Short Summary 2.4",
                                         problem_text="Sample Problem Test Goes Here 6")

    db.session.add_all([problemstatement1, problemstatement2, problemstatement3, problemstatement4,
                        problemstatement5, problemstatement6])

    db.session.commit()
