import re
from app.models import EmailContent

def clean_email_body(body: str):
    return body.strip().replace('[', '').replace(']', '')

def extract_email_data(email_body: str) -> EmailContent:
    """Parse raw email body to EmailContent object
    Args:
        email_content (str): email body as string
    Returns:
        EmailContent: parsed data as EmailContent object
    Note:
        This function uses regex to extract specific fields from the email body.
        Follow the expected email format for accurate parsing.
    """
    email_data = None
    email_data = EmailContent()
    section = None
    
    for line in email_body.splitlines():
        line = line.strip()
        if not line:
            continue
        
        if re.match(r'Customer\s+Name:', line, re.IGNORECASE):
            email_data.customer_name = line.split(':', 1)[1].strip()
        elif re.match(r'Start\s+Date:', line, re.IGNORECASE):
            email_data.start_date = line.split(':', 1)[1].strip()
        elif re.match(r'End\s+Date:', line, re.IGNORECASE):
            email_data.end_date = line.split(':', 1)[1].strip()
        elif re.match(r'Number\s+Of\s+Pax:', line, re.IGNORECASE):
            email_data.total_pax = int(line.split(':', 1)[1].strip())
        elif re.match(r'Booking\s+Staff:', line, re.IGNORECASE):
            email_data.operator_name = line.split(':', 1)[1].strip()
        elif re.match(r'Vehicle\s+Type:', line, re.IGNORECASE):
            email_data.vehicle_type = line.split(':', 1)[1].strip()
        elif re.match(r'Total\s+Fee\s+=', line, re.IGNORECASE):
            _price = line.split('=', 1)[1].strip()
            price_match = re.search(r'([\d,]+)', _price)
            if price_match:
                email_data.total_fee = int(price_match.group(1).replace(',', ''))
            else:
                email_data.total_fee = 0
        elif re.match(r'Payment\s+Method:', line, re.IGNORECASE):
            email_data.payment_method = line.strip()
                
        # sections matching
        elif re.match(r'\[Staff\s+(Assignment|Management)\]', line, re.IGNORECASE):
            section = 'staff_assignment'
            continue
        elif re.match(r'\[Route Plan / Itinerary\]', line, re.IGNORECASE):
            section = 'itinerary'
            continue
        elif re.match(r'\[Request(s)?\]', line, re.IGNORECASE):
            section = 'requests'
            continue
        elif re.match(r'\[Taxi\s+Charter\s+Fee\]', line, re.IGNORECASE):
            section = 'taxi_charter'
            continue
        elif '━' in line: # separator line
            section = None
            continue
        
        # section content parsing
        if section == 'staff_assignment' and line.startswith('-'):
            _line = line[1:].strip().split(':', 1)
            if len(_line) == 2:
                role = _line[0].strip()
                name = _line[1].strip()
                email_data.staff_assignment[role] = name
                
        elif section == 'itinerary':
            clean_line = line.rstrip('\n')
            if clean_line.startswith("---"): email_data.iternary.append("")
            else: email_data.iternary.append(clean_line)
            
        elif section == 'requests':
            clean_line = line.rstrip('\n')
            line = re.sub(r'-\s*', '', clean_line) # remove leading dash and spaces
            if line: email_data.requests.append(line)
        elif section == 'taxi_charter':
            clean_line = line.rstrip('\n')
            email_data.taxi_charter_option = clean_line
            
            
    return email_data

    
def extract_email_data_jp(email_body: str) -> EmailContent:
    """Parse raw email body to EmailContent object for Japanese format
    Args:
        email_content (str): email body as string
    Returns:
        EmailContent: parsed data as EmailContent object
    Note:
        This function uses regex to extract specific fields from the email body.
        Follow the expected email format for accurate parsing.
    """
    email_data = None
    email_data = EmailContent()
    section = None
    
    for line in email_body.splitlines():
        line = line.strip()
        if not line:
            continue
        
        if re.match(r'(Customer\s+Name:|お客様名[:：]|顧客名[:：])', line, re.IGNORECASE):
            email_data.customer_name = line.split(':', 1)[1].strip()
        elif re.match(r'(Start\s+Date:|開始日[:：])', line, re.IGNORECASE):
            email_data.start_date = line.split(':', 1)[1].strip()
        elif re.match(r'(End\s+Date:|終了日[:：])', line, re.IGNORECASE):
            email_data.end_date = line.split(':', 1)[1].strip()
        elif re.match(r'(Number\s+Of\s+Pax:|人数[:：])', line, re.IGNORECASE):
            email_data.total_pax = int(line.split(':', 1)[1].strip())
        elif re.match(r'(Booking\s+Staff:|予約担当者[:：])', line, re.IGNORECASE):
            email_data.operator_name = line.split(':', 1)[1].strip()
        elif re.match(r'(Vehicle\s+Type:|車両タイプ[:：])', line, re.IGNORECASE):
            email_data.vehicle_type = line.split(':', 1)[1].strip()
        elif re.match(r'(Total\s+Fee\s+=|総額\s*=)', line, re.IGNORECASE):
            _price = line.split('=', 1)[1].strip()
            price_match = re.search(r'([\d,]+)', _price)
            if price_match:
                email_data.total_fee = int(price_match.group(1).replace(',', ''))
            else:
                email_data.total_fee = 0
        elif re.match(r'(Payment\s+Method:|支払い方法[:：])', line, re.IGNORECASE):
            email_data.payment_method = line.strip()
        
        # sections matching
        elif re.match(r'\[(Staff\s+(Assignment|Management)|スタッフ(手配|管理))\]', line, re.IGNORECASE):
            section = 'staff_assignment'
            continue
        elif re.match(r'\[(Route Plan / Itinerary|行程表|旅程)\]', line, re.IGNORECASE):
            section = 'itinerary'
            continue
        elif re.match(r'\[(Request(s)?|ご要望)\]', line, re.IGNORECASE):
            section = 'requests'
            continue
        elif '━' in line: # separator line
            section = None
            continue
        
        # section content parsing
        if section == 'staff_assignment' and line.startswith('-'):
            _line = line[1:].strip().split(':', 1)
            if len(_line) == 2:
                role = _line[0].strip()
                name = _line[1].strip()
                email_data.staff_assignment[role] = name
                
        elif section == 'itinerary':
            clean_line = line.rstrip('\n')
            if clean_line.startswith("---"): email_data.iternary.append("")
            else: email_data.iternary.append(clean_line)
            
        elif section == 'requests':
            clean_line = line.rstrip('\n')
            line = re.sub(r'-\s*', '', clean_line) # remove leading dash and spaces
            if line: email_data.requests.append(line)
            
            
    return email_data
