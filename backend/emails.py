import smtplib
import env
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = env.EMAIL
password = env.EMAIL_PASSWORD


def send_order_confirmation(id: int, email: str, name: str, phone: str, address: dict):
    receiver_email = email

    message = MIMEMultipart("alternative")
    message["Subject"] = "Děkujeme za Vaši objednávku"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"""\
    Dobrý den {name}, \n
    Děkujeme Vám za objadnávku č.{id}\n
    Objednávku právě zpracováváme a hned jak to bude možné odešleme ji na Vámi zadanou adresu: \n
    {name}, {phone} \n 
    {address["city"]} {address["postal_code"]} \n
    {address["line1"]} \n
    Se srdečným pozdravem, \n
    Váš tým Weathery"""
    html = f"""\
    <html>
      <body>
        <h3>Dobrý den {name}</h3>
        <p>Děkujeme Vám za objadnávku č.<a href="https://weathery.svs.gyarab.cz/objednavka/{id}">{id}</a></p>
        <p>Objednávku právě zpracováváme a hned jak to bude možné odešleme ji na Vámi zadanou adresu: <br>
          <i>{name}, {phone}<br>
          {address["city"]}, {address["line1"]}<br>
          {address["postal_code"]}</i><br>
        </p>
        <p>Se srdečným pozdravem, <br>
        Váš tým Weathery</p>
      </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
