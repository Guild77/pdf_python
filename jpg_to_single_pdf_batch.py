import fitz
import os

def jpg_to_single_pdf():
    OUTPUT_FILE = "images_fusionnees.pdf"
    current_dir = os.getcwd()
    files = [f for f in os.listdir(current_dir) if f.lower().endswith(('.jpg', '.jpeg'))]
    files.sort() # Important pour l'ordre des pages

    doc = fitz.open() # Nouveau PDF vide

    for filename in files:
        print(f"Ajout de {filename}...")
        img = fitz.open(filename)  # Ouvrir l'image
        rect = img[0].rect         # Récupérer les dimensions de l'image
        pdfbytes = img.convert_to_pdf() # Convertir en PDF
        img.close()
        
        imgPDF = fitz.open("pdf", pdfbytes) # Ouvrir le bloc PDF temporaire
        page = doc.new_page(width = rect.width, height = rect.height) # Créer page
        page.show_pdf_page(rect, imgPDF, 0) # Dessiner l'image sur la page

    doc.save(OUTPUT_FILE)
    print(f"✅ Fichier final créé : {OUTPUT_FILE}")

if __name__ == "__main__":
    jpg_to_single_pdf()