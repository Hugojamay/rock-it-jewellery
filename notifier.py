from twilio.rest import Client
from config import Config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_whatsapp_alert(payload, post_url):
    try:
        if not Config.TWILIO_ACCOUNT_SID or not Config.TWILIO_AUTH_TOKEN:
            print("⚠️ Twilio no configurado. Alerta de WhatsApp omitida.")
            return

        client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
        
        message_body = (
            f"🚨 *NUEVO PROSPECTO DETECTADO* 🚨\n\n"
            f"👤 *Usuario:* {payload['username']}\n"
            f"🌐 *Plataforma:* {payload['platform']}\n"
            f"💎 *Interés:* {payload['problem']}\n"
            f"⚡ *Urgencia:* {payload['urgency']}\n\n"
            f"💬 *Lo que escribió:* \"{payload['post_text']}\"\n\n"
            f"💡 *Mensaje sugerido para responder:* \n_{payload['suggested_message']}_\n\n"
            f"🔗 *Enlace:* {post_url}"
        )

        message = client.messages.create(
            body=message_body,
            from_=Config.TWILIO_WHATSAPP_NUMBER,
            to=Config.MY_WHATSAPP_NUMBER
        )
        print(f"✅ Alerta de WhatsApp enviada con éxito. SID: {message.sid}")
    except Exception as e:
        print(f"❌ Error al enviar WhatsApp: {str(e)}")

def send_email_alert(payload, post_url):
    try:
        if not Config.SENDER_EMAIL or not Config.SENDER_PASSWORD:
            print("⚠️ SMTP no configurado. Alerta de email omitida.")
            return

        msg = MIMEMultipart()
        msg['From'] = Config.SENDER_EMAIL
        msg['To'] = Config.DESTINATION_EMAIL
        msg['Subject'] = f"💎 Nuevo Prospecto Joyería: {payload['problem']}"

        body = (
            f"Nuevo prospecto capturado:\n\n"
            f"Usuario: {payload['username']}\n"
            f"Interés: {payload['problem']}\n"
            f"Urgencia: {payload['urgency']}\n"
            f"Texto: {payload['post_text']}\n\n"
            f"Mensaje sugerido:\n{payload['suggested_message']}\n\n"
            f"Enlace: {post_url}"
        )
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
        server.starttls()
        server.login(Config.SENDER_EMAIL, Config.SENDER_PASSWORD)
        server.sendmail(Config.SENDER_EMAIL, Config.DESTINATION_EMAIL, msg.as_string())
        server.quit()
        print("✅ Alerta por Email enviada con éxito.")
    except Exception as e:
        print(f"❌ Error al enviar Email: {str(e)}")