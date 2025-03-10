import os
import json
import base64
from email import encoders
from dotenv import load_dotenv
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from mensal_summary.create_pdf import create_pdf

load_dotenv()

PDF_PATH = "relatorio_mensal.pdf"

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def send_summary(destination, dashboard_df, om_data, expenses_data):
    create_pdf(dashboard_df, om_data, expenses_data)
    enviar_email_com_anexo(
        destinatario=destination,
        assunto="Relatório Mensal",
        mensagem="Segue em anexo o relatório mensal.",
        pdf_path=PDF_PATH,
    )


def carregar_credenciais():
    creds = None
    token_str = os.getenv("GMAIL_TOKEN")

    if token_str:
        token_data = json.loads(token_str)

        # Converter expiry para um objeto datetime, se necessário
        from datetime import datetime

        if "expiry" in token_data and isinstance(token_data["expiry"], str):
            token_data["expiry"] = datetime.strptime(
                token_data["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )

        creds = Credentials(**token_data)

        # Se o token expirou, tenta atualizar automaticamente
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            salvar_token(creds)  # Atualiza o token no .env

    else:
        # Caso não haja token, inicia o fluxo de autenticação
        creds = autenticar_usuario()
        salvar_token(creds)  # Salva o novo token no .env

    return creds


def salvar_token(creds):
    """Salva o token atualizado no .env"""
    token_dict = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
    }
    os.environ["GMAIL_TOKEN"] = json.dumps(token_dict)

    # Atualiza o .env
    with open(".env", "w") as env_file:
        env_file.write(f"GMAIL_TOKEN={json.dumps(token_dict)}\n")


def enviar_email_com_anexo(destinatario, assunto, mensagem, pdf_path):
    creds = carregar_credenciais()
    service = build("gmail", "v1", credentials=creds)
    msg = MIMEMultipart()
    msg["From"] = os.getenv("GMAIL_SENDER", "seuemail@gmail.com")
    msg["To"] = destinatario
    msg["Subject"] = assunto

    # Corpo do e-mail
    msg.attach(MIMEText(mensagem, "plain"))

    # Adicionar anexo PDF
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(pdf_path)}",
        )
        msg.attach(part)
    else:
        print(f"Erro: O arquivo {pdf_path} não foi encontrado.")

    # Enviar a mensagem
    raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    message = {"raw": raw_message}

    try:
        sent_message = (
            service.users().messages().send(userId="me", body=message).execute()
        )
        print(f"E-mail enviado com sucesso! ID: {sent_message['id']}")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")


def autenticar_usuario():
    """Inicia o fluxo OAuth2 para autenticação do usuário."""
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)
    return creds


if __name__ == "__main__":
    enviar_email_com_anexo(
        destinatario="destinatario@exemplo.com",
        assunto="Relatório Mensal",
        mensagem="Segue em anexo o relatório mensal.",
        pdf_path=PDF_PATH,
    )
