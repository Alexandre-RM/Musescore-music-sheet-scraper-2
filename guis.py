import enum
from io import BytesIO
import tkinter as tk
import base64
from tkinter import ttk
from PIL import Image, ImageTk
from pypdf import ImageType

import validators

def setWindowIcon(window:tk.Tk):
    base64icon = "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"
    image_data = base64.b64decode(base64icon)
    image = Image.open(BytesIO(image_data))
    
    image = image.convert("RGBA")
    image = ImageTk.PhotoImage(image)

    window.iconphoto(True, image)

class UiProgressBar():
    def __init__(self, title:str) -> None:
        progressBarSize = 200

        self.progress = 0
        self.status = "Current text"
        
        self.window = tk.Tk()
        #self.window.iconbitmap("icon.ico")
        setWindowIcon(self.window)
        self.window.title(title)
        self.window.minsize(int(progressBarSize*1.2), 10)

        self.statusLabel = tk.Label(self.window, text = "???")
        self.statusLabel.pack(pady=10)

        self.progressBar = ttk.Progressbar(self.window, orient="horizontal", length=progressBarSize, mode="determinate")
        self.progressBar.pack(pady=10)


    def updateProgress(self, progress:float) -> "UiProgressBar":
        """_summary_

        Args:
            progress (int): The % of completion, as a value between 0 and 1
        """
        self.progress = progress
        self.progressBar["value"] = progress * 100

        self.window.update()

        if progress > 0.99:
            self.window.withdraw()
        else:
            self.window.deiconify()
    
        return self


    def updateLabel(self, label) -> "UiProgressBar":
        self.status = label
        self.statusLabel.config(text=label)

        self.window.update()

        return self


class UiSelectMusicUrl():
    def __init__(self, title:str):        
        self.window = tk.Tk()
        #self.window.iconbitmap("icon.ico")
        setWindowIcon(self.window)
        self.window.title(title)
        self.window.minsize(200, 10)
        
        self.window.protocol("WM_DELETE_WINDOW", self.destroy)

        steps = "Etapes : \n \
                         1. Ouvrir le site musescore.com \n \
                         2. Choisir une partition et l'ouvrir \n \
                         3. Copier l'url de la partition à télécharger \n \
                         4. Faire un clic droit dans le champ ci-dessous \n \
                         5. Cliquer sur 'Valider' \n \
                         6. Attendre la fin du téléchargement \n \
                        (dans le même dossier que le logiciel)"
        
        for index, step in enumerate(steps.split("\n")):
            label = tk.Label(self.window, text=step.strip())
            label.grid(row=index, pady=0)

        self.textField = tk.Entry(self.window)
        self.textField.grid(row=index + 1, pady=10)
        self.textField.bind("<Button-3>", self._textFieldRightClick)

        self.alertLabel = tk.Label(self.window, text="Veuillez saisir une url Musescore valide.", fg="red")

        self.button = tk.Button(self.window, text="Valider", command=self._buttonClick)
        self.button.grid(row=index + 2, pady=10)

        self.url = ""

    def _textFieldRightClick(self, event):
        clipboardContent = self.window.clipboard_get()
        self.textField.delete(0, tk.END)
        self.textField.insert(0, clipboardContent)


    def _buttonClick(self):
        if validators.url(self.textField.get()) and "musescore.com" in self.textField.get():
            self.url = self.textField.get()
            self.window.destroy()
        else:
            self.alertLabel.grid(row=self.window.grid_size()[1])
            self.button.grid(row=self.window.grid_size()[1])


    def show(self, debug:bool = False) -> str:
        if not debug:
            self.window.mainloop()
        else:
            self.url = "https://musescore.com/mmc418-2/scores/2454041"
            self.window.destroy()
            
        return self.url
    
    def destroy(self):
        self.url = ""
        self.window.destroy()


if __name__ == "__main__":
    print(UiSelectMusicUrl("Select music URL").show())

