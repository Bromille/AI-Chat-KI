import torch
from transformers import pipeline

generator = pipeline('text-generation', model='gpt2')

def generiere_text(prompt, max_laenge=50, anzahl_antworten=1):
    """Generiert Text basierend auf einem Prompt."""
    ergebnisse = generator(prompt, max_length=max_laenge, num_return_sequences=anzahl_antworten)
    return [ausgabe['generated_text'] for ausgabe in ergebnisse]

def merke_dir(text, dateiname="gedaechtnis.txt"):
    try:
        with open(dateiname, "a") as f:
            f.write(text + "\n")
        print(f"KI: Habe mir '{text}' in '{dateiname}' gemerkt.")
    except Exception as e:
        print(f"KI: Fehler beim Speichern in die Datei: {e}")

def erinnere_dich(suchbegriff=None, dateiname="gedaechtnis.txt"):
    """Liest die Datei und gibt Zeilen zurück, die den Suchbegriff enthalten (oder alle Zeilen)."""
    erinnerungen = []
    try:
        with open(dateiname, "r") as f:
            for zeile in f:
                zeile = zeile.strip()
                if suchbegriff is None or suchbegriff.lower() in zeile.lower():
                    erinnerungen.append(zeile)
        if suchbegriff:
            print(f"KI: Habe '{suchbegriff}' in meinen Erinnerungen gefunden:")
        elif erinnerungen:
            print("KI: Meine bisherigen Erinnerungen:")
        return erinnerungen
    except FileNotFoundError:
        print(f"KI: Die Datei '{dateiname}' wurde noch nicht erstellt.")
        return []
    except Exception as e:
        print(f"KI: Fehler beim Lesen der Datei: {e}")
        return []

if __name__ == "__main__":
    print("KI: Hallo! Ich kann schreiben und mir Dinge merken.")
    while True:
        nutzer_eingabe = input("Du: ")
        if nutzer_eingabe.lower() == "schreibe etwas":
            prompt = input("KI: Worüber soll ich schreiben? ")
            generierter_text = generiere_text(prompt)[0]
            print(f"KI: {generierter_text}")
        elif nutzer_eingabe.lower() == "merke dir":
            text_zum_merken = input("KI: Was soll ich mir merken? ")
            merke_dir(text_zum_merken)
        elif nutzer_eingabe.lower() == "erinnere dich":
            suchbegriff = input("KI: Wonach soll ich in meinen Erinnerungen suchen? (oder leer lassen für alle) ")
            erinnerungen = erinnere_dich(suchbegriff)
            for erinnerung in erinnerungen:
                print(f"- {erinnerung}")
        elif nutzer_eingabe.lower() == "tschüss":
            print("KI: Auf Wiedersehen!")
            break
        else:
            print("KI: Ich kann schreiben ('schreibe etwas'), mir Dinge merken ('merke dir') und mich erinnern ('erinnere dich').")