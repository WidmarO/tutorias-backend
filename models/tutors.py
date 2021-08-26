from db import db

class TutorsModel(db.Model):
    _tablename_ = 'tutors'
    
	# cod_tutor varchar(6),
	# cod_teacher varchar(6),
	# cod_tutoring_program varchar(6),
	# schedule varchar(250),
	# place varchar(100),
	# primary Key(cod_tutor),
	# foreign key(cod_teacher) references teachers(cod_teacher),
	# foreign key(cod_tutoring_program) references tutoring_programs(cod_tutoring_program)

    cod_tutor = db.Column(db.String(6), primary_key=True, unique = True)
    cod_teacher = db.Column(db.String(6), db.ForeignKey('teacher.cod_teacher'))
    cod_tutoring_program = db.Column(db.String(6), db.ForeignKey('tutoring_programs.cod_tutoring_program'))
    schedule = db.Column(db.String(250))
    place = db.Column(db.String(100))

    #relation
    quotes = db.relationship('QuotesModel')
    tutor_students = db.relationship('Tutor_StudentsModel')
    student_helpers = db.relationship('Student_HelperModel')
    student_helper_tutors = db.relationship('Student_Helper_TutorsModel') 


    def _init_(self, cod_tutor, cod_teacher, cod_tutoring_program, schedule, place):
        self.cod_tutor = cod_tutor
        self.cod_teacher = cod_teacher
        self.cod_tutoring_program = cod_tutoring_program
        self.schedule = schedule
        self.place = place


    def json(self):
        return {'cod_tutor': self.cod_tutor,
                'cod_teacher': self.cod_teacher,
                'cod_tutoring_program': self.cod_tutoring_program,
                'schedule': self.schedule,
                'place': self.place,
                }

    def update_data(self, cod_tutor, cod_teacher, cod_tutoring_program, schedule, place):
        self.cod_tutor = cod_tutor
        self.cod_teacher = cod_teacher
        self.cod_tutoring_program = cod_tutoring_program
        self.schedule = schedule
        self.place = place

    @classmethod
    def find_by_cod_tutor(cls, _cod_tutor):
        # -> SELECT * FROM items where cod_coordinator=cod_coordinator LIMIT 1
        return cls.query.filter_by(cod_tutor=_cod_tutor).first()
    
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