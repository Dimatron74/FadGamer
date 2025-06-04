import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Настройки
smtp_server = 'smtp.mail.ru'
port = 465
login = 'dimalogachevlivny@xmail.ru'
password = 'sS3rNSTm8G23D6ZlYPof'

# Создаем сообщение
msg = MIMEMultipart()
msg['From'] = login
msg['To'] = 'dimalogachevlivny@gmail.com'
msg['Subject'] = 'Тестовое письмо'
body = 'Привет! Это тестовое сообщение.'
msg.attach(MIMEText(body, 'plain'))

try:
    with smtplib.SMTP_SSL(smtp_server, port) as server:
        print("Подключение...")
        server.login(login, password)
        print("Авторизация успешна")
        server.sendmail(login, 'dimalogachevlivny@gmail.com', msg.as_string())
        print("Письмо отправлено!")
except Exception as e:
    print("Ошибка:", str(e))