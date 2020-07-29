import requests
import smtplib, ssl

delayMessage = "File {} at your desk is delayed by {} days!"

def send_mail(receiver,fid,delay):
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "foodwastagemanger@gmail.com"
    password = 'shreyatej93'
    receiver_email = receiver  # "kadusaswit16e@student.mes.ac.in"
    subject = "File Delay"
    message = """\
    Subject: File delay

    """+delayMessage.format(fid,delay)

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        # TODO: Send email here
        server.sendmail(sender_email, receiver_email, message)

    except Exception as e:
        # Print any error messages to stdout
        print(e)
    # finally:
    # server.quit()

send_mail("sahilkadu12@gmail.com","654","50")