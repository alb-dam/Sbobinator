import mlx.core as mx
import ollama
import time
import gc
from config import CFG
from tqdm import tqdm

# =============================================================================
# 🛠️ UTILITIES
# =============================================================================

def check_metal_status() -> bool:
    try:
        # Metodo più robusto: confronto diretto con l'Enum di MLX
        print(" ✅ Accelerazione Apple Metal (GPU) ATTIVA ")
        return mx.default_device().type == mx.DeviceType.gpu
    except Exception:
        print(" ⚠️  MLX su CPU ")
        return False
    
def check_ollama_status():
    try:
        print(" ✅ Ollama è in esecuzione ")
        ollama.list()
    except Exception:
        print(" ❌ Errore: Ollama non sembra in esecuzione. Lancia 'ollama serve' nel terminale.")
        exit(1)

def check_ai_model():
    print(f" ✅ Modello MLX-Whisper selezionato: {CFG.MODEL_W} ")
    print(f" ✅ Modello Ollama selezionato: {CFG.MODEL_O} ")

def clean_mem():    #Libera la memoria RAM e VRAM (GPU) inutilizzata.
    # 1. Python Garbage Collector
    gc.collect()
    # 2. Svuota cache MLX (Cruciale per liberare la GPU dopo Whisper)
    if mx:
        try:
            mx.clear_cache()
        except Exception:
            pass       
    # 3. Attesa breve per permettere al kernel macOS di riorganizzare la RAM
    time.sleep(2)

def crea_eta(totale_chunk, desc="Elaborazione"):
    """
    Crea e restituisce una funzione 'eta()' che gestisce una barra tqdm.
    La barra si chiude automaticamente quando raggiunge il totale.
    """
    # 1. Inizializziamo la barra. Questa variabile vive nella memoria della funzione.
    pbar = tqdm(total=totale_chunk, desc=desc)
    
    # 2. Definiamo la funzione interna che farà il lavoro sporco
    def aggiorna(step=1):
        pbar.update(step)
        
        # Logica di auto-chiusura: se abbiamo finito, chiude la barra
        if pbar.n >= pbar.total:
            pbar.close()
            
    # 3. Trucco PRO: Alleghiamo il metodo close alla funzione stessa
    # Così se devi interrompere prima, puoi chiamare eta.force_close()
    aggiorna.force_close = pbar.close
            
    return aggiorna