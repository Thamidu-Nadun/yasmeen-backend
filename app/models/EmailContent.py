import json

class EmailContent:
    def __init__(self, customer_name: str = None, start_date = "YY/MM/DD", end_date="YY/MM/DD",
                 total_pax: int = 0, operator_name: str = None,
                 vehicle_type: str = None,
                 staff_assignment: dict = None,
                 iternary: list = None,
                 requests: list = None,
                 total_fee: int = 0,
                 payment_method: str = None):
        self.customer_name = customer_name
        self.start_date = start_date
        self.end_date = end_date
        self.total_pax = total_pax
        self.operator_name = operator_name
        self.vehicle_type = vehicle_type
        self.staff_assignment = staff_assignment if staff_assignment is not None else {}
        self.iternary = iternary if iternary is not None else []
        self.requests = requests if requests is not None else []
        self.total_fee = total_fee
        self.payment_method = payment_method
        
    def __str__(self):
        return json.dumps({
            "customer_name": self.customer_name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "total_pax": self.total_pax,
            "operator_name": self.operator_name,
            "vehicle_type": self.vehicle_type,
            "staff_assignment": self.staff_assignment,
            "iternary": self.iternary,
            "requests": self.requests,
            "total_fee": self.total_fee,
            "payment_method": self.payment_method
        }, indent=4)

    @classmethod
    def from_str_dict(cls, email_content_str: str):
        try:
            content_dict = json.loads(email_content_str)
            return cls(
                customer_name=content_dict.get("customer_name"),
                start_date=content_dict.get("start_date"),
                end_date=content_dict.get("end_date"),
                total_pax=content_dict.get("total_pax", 0),
                operator_name=content_dict.get("operator_name"),
                vehicle_type=content_dict.get("vehicle_type"),
                staff_assignment=content_dict.get("staff_assignment", {}),
                iternary=content_dict.get("iternary", []),
                requests=content_dict.get("requests", []),
                total_fee=content_dict.get("total_fee", 0),
                payment_method=content_dict.get("payment_method")
            )
        except json.JSONDecodeError as e:
            print(f"Error decoding email content: {e}")
            return cls()  # Return an empty EmailContent object on error
        
    def to_human_readable_string(self):
        return f"""
    Customer Name: {self.customer_name}
    Start Date: {self.start_date}
    End Date: {self.end_date}
    Total Pax: {self.total_pax}
    Operator Name: {self.operator_name}
    Vehicle Type: {self.vehicle_type}
    Staff Assignment: {json.dumps(self.staff_assignment, indent=4)}
    Iternary: {json.dumps(self.iternary, indent=4)}
    Requests: {json.dumps(self.requests, indent=4)}
    Total Fee: {self.total_fee}
    Payment Method: {self.payment_method}
    """

class Email:
    def __init__(self, to_email: str, subject: str, email_content: EmailContent):
        self.to_email = to_email
        self.subject = subject
        self.email_content = email_content
        
    def __str__(self):
        _email_content = json.loads(str(self.email_content))
        return json.dumps({
            "to_email": self.to_email,
            "subject": self.subject,
            "email_content": _email_content
        }, indent=4)