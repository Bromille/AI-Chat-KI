import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import logging

# Konfiguration der Protokollierung
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Laden des GPT-2 Modells und Tokenizers
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# 2. Funktion zur Textgenerierung mit GPT-2
def generiere_text_gpt2(prompt, max_length=100):
    """Generiert Text kontrolliert mit GPT-2."""
    try:
        inputs = tokenizer.encode(prompt, return_tensors="pt")
        outputs = model.generate(inputs, max_length=max_length, num_return_sequences=1, no_repeat_ngram_size=2, top_p=0.9, temperature=0.7)
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text.strip()
    except Exception as e:
        logging.error(f"Fehler bei der Textgenerierung: {e}")
        return "Entschuldigung, ich konnte nichts generieren."

# 3. Funktion zur Erstellung der Sprachlevel
def sprach_level_up(level):
    """Erhöht das Sprachlevel und macht die Sprache schwieriger."""
    if level == 1:
        return "A1 - Anfänger", "Wortschatz: Begrüßung, Zahlen, einfache Sätze"
    elif level == 2:
        return "A2 - Grundkenntnisse", "Wortschatz: Familie, Hobbys, Zeitangaben"
    elif level == 3:
        return "B1 - Mittelstufe", "Wortschatz: Reisen, Gefühle, einfache Texte verstehen"
    elif level == 4:
        return "B2 - Fortgeschritten", "Wortschatz: Diskussionen führen, abstrakte Themen"
    else:
        return "C1 - Expertenniveau", "Wortschatz: Komplexe Themen, akademische Texte"

# 4. Sprachlern-Mechanismus mit GPT-2
def lerne_sprache(sprache, lernsprache, level):
    sprache_level, vocab = sprach_level_up(level)
    
    print(f"\nDu lernst {lernsprache} auf Niveau {sprache_level}.")
    print(f"Wortschatz: {vocab}")
    
    # Interaktive Frage basierend auf dem aktuellen Level
    frage = f"Wie sagst du 'Hallo' auf {lernsprache}?"
    print(f"Frage: {frage}")
    
    # GPT-2 übernimmt das Feedback und die Antwort
    prompt_feedback = f"Erkläre auf {lernsprache} einfach, wie man 'Hallo' sagt, wenn der Lernende Anfänger ist."
    feedback = generiere_text_gpt2(prompt_feedback)
    print(f"KI Feedback: {feedback}")
    
    antwort = input(f"Antwort auf {lernsprache}: ")
    
    # Die KI kann Feedback geben und das Niveau erhöhen, wenn es korrekt ist
    if antwort.lower() == "hallo" and lernsprache.lower() == "deutsch":
        print("Richtig! Du hast ein Level-Up erreicht!")
        level += 1
    else:
        print("Das war nicht richtig, versuche es noch einmal.")
    
    return level

# 5. Funktion zur Sprachwahl und Levelbestimmung
def starte_sprachlernen():
    """Sprachlernprozess starten und Benutzer fragen, welche Sprachen sie lernen möchten."""
    print("Willkommen zum Sprachlerner!")
    main_sprache = input("Wähle deine Hauptsprache (z.B. Deutsch, Englisch): ")
    lern_sprache = input("Wähle die Sprache, die du lernen möchtest (z.B. Spanisch, Französisch): ")
    
    level = 1  # Startniveau
    while level <= 5:
        level = lerne_sprache(main_sprache, lern_sprache, level)
        
        if level > 5:
            print("Herzlichen Glückwunsch! Du hast das höchste Level erreicht!")
            break
        else:
            weiter = input("Möchtest du weitermachen? (Ja/Nein): ")
            if weiter.lower() != "ja":
                break

# 6. Hauptinteraktionsschleife
if __name__ == "__main__":
    starte_sprachlernen()