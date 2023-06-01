import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib import colors

# Make API request and extract desired information
response = requests.get('https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow')
data = response.json()
print(data)
# Check if the response contains any questions
if 'items' in data:
    questions = data['items'][:50]  # Fetch the first 50 questions
else:
    questions = []

# Create PDF document
pdf_buffer = BytesIO()
pdf = canvas.Canvas(pdf_buffer)

# Set the font for header
pdf.setFont("Helvetica-Bold", 16)  # Set the font as bold
pdf.setFillColor(colors.red)  # Set the fill color as red

# Add header
header_text = 'Stack Overflow Information'
pdf.drawString(10, 800, header_text)

# Set the font for information
pdf.setFont("Helvetica", 12)

# Add extracted information to the PDF
y_pos = 780  # Initial y-position for the first question
for question in questions:
    title = question['title']
    link = question['link']
    view_count = question['view_count']
    
    info_text = f'\nTitle: {title}\nQuestion Link: {link}\nView Count: {view_count}'
    pdf.drawString(10, y_pos, info_text)
    y_pos -= 60  # Decrease y-position for the next question

pdf.showPage()
pdf.save()

# Save the PDF file locally
with open('stackoverflow_info.pdf', 'wb') as file:
    file.write(pdf_buffer.getvalue())

# Read the PDF content and extract text
pdf_text = []
with open('stackoverflow_info.pdf', 'rb') as file:
    pdf_reader = PdfReader(file)
    for page in pdf_reader.pages:
        pdf_text.append(page.extract_text())

# Extracted text content
text_content = '\n'.join(pdf_text)

# Send the text content via email
smtp_username = input("Enter your username: ")
smtp_password = input("Enter your password: ")
recipient_email = input("Enter the recipient: ")

# Compose email message
msg = MIMEMultipart()
msg['From'] = smtp_username
msg['To'] = recipient_email
msg['Subject'] = 'Stack Overflow Information'

# Attach the text content as email body
email_body = '\n'.join(f'<strong>{question["title"]}</strong><br>{question["link"]}<br>View Count: {question["view_count"]}<br><br>' for question in questions)
msg.attach(MIMEText(email_body, 'html'))

# Send email
with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.send_message(msg)

print('Successful')
