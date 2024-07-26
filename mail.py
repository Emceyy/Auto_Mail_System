import smtplib # açılımı: Simple Mail Transfer Protocol

# mail oluşturmak ve düzenlemek için kullandığımız kütüpahaneler:
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# .env dosyasından çekmek için kullandığımız kütüphaneler:
import os
from dotenv import load_dotenv

def send_email():

    load_dotenv() # env dosyasındaki verilerimizi çağırıyoruz.

    sender_password = os.getenv("SENDER_PASSWORD")
    sender_email = os.getenv("SENDER_EMAIL")
    recipient_email = os.getenv("RECIPIENT_EMAIL")
    subject = "Scada Aşım Bilgisi"

    while True:
        user_input = input("Değer Giriniz (Çıkmak için 'q' ya basınız): ")
        if user_input.lower() == "q":
            break

        try:
            Scada_Value = int(user_input)
            base_value = int(os.getenv("BASE_VALUE"))

            if Scada_Value >= 0.8 * base_value:
                # girilen değer base değerin yüzde seksenini aştığı takdirde mail gönderilecek.
                body = f"Scada Değeri Aşıldı\nBase Değer: {base_value}\nGirilen Değer: {Scada_Value}"

                smtp_server = "smtp.gmail.com"
                smtp_port = 587

                with smtplib.SMTP(smtp_server, smtp_port) as server: # with ile işlem bittikten sonra SMTP otomatik olarak sonlanır.

                    server.starttls()
                    server.login(sender_email, sender_password)

                    # mail oluşturuluyor:
                    msg = MIMEMultipart("alternative")
                    msg["Subject"] = subject
                    msg["From"] = sender_email
                    msg["To"] = recipient_email

                    part1 = MIMEText(body, "plain", "utf-8")
                    msg.attach(part1)

                    server.sendmail(sender_email, recipient_email, msg.as_string())
                    print("Email sent successfully!")
            else:
                print("Scada Değeri Aşılmadı.")
        except ValueError:
            print("Invalid input. Please enter a valid integer or 'q' to quit.")

if __name__ == "__main__":
    send_email()
