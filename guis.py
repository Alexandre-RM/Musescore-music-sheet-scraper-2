import tkinter as tk
from tkinter import ttk

import validators

class UiProgressBar():
    def __init__(self, title:str) -> None:
        progressBarSize = 200

        self.progress = 0
        self.status = "Current text"
        
        self.window = tk.Tk()
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
        self.window.title(title)
        self.window.minsize(200, 10)
        
        self.window.protocol("WM_DELETE_WINDOW", self.destroy)

        self.label = tk.Label(self.window, text="Copier/coller l'url Musescore de la partition à télécharger :")
        self.label.grid(row=0, pady=10)

        self.textField = tk.Entry(self.window)
        self.textField.grid(row=1, pady=10)

        self.alertLabel = tk.Label(self.window, text="Veuillez saisir une url Musescore valide.", fg="red")

        self.button = tk.Button(self.window, text="Valider", command=self._buttonClick)
        self.button.grid(row=2, pady=10)

        self.url = ""


    def _buttonClick(self):
        if validators.url(self.textField.get()) and "musescore.com" in self.textField.get():
            self.url = self.textField.get()
            self.window.destroy()
        else:
            self.alertLabel.grid(row=2)
            self.button.grid(row=3)


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



#print(UiSelectMusicUrl("Select music URL").show())

