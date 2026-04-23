# 📚 API Documentation

> Complete reference guide for all Email Agent PDF Generation Backend endpoints

---

## Table of Contents

1. [Authentication](#authentication)
2. [Base URL](#base-url)
3. [Email Endpoints](#email-endpoints)
4. [Log Endpoints](#log-endpoints)
5. [Response Format](#response-format)
6. [Error Codes](#error-codes)
7. [Examples](#examples)

---

## 🔐 Authentication

Currently, the API **does not require authentication**. All endpoints are publicly accessible.

**Future Enhancement:** Add JWT or API key authentication (see IMPROVE.md)

---

## 🌐 Base URL

```
http://localhost:5000
```

All endpoints should be prefixed with this URL.

---

## 📧 Email Endpoints

### 1️⃣ List All Emails

Retrieve all emails stored in the system.

```http
GET /api/email
```

#### Parameters

None required

#### Response

**Status:** `200 OK`

```json
[
  {
    "id": 1,
    "recipient": "john@example.com",
    "subject": "April Invoice",
    "mail_type": "invoice",
    "body": "Customer Name: John Doe\n...",
    "pdf_path": "pdf/2026/04/23/john_doe_invoice.pdf"
  },
  {
    "id": 2,
    "recipient": "jane@example.com",
    "subject": "May Report",
    "mail_type": "report",
    "body": "Customer Name: Jane Smith\n...",
    "pdf_path": "pdf/2026/04/23/jane_smith_report.pdf"
  }
]
```

#### Example Usage

**cURL:**

```bash
curl http://localhost:5000/api/email
```

**Python:**

```python
import requests

response = requests.get('http://localhost:5000/api/email')
emails = response.json()
print(emails)
```

**JavaScript:**

```javascript
fetch("http://localhost:5000/api/email")
  .then((res) => res.json())
  .then((data) => console.log(data));
```

---

### 2️⃣ Get Specific Email

Retrieve details of a single email by ID.

```http
GET /api/email/{id}
```

#### Parameters

| Name | Type    | Description               |
| ---- | ------- | ------------------------- |
| `id` | Integer | Email ID (path parameter) |

#### Response

**Status:** `200 OK`

```json
{
  "id": 1,
  "recipient": "john@example.com",
  "subject": "April Invoice",
  "mail_type": "invoice",
  "body": "Customer Name: John Doe\nStart Date: 2026-04-01\nEnd Date: 2026-04-30\nAmount: 1000.00",
  "pdf_path": "pdf/2026/04/23/john_doe_invoice.pdf"
}
```

#### Error Response

**Status:** `404 Not Found`

```json
{
  "error": "Email not found"
}
```

#### Example Usage

**cURL:**

```bash
curl http://localhost:5000/api/email/1
```

**Python:**

```python
import requests

response = requests.get('http://localhost:5000/api/email/1')
if response.status_code == 200:
    email = response.json()
    print(email)
else:
    print(f"Error: {response.status_code}")
```

**JavaScript:**

```javascript
fetch("http://localhost:5000/api/email/1")
  .then((res) => {
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  })
  .then((data) => console.log(data))
  .catch((err) => console.error(err));
```

---

### 3️⃣ Create Email (Trigger PDF Generation)

Create a new email and automatically generate a PDF from the parsed content.

```http
POST /api/email
Content-Type: application/json
```

#### Request Body

```json
{
  "recipient": "user@example.com",
  "subject": "Invoice Report",
  "body": "Customer Name: John Doe\nStart Date: 2026-04-01\nEnd Date: 2026-04-30\nAmount: 1500.00",
  "mail_type": "invoice"
}
```

#### Parameters

| Name        | Type         | Required | Description                                   |
| ----------- | ------------ | -------- | --------------------------------------------- |
| `recipient` | Email String | ✅       | Valid email address                           |
| `subject`   | String       | ✅       | Email subject (max 255 chars)                 |
| `body`      | String       | ✅       | Email content with parsed fields              |
| `mail_type` | String       | ✅       | Category: "invoice", "report", "confirmation" |

#### Response

**Status:** `201 Created`

```json
{
  "id": 3,
  "recipient": "user@example.com",
  "subject": "Invoice Report",
  "mail_type": "invoice",
  "body": "Customer Name: John Doe\nStart Date: 2026-04-01\nEnd Date: 2026-04-30\nAmount: 1500.00",
  "pdf_path": "pdf/2026/04/23/user_invoice.pdf"
}
```

#### Error Responses

**Status:** `400 Bad Request` - Invalid JSON

```json
{
  "error": "Request must be JSON"
}
```

**Status:** `400 Bad Request` - Invalid data format

```json
{
  "error": "Invalid data format"
}
```

**Status:** `400 Bad Request` - Invalid email format

```json
{
  "error": "Invalid email address"
}
```

#### Email Body Format

```
Customer Name: John Doe
Start Date: 2026-04-01
End Date: 2026-04-30
Amount: 1500.00
Description: Monthly services
Invoice Number: INV-2026-001
```

**⚠️ Important:** Ensure your email body contains properly formatted fields. The system uses regex to extract:

- `Customer Name: <name>`
- `Start Date: <YYYY-MM-DD>`
- `End Date: <YYYY-MM-DD>`

#### Example Usage

**cURL:**

```bash
curl -X POST http://localhost:5000/api/email \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": "user@example.com",
    "subject": "Invoice Report",
    "body": "Customer Name: John Doe\nStart Date: 2026-04-01\nEnd Date: 2026-04-30\nAmount: 1500.00",
    "mail_type": "invoice"
  }'
```

**Python:**

```python
import requests

payload = {
    "recipient": "user@example.com",
    "subject": "Invoice Report",
    "body": "Customer Name: John Doe\nStart Date: 2026-04-01\nEnd Date: 2026-04-30\nAmount: 1500.00",
    "mail_type": "invoice"
}

response = requests.post('http://localhost:5000/api/email', json=payload)
print(response.status_code)
print(response.json())
```

**JavaScript:**

```javascript
const payload = {
  recipient: "user@example.com",
  subject: "Invoice Report",
  body: "Customer Name: John Doe\nStart Date: 2026-04-01\nEnd Date: 2026-04-30\nAmount: 1500.00",
  mail_type: "invoice",
};

fetch("http://localhost:5000/api/email", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(payload),
})
  .then((res) => res.json())
  .then((data) => console.log(data));
```

---

### 4️⃣ Update Email

Update an existing email record.

```http
PUT /api/email/{id}
Content-Type: application/json
```

#### Parameters

| Name | Type    | Description               |
| ---- | ------- | ------------------------- |
| `id` | Integer | Email ID (path parameter) |

#### Response

**Status:** `200 OK`

```json
{}
```

⚠️ **Note:** Currently returns empty response. See IMPROVE.md for enhancements.

---

### 5️⃣ Delete Email

Delete an email record by ID.

```http
DELETE /api/email/{id}
```

#### Parameters

| Name | Type    | Description               |
| ---- | ------- | ------------------------- |
| `id` | Integer | Email ID (path parameter) |

#### Response

**Status:** `200 OK`

```json
{
  "message": "Email deleted successfully"
}
```

#### Error Response

**Status:** `404 Not Found`

```json
{
  "error": "Email not found"
}
```

#### Example Usage

**cURL:**

```bash
curl -X DELETE http://localhost:5000/api/email/1
```

**Python:**

```python
import requests

response = requests.delete('http://localhost:5000/api/email/1')
print(response.json())
```

**JavaScript:**

```javascript
fetch("http://localhost:5000/api/email/1", {
  method: "DELETE",
})
  .then((res) => res.json())
  .then((data) => console.log(data));
```

---

## 📊 Log Endpoints

### Get All Logs

Retrieve all system and user event logs.

```http
GET /api/log
```

#### Parameters

None required

#### Response

**Status:** `200 OK`

```json
[
  {
    "id": 1,
    "event_type": "user",
    "message": "Email parsed successfully for recipient: john@example.com",
    "status": true,
    "timestamp": "2026-04-23 10:30:45"
  },
  {
    "id": 2,
    "event_type": "system",
    "message": "PDF generated and saved successfully",
    "status": true,
    "timestamp": "2026-04-23 10:30:46"
  },
  {
    "id": 3,
    "event_type": "system",
    "message": "Email parsing failed: Invalid date format",
    "status": false,
    "timestamp": "2026-04-23 10:31:15"
  }
]
```

#### Log Entry Structure

| Field        | Type    | Description                       |
| ------------ | ------- | --------------------------------- |
| `id`         | Integer | Log entry ID                      |
| `event_type` | String  | "system" or "user"                |
| `message`    | String  | Event description                 |
| `status`     | Boolean | Success (true) or failure (false) |
| `timestamp`  | String  | When event occurred               |

#### Example Usage

**cURL:**

```bash
curl http://localhost:5000/api/log
```

**Python:**

```python
import requests

response = requests.get('http://localhost:5000/api/log')
logs = response.json()
for log in logs:
    print(f"[{log['timestamp']}] {log['event_type']}: {log['message']}")
```

---

## 📤 Response Format

All API responses follow a consistent format:

### Success Response

```json
{
  "id": 1,
  "recipient": "user@example.com",
  "subject": "Invoice",
  ...
}
```

### Error Response

```json
{
  "error": "Description of what went wrong"
}
```

### List Response

```json
[
  { /* item 1 */ },
  { /* item 2 */ },
  ...
]
```

---

## ⚠️ Error Codes

| Code    | Message               | Meaning                                           |
| ------- | --------------------- | ------------------------------------------------- |
| **200** | OK                    | Request successful                                |
| **201** | Created               | Resource created successfully                     |
| **400** | Bad Request           | Invalid request format or missing required fields |
| **404** | Not Found             | Resource doesn't exist                            |
| **500** | Internal Server Error | Server-side error (uncommon)                      |

---

## 📋 Request/Response Examples

### Complete Workflow Example

#### Step 1: Create Email with PDF Generation

```bash
curl -X POST http://localhost:5000/api/email \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": "client@company.com",
    "subject": "Q2 2026 Invoice",
    "body": "Customer Name: ABC Corporation\nStart Date: 2026-04-01\nEnd Date: 2026-06-30\nAmount: 5000.00\nDescription: Consulting Services",
    "mail_type": "invoice"
  }'
```

**Response:**

```json
{
  "id": 5,
  "recipient": "client@company.com",
  "subject": "Q2 2026 Invoice",
  "mail_type": "invoice",
  "body": "Customer Name: ABC Corporation\nStart Date: 2026-04-01\nEnd Date: 2026-06-30\nAmount: 5000.00\nDescription: Consulting Services",
  "pdf_path": "pdf/2026/04/23/client_invoice.pdf"
}
```

#### Step 2: Verify PDF was Generated

Check the `pdf_path` field - the PDF file should exist at that location.

#### Step 3: Retrieve the Email

```bash
curl http://localhost:5000/api/email/5
```

#### Step 4: View System Logs

```bash
curl http://localhost:5000/api/log
```

#### Step 5: Delete if Needed

```bash
curl -X DELETE http://localhost:5000/api/email/5
```

---

## 🔗 Integration Examples

### React Integration

```javascript
async function createInvoiceEmail(emailData) {
  try {
    const response = await fetch("http://localhost:5000/api/email", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        recipient: emailData.email,
        subject: emailData.subject,
        body: emailData.body,
        mail_type: "invoice",
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const result = await response.json();
    console.log("PDF generated at:", result.pdf_path);
    return result;
  } catch (error) {
    console.error("Failed to create invoice:", error);
  }
}
```

### Django Integration

```python
import requests

def generate_invoice_pdf(customer_data):
    payload = {
        "recipient": customer_data['email'],
        "subject": f"Invoice {customer_data['invoice_num']}",
        "body": f"""Customer Name: {customer_data['name']}
Start Date: {customer_data['start_date']}
End Date: {customer_data['end_date']}
Amount: {customer_data['amount']}""",
        "mail_type": "invoice"
    }

    response = requests.post('http://localhost:5000/api/email', json=payload)
    return response.json()
```

### Vue Integration

```javascript
import axios from "axios";

const emailService = {
  async createEmail(emailData) {
    try {
      const { data } = await axios.post("/api/email", emailData);
      return data;
    } catch (error) {
      console.error("API Error:", error.response.data);
      throw error;
    }
  },

  async getEmail(id) {
    const { data } = await axios.get(`/api/email/${id}`);
    return data;
  },

  async deleteEmail(id) {
    await axios.delete(`/api/email/${id}`);
  },
};
```

---

## 💡 Tips & Best Practices

✅ **Do:**

- Validate email addresses before sending to API
- Use consistent date format (YYYY-MM-DD)
- Check HTTP status codes in your client
- Store the `pdf_path` for later access
- Include all required fields in requests

❌ **Don't:**

- Send malformed JSON
- Use invalid email addresses
- Forget the Content-Type header
- Make requests without error handling
- Store sensitive data in email body

---

## 🆘 Troubleshooting

### Problem: "Invalid JSON" Error

**Solution:** Ensure Content-Type header is `application/json` and JSON is properly formatted

### Problem: "Email not found" 404

**Solution:** Verify the email ID exists with `GET /api/email`

### Problem: PDF not generating

**Solution:** Check email body format matches expected regex patterns (see Email Body Format section)

### Problem: Connection refused

**Solution:** Ensure Flask app is running on `http://localhost:5000`

---

<div align="center">

**Need more help? Check README.md and IMPROVE.md**

[⬆ Back to Top](#-api-documentation)

</div>
