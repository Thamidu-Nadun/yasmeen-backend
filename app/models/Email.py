from extensions import db

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipient = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    mail_type = db.Column(db.String(50), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pdf_path = db.Column(db.String(255), nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'recipient': self.recipient,
            'subject': self.subject,
            'mail_type': self.mail_type,
            'body': self.body,
            'pdf_path': self.pdf_path
        }
    