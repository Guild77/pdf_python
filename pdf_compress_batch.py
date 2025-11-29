import fitz  # PyMuPDF
import os

def compress_single_pdf(input_path, output_path):
    """
    Fonction cœur qui compresse un fichier spécifique (votre logique originale).
    """
    # --- RÉGLAGES CIBLÉS ---
    GRAYSCALE = True 
    QUALITY = 40
    DPI = 130
    # -----------------------

    try:
        doc = fitz.open(input_path)
        new_doc = fitz.open()

        # On évite d'imprimer chaque page pour ne pas inonder la console en mode batch
        # print(f"Traitement de {input_path} ({len(doc)} pages)...")

        for page_num, page in enumerate(doc):
            zoom = DPI / 72
            mat = fitz.Matrix(zoom, zoom)
            
            if GRAYSCALE:
                pix = page.get_pixmap(matrix=mat, colorspace=fitz.csGRAY)
            else:
                pix = page.get_pixmap(matrix=mat)

            img_bytes = pix.tobytes("jpg", jpg_quality=QUALITY)

            new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
            new_page.insert_image(new_page.rect, stream=img_bytes)

        new_doc.save(output_path, garbage=4, deflate=True)
        
        # Stats
        old_size = os.path.getsize(input_path) / (1024 * 1024)
        new_size = os.path.getsize(output_path) / (1024 * 1024)
        reduction = (1 - (new_size / old_size)) * 100

        print(f"✅ {os.path.basename(input_path)} -> {os.path.basename(output_path)}")
        print(f"   Origine: {old_size:.2f} MB | Final: {new_size:.2f} MB | Gain: {reduction:.1f}%")

    except Exception as e:
        print(f"❌ Erreur sur {input_path} : {e}")
    finally:
        if 'doc' in locals(): doc.close()
        if 'new_doc' in locals(): new_doc.close()

def batch_compress():
    """
    Scanne le répertoire courant et compresse tous les PDF éligibles.
    """
    # Récupère le dossier où se trouve le script
    current_dir = os.getcwd()
    
    # Liste tous les fichiers PDF
    files = [f for f in os.listdir(current_dir) if f.lower().endswith('.pdf')]
    
    count = 0
    print(f"📂 Démarrage du traitement par lot dans : {current_dir}")
    print("-" * 50)

    for filename in files:
        # 1. On ignore les fichiers déjà compressés pour ne pas faire "fichier_compress_compress.pdf"
        if "_compress.pdf" in filename:
            continue
        
        # 2. On ignore le fichier fusionné final s'il existe (optionnel)
        if "fusionne" in filename:
            continue

        # 3. Construction du nom de sortie
        # Exemple : "mon_contrat.pdf" devient "mon_contrat_compress.pdf"
        base_name = os.path.splitext(filename)[0]
        output_filename = f"{base_name}_compress.pdf"
        
        # Chemins complets
        input_path = os.path.join(current_dir, filename)
        output_path = os.path.join(current_dir, output_filename)

        # 4. Exécution
        compress_single_pdf(input_path, output_path)
        count += 1

    print("-" * 50)
    print(f"🚀 Terminé ! {count} fichiers traités.")

if __name__ == "__main__":
    batch_compress()