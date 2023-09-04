import requests
import json
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def execute():
    url = "https://weatherapi-com.p.rapidapi.com/current.json"

    querystring = {"q":"17.4401, 78.3489"}

    headers = {
        "X-RapidAPI-Key": os.environ["API_TOKEN"],
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    response  = response.content.decode("utf-8")
    response = json.loads(response)


    # Set up your email parameters
    sender_email = "tarunmuchhal11@gmail.com"
    recipient_email = "tarunmuchhal11@gmail.com"
    subject = "Sending weather data"
    smtp_server = "smtp.gmail.com" 
    smtp_port = 587  # Port for TLS (587 for Gmail)
    smtp_username = "tarunmuchhal11@gmail.com"
    smtp_password = os.environ["GMAIL_USER"]

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    html_content = f"""
    <html>
    <body style="font-size: 18px;">
        <p>Here is a PNG image:</p>
        <br/><strong>"Today we mostly experience : "   <strong/>, {response["current"]["condition"]["text"]}<strong/>
        <br/><strong>"Time : "                         <strong/>, {response["current"]["last_updated"]}
        <br/><strong>"Temprature : "                   <strong/>, {response["current"]["temp_c"]}
        <br/><strong>"Wind speed : "                   <strong/>, {str(response["current"]["wind_kph"]) + " km/h"}
        <br/><strong>"Humidity level : "               <strong/>, {str(response["current"]["humidity"]) + "%"}
        <br/><strong>"Cloud :"                         <strong/>, {str(response["current"]["cloud"]) + "%"}
    </body>
    </html>
    """
    # Attach the HTML content to the email
    html_part = MIMEText(html_content, "html")
    message.attach(html_part)
    # Create an SMTP connection and send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Email sending failed: {str(e)}")
    finally:
        server.quit()


if __name__ == "__main__":
    execute()
