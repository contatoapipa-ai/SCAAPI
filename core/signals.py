import sys 
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import subprocess
import threading

def backup():
    subprocess.run(
        [sys.executable, "manage.py", "dumpdata", "--indent", "2"],
        stdout=open("backup.json", "w", encoding="utf-8")
    )

    subprocess.run(["git", "add", "backup.json", "media", "db.sqlite3"])
    subprocess.run(["git", "commit", "-m", "Backup automático"])
    subprocess.run(["git", "push"])

@receiver(post_save)
def salvar_backup(sender, **kwargs):
    threading.Thread(target=backup).start()

@receiver(post_delete)
def excluir_backup(sender, **kwargs):
    threading.Thread(target=backup).start()