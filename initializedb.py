import sys
sys.path.insert(0,"/var/www/python/python-hackathon-webapp/")

from hackathon import db
from hackathon.mod_authorization.models import User
from hackathon.mod_codesubmission.models import Competition # Team, TeamParticipant


if __name__ == "__main__":
    # TBD - Change create_all to create database only if file does not exist.
    db.create_all()

    # TBD - Change code to make sure record is inserted only if it does not exist.
    user1 = User(id=1,username='TestUser',email='martious@gmail.com',name='Test User',password='test',is_kerberos=False)
    user2 = User(id=2,username='himanshu',email='himanshu.shrotri@gmail.com',name='Himanshu Shrotri',password='test',is_kerberos=False)
    user3 = User(id=3,username='pratik',email='pratikajmera@gmail.com',name='Pratik Ajmera',password='test',is_kerberos=False)
    user4 = User(id=4,username='ajmera@INTRANET.MARTIOUS.COM',email='pratik.ajmera@martious.com',name='Pratik Ajmera',is_kerberos=True)
    db.session.add_all([user1,user2,user3,user4])

    competition = Competition(id=1,name='Martious Hackathon')
    competition.competition_participants.append(user1)
    competition.competition_participants.append(user2)
    competition.competition_participants.append(user3)
    competition.competition_participants.append(user4)
    db.session.add(competition)




    
    

    '''
    team = Team(id=1,name='TestTeam 1')
    db.session.add(team)
    team = Team(id=2,name='TestTeam 2')
    db.session.add(team)
    
    teamparticipant = TeamParticipant(id=1,user_id=1, team_id=1)
    db.session.add(teamparticipant)
    teamparticipant = TeamParticipant(id=2,user_id=2, team_id=1)
    db.session.add(teamparticipant)
    teamparticipant = TeamParticipant(id=3,user_id=3, team_id=2)
    db.session.add(teamparticipant)
    teamparticipant = TeamParticipant(id=4,user_id=4, team_id=2)
    db.session.add(teamparticipant)
    '''

    db.session.commit()