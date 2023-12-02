from App.database import db

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    __tablename__ = 'departments'  # Explicitly set the table name

    def __repr__(self):
        return f"Department('{self.name}')"
