import os
from dataclasses import dataclass, field

# =============================================================================
# ⚙️ CONFIGURAZIONE E COSTANTI
# =============================================================================
@dataclass
class Config:
    # --- File System ---
    # I percorsi possono essere relativi o assoluti
    INPUT_FOLDER: str = "Audio"
    OUTPUT_FOLDER: str = "MD files"
    TEXT_FOLDER: str = "TXT files"
    TEMP_FOLDER: str = "temp"
    # Sottocartelle Temp (Create dinamicamente in base a TEMP_FOLDER)
    TEMP_AUDIO: str = os.path.join(TEMP_FOLDER, "audio")
    TEMP_TEXT: str = os.path.join(TEMP_FOLDER, "text")
    TEMP_MD: str = os.path.join(TEMP_FOLDER, "md")
    SUPPORTED_EXT: tuple = ('.mp3', '.wav', '.m4a', '.m4b', '.aac')
    # --- Audio Processing ---
    CHUNK_SEC: int = 300         
    OVERLAP_SEC: int = 1
    # --- Whisper (Trascrizione) ---
    MODEL_W: str = "large-v3-turbo"   #set large-v3 for best quality   
    BEAM_SIZE: int = 2             
    WHISPER_PROMPT: str = (
        "Trascrizione di lezioni universitarie di Geometria e Algebra Lineare. "
        "Argomenti: vettori v, matrici, rango, determinante, Gauss-Jordan, vettori linearmente indipendenti, "
        "sistemi lineari, k-spazio vettoriale V, campo K, sottospazi U V W, insieme V, vettori linermente dipendenti, "
        "combinazione lineare, vettori generatori, Span, indipendenza, basi, dimensione, Grassmann. "
        "Applicazioni lineari f, Kernel, Immagine, autovalori lambda, autovettori, "
        "diagonalizzazione, spazio euclideo R^n, prodotto scalare, Gram-Schmidt, "
        "teorema spettrale, geometria affine, rette, piani, coniche, quadriche."
    )
    # --- Ollama (Rielaborazione) ---
    MODEL_O: str = "qwen3:14b"
    CTX_SIZE: int = 4096           
    OLLAMA_PROMPT: str = (
        "Sei un assistente universitario esperto in **GEOMETRIA E ALGEBRA LINEARE**.\n"
        "Stai elaborando la parte {idx} di {total_chunks} di una lezione.\n\n"
        "OBIETTIVO:\n"
        "Riscrivere il testo parlato in appunti universitari rigorosi in LaTeX.\n\n"
        "ISTRUZIONI SUL CONTESTO:\n"
        "Ti verrà fornito un 'CONTESTO PRECEDENTE'. Usalo SOLO per mantenere coerenza.\n"
        "**NON RIPETERE** ciò che è scritto nel contesto precedente.\n\n"
        "REGOLE DI FORMATTAZIONE (LaTeX):\n"
        "1. Inline: $...$, Blocchi: $$...$$\n"
        "2. Matrici: ambiente `bmatrix`.\n"
        "3. Sistemi: ambiente `cases`.\n"
        "4. Vettori: grassetto $\\mathbf{{v}}$ (non freccia).\n"
        "5. Struttura: Usa ## per argomenti e ### per dettagli.\n"
        "6. Definizioni/Teoremi: Usa grassetto **Definizione:** / **Teorema:**.\n"
        "7. Output: Solo il testo formattato, niente saluti o commenti."
    )
    # 2. TEXT_CHUNK_SIZE: Quanto testo (in CARATTERI) mandiamo alla volta.
    # Calcolo: 4096 token * 0.6 (margine sicurezza) * 4 caratteri/token = ~8000 caratteri.
    CHUNK_TOKENS: int = 2000     
    CHUNK_OVERLAP_TOKENS: int = 200

    def __post_init__(self):
        # Creazione automatica cartelle se non esistono
        for folder in [self.INPUT_FOLDER, self.OUTPUT_FOLDER, self.TEMP_FOLDER]:
            os.makedirs(folder, exist_ok=True)

CFG = Config()    