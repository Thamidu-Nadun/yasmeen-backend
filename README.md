# 📧 Email Agent PDF Generation Backend

> A powerful Flask-based backend service that intelligently parses emails, extracts structured data, and generates beautifully formatted PDF documents.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-green?logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-blue?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎯 Project Overview

Email Agent PDF Generation Backend is a sophisticated automation service that:

- ✅ Receives email data through RESTful API endpoints
- ✅ Intelligently parses unstructured email content using advanced regex patterns
- ✅ Generates professional PDF documents from parsed data
- ✅ Manages comprehensive audit logs and event tracking
- ✅ Stores email metadata with associated PDF file paths
- ✅ Provides real-time status and error handling

Perfect for **invoice generation**, **report automation**, **document management**, and **workflow automation** systems.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory:**

```bash
cd pdf_generation_backend
```

2. **Create a virtual environment:**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

### Running the Application

```bash
# Development mode
python app.py

# The API will be available at: http://localhost:5000
```

---

## 📁 Project Structure

```
pdf_generation_backend/
├── 📄 app.py                    # Main Flask application & route definitions
├── 📄 config.py                 # Configuration settings
├── 📄 extensions.py             # Extension initialization (SQLAlchemy)
├── 📄 requirements.txt           # Project dependencies
│
├── 📁 app/                      # Application logic
│   ├── 📁 dto/                  # Data Transfer Objects (Pydantic models)
│   │   └── email_dto.py         # Email input validation
│   │
│   ├── 📁 models/               # Database models
│   │   ├── Email.py             # Email entity
│   │   ├── EmailContent.py      # Parsed email content
│   │   └── Log.py               # Audit logs
│   │
│   ├── 📁 repo/                 # Repository (Data access layer)
│   │   ├── email_repo.py        # Email CRUD operations
│   │   └── LogRepo.py           # Log management
│   │
│   ├── 📁 service/              # Business logic layer
│   │   ├── email_service.py     # Email processing logic
│   │   └── log_service.py       # Logging service
│   │
│   └── 📁 utils/                # Utility functions
│       ├── email_parser.py      # Email parsing logic
│       ├── email_sender.py      # Email sending (optional)
│       ├── logger.py            # Logging utilities
│       └── 📁 pdf_generation/   # PDF generation module
│           ├── app.py           # PDF generation logic
│           ├── filters.py       # Jinja2 filters
│           ├── 📁 templates/    # HTML templates for PDF
│           │   ├── confirmation.html
│           │   └── template_confirmation.html
│           └── 📁 static/       # Static assets (CSS, images)
│
├── 📁 instance/                 # Instance folder
│   └── db.sqlite3               # SQLite database
│
└── 📁 pdf/                      # Generated PDF storage
    └── 📁 2026/04/23/           # Organized by date
```

---

## 🔌 API Endpoints

### 📬 Email Management

#### Get All Emails

```http
GET /api/email
```

**Response:** Array of all stored emails

#### Get Specific Email

```http
GET /api/email/{id}
```

**Response:** Single email details or 404 if not found

#### Create Email (Trigger PDF Generation)

```http
POST /api/email
Content-Type: application/json

{
  "recipient": "user@example.com",
  "subject": "Invoice Report",
  "body": "Customer Name: John Doe\nStart Date: 2026-04-01\nEnd Date: 2026-04-30\n...",
  "mail_type": "invoice"
}
```

**Response:** Created email with PDF path (201 Created)

#### Delete Email

```http
DELETE /api/email/{id}
```

**Response:** Success message or 404

### 📊 Logging

#### Get All Logs

```http
GET /api/log
```

**Response:** Array of all system and user events

---

## 📋 Email Body Format

For successful parsing, structure your email body as follows:

```
Customer Name: John Doe
Start Date: 2026-04-01
End Date: 2026-04-30
Amount: 1000.00
Description: Monthly service invoice
...
```

**Supported Fields:**

- `Customer Name` - Client name
- `Start Date` - Period start (YYYY-MM-DD)
- `End Date` - Period end (YYYY-MM-DD)
- Additional custom fields (parsed based on implementation)

---

## 🔧 Configuration

Edit `config.py` to modify settings:

```python
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### Environment Variables (Optional)

Create a `.env` file for sensitive data:

```env
FLASK_ENV=development
FLASK_DEBUG=False
DATABASE_URL=sqlite:///db.sqlite3
```

---

## 🎨 PDF Generation

The system generates PDFs using:

- **Jinja2** - HTML template rendering with custom filters
- **Playwright** - Headless browser for HTML-to-PDF conversion
- **Custom Filters** - Format data (currency, dates, etc.)

Templates are located in `app/utils/pdf_generation/templates/`

---

## 📝 How It Works

```
1. Client sends email via POST /api/email
                    ↓
2. API validates input (EmailDTO)
                    ↓
3. Email body parsed → structured data (EmailContent)
                    ↓
4. Parsed data injected into Jinja2 template
                    ↓
5. Template rendered as HTML
                    ↓
6. Playwright generates PDF from HTML
                    ↓
7. PDF saved to date-organized directory
                    ↓
8. Email metadata + PDF path stored in database
                    ↓
9. User/system events logged
                    ↓
10. Response sent to client with email details
```

---

## 🛡️ Error Handling

| Error               | Status | Meaning                                  |
| ------------------- | ------ | ---------------------------------------- |
| Invalid JSON        | 400    | Request body is not valid JSON           |
| Invalid Data Format | 400    | Required fields are missing or malformed |
| Email Not Found     | 404    | Email ID doesn't exist                   |
| Not Found           | 404    | Endpoint doesn't exist                   |

---

## 📦 Dependencies

| Package              | Purpose                         |
| -------------------- | ------------------------------- |
| **Flask**            | Web framework                   |
| **Flask-SQLAlchemy** | ORM for database                |
| **Pydantic**         | Data validation                 |
| **Jinja2**           | Template engine                 |
| **Playwright**       | Browser automation for PDF      |
| **python-dotenv**    | Environment variable management |

---

## 🧪 Testing

### Manual Testing with cURL

```bash
# Get all emails
curl http://localhost:5000/api/email

# Get specific email
curl http://localhost:5000/api/email/1

# Create new email
curl -X POST http://localhost:5000/api/email \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": "user@example.com",
    "subject": "Test Invoice",
    "body": "Customer Name: Test\nStart Date: 2026-04-01\nEnd Date: 2026-04-30",
    "mail_type": "invoice"
  }'

# Get logs
curl http://localhost:5000/api/log

# Delete email
curl -X DELETE http://localhost:5000/api/email/1
```

---

## 📊 Database Schema

### Email Table

| Column    | Type    | Description                      |
| --------- | ------- | -------------------------------- |
| id        | INTEGER | Primary key                      |
| recipient | STRING  | Email address                    |
| subject   | STRING  | Email subject                    |
| mail_type | STRING  | Category (invoice, report, etc.) |
| body      | TEXT    | Raw email content                |
| pdf_path  | STRING  | Generated PDF file path          |

### Log Table

| Column     | Type     | Description         |
| ---------- | -------- | ------------------- |
| id         | INTEGER  | Primary key         |
| event_type | STRING   | System or User      |
| message    | STRING   | Event description   |
| status     | BOOLEAN  | Success/Failure     |
| timestamp  | DATETIME | When event occurred |

---

## 🚦 Logging

The system tracks two types of events:

### User Events

- Email parsing completion
- PDF generation success/failure
- Document storage

### System Events

- Database operations
- Service failures
- Error conditions

View all events at: `GET /api/log`

---

## 💡 Use Cases

✅ **Invoice Management** - Auto-generate invoices from email data
✅ **Report Automation** - Create periodic reports from parsed emails
✅ **Document Archival** - Organize and store documents by date
✅ **Audit Trails** - Complete logging of all operations
✅ **Workflow Integration** - Integrate with email systems and CRMs

---

## 📞 Support & Contribution

For issues, questions, or improvements, please refer to:

- **API Documentation:** See `API_DOCS.md`
- **Improvement Guide:** See `IMPROVE.md`
- **Code Structure:** Review comments in source files

---

## 📜 License

This project is licensed under the MIT License - feel free to use it in your projects!

---

<div align="center">

**Made with ❤️ for automation enthusiasts**

[⬆ Back to Top](#-email-agent-pdf-generation-backend)

</div>
