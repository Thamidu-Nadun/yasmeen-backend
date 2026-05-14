import os, datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from . import filters
from playwright.sync_api import sync_playwright
from ...models.EmailContent import EmailContent
import extensions

def render_template(html_template, data):
    template_dir = Path(__file__).parent / "templates"
    env = Environment(loader=FileSystemLoader(template_dir))
    env.filters['comma'] = filters.comma_format
    template = env.get_template(html_template)
    
    return template.render(data)

def generate_pdf(output_path, parsed_email_content: EmailContent):
    print("browser", extensions.browser)
    page = extensions.browser.new_page()
    try:
        start_date, end_date = None, None
        
        try:
            start_date = datetime.datetime.strptime(parsed_email_content.start_date, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(parsed_email_content.end_date, "%Y-%m-%d")
            
            issue_number = str(start_date.year) + " / " + start_date.strftime("%m%d") + "-" + end_date.strftime("%m%d")
           
        except Exception as e:
            print(f"Error parsing dates: {e}")
            issue_number = "N/A"
        
        generated_date = datetime.datetime.now().strftime("%Y / %m%d")
        content_injected = {
            "name": parsed_email_content.customer_name,
            "issue_number": issue_number,
            "generated_date": generated_date,
            "month": start_date.strftime("%b").upper() if start_date else "N/A",
            "passenger_count": parsed_email_content.total_pax,
            "operator": parsed_email_content.operator_name,
            "plans": '<br/>'.join(parsed_email_content.iternary),
            "requests": parsed_email_content.requests,
            "remarks": [
                "some remarks",
                "some more remarks"
            ],
            "vehicle_type": parsed_email_content.vehicle_type,
            "staff_assignment": parsed_email_content.staff_assignment,
            "total_fee": parsed_email_content.total_fee,
            "payment_method": parsed_email_content.payment_method if parsed_email_content.payment_method else "N/A",
            "taxi_charter_option": parsed_email_content.taxi_charter_option if parsed_email_content.taxi_charter_option else "N/A",
        }
        
        content = render_template("template_confirmation.html", content_injected)
        page.set_content(content)
        page.pdf(path=output_path, 
                format='A4', 
                print_background=True, 
                display_header_footer=False,
                margin={
                    "top": "8mm",
                    "bottom": "8mm",
                    "left": "8mm",
                    "right": "8mm"
                })
    except Exception as e:
        print(f"Error generating PDF: {e}")
    finally:
        page.close()


def save_pdf(file_name: str, parsed_email_content: EmailContent, out_path: str) -> str:
    """Generate PDF and save it in storage

    Args:
        file_name (string): Name of the file.
        email_body (TEXT): email body content to be included in the PDF
        out_path (string): the directory where the generated PDF will be saved

    Returns:
        string: path to the saved PDF file
    """
    output_path = os.path.join(out_path, f"{file_name}.pdf")
    if not os.path.exists(out_path):
        os.makedirs(out_path)
        
    print(f"Generating PDF at: {output_path}")
    generate_pdf(output_path, parsed_email_content)
    print(f"PDF generated and saved at: {output_path}")
    return output_path