import fitz  # PyMuPDF
import os

def rotate_pdfs_90_left():
    """
    Tourne toutes les pages de tous les fichiers PDF du dossier courant
    de 90 degrés vers la GAUCHE (Sens anti-horaire).
    """
    current_dir = os.getcwd()
    
    files = [f for f in os.listdir(current_dir) if f.lower().endswith('.pdf')]
    
    # On ignore les fichiers déjà traités
    files = [f for f in files if "_left" not in f]

    if not files:
        print("❌ Aucun fichier PDF trouvé.")
        return

    print(f"📂 {len(files)} fichiers trouvés. Rotation GAUCHE en cours...")
    print("-" * 50)

    count = 0
    for filename in files:
        try:
            doc = fitz.open(filename)
            
            for page in doc:
                current_rotation = page.rotation
                
                # C'est la seule ligne qui change : -90 au lieu de +90
                # PyMuPDF gère automatiquement le calcul (0 - 90 devient 270)
                page.set_rotation(current_rotation - 90)

            base_name = os.path.splitext(filename)[0]
            # On ajoute un suffixe explicite
            output_filename = f"{base_name}_rotated_left.pdf"
            
            doc.save(output_filename)
            print(f"✅ {filename} -> {output_filename} (Rotation Gauche)")
            count += 1
            
            doc.close()

        except Exception as e:
            print(f"⚠️ Erreur sur {filename} : {e}")

    print("-" * 50)
    print(f"🚀 Terminé ! {count} fichiers pivotés à gauche.")

if __name__ == "__main__":
    rotate_pdfs_90_left()