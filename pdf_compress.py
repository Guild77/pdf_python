import fitz  # PyMuPDF
import os

def compress_pdf_target_1_6mb(input_path, output_path):
    """
    Tente d'atteindre ~1.5 MB en passant en niveaux de gris et en ajustant la compression.
    """
    # --- RÉGLAGES CIBLÉS POUR 1.6 MB ---
    # Niveaux de gris : True (Enlève la couleur, énorme gain de place)
    GRAYSCALE = True 
    # Qualité JPEG : 40 (Suffisant pour du texte administratif)
    QUALITY = 40
    # Résolution : 130 DPI (Un tout petit peu moins que 140, mais reste lisible)
    DPI = 130
    # -----------------------------------

    try:
        doc = fitz.open(input_path)
        new_doc = fitz.open()

        print(f"Traitement de {len(doc)} pages en mode Grayscale={GRAYSCALE}...")

        for page_num, page in enumerate(doc):
            zoom = DPI / 72
            mat = fitz.Matrix(zoom, zoom)
            
            # L'ASTUCE EST ICI : colorspace=fitz.csGRAY
            # On force la capture de l'image en niveaux de gris
            if GRAYSCALE:
                pix = page.get_pixmap(matrix=mat, colorspace=fitz.csGRAY)
            else:
                pix = page.get_pixmap(matrix=mat)

            # Compression JPEG
            img_bytes = pix.tobytes("jpg", jpg_quality=QUALITY)

            new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
            new_page.insert_image(new_page.rect, stream=img_bytes)
            
            print(f" -> Page {page_num + 1} optimisée.")

        new_doc.save(output_path, garbage=4, deflate=True)
        
        # Stats
        old_size = os.path.getsize(input_path) / (1024 * 1024)
        new_size = os.path.getsize(output_path) / (1024 * 1024)
        reduction = (1 - (new_size / old_size)) * 100

        print("-" * 30)
        print(f"✅ TERMINÉ !")
        print(f"Taille originale : {old_size:.2f} MB")
        print(f"Nouvelle taille  : {new_size:.2f} MB")
        print(f"Réduction        : {reduction:.1f}%")
        print("-" * 30)

    except Exception as e:
        print(f"❌ Erreur : {e}")
    finally:
        if 'doc' in locals(): doc.close()
        if 'new_doc' in locals(): new_doc.close()

if __name__ == "__main__":
    input_file = "Notice de renseignements à caractère financier_Mireya DARRAS.pdf"
    output_file = "Notice de renseignements à caractère financier_Mireya DARRAS_compress.pdf"
    
    compress_pdf_target_1_6mb(input_file, output_file)