# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# def send_email(subject, body, to_email, smtp_server, smtp_port, smtp_username, smtp_password):
#     # Create the MIME object
#     message = MIMEMultipart()
#     message['From'] = smtp_username
#     message['To'] = to_email
#     message['Subject'] = subject

#     # Attach the body of the email
#     message.attach(MIMEText(body, 'plain'))

#     # Connect to the SMTP server
#     with smtplib.SMTP(smtp_server, smtp_port) as server:
#         # Login to the SMTP server
#         server.login(smtp_username, smtp_password)

#         # Send the email
#         server.sendmail(smtp_username, to_email, message.as_string())

#     print("Email sent successfully!")

# # Example usage
# # subject = "Test Email"
# # body = "This is a test email sent from Python."
# # to_email = "recipient@example.com"
# # smtp_server = "smtp.example.com"
# # smtp_port = 587  # Use the appropriate port for your SMTP server
# # smtp_username = "your_username"
# # smtp_password = "your_password"

# # # Call the function to send the email
# # send_email(subject, body, to_email, smtp_server, smtp_port, smtp_username, smtp_password)
