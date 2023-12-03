from App.database import db
plan_course_bridge = db.Table('plan_course_bridge',
  db.Column ('plan_id',db.Integer, db.ForeignKey('course_plan.id')),
  db.Column('course_id',db.ForeignKey('course_plan_course.id'))
) 