import subprocess

# Spécifiez la commande PyInstaller que vous souhaitez exécuter
command = "pyinstaller --noconsole --onefile main.py"

# Utilisez subprocess pour exécuter la commande
subprocess.call(command, shell=True)
