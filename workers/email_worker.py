"""
Worker Email — ATS Platform
Consomme la file Redis `email_jobs` et envoie les emails via SMTP.
"""

import json
import logging
import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import redis

# ---------- Logging ----------
logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEBUG", "false").lower() == "true" else logging.INFO,
    format="%(asctime)s [%(levelname)s] email_worker — %(message)s",
)
log = logging.getLogger(__name__)

# ---------- Config ----------
REDIS_URL    = os.getenv("REDIS_URL", "redis://redis:6379")
EMAIL_QUEUE  = os.getenv("EMAIL_QUEUE", "email_jobs")
MAX_RETRIES  = 3

SMTP_HOST    = os.getenv("SMTP_HOST", "mailhog")
SMTP_PORT    = int(os.getenv("SMTP_PORT", "1025"))
SMTP_USER    = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM    = os.getenv("SMTP_FROM", "noreply@ats-local.dev")
SMTP_TLS     = os.getenv("SMTP_TLS", "false").lower() == "true"


def connect_redis() -> redis.Redis:
    """Connexion Redis avec retry."""
    for attempt in range(10):
        try:
            client = redis.from_url(REDIS_URL, decode_responses=True)
            client.ping()
            log.info("✅ Connecté à Redis")
            return client
        except redis.exceptions.ConnectionError:
            log.warning(f"Redis non disponible, tentative {attempt + 1}/10...")
            time.sleep(2)
    raise RuntimeError("Impossible de se connecter à Redis après 10 tentatives.")


def send_email(to: str, subject: str, body_text: str, body_html: str = "") -> None:
    """Envoie un email via SMTP (MailHog en local, SendGrid en prod)."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = SMTP_FROM
    msg["To"]      = to

    msg.attach(MIMEText(body_text, "plain"))
    if body_html:
        msg.attach(MIMEText(body_html, "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        if SMTP_TLS:
            server.starttls()
        if SMTP_USER and SMTP_PASSWORD:
            server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_FROM, to, msg.as_string())

    log.info(f"📧 Email envoyé → {to} | Sujet : {subject}")


def process_job(job: dict) -> None:
    """
    Traite un job d'envoi d'email.
    job = {
        "candidature_id": "uuid",
        "type": "accusé_reception" | "alerte_score" | "changement_etape",
        "destinataire": "email@exemple.com",
        "variables": { "nom": "...", "titre_offre": "...", ... }
    }
    """
    candidature_id = job.get("candidature_id")
    email_type     = job.get("type", "inconnu")
    destinataire   = job.get("destinataire")
    variables      = job.get("variables", {})

    log.info(f"📨 Traitement email — type={email_type} | destinataire={destinataire}")

    # TODO : charger le template depuis PostgreSQL (table template_email)
    # Pour l'instant, templates en dur pour démarrer

    if email_type == "accusé_reception":
        subject   = f"Votre candidature pour : {variables.get('titre_offre', '')}"
        body_text = (
            f"Bonjour {variables.get('nom', '')},\n\n"
            f"Nous avons bien reçu votre candidature pour l'offre "
            f"\"{variables.get('titre_offre', '')}\".\n\n"
            f"Nous reviendrons vers vous sous peu.\n\n"
            f"Bonne journée."
        )

    elif email_type == "alerte_score":
        subject   = f"⚡ Candidature à fort potentiel — {variables.get('titre_offre', '')}"
        body_text = (
            f"Bonjour,\n\n"
            f"La candidature de {variables.get('nom_candidat', '')} vient d'obtenir "
            f"un score de {variables.get('score', '')}% pour l'offre "
            f"\"{variables.get('titre_offre', '')}\".\n\n"
            f"Consultez-la dès maintenant dans votre pipeline."
        )

    elif email_type == "changement_etape":
        subject   = f"Mise à jour de votre candidature — {variables.get('titre_offre', '')}"
        body_text = (
            f"Bonjour {variables.get('nom', '')},\n\n"
            f"Votre candidature pour \"{variables.get('titre_offre', '')}\" "
            f"a été mise à jour : {variables.get('nouvelle_etape', '')}.\n\n"
            f"Bonne journée."
        )

    else:
        log.warning(f"Type d'email inconnu : {email_type}")
        return

    # Retry jusqu'à MAX_RETRIES fois
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            send_email(destinataire, subject, body_text)
            # TODO : écrire le résultat dans envoi_email (PostgreSQL) → statut=success
            return
        except Exception as e:
            log.warning(f"Tentative {attempt}/{MAX_RETRIES} échouée : {e}")
            if attempt < MAX_RETRIES:
                time.sleep(5 * attempt)  # backoff exponentiel simple

    # TODO : écrire le résultat dans envoi_email → statut=echec
    log.error(f"❌ Échec définitif de l'envoi email pour candidature_id={candidature_id}")


def main():
    log.info("🚀 email_worker démarré — en attente de jobs...")
    r = connect_redis()

    while True:
        try:
            result = r.blpop(EMAIL_QUEUE, timeout=5)

            if result is None:
                continue

            _, raw = result
            job = json.loads(raw)
            log.debug(f"Job reçu : {job}")

            try:
                process_job(job)
            except Exception as e:
                log.error(f"❌ Erreur lors du traitement du job {job} : {e}")

        except redis.exceptions.ConnectionError:
            log.error("Connexion Redis perdue, reconnexion dans 3s...")
            time.sleep(3)
            r = connect_redis()

        except Exception as e:
            log.error(f"Erreur inattendue : {e}")
            time.sleep(1)


if __name__ == "__main__":
    main()