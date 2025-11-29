import fitz  # PyMuPDF
import os

# Nom du fichier final
OUTPUT_FILENAME = "dossier_complet_fusionne.pdf"

def merge_pdfs_in_directory():
    # 1. Récupérer tous les fichiers PDF du dossier courant (.)
    # os.listdir('.') liste tout ce qu'il y a dans le dossier du script
    files = [f for f in os.listdir('.') if f.endswith('.pdf')]

    # 2. Éviter de fusionner le fichier de sortie s'il existe déjà
    if OUTPUT_FILENAME in files:
        files.remove(OUTPUT_FILENAME)

    # 3. Trier les fichiers par ordre alphabétique
    # C'est crucial pour que les pages soient dans le bon ordre.
    # Conseil : Numérotez vos fichiers (1_..., 2_..., 3_...)
    files.sort()

    if not files:
        print("❌ Aucun fichier PDF trouvé dans ce répertoire.")
        return

    print(f"📂 {len(files)} fichiers trouvés à fusionner :")
    for f in files:
        print(f"  - {f}")

    # 4. Création du document vide qui recevra tout
    merged_doc = fitz.open()

    # 5. Boucle d'insertion
    for filename in files:
        try:
            # Ouvre le document courant
            with fitz.open(filename) as doc:
                # Insère toutes les pages du document courant dans le document final
                merged_doc.insert_pdf(doc)
        except Exception as e:
            print(f"⚠️ Erreur impossible de lire {filename} : {e}")

    # 6. Sauvegarde finale
    merged_doc.save(OUTPUT_FILENAME)
    
    print("-" * 40)
    print(f"✅ FUSION RÉUSSIE !")
    print(f"Fichier créé : {OUTPUT_FILENAME}")
    print("-" * 40)

if __name__ == "__main__":
    merge_pdfs_in_directory()