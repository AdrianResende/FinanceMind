import logging

from app.core.config import get_settings

logger = logging.getLogger("financemind.email")
settings = get_settings()


def send_email(to: str, subject: str, html: str) -> None:
    if not settings.resend_api_key:
        logger.info("RESEND_API_KEY não configurada — email não enviado. Para: %s | Assunto: %s\n%s", to, subject, html)
        return

    import resend

    resend.api_key = settings.resend_api_key
    resend.Emails.send(
        {
            "from": settings.email_from,
            "to": [to],
            "subject": subject,
            "html": html,
        }
    )


def send_verification_email(to: str, token: str) -> None:
    link = f"{settings.frontend_url}/verificar-email?token={token}"
    send_email(
        to=to,
        subject="Confirme seu email no FinanceMind",
        html=f'<p>Clique para confirmar seu email: <a href="{link}">{link}</a></p>',
    )


def send_password_reset_email(to: str, token: str) -> None:
    link = f"{settings.frontend_url}/redefinir-senha?token={token}"
    send_email(
        to=to,
        subject="Redefinição de senha — FinanceMind",
        html=f'<p>Clique para redefinir sua senha: <a href="{link}">{link}</a></p><p>Se você não solicitou, ignore este email.</p>',
    )
