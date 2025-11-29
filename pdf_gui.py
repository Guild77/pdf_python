import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import fitz  # PyMuPDF
import os
import threading

class PDFToolboxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ma PDF Toolbox")
        self.root.geometry("600x500")
        
        # Liste des fichiers stockés
        self.file_list = []

        # --- ZONE DE GLISSER-DÉPOSER ---
        self.lb_frame = tk.Frame(root)
        self.lb_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.label_info = tk.Label(self.lb_frame, text="⬇️ Glissez vos fichiers PDF ici ⬇️", font=("Arial", 12, "bold"), fg="gray")
        self.label_info.pack(pady=5)

        self.listbox = tk.Listbox(self.lb_frame, selectmode=tk.EXTENDED, bg="#f0f0f0", font=("Consolas", 9))
        self.listbox.pack(fill="both", expand=True, side="left")
        
        # Scrollbar pour la liste
        self.scrollbar = tk.Scrollbar(self.lb_frame, orient="vertical", command=self.listbox.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # Activation du Drag & Drop
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind('<<Drop>>', self.drop_files)

        # --- BOUTONS D'ACTION ---
        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(fill="x", padx=10, pady=10)

        # Bouton Vider
        self.btn_clear = tk.Button(self.btn_frame, text="🗑️ Vider la liste", command=self.clear_list, bg="#ffcccc")
        self.btn_clear.pack(side="left", padx=5)

        # Bouton Compresser
        self.btn_compress = tk.Button(self.btn_frame, text="📉 Compresser (-50%)", command=lambda: self.run_action("compress"), bg="#ccffcc", height=2)
        self.btn_compress.pack(side="right", padx=5)

        # Bouton Fusionner
        self.btn_merge = tk.Button(self.btn_frame, text="🔗 Fusionner tout", command=lambda: self.run_action("merge"), bg="#cce5ff", height=2)
        self.btn_merge.pack(side="right", padx=5)

        # --- BARRE DE STATUT ---
        self.status_var = tk.StringVar()
        self.status_var.set("Prêt.")
        self.status_label = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor="w")
        self.status_label.pack(side="bottom", fill="x")

    def drop_files(self, event):
        """Gère les fichiers déposés dans la fenêtre"""
        # Le format retourné par Windows peut contenir des accolades { } s'il y a des espaces
        # On fait un petit nettoyage
        raw_files = event.data
        if raw_files.startswith('{') and raw_files.endswith('}'):
             # Cas complexe Windows avec espaces
             paths = self.parse_windows_paths(raw_files)
        else:
             # Cas simple (un seul fichier ou Linux/Mac)
             paths = root.tk.splitlist(raw_files)

        for path in paths:
            if path.lower().endswith('.pdf') and path not in self.file_list:
                self.file_list.append(path)
                self.listbox.insert(tk.END, path)
                self.status_var.set(f"Ajouté : {os.path.basename(path)}")

    def parse_windows_paths(self, data):
        """Nettoie les chemins Windows bizarres avec des accolades"""
        # Cette fonction est une astuce pour tkinterdnd2 sur Windows
        paths = []
        current = ""
        in_braces = False
        for char in data:
            if char == '{':
                in_braces = True
            elif char == '}':
                in_braces = False
            elif char == ' ' and not in_braces:
                if current:
                    paths.append(current)
                    current = ""
            else:
                current += char
        if current:
            paths.append(current)
        return paths

    def clear_list(self):
        self.file_list = []
        self.listbox.delete(0, tk.END)
        self.status_var.set("Liste vidée.")

    def run_action(self, action_type):
        if not self.file_list:
            messagebox.showwarning("Attention", "La liste est vide !")
            return

        # On lance le travail dans un "Thread" séparé pour ne pas figer l'interface
        thread = threading.Thread(target=self.process_files, args=(action_type,))
        thread.start()

    def process_files(self, action_type):
        """La logique métier (Vos scripts PyMuPDF)"""
        count = 0
        try:
            if action_type == "compress":
                self.status_var.set("⏳ Compression en cours...")
                for file_path in self.file_list:
                    
                    # LOGIQUE DE COMPRESSION (reprise de votre script)
                    doc = fitz.open(file_path)
                    new_doc = fitz.open()
                    for page in doc:
                        pix = page.get_pixmap(matrix=fitz.Matrix(150/72, 150/72), colorspace=fitz.csGRAY)
                        img_bytes = pix.tobytes("jpg", jpg_quality=40)
                        new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
                        new_page.insert_image(new_page.rect, stream=img_bytes)
                    
                    output = os.path.splitext(file_path)[0] + "_compress_gui.pdf"
                    new_doc.save(output, garbage=4, deflate=True)
                    count += 1
                
                self.status_var.set(f"✅ Terminé ! {count} fichiers compressés.")
                messagebox.showinfo("Succès", f"{count} fichiers compressés avec succès.")

            elif action_type == "merge":
                self.status_var.set("⏳ Fusion en cours...")
                merged_doc = fitz.open()
                # On s'assure de l'ordre (facultatif, ici c'est l'ordre d'ajout dans la liste)
                for file_path in self.file_list:
                    with fitz.open(file_path) as doc:
                        merged_doc.insert_pdf(doc)
                
                # Sauvegarde dans le dossier du premier fichier
                first_dir = os.path.dirname(self.file_list[0])
                output = os.path.join(first_dir, "fusion_gui.pdf")
                merged_doc.save(output)
                
                self.status_var.set(f"✅ Fusion terminée : {os.path.basename(output)}")
                messagebox.showinfo("Succès", f"Fichier créé :\n{output}")

        except Exception as e:
            self.status_var.set("❌ Erreur")
            messagebox.showerror("Erreur", str(e))

if __name__ == "__main__":
    # On utilise TkinterDnD.Tk au lieu de tk.Tk pour activer le Drag&Drop
    root = TkinterDnD.Tk()
    app = PDFToolboxApp(root)
    root.mainloop()