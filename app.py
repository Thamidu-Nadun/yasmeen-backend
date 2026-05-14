"""
GNU LESSER GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) 2007 Free Software Foundation, Inc.

This library is free software: you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this library. If not, see <https://www.gnu.org/licenses/>.
"""


from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from extensions import db, init_browser
from config import Config
from app.constant import HTTPStatusCodes
from app.dto.email_dto import EmailDTO
from app.service.email_service import (
    get_emails as service_get_emails,
    get_email as service_get_email,
    get_email_by_mali as service_get_email_by_mail,
    get_email_by_page as service_get_email_by_page,
    save_email as service_save_email,
    delete_email_by_id,
)
from app.service.log_service import (
    service_get_logs
)
from app.service.email_sender_service import send_mail_to_recipient

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

db.init_app(app)
with app.app_context():
    db.create_all()

init_browser()

# Emails Routes

# Get all emails
@app.route('/api/email', methods=['GET'])
def list_emails():
    sort = request.args.get('sort', 'desc')
    page = request.args.get('start', 0, type=int)
    limit = request.args.get('limit', 20, type=int)
    
    if sort == 'desc':
        return jsonify(service_get_email_by_page(page, limit, sort="desc"))
    else:
        return jsonify(service_get_email_by_page(page, limit, sort="asc"))

# Get email by ID
@app.route('/api/email/<int:email_id>', methods=['GET'])
def fetch_email(email_id):
    email = service_get_email(email_id)
    if email is None:
        return jsonify({'error': 'Email not found'}), HTTPStatusCodes.NOT_FOUND
    return jsonify(email)

# Create a new email
@app.route('/api/email', methods=['POST'])
def create_email():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), HTTPStatusCodes.BAD_REQUEST
    
    try:
        json_data = request.get_json()
        if json_data is None:
            return jsonify({'error': 'Invalid JSON data'}), HTTPStatusCodes.BAD_REQUEST
        
        data = EmailDTO(**json_data)
        
        # print(f"Received email data: {data.model_dump()}")
        
        saved_mail = service_save_email(
            recipient=data.recipient,
            subject=data.subject,
            body=data.body,
            mail_type=data.mail_type,
            language=data.language
        )
        
        return jsonify(saved_mail), HTTPStatusCodes.CREATED
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({'error': 'Invalid data format'}), HTTPStatusCodes.BAD_REQUEST

# Update an existing email
@app.route('/api/email/<int:email_id>', methods=['PUT'])
def update_email(email_id):
    return jsonify({})

# Delete an email
@app.route('/api/email/<int:email_id>', methods=['DELETE'])
def delete_email(email_id):
    res = delete_email_by_id(email_id)
    if not res:
        return jsonify({'error': 'Email not found'}), 404
    return jsonify({'message': 'Email deleted successfully'})

# send email
@app.route('/api/email/send/<int:email_id>', methods=['POST'])
def send_email(email_id):
    res = send_mail_to_recipient(email_id)
    if not res:
        return jsonify({'error': 'Failed to send email'}), HTTPStatusCodes.INTERNAL_SERVER_ERROR
    return jsonify({'message': 'Email sent successfully'})

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
    
    return send_file(pdf_path, as_attachment=False, mimetype='application/pdf')

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), HTTPStatusCodes.NOT_FOUND

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False, port=5000, threaded=False)


