import subprocess
import requests
import socket
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import uuid

# 获取RustDesk ID
def get_rustdesk_id():
    try:
        result = subprocess.run(['sudo', 'rustdesk', '--get-id'], capture_output=True, text=True, check=True)
        rustdesk_id = result.stdout.strip()
        return rustdesk_id
    except subprocess.CalledProcessError as e:
        return f"Error retrieving RustDesk ID: {e}"

# 获取公共IP地址
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        return response.text
    except requests.RequestException as e:
        return f"Error retrieving IP: {e}"

# 获取本地局域网IP地址
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.254.254.254', 1))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        return f"Error retrieving local IP: {e}"

# 获取开放端口信息
def get_open_ports():
    return [80, 22]  # 用于示例的静态列表

# 获取时间戳
def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 获取MAC地址
def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0, 11, 2)])

# 发送邮件
def send_email(subject, body, to_email):
    from_email = 'your_email@example.com'
    password = 'your_app_specific_password'

    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, message.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")

# 主函数
def main():
    public_ip = get_public_ip()
    local_ip = get_local_ip()
    open_ports = get_open_ports()
    rustdesk_id = get_rustdesk_id()
    timestamp = get_timestamp()
    mac_address = get_mac_address()

    email_subject = "Client NB IP, MAC, and Port Report"
    email_body = (
        f"Time: {timestamp}\n"
        f"Public IP: {public_ip}\n"
        f"Local IP: {local_ip}\n"
        f"MAC Address: {mac_address}\n"
        f"RustDesk ID: {rustdesk_id}\n"
        f"Open Ports: {open_ports}\n"
    )

    send_email(email_subject, email_body, 'recipient_email@example.com')
    print(f"Report sent: Public IP - {public_ip}, Local IP - {local_ip}, MAC - {mac_address}")

if __name__ == "__main__":
    main()
