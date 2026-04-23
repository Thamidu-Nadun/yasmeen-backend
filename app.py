from flask import Flask, request, jsonify, send_file
from extensions import db
from config import Config
from app.constant import HTTPStatusCodes
from app.dto.email_dto import EmailDTO
from app.service.email_service import (
    get_emails as service_get_emails,
    get_email as service_get_email,
    get_email_by_mali as service_get_email_by_mail,
    save_email as service_save_email,
    delete_email_by_id,
)
from app.service.log_service import (
    service_get_logs
)

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
with app.app_context():
    db.create_all()

# Emails Routes

@app.route('/api/email', methods=['GET'])
def list_emails():
    return jsonify(service_get_emails())

@app.route('/api/email/<int:email_id>', methods=['GET'])
def fetch_email(email_id):
    email = service_get_email(email_id)
    if email is None:
        return jsonify({'error': 'Email not found'}), HTTPStatusCodes.NOT_FOUND
    return jsonify(email)

@app.route('/api/email', methods=['POST'])
def create_email():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), HTTPStatusCodes.BAD_REQUEST
    
    try:
        data = EmailDTO(**request.get_json())
        if data is None:
            return jsonify({'error': 'Invalid JSON data'}), HTTPStatusCodes.BAD_REQUEST
        
        # print(f"Received email data: {data.model_dump()}")
        
        saved_mail = service_save_email(
            recipient=data.recipient,
            subject=data.subject,
            body=data.body,
            mail_type=data.mail_type
        )
        
        return jsonify(saved_mail), HTTPStatusCodes.CREATED
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({'error': 'Invalid data format'}), HTTPStatusCodes.BAD_REQUEST

@app.route('/api/email/<int:email_id>', methods=['PUT'])
def update_email(email_id):
    return jsonify({})

@app.route('/api/email/<int:email_id>', methods=['DELETE'])
def delete_email(email_id):
    res = delete_email_by_id(email_id)
    if not res:
        return jsonify({'error': 'Email not found'}), 404
    return jsonify({'message': 'Email deleted successfully'})

# Logs Routes
@app.route('/api/log', methods=['GET'])
def get_logs():
    logs = service_get_logs()
    return jsonify(logs)

# PDF Routes
@app.route('/api/pdf/<int:email_id>', methods=['GET'])
def get_pdf(email_id):
    email = service_get_email(email_id)
    if email is None:
        return jsonify({'error': 'Email not found'}), HTTPStatusCodes.NOT_FOUND
    
    pdf_path = email.get('pdf_path')
    if not pdf_path:
        return jsonify({'error': 'PDF not found for this email'}), HTTPStatusCodes.NOT_FOUND
    
    return jsonify({'pdf_path': pdf_path})

@app.route('/api/pdf/download/<int:email_id>', methods=['GET'])
def download_pdf(email_id):
    email = service_get_email(email_id)
    if email is None:
        return jsonify({'error': 'Email not found'}), HTTPStatusCodes.NOT_FOUND
    
    pdf_path = email.get('pdf_path')
    if not pdf_path:
        return jsonify({'error': 'PDF not found for this email'}), HTTPStatusCodes.NOT_FOUND
    
    return send_file(pdf_path, as_attachment=True)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), HTTPStatusCodes.NOT_FOUND

if __name__ == '__main__':
    app.run(debug=False, port=5000)


