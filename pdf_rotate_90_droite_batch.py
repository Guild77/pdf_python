import fitz  # PyMuPDF
import os

def rotate_pdfs_90_right():
    """
    Tourne toutes les pages de tous les fichiers PDF du dossier courant
    de 90 degrés vers la droite (Sens horaire).
    """
    current_dir = os.getcwd()
    
    # Récupération des fichiers PDF
    files = [f for f in os.listdir(current_dir) if f.lower().endswith('.pdf')]
    
    # On ignore les fichiers déjà traités pour éviter les boucles si on relance
    files = [f for f in files if "_rotated" not in f]

    if not files:
        print("❌ Aucun fichier PDF trouvé.")
        return

    print(f"📂 {len(files)} fichiers trouvés. Rotation en cours...")
    print("-" * 50)

    count = 0
    for filename in files:
        try:
            doc = fitz.open(filename)
            
            # Pour chaque page du document
            for page in doc:
                # 1. On récupère la rotation actuelle (souvent 0)
                current_rotation = page.rotation
                
                # 2. On ajoute 90 degrés
                # PyMuPDF gère automatiquement le modulo (360+90 devient 90)
                page.set_rotation(current_rotation + 90)

            # 3. Sauvegarde
            base_name = os.path.splitext(filename)[0]
            output_filename = f"{base_name}_rotated.pdf"
            
            doc.save(output_filename)
            print(f"✅ {filename} -> {output_filename} (Rotation effectuée)")
            count += 1
            
            doc.close()

        except Exception as e:
            print(f"⚠️ Erreur sur {filename} : {e}")

    print("-" * 50)
    print(f"🚀 Terminé ! {count} fichiers pivotés.")

if __name__ == "__main__":
    rotate_pdfs_90_right()