from extensions import db

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user,
            'type': self.type,
            'timestamp': self.timestamp.isoformat(),
            'status': self.status
        }