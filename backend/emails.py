import smtplib
import env
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = env.EMAIL
password = env.EMAIL_PASSWORD


def send_email(receiver_email: str, subject: str, text: str, html: str):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


def send_order_confirmation(id: int, email: str, name: str, address: dict):
    subject = "Děkujeme za Vaši objednávku"
    text = f"""\
    Dobrý den {name}, \n
    Děkujeme Vám za objadnávku č.{id}\n
    Objednávku právě zpracováváme a hned jak to bude možné odešleme ji na Vámi zadanou adresu: \n
    {name}, \n 
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
          <i>{name},<br>
          {address["city"]}, {address["line1"]}<br>
          {address["postal_code"]}</i><br>
        </p>
        <p>Se srdečným pozdravem, <br>
        Váš tým Weathery</p>
      </body>
    </html>
    """
    send_email(email, subject, text, html)


def send_state_info(id: int, email: str, state: str):
    subject = "Změna svavu objednávky"
    text = f"""\
    Dobrý den, \n
    Chceme Vám oznámít, že stav u objednávky č.{id} se změnil na "{state}"\n
    Se srdečným pozdravem, \n
    Váš tým Weathery"""
    html = f"""\
    <html>
      <body>
        <h3>Dobrý den</h3>
        <p>Chceme Vám oznámít, že stav u objednávky č.<a href="https://weathery.svs.gyarab.cz/objednavka/{id}">{id} se změnil.</a></p>
        <p>Se srdečným pozdravem, <br>
        Váš tým Weathery</p>
      </body>
    </html>
    """
    send_email(email, subject, text, html)


def send_new_order_notification(id: int, emails: str):
    subject = "Nová objednávka"
    text = f"""\
    Mily admine, \n
    Prave vam prisla nova objednavka č.{id}, \n
    Pokuste se co nejdrive tudo objednavku vyridit :).
    """
    html = f"""
    <html>
        <body>
            <h3>Mily admine</h3>
            <p>Prave vam prisla nova objednavka č.<a href="https://weathery.svs.gyarab.cz/objednavka/{id}">{id}</a>,</p>
            <p>Pokuste se co nejdrive tudo objednavku vyridit :).</p> 
        </body>
    </html>
    """
    send_email(emails, subject, text, html)
