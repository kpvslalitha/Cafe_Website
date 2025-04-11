from flask import Flask, request, jsonify
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        name = request.form['Name']
        email = request.form['Email']
        people = request.form['People']
        date = request.form['Date']
        message = request.form['Message']

        # Compose email
        msg = EmailMessage()
        msg['Subject'] = 'Reservation Confirmation'
        msg['From'] = os.environ.get('EMAIL_USER')
        msg['To'] = email
        msg.set_content(f"""Hi {name},

Thanks for your reservation!

Details:
People: {people}
Date: {date}
Message: {message}

We look forward to seeing you!
""")

        # Send email
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(os.environ.get('EMAIL_USER'), os.environ.get('EMAIL_PASS'))
            smtp.send_message(msg)

        return 'Email sent successfully!'
    except Exception as e:
        return f'Error: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
