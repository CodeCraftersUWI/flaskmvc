from App.database import db
course_self_bridge = db.Table('course_self_bridge',
  db.Column ('linking_course_id',db.Integer, db.ForeignKey('course.course_id')),
  db.Column('target_course_id',db.ForeignKey('course.course_id'))
)