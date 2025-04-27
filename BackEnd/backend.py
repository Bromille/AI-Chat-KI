import torch
from transformers import pipeline
import logging
import re
import random

# Konfiguration der Protokollierung
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 1. Textgenerierungsmodell laden
try:
    generator = pipeline('text-generation', model='gpt2')
    logging.info("Textgenerierungsmodell geladen.")
except Exception as e:
    logging.error(f"Fehler beim Laden des Textgenerierungsmodells: {e}")
    exit()

# 2. Funktion zum Generieren von Text
def generiere_text(prompt, max_laenge=50, anzahl_antworten=1):
    """Generiert Text basierend auf einem Prompt."""
    try:
        ergebnisse = generator(prompt, max_length=max_laenge, num_return_sequences=anzahl_antworten)
        return [ausgabe['generated_text'] for ausgabe in ergebnisse]
    except Exception as e:
        logging.error(f"Fehler bei der Textgenerierung: {e}")
        return ["KI: Ich konnte keinen Text generieren."]

# 3. Funktion zum "Merken" von Informationen in einer Textdatei
def merke_dir(text, dateiname="gedaechtnis.txt"):
    """Schreibt Text in eine Datei."""
    try:
        with open(dateiname, "a", encoding="utf-8") as f:
            f.write(text + "\n")
        logging.info(f"Habe mir '{text}' in '{dateiname}' gemerkt.")
    except Exception as e:
        logging.error(f"Fehler beim Speichern in die Datei: {e}")

# 4. Funktion zum Abrufen von "Erinnerungen" aus der Textdatei
def erinnere_dich(suchbegriff=None, dateiname="gedaechtnis.txt"):
    """Liest die Datei und gibt Zeilen zurück, die den Suchbegriff enthalten (oder alle Zeilen)."""
    erinnerungen = []
    try:
        with open(dateiname, "r", encoding="utf-8") as f:
            for zeile in f:
                zeile = zeile.strip()
                if suchbegriff is None or suchbegriff.lower() in zeile.lower():
                    erinnerungen.append(zeile)
        if suchbegriff:
            logging.info(f"Habe '{suchbegriff}' in meinen Erinnerungen gefunden:")
        elif suchbegriff is None and erinnerungen:
            logging.info("Meine bisherigen Erinnerungen:")
        return erinnerungen
    except FileNotFoundError:
        logging.warning(f"Die Datei '{dateiname}' wurde noch nicht erstellt.")
        return []
    except Exception as e:
        logging.error(f"Fehler beim Lesen der Datei: {e}")
        return []

# 5. Funktion zum Abrufen einer passenden Antwort oder zum Generieren einer Antwort
def gib_antwort(frage, dateiname="gedaechtnis.txt"):
    """Versucht, eine passende Antwort in den Erinnerungen zu finden, oder generiert eine Antwort."""
    erinnerungen = erinnere_dich(frage, dateiname)
    passende_antworten = [erinnerung.split(" | ")[1] for erinnerung in erinnerungen if " | " in erinnerung and frage.lower() in erinnerung.split(" | ")[0].lower()]

    if passende_antworten:
        antwort = random.choice(passende_antworten)
        logging.info(f"KI: (Erinnerung) {antwort}")
        return antwort
    else:
        antwort = generiere_text(frage)[0]
        logging.info(f"KI: (Generiert) {antwort}")
        return antwort

# 6. Funktion zum Vorbereiten des Gedächtnisses mit Vorwissen
def lade_vorwissen(dateiname="gedaechtnis.txt"):
    """Lädt grundlegendes Vorwissen in die Gedächtnisdatei."""
    vorwissen = [
        "Die Erde ist ein Planet. | Das ist richtig.",
        "Der Himmel ist blau. | Das ist richtig.",
        "Wasser ist nass. | Das ist richtig.",
        "Feuer ist heiß. | Das ist richtig.",
        "Menschen sind Säugetiere. | Das ist richtig.",
        "Ein Vogel kann fliegen. | Das ist richtig.",
        "Fische leben im Wasser. | Das ist richtig.",
        "Bäume wachsen im Wald. | Das ist richtig.",
        "Die Sonne scheint am Tag. | Das ist richtig.",
        "Der Mond scheint in der Nacht. | Das ist richtig.",
        "Hallo ist eine Begrüßung. | Das ist richtig.",
        "Danke ist ein Ausdruck von Dankbarkeit. | Das ist richtig."
    ]
    for eintrag in vorwissen:
        merke_dir(eintrag, dateiname)
    logging.info("Vorwissen geladen.")

# 7. Funktion zum Bewerten der Antwort und Anpassen des Gedächtnisses
def bewerte_antwort(frage, antwort, dateiname="gedaechtnis.txt"):
    """Bewertet die Antwort der KI implizit und passt das Gedächtnis an."""
    # Diese Funktion ist jetzt leer, da wir kein explizites Feedback mehr verwenden.
    pass

# 8. Funktion zum Analysieren der Benutzereingabe und Anpassen des Verhaltens
def analysiere_eingabe(eingabe, gespraechsverlauf, dateiname="gedaechtnis.txt"):
    """Analysiert die Eingabe des Benutzers und passt das Verhalten der KI an."""
    # 1. Speichere die Eingabe im Gedächtnis
    merke_dir(f"Du: {eingabe}", dateiname)
    logging.info(f"Benutzereingabe gespeichert: {eingabe}")

    # 2. Extrahiere Schlüsselwörter und Konzepte
    schluesselwoerter = re.findall(r'\b\w+\b', eingabe.lower())  # Einfache Schlüsselwortextraktion
    logging.debug(f"Schlüsselwörter extrahiert: {schluesselwoerter}")

    # 3. Versuche, Muster im Gesprächsverlauf zu erkennen
    if len(gespraechsverlauf) > 2:
        letzte_eingabe_benutzer = gespraechsverlauf[-2]
        letzte_antwort_ki = gespraechsverlauf[-1]

        # Beispiel: Wenn Benutzer ähnliche Fragen stellt, antworte ähnlich
        if "?" in eingabe and "?" in letzte_eingabe_benutzer:
            antworten = erinnere_dich(letzte_eingabe_benutzer, dateiname)
            if antworten:
                letzte_antwort = antworten[-1].split("KI: ")[-1]
                neue_antwort = generiere_text(eingabe + " " + letzte_antwort, max_laenge=50)[0]
                merke_dir(f"Du: {eingabe} | KI: {neue_antwort}", dateiname)
                logging.info(f"KI passt Antwort an ähnliche Frage an: {neue_antwort}")

        # Erkennen von Meinungsäußerung und zustimmen/widersprechen
        meinungswoerter = ["ich denke", "ich glaube", "meiner meinung nach", "finde ich", "bin der ansicht"]
        if any(wort in eingabe.lower() for wort in meinungswoerter):
            if "nicht" in letzte_antwort_ki.lower():
                antwort = "Ich stimme dir zu."
                merke_dir(f"{eingabe} | {antwort}")
                logging.info("KI stimmt zu")
            else:
                antwort = "Ich stimme dir nicht zu."
                merke_dir(f"{eingabe} | {antwort}")
                logging.info("KI widerspricht")

        # Reaktion auf Begrüßungen
        begruessungen = ["hallo", "moin", "guten tag", "servus"]
        if any(wort in eingabe.lower() for wort in begruessungen):
            antwort = random.choice(begruessungen) + "!"
            merke_dir(f"{eingabe} | {antwort}")
            logging.info("KI erwidert Begrüßung")

        # Reaktion auf Dankbarkeit
        dankeswoerter = ["danke", "vielen dank", "dankeschön"]
        if any(wort in eingabe.lower() for wort in dankeswoerter):
            antwort = "Gern geschehen!"
            merke_dir(f"{eingabe} | {antwort}")
            logging.info("KI reagiert auf Dankbarkeit")

    # 4. Antworte auf die Eingabe
    antwort = gib_antwort(eingabe, dateiname)
    return antwort

# 9. Hauptinteraktionsschleife
if __name__ == "__main__":
    print("KI: Hallo! Ich lerne durch unsere Interaktion.")
    logging.info("KI gestartet.")
    gedaechtnis_datei = "gedaechtnis.txt"
    gespraechsverlauf = []
    lade_vorwissen(gedaechtnis_datei)

    while True:
        nutzer_eingabe = input("Du: ")
        logging.debug(f"Benutzereingabe: {nutzer_eingabe}")
        gespraechsverlauf.append(f"Du: {nutzer_eingabe}")

        antwort = analysiere_eingabe(nutzer_eingabe, gespraechsverlauf, gedaechtnis_datei)
        print(antwort)
        gespraechsverlauf.append(f"KI: {antwort}")

        if nutzer_eingabe.lower() == "tschüss":
            print("KI: Auf Wiedersehen!")
            logging.info("KI beendet.")
            break
        elif nutzer_eingabe.lower() == "schreibe etwas":
            prompt = input("KI: Worüber soll ich schreiben? ")
            generierter_text = generiere_text(prompt)[0]
            print(f"KI: {generierter_text}")
            gespraechsverlauf.append(f"KI: {generierter_text}")
        elif nutzer_eingabe.lower() == "merke dir":
            text_zum_merken = input("KI: Was soll ich mir merken? (Eingabe im Format 'Frage | Antwort') ")
            if " | " in text_zum_merken:
                merke_dir(text_zum_merken, gedaechtnis_datei)
            else:
                print("KI: Bitte gib den Text im Format 'Frage | Antwort' ein.")
                logging.warning("Benutzer hat versucht, etwas im falschen Format zu speichern.")
        elif nutzer_eingabe.lower() == "erinnere dich":
            suchbegriff = input("KI: Wonach soll ich in meinen Erinnerungen suchen? (oder leer lassen für alle) ")
            erinnerungen = erinnere_dich(suchbegriff, gedaechtnis_datei)
            if erinnerungen:
                for erinnerung in erinnerungen:
                    print(f"- {erinnerung}")
            else:
                print("KI: Ich habe nichts gefunden.")

