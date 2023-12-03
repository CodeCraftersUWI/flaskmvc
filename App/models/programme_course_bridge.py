from App.database import db
programme_course_bridge = db.Table('programme_course_bridge',
  db.Column ('programme_id',db.Integer, db.ForeignKey('programme.programmId')),
  db.Column('course_id',db.ForeignKey('course.course_id'))
)