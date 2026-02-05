import os
import shutil
from config import CFG

def init_folders():
    """Crea le cartelle necessarie se non esistono."""
    folders = [
        CFG.INPUT_FOLDER, 
        CFG.OUTPUT_FOLDER, 
        CFG.TEXT_FOLDER, 
        CFG.TEMP_FOLDER,
        CFG.TEMP_AUDIO, # temp/audio
        CFG.TEMP_TEXT,  # temp/text
        CFG.TEMP_MD     # temp/md
    ]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"📁 Creata cartella: {folder}")

def scan_files(type):
    """Restituisce la lista dei file in funzione del tipo richiesto."""
    if type == "audio":
        if not os.path.exists(CFG.INPUT_FOLDER):
            return []       
        return [
            f for f in os.listdir(CFG.INPUT_FOLDER) 
            if f.lower().endswith(CFG.SUPPORTED_EXT) and not f.startswith("._")
        ]
    elif type == "text":
        if not os.path.exists(CFG.TEXT_FOLDER):
            return []  
        return [f for f in os.listdir(CFG.TEXT_FOLDER)]
    elif type == "md":
        if not os.path.exists(CFG.OUTPUT_FOLDER):
            return []       
        return [f for f in os.listdir(CFG.OUTPUT_FOLDER)]
    else:
        raise ValueError("Tipo di file non supportato. Usa 'audio', 'text' o 'md'.")

def get_paths(filename):
    """
    Restituisce un dizionario con tutti i percorsi assoluti/relativi necessari per un file.
    Centralizza la logica dei percorsi in un unico punto.
    """
    base_name = os.path.splitext(filename)[0]
    
    return {
        "name": base_name,
        "input": os.path.join(CFG.INPUT_FOLDER, filename),
        "output": os.path.join(CFG.OUTPUT_FOLDER, f"{base_name}.md"),
        "txt": os.path.join(CFG.TEXT_FOLDER, f"{base_name}.txt"),
        # Percorsi Temporanei Organizzati
        "temp_audio_dir": os.path.join(CFG.TEMP_AUDIO, base_name),
        "temp_txt_file": os.path.join(CFG.TEMP_TEXT, f"{base_name}.txt.tmp"),
        "temp_md_file": os.path.join(CFG.TEMP_MD, f"{base_name}.md.tmp")
    }

def clean_temp_folder():
    """Rimuove completamente la cartella temp e la ricrea pulita."""
    if os.path.exists(CFG.TEMP_FOLDER):
        shutil.rmtree(CFG.TEMP_FOLDER)