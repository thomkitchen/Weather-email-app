import smtplib
from email.mime.text import MIMEText

#Module to send an email. Accepts a recipient, subject and body text and uses mailgun to send the email
class SendEmail():
	def send(self, to, subject, body):
		try:
			g_user = "thomkitchenKLAVIYOTEST@gmail.com"
			g_pass = "testtest1"
			msg = MIMEText(body, 'html')
			msg['Subject'] = subject
			msg['From']    = "thomkitchenKLAVIYOTEST@gmail.com"
			msg['To']      = to

			s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
			s.ehlo()
			s.login(g_user, g_pass)
			s.sendmail(msg['From'], msg['To'], msg.as_string())
			s.quit()
			print("Successfully sent email to " + msg['to'])
		except (smtplib.SMTPDataError):
			print( "Error sending email to " + msg['to'] + ". They most likely haven't accepted the invite to receive emails from this address")