"""
Worker Parsing — ATS Platform
Consomme la file Redis `parsing_jobs` et extrait les données des CV (PDF/DOCX).
"""

import json
import logging
import os
import time

import redis

# ---------- Logging ----------
logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEBUG", "false").lower() == "true" else logging.INFO,
    format="%(asctime)s [%(levelname)s] parsing_worker — %(message)s",
)
log = logging.getLogger(__name__)

# ---------- Config ----------
REDIS_URL     = os.getenv("REDIS_URL", "redis://redis:6379")
PARSING_QUEUE = os.getenv("PARSING_QUEUE", "parsing_jobs")
MAX_RETRIES   = int(os.getenv("PARSING_MAX_RETRIES", "3"))
TIMEOUT       = int(os.getenv("PARSING_TIMEOUT", "30"))


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


def process_job(job: dict) -> None:
    """
    Traite un job de parsing.
    job = { "candidature_id": "uuid", "cv_path": "s3://bucket/key" }
    """
    candidature_id = job.get("candidature_id")
    cv_path        = job.get("cv_path")

    log.info(f"📄 Traitement parsing — candidature_id={candidature_id}")

    # TODO : implémenter les étapes suivantes
    # 1. Télécharger le fichier CV depuis MinIO/S3 (boto3)
    # 2. Détecter le type (PDF ou DOCX)
    # 3. Extraire le texte brut (pdfplumber / python-docx)
    # 4. Parser le texte : nom, email, compétences, expérience, formation
    # 5. Écrire le résultat dans extraction_cv (PostgreSQL)
    # 6. Calculer le score et mettre à jour candidature.score_global
    # 7. Si score > seuil_alerte → pousser un job dans email_jobs

    log.info(f"✅ Parsing terminé — candidature_id={candidature_id}")


def main():
    log.info("🚀 parsing_worker démarré — en attente de jobs...")
    r = connect_redis()

    while True:
        try:
            # BLPOP bloque jusqu'à qu'un job arrive (timeout=5s pour éviter le freeze)
            result = r.blpop(PARSING_QUEUE, timeout=5)

            if result is None:
                continue  # timeout, on reboucle

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