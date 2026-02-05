import os
import shutil
import subprocess
from chonkie import TokenChunker
import tiktoken
from config import CFG


# =============================================================================
# 1️⃣ FASE AUDIO: Crea n file audio di lunghezza fissa con FFmpeg
# =============================================================================

def audio_chunk_generator(input_file_path, specific_temp_dir):
    """
    input_file_path: percorso completo del file audio sorgente
    specific_temp_dir: cartella temporanea dedicata a QUESTO file
    """
    if os.path.exists(specific_temp_dir): 
        shutil.rmtree(specific_temp_dir)
    os.makedirs(specific_temp_dir)
    
    output_pattern = os.path.join(specific_temp_dir, "chunk_%03d.wav")
    
    print(f"   ✂️  Segmentazione audio in corso...")
    try:
        subprocess.run([
            "ffmpeg", "-y", "-v", "error",
            "-i", input_file_path,
            "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
            "-f", "segment",
            "-segment_time", str(CFG.CHUNK_SEC),
            "-reset_timestamps", "1",
            output_pattern
        ], check=True)
    except subprocess.CalledProcessError:
        print(f"   ❌ Errore FFmpeg su file: {input_file_path}")
        return []
    
    chunks = sorted([
        os.path.join(specific_temp_dir, f) 
        for f in os.listdir(specific_temp_dir) 
        if f.endswith(".wav")
    ])
    return chunks

# =============================================================================
# 1️⃣ FASE TESTO: Crea unico file txt di lunghezza fissa con taglio intelligente per spazi
# =============================================================================

def text_chunk_generator(text):
    """
    Divide il testo in chunk basati sui token usando Chonkie.
    Rispetta i confini delle frasi ed è molto più preciso del taglio per caratteri.
    """
    if not text or len(text.strip()) == 0:
        return []

    # Inizializza il chunker
    # Usa 'gpt-4o' come tokenizer di base (è veloce e preciso per le stime).
    # Se vuoi essere purista potresti usare tokenizer di HuggingFace, 
    # ma questo aggiunge pesantezza inutile.
    tokenizer = tiktoken.get_encoding("cl100k_base")
    chunker = TokenChunker(
        tokenizer=tokenizer, 
        chunk_size=CFG.CHUNK_TOKENS, 
        chunk_overlap=CFG.CHUNK_OVERLAP_TOKENS
    )

    # Chonkie restituisce una lista di oggetti Chunk. 
    # Noi estraiamo solo il testo (.text)
    chunks = chunker(text)
    
    # Restituiamo una lista di stringhe
    return [chunk.text for chunk in chunks]