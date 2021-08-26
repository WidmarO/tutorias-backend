from db import db
from datetime import datetime

class QuotesModel(db.Model):
    _tablename_ = 'quotes'
    
	# cod_quote varchar(6),
	# cod_tutor varchar(6),
	# cod_student varchar(6),
	# date_time datetime,
	# g_description varchar(300),
	# p_description varchar(300),
	# diagnosis varchar(300),
	# cod_tutoring_program varchar(6),
	# primary key(cod_quote),
	# foreign key(cod_student) references students(cod_student),
	# foreign key(cod_tutor) references tutors(cod_tutor),
	# foreign key(cod_tutoring_program) references tutoring_programs(cod_tutoring_program)

    cod_quote = db.Column(db.String(6), primary_key=True)
    cod_tutor = db.Column(db.String(6), db.ForeignKey('tutors.cod_tutor'))
    cod_student = db.Column(db.String(6), db.ForeignKey('students.cod_student'))
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    g_description = db.Column(db.String(300))
    p_description = db.Column(db.String(300))
    diagnosis = db.Column(db.String(300))
    cod_tutoring_program = db.Column(db.String(6), db.ForeignKey('tutoring_programs.cod_tutoring_program'))

    #relation
    
    #cod_coordinator = db.relationship('Tutoring_ProgramModel')

    def _init_(self, cod_quote, cod_tutor, cod_student,date_time,g_description,p_description,diagnosis,cod_tutoring_program):
        self.cod_quote = cod_quote
        self.cod_tutor = cod_tutor
        self.cod_student= cod_student
        self.date_time = date_time
        self.g_description= g_description
        self.p_description = p_description
        self.diagnosis= diagnosis
        self.cod_tutoring_program= cod_tutoring_program



    def json(self):
        return {'cod_quote': self.cod_quote,
                'cod_tutor': self.cod_tutor,
                'cod_student': self.cod_student,
                'date_time': self.date_time,
                'g_description': self.g_description,
                'p_description': self.p_description,
                'diagnosis': self.diagnosis,
                'cod_tutoring_program': self.cod_tutoring_program,
                }

    def update_data(self,cod_quote, cod_tutor, cod_student,date_time,g_description,p_description,diagnosis,cod_tutoring_program):
        self.cod_quote = cod_quote
        self.cod_tutor = cod_tutor
        self.cod_student= cod_student
        self.date_time = date_time
        self.g_description= g_description
        self.p_description = p_description
        self.diagnosis= diagnosis
        self.cod_tutoring_program= cod_tutoring_program


    @classmethod
    def find_by_cod_quote(cls, _cod_quote):
        # -> SELECT * FROM items where cod_coordinator=cod_coordinator LIMIT 1
        return cls.query.filter_by(cod_quote=_cod_quote).first()
    
    @classmethod
    def find_all(cls):
        # -> SELECT * FROM items
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()