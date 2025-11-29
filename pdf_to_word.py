from pdf2docx import Converter
import os

def pdf_to_word_batch():
    """
    Convertit tous les "vrais" PDF du dossier courant en format Word (.docx)
    en essayant de préserver la mise en page exacte.
    """
    current_dir = os.getcwd()
    
    # Liste des PDF (on exclut ceux qu'on a générés nous-mêmes si besoin)
    pdf_files = [f for f in os.listdir(current_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("❌ Aucun fichier PDF trouvé.")
        return

    print(f"📂 {len(pdf_files)} fichiers trouvés. Conversion vers Word...")
    print("-" * 50)

    for filename in pdf_files:
        # On évite de convertir des fichiers temporaires ou déjà traités
        if filename.startswith("~$"): continue

        docx_filename = os.path.splitext(filename)[0] + ".docx"
        
        # Si le fichier Word existe déjà, on passe (ou on écrase selon votre choix)
        if os.path.exists(docx_filename):
            print(f"⏩ {docx_filename} existe déjà. Ignoré.")
            continue

        try:
            print(f"🔄 Conversion de : {filename} ...")
            
            # 1. Initialisation du convertisseur
            cv = Converter(filename)
            
            # 2. Conversion (start=0, end=None convertit tout le document)
            # multi_processing=True peut accélérer sur les gros fichiers
            cv.convert(docx_filename, start=0, end=None)
            
            # 3. Fermeture (Important pour libérer le fichier)
            cv.close()
            
            print(f"✅ Terminé : {docx_filename}")
            
        except Exception as e:
            print(f"⚠️ Erreur sur {filename} : {e}")

    print("-" * 50)
    print("🚀 Opération terminée !")

if __name__ == "__main__":
    pdf_to_word_batch()