import subprocess

# Spécifiez la commande PyInstaller que vous souhaitez exécuter
commandInstallRequirements = "pip install pipreqs pyinstaller"
commandPipReqs = "pipreqs . --force"
commandInstaller = "pyinstaller \
    --clean \
    --noconsole \
    --onefile \
    --name Musescore_Music_Sheets_Scrapper \
    --icon icon.ico \
    main.py"

# Utilisez subprocess pour exécuter la commande
subprocess.call(commandInstallRequirements, shell=True)
subprocess.call(commandPipReqs, shell=True)
subprocess.call(commandInstaller, shell=True)
