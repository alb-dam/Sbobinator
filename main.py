import sys
from utility import check_metal_status, check_ollama_status, check_ai_model
from core import data, todo
from core.pipeline import run_transcription_pipeline, run_elaboration_pipeline

def main():
    # Avvolgiamo tutto in un try block per gestire l'uscita manuale
    try:
        # --- 1. Setup Ambiente ---
        print("🚀 Avvio Pipeline Universitaria...")
        check_metal_status()
        check_ollama_status()
        check_ai_model()
        data.init_folders()
        
        # --- 2. Flusso Completo (Audio -> TXT -> MD) ---
        files_audio = todo.todo_text() 

        if files_audio:
            print(f"\n📂 Trovati {len(files_audio)} nuovi file audio da processare.")
        
        for filename in files_audio:
            paths = data.get_paths(filename)
            print(f"\n🔹 Inizio lavorazione su: {filename}")
            
            # A. Pipeline Trascrizione
            # Nota: run_transcription_pipeline gestisce già la pulizia interna se interrompi
            transcription_result = run_transcription_pipeline(paths)
            
            if transcription_result:
                print(f"   🧠 Rielaborazione immediata...")
                run_elaboration_pipeline(paths)
                print(f"   ✅ Completato: {paths['output']}")
            else:
                print(f"   ❌ Errore nella trascrizione o interruzione. Salto rielaborazione.")

        # --- 3. Recupero File Testo "Orfani" ---
        files_txt_orphans = todo.todo_md()
        
        if files_txt_orphans:
            print(f"\n📄 Trovati {len(files_txt_orphans)} file di testo in attesa di elaborazione.")

        for filename in files_txt_orphans:
            paths = data.get_paths(filename)
            print(f"\n🔹 Elaborazione testo esistente: {filename}")
            run_elaboration_pipeline(paths)
            print(f"   ✅ Completato: {paths['output']}")

        # --- 4. Chiusura ---
        data.clean_temp_folder()
        print("\n🏁 Tutta la coda di lavorazione è terminata.")

    except KeyboardInterrupt:
        # Questo blocco cattura il Ctrl+C finale
        print("\n\n🛑 Interruzione manuale rilevata. Uscita sicura.")
        # Facciamo un'ultima pulizia della cartella temp per sicurezza
        data.clean_temp_folder()
        sys.exit(0)

if __name__ == "__main__":
    main()