import logging
import os
from transformers import pipeline, set_seed

# Logging einrichten
logging.basicConfig(level=logging.INFO)

# GPT-2 Textgenerator initialisieren
generator = pipeline('text-generation', model='gpt2')
set_seed(42)

# --- Funktionen ---

def merke_dir(text, dateiname="gedaechtnis.txt"):
    """Speichert neues Wissen."""
    if not os.path.exists(dateiname):
        open(dateiname, 'w').close()

    with open(dateiname, "a", encoding="utf-8") as f:
        f.write(text + "\n")

def erinnere_dich(frage, dateiname="gedaechtnis.txt"):
    """Sucht nach gespeicherten Antworten."""
    if not os.path.exists(dateiname):
        return []

    with open(dateiname, "r", encoding="utf-8") as f:
        erinnerungen = f.readlines()

    erinnerungen = [e.strip() for e in erinnerungen if e.strip()]
    passende_antworten = []

    for erinnerung in erinnerungen:
        if " | " in erinnerung:
            gespeicherte_frage, gespeicherte_antwort = erinnerung.split(" | ", 1)
            if frage.lower() in gespeicherte_frage.lower():
                passende_antworten.append(gespeicherte_antwort)

    return passende_antworten

def gib_antwort(frage, level, dateiname="gedaechtnis.txt"):
    """Gibt eine Antwort mit Level-Steuerung."""
    erinnerungen = erinnere_dich(frage, dateiname)

    if erinnerungen:
        antwort = erinnerungen[0]
        logging.info(f"KI: (Erinnerung) {antwort}")
        return antwort
    else:
        antwort = generiere_antwort(frage, level)
        logging.info(f"KI: (GPT-generiert) {antwort}")
        merke_dir(f"{frage} | {antwort}", dateiname)
        return antwort

def generiere_antwort(frage, level, max_laenge=50):
    """Generiert eine Antwort je nach Level."""
    # Level definiert, wie kompliziert gesprochen wird
    if level == 1:
        prompt = f"Antwort auf einfachem Niveau A1: {frage}\nAntwort:"
    elif level == 2:
        prompt = f"Antworte etwas detaillierter auf Niveau A2: {frage}\nAntwort:"
    elif level == 3:
        prompt = f"Antworte auf B1 Niveau mit normalen Sätzen: {frage}\nAntwort:"
    elif level == 4:
        prompt = f"Antworte auf B2 Niveau mit komplexeren Sätzen: {frage}\nAntwort:"
    else:
        prompt = f"Antworte auf C1 Niveau sehr natürlich und ausführlich: {frage}\nAntwort:"

    outputs = generator(
        prompt,
        max_length=max_laenge,
        num_return_sequences=1,
        do_sample=False  # wichtig: KEIN Sampling (keine Zufälle)
    )

    antwort = outputs[0]["generated_text"]
    # Nur den Antwortteil nehmen
    if "Antwort:" in antwort:
        antwort = antwort.split("Antwort:")[-1].strip()

    return antwort

def lade_basiswissen(dateiname="gedaechtnis.txt"):
    """Lädt Grundwissen ins Gedächtnis."""
    wissen = [
        ("Wie heißt du?", "Ich heiße LingoBot."),
        ("Wo wohnst du?", "Ich wohne im Internet."),
        ("Was ist dein Ziel?", "Ich helfe dir beim Sprachenlernen!"),
        ("Wie geht es dir?", "Mir geht es gut, danke!")
    ]
    for frage, antwort in wissen:
        merke_dir(f"{frage} | {antwort}", dateiname)
    logging.info("Basiswissen geladen.")

# --- Hauptprogramm ---

if __name__ == "__main__":
    dateiname = "gedaechtnis.txt"

    # Nur beim ersten Mal Basiswissen laden
    if not os.path.exists(dateiname):
        lade_basiswissen(dateiname)

    print("Willkommen bei LingoBot! Stelle deine Frage. (Tippe 'exit' zum Beenden)")

    # Starte auf Level 1
    aktuelles_level = 1

    while True:
        benutzerfrage = input("\nDu: ").strip()

        if benutzerfrage.lower() in ("exit", "quit", "stop"):
            print("Tschüss und bis bald!")
            break

        # Sonderbefehl: Level erhöhen
        if benutzerfrage.lower() == "level up":
            aktuelles_level = min(5, aktuelles_level + 1)
            print(f"Neues Sprachlevel: {aktuelles_level}")
            continue

        antwort = gib_antwort(benutzerfrage, aktuelles_level, dateiname)
        print("KI:", antwort)
