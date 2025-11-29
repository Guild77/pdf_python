import fitz  # PyMuPDF
import os

def pdf_to_jpg_explode():
    """
    Convertit chaque page de chaque PDF du dossier en image JPG.
    Crée un sous-dossier par PDF pour ranger les images.
    """
    current_dir = os.getcwd()
    
    # Récupération des fichiers PDF
    files = [f for f in os.listdir(current_dir) if f.lower().endswith('.pdf')]
    
    # On évite de traiter les fichiers déjà compressés ou générés par nos scripts précédents
    # (Optionnel, vous pouvez retirer ce filtre si vous voulez tout traiter)
    files = [f for f in files if "_images" not in f]

    if not files:
        print("❌ Aucun fichier PDF trouvé.")
        return

    print(f"📂 {len(files)} fichiers PDF trouvés. Démarrage de l'extraction...")
    print("-" * 50)

    for pdf_file in files:
        try:
            doc = fitz.open(pdf_file)
            base_name = os.path.splitext(pdf_file)[0]
            
            # 1. Créer un dossier spécifique pour ce PDF
            output_folder = os.path.join(current_dir, f"{base_name}_images")
            os.makedirs(output_folder, exist_ok=True)
            
            print(f"Traite : {pdf_file} ({len(doc)} pages) -> Dossier : {base_name}_images/")

            for page_num, page in enumerate(doc):
                # 2. Définir la qualité (Résolution)
                # zoom = 2 correspond environ à 150 DPI (qualité écran/lecture)
                # zoom = 3 correspond environ à 200-300 DPI (qualité impression)
                zoom = 2
                mat = fitz.Matrix(zoom, zoom)
                
                # 3. Rendu de la page en image (Pixmap)
                pix = page.get_pixmap(matrix=mat)
                
                # 4. Sauvegarde
                # Nommage : page_001.jpg, page_002.jpg...
                image_name = f"page_{page_num + 1:03d}.jpg"
                save_path = os.path.join(output_folder, image_name)
                
                pix.save(save_path)

            doc.close()
            
        except Exception as e:
            print(f"⚠️ Erreur sur {pdf_file} : {e}")

    print("-" * 50)
    print("🚀 Extraction terminée !")

if __name__ == "__main__":
    pdf_to_jpg_explode()