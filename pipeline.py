import os
import shutil
from tqdm import tqdm

# Moduli Locali
from config import CFG
from utility import clean_mem, crea_eta
from core import chunking               
from core import ai                     

def run_transcription_pipeline(paths):
    """Gestisce il flusso di trascrizione con salvataggio in temp/text."""

    # 1. Preparazione Audio (i chunk vanno in temp/audio/NomeFile/)
    # Nota: paths["temp_audio_dir"] viene popolato da data.py
    chunks = chunking.audio_chunk_generator(paths["input"], paths["temp_audio_dir"])
    if not chunks: return None

    # 2. Loop Trascrizione
    parts = []
    total_chunk = len(chunks)
    print(f"\n   🎙️  Trascrizione audio")
    eta = crea_eta(total_chunk, desc="Trascrizione Audio")

    try:
        for chunk in chunks:
            text = ai.transcribe_audio_chunk(chunk)
            if text: parts.append(text)
            eta()
            clean_mem()

        full_text = " ".join(parts)
        
        # 3. Salvataggio Atomico (Scrive in temp/text -> Sposta in TXT files)
        if full_text:
            # Scrittura nel percorso temporaneo organizzato
            with open(paths["temp_txt_file"], "w", encoding="utf-8") as f:
                f.write(full_text)
            
            # Spostamento nel percorso finale
            os.replace(paths["temp_txt_file"], paths["txt"])
            
        # Pulizia chunks audio
        if os.path.exists(paths["temp_audio_dir"]):
            shutil.rmtree(paths["temp_audio_dir"])
            
        return full_text

    except (KeyboardInterrupt, Exception) as e:
        print(f"\n   ❌ Interruzione! Pulizia file temporanei...")
        if os.path.exists(paths["temp_audio_dir"]):
            shutil.rmtree(paths["temp_audio_dir"])
        if os.path.exists(paths["temp_txt_file"]):
            os.remove(paths["temp_txt_file"])
        raise e


def run_elaboration_pipeline(paths):
    """
    Legge il file txt e salva l'elaborazione in temp/md -> MD files.
    """
    
    if not os.path.exists(paths["txt"]):
        print(f"⚠️ Errore: File non trovato: {paths['txt']}")
        return

    with open(paths["txt"], "r", encoding="utf-8") as f:
        transcript = f.read()

    chunks = chunking.text_chunk_generator(transcript)
    
    if not chunks:
        print("   ⚠️ Il file è vuoto.")
        return

    print(f"\n   🧠 Elaborazione testo ({len(chunks)} blocchi)")
    
    total = len(chunks)
    prev_context = ""
    eta = crea_eta(total, desc="Elaborazione Testo")

    try:
        # Scrittura nel percorso temporaneo organizzato (temp/md/Nome.md.tmp)
        with open(paths["temp_md_file"], "w", encoding="utf-8") as f:
            
            for i, chunk in enumerate(chunks):
                content = ai.elaborate_text_chunk(chunk, i+1, total, prev_context)
                
                if content:
                    f.write(content + "\n\n")
                    f.flush()
                    prev_context = content
                
                eta()
                clean_mem()

        # Spostamento nel percorso finale
        os.replace(paths["temp_md_file"], paths["output"])
    
    except (KeyboardInterrupt, Exception) as e:
        print(f"\n   ❌ Interruzione! Il file parziale non verrà salvato.")
        if os.path.exists(paths["temp_md_file"]):
            os.remove(paths["temp_md_file"])
        raise e