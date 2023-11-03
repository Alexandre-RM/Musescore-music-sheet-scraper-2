import sys
import webScrapping

if __name__ == "__main__":
    """
        Arg 0 : debug mode (1: True, 0: False)
    """
    # Récupérer les arguments à partir de la ligne de commande
    args = sys.argv[1:]  # sys.argv[0] est le nom du script lui-même

    debugMode = len(args) > 0 and args[0] == 1

    webScrapping.executeScrapping(debugMode)
