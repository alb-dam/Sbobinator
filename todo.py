from core import data

def todo_text():
    """
    Restituisce la lista dei FILE audio (es. 'nome.mp3') che non hanno 
    ancora una corrispondenza in text o md.
    """
    # 1. Creiamo una mappa per gli audio: { "nome_pulito": "nome_reale.mp3" }
    #    Questo ci serve per recuperare il file originale alla fine.
    audio_map = {
        data.get_paths(f)["name"]: f 
        for f in data.scan_files("audio")
    }
    
    # 2. Ottieni i set di nomi puliti per text e md
    #    Usiamo i set {} subito per velocità
    fatti_txt = {data.get_paths(f)["name"] for f in data.scan_files("text")}
    fatti_md  = {data.get_paths(f)["name"] for f in data.scan_files("md")}

    # 3. Calcola i nomi puliti che mancano (Set Difference)
    #    Tutte le chiavi audio MENO quelli fatti in txt MENO quelli fatti in md
    da_fare_nomi_puliti = set(audio_map.keys()) - fatti_txt - fatti_md
    
    # 4. Ricostruisci la lista usando i nomi file originali dalla mappa
    #    Restituisce es: ['intervista.mp3', 'meeting.wav']
    return [audio_map[name] for name in da_fare_nomi_puliti]

def todo_md():
    """
    Restituisce la lista dei file di TESTO (.txt) che non hanno 
    ancora un corrispondente file MD.
    """
    # 1. Mappa dei file SORGENTE (Text): { "nome_progetto": "nome_progetto.txt" }
    #    Ci serve la mappa per recuperare il nome con l'estensione alla fine.
    text_map = {
        data.get_paths(f)["name"]: f 
        for f in data.scan_files("text")
    }
    
    # 2. Set dei file DESTINAZIONE (MD): ci basta solo l'insieme dei nomi puliti
    #    Questi sono quelli "già fatti".
    fatti_md = {
        data.get_paths(f)["name"] 
        for f in data.scan_files("md")
    }
    
    # 3. Calcolo della differenza: SORGENTE - DESTINAZIONE
    #    (Tutti i testi disponibili) MENO (Quelli che hanno già un MD)
    da_fare_nomi = set(text_map.keys()) - fatti_md
    
    # 4. Ricostruisci la lista restituendo i file .txt originali
    return [text_map[name] for name in da_fare_nomi]
    