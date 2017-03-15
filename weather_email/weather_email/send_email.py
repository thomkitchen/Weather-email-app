import smtplib
from email.mime.text import MIMEText

#Module to send an email. Accepts a recipient, subject and body text and uses mailgun to send the email
class SendEmail():
	def send(to, subject, body):
		try:
			msg = MIMEText(body, 'html')
			msg['Subject'] = subject
			msg['From']    = "klaviyo_coding@challenge.com"
			msg['To']      = to

			s = smtplib.SMTP('smtp.mailgun.org', 587)
			s.login('postmaster@sandbox0abca8b8d2d3490cb4455295e313b18c.mailgun.org', 'c3dc6f55bf4774a93c1ee09b0f36e0cc')
			s.sendmail(msg['From'], msg['To'], msg.as_string())
			s.quit()
			print("Successfully sent email to " + msg['to'])
		except (smtplib.SMTPDataError):
			print( "Error sending email to " + msg['to'] + ". They most likely haven't accepted the invite to receive emails from this address")