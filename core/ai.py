import mlx_whisper
import ollama
from config import CFG
from utility import clean_mem
# =============================================================================
# 🎙️ TRASCRIZIONE CON WHISPER
# =============================================================================

def transcribe_audio_chunk(audio_path):
    """
    Trascrive un singolo file audio usando Whisper su MLX.
    Restituisce la stringa di testo o None in caso di errore persistente.
    """
    model_path = f"mlx-community/whisper-{CFG.MODEL_W}"
    
    # Tentativi di retry in caso di glitch della VRAM
    for attempt in range(3):
        try:
            result = mlx_whisper.transcribe(
                audio_path, 
                path_or_hf_repo=model_path,
                language="it", 
                initial_prompt=CFG.WHISPER_PROMPT,
                verbose=None
            )
            return result["text"].strip()
        except Exception as e:
            print(f"      ⚠️ Whisper Retry {attempt+1}/3: {e}")
            clean_mem()
            
    return None

# =============================================================================
# 3️⃣ ELABORAZIONE CON OLLAMA
# =============================================================================

def elaborate_text_chunk(text_chunk, chunk_index, total_chunks, prev_context):
    """
    Invia un blocco di testo a Ollama per la rielaborazione.
    Restituisce il testo elaborato o None.
    """
    sys_prompt = CFG.OLLAMA_PROMPT.format(idx=chunk_index, total_chunks=total_chunks)
    
    # Costruzione del prompt utente con il contesto precedente
    context_block = f"=== CONTESTO PRECEDENTE ===\n{prev_context[-1000:]}\n\n" if prev_context else ""
    user_content = f"{context_block}=== TESTO DA ELABORARE ===\n{text_chunk}"

    try:
        response = ollama.chat(
            model=CFG.MODEL_O,
            messages=[
                {'role': 'system', 'content': sys_prompt},
                {'role': 'user', 'content': user_content}
            ],
            options={
                'temperature': 0.1, 
                'num_ctx': CFG.CTX_SIZE
            }
        )
        return response['message']['content']
    except Exception as e:
        print(f"      ❌ Errore Ollama: {e}")
        return None