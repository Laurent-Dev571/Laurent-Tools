import tkinter as tk
from tkinter import messagebox, filedialog
import random
import string
import os
import zipfile
from PIL import Image
import speedtest

# ===== STYLE =====
bg = "#0a0a0a"
fg = "#00ffcc"
btn_bg = "#1a1a1a"
btn_fg = "#00ffcc"
btn_special = "#00ccaa"

FONT = ("Segoe UI", 9)
FONT_BOLD = ("Segoe UI", 9, "bold")
FONT_TITLE = ("Segoe UI", 14, "bold")
FONT_TOOL = ("Segoe UI", 10, "bold")

root = tk.Tk()
root.title("Laurent Tools")
root.geometry("850x650")
root.configure(bg=bg)

tk.Label(root, text="🛠️ LAURENT TOOLS", font=FONT_TITLE, fg=fg, bg=bg).pack(pady=(15, 0))
tk.Label(root, text="Boîte à outils créée par Laurent Bajika", font=FONT, fg="#aaaaaa", bg=bg).pack(pady=(0, 10))

# ===== OUTIL 1 : GÉNÉRATEUR =====
def ouvrir_generateur():
    fen = tk.Toplevel(root)
    fen.title("Générateur")
    fen.geometry("480x380")
    fen.configure(bg=bg)
    tk.Label(fen, text="🔐 GÉNÉRATEUR", font=FONT_TITLE, fg=fg, bg=bg).pack(pady=(15, 5))
    tk.Label(fen, text="Longueur :", font=FONT_BOLD, fg="white", bg=bg).pack()
    lv = tk.IntVar(value=16)
    f1 = tk.Frame(fen, bg=bg)
    f1.pack()
    for v in [8, 12, 16, 24, 32]:
        tk.Radiobutton(f1, text=str(v), variable=lv, value=v, fg="white", bg=bg, selectcolor="#333", font=FONT).pack(side=tk.LEFT, padx=5)
    tk.Label(fen, text="Inclure :", font=FONT_BOLD, fg="white", bg=bg).pack(pady=(10, 0))
    f2 = tk.Frame(fen, bg=bg)
    f2.pack()
    a, b, c, d = tk.BooleanVar(value=True), tk.BooleanVar(value=True), tk.BooleanVar(value=True), tk.BooleanVar(value=True)
    tk.Checkbutton(f2, text="Min", variable=a, fg="white", bg=bg, selectcolor="#333", font=FONT).pack(side=tk.LEFT, padx=3)
    tk.Checkbutton(f2, text="Maj", variable=b, fg="white", bg=bg, selectcolor="#333", font=FONT).pack(side=tk.LEFT, padx=3)
    tk.Checkbutton(f2, text="Chiffres", variable=c, fg="white", bg=bg, selectcolor="#333", font=FONT).pack(side=tk.LEFT, padx=3)
    tk.Checkbutton(f2, text="Symboles", variable=d, fg="white", bg=bg, selectcolor="#333", font=FONT).pack(side=tk.LEFT, padx=3)
    e = tk.Entry(fen, font=("Courier New", 12, "bold"), bg="#1a1a1a", fg=fg, width=35, justify="center")
    e.pack(pady=15)

    def gen():
        ch = ""
        if a.get(): ch += string.ascii_lowercase
        if b.get(): ch += string.ascii_uppercase
        if c.get(): ch += string.digits
        if d.get(): ch += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not ch:
            messagebox.showwarning("Erreur", "Coche au moins une option !")
            return
        e.delete(0, tk.END)
        e.insert(0, "".join(random.choice(ch) for _ in range(lv.get())))

    def cop():
        if e.get():
            fen.clipboard_clear()
            fen.clipboard_append(e.get())
            messagebox.showinfo("Copié !", "Copié.")

    f3 = tk.Frame(fen, bg=bg)
    f3.pack()
    tk.Button(f3, text="🎲 Générer", font=FONT_BOLD, bg=btn_special, fg="black", padx=15, pady=6, command=gen).pack(side=tk.LEFT, padx=5)
    tk.Button(f3, text="📋 Copier", font=FONT_BOLD, bg=btn_bg, fg=btn_fg, padx=15, pady=6, command=cop).pack(side=tk.LEFT, padx=5)

# ===== OUTIL 2 : CALCULATRICE =====
def ouvrir_calculatrice():
    fen = tk.Toplevel(root)
    fen.title("Calculatrice")
    fen.geometry("320x450")
    fen.configure(bg=bg)
    tk.Label(fen, text="🧮 CALCULATRICE", font=FONT_TITLE, fg=fg, bg=bg).pack(pady=(15, 10))
    e = tk.Entry(fen, font=("Courier New", 20, "bold"), bg="#1a1a1a", fg=fg, justify="right", bd=0)
    e.pack(fill=tk.X, padx=15, pady=5, ipady=12)

    def aj(v):
        e.insert(tk.END, str(v))

    def ef():
        e.delete(0, tk.END)

    def ca():
        try:
            r = eval(e.get())
            e.delete(0, tk.END)
            e.insert(0, str(r))
        except:
            e.delete(0, tk.END)
            e.insert(0, "Erreur")

    f = tk.Frame(fen, bg=bg)
    f.pack(pady=10)
    for (t, l, c) in [("7",0,0),("8",0,1),("9",0,2),("/",0,3),("4",1,0),("5",1,1),("6",1,2),("*",1,3),("1",2,0),("2",2,1),("3",2,2),("-",2,3),("0",3,0),(".",3,1),("=",3,2),("+",3,3)]:
        cmd, col, fgc = (ca, btn_special, "black") if t == "=" else ((lambda x=t: aj(x)), btn_bg, btn_fg)
        tk.Button(f, text=t, font=("Segoe UI", 12, "bold"), bg=col, fg=fgc, width=4, height=2, relief="flat", command=cmd).grid(row=l, column=c, padx=2, pady=2)
    tk.Button(fen, text="C — Effacer", font=FONT_BOLD, bg="#cc3333", fg="white", padx=15, pady=6, command=ef).pack(pady=8)

# ===== OUTIL 3 : BLOC-NOTES =====
def ouvrir_bloc_notes():
    fen = tk.Toplevel(root)
    fen.title("Bloc-notes")
    fen.geometry("550x450")
    fen.configure(bg=bg)
    tk.Label(fen, text="📝 BLOC-NOTES", font=FONT_TITLE, fg=fg, bg=bg).pack(pady=(15, 5))
    t = tk.Text(fen, font=("Segoe UI", 10), bg="#1a1a1a", fg="white", insertbackground="white", wrap="word", bd=0)
    t.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

    def enr():
        f = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Texte", "*.txt")])
        if f:
            with open(f, "w", encoding="utf-8") as file:
                file.write(t.get("1.0", tk.END))
            messagebox.showinfo("OK", "Enregistré !")

    def ouv():
        f = filedialog.askopenfilename(filetypes=[("Texte", "*.txt")])
        if f:
            with open(f, "r", encoding="utf-8") as file:
                t.delete("1.0", tk.END)
                t.insert("1.0", file.read())

    def eff():
        if messagebox.askyesno("?", "Effacer tout ?"):
            t.delete("1.0", tk.END)

    f = tk.Frame(fen, bg=bg)
    f.pack(pady=8)
    tk.Button(f, text="💾 Enregistrer", font=FONT_BOLD, bg=btn_special, fg="black", padx=12, pady=6, command=enr).pack(side=tk.LEFT, padx=4)
    tk.Button(f, text="📂 Ouvrir", font=FONT_BOLD, bg=btn_bg, fg=btn_fg, padx=12, pady=6, command=ouv).pack(side=tk.LEFT, padx=4)
    tk.Button(f, text="🗑️ Effacer", font=FONT_BOLD, bg="#cc3333", fg="white", padx=12, pady=6, command=eff).pack(side=tk.LEFT, padx=4)

# ===== OUTIL 4 : COMPRESSEUR ZIP =====
def ouvrir_compresseur():
    fen = tk.Toplevel(root)
    fen.title("Compresseur ZIP")
    fen.geometry("550x400")
    fen.configure(bg=bg)
    tk.Label(fen, text="📦 COMPRESSEUR ZIP", font=FONT_TITLE, fg=fg, bg=bg).pack(pady=(15, 5))
    tk.Label(fen, text="Choisis une action :", font=FONT_BOLD, fg="white", bg=bg).pack(pady=10)

    def comp():
        fs = filedialog.askopenfilenames(title="Fichiers à compresser")
        if not fs:
            return
        zn = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP", "*.zip")])
        if not zn:
            return
        try:
            with zipfile.ZipFile(zn, "w", zipfile.ZIP_DEFLATED) as z:
                for f in fs:
                    z.write(f, os.path.basename(f))
            messagebox.showinfo("OK", f"Créé : {zn}")
        except Exception as ex:
            messagebox.showerror("Erreur", str(ex))

    def dec():
        zf = filedialog.askopenfilename(filetypes=[("ZIP", "*.zip")])
        if not zf:
            return
        dd = filedialog.askdirectory(title="Dossier de destination")
        if not dd:
            return
        try:
            with zipfile.ZipFile(zf, "r") as z:
                z.extractall(dd)
            messagebox.showinfo("OK", f"Extrait dans : {dd}")
        except Exception as ex:
            messagebox.showerror("Erreur", str(ex))

    tk.Button(fen, text="📦 Compresser des fichiers en ZIP", font=FONT_BOLD, bg=btn_special, fg="black", padx=20, pady=10, command=comp).pack(pady=15)
    tk.Button(fen, text="📂 Décompresser une archive ZIP", font=FONT_BOLD, bg=btn_bg, fg=btn_fg, padx=20, pady=10, command=dec).pack(pady=10)

# ===== OUTIL 5 : CONVERTISSEUR D'IMAGES =====
def ouvrir_convertisseur():
    fen = tk.Toplevel(root)
    fen.title("Convertisseur d'images")
    fen.geometry("500x450")
    fen.configure(bg=bg)
    tk.Label(fen, text="🖼️ CONVERTISSEUR D'IMAGES", font=FONT_TITLE, fg=fg, bg=bg).pack(pady=(15, 5))
    tk.Label(fen, text="Sélectionne une image à convertir :", font=FONT_BOLD, fg="white", bg=bg).pack(pady=10)

    format_var = tk.StringVar(value="PNG")
    fichier_var = tk.StringVar(value="Aucun fichier sélectionné")

    def choisir():
        f = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.webp *.gif")], title="Choisir une image")
        if f:
            fichier_var.set(f)

    tk.Label(fen, textvariable=fichier_var, font=FONT, fg="#888888", bg=bg, wraplength=400).pack(pady=5)
    tk.Button(fen, text="📂 Choisir une image", font=FONT_BOLD, bg=btn_bg, fg=btn_fg, padx=15, pady=6, command=choisir).pack(pady=10)

    tk.Label(fen, text="Format de destination :", font=FONT_BOLD, fg="white", bg=bg).pack(pady=(15, 5))
    f = tk.Frame(fen, bg=bg)
    f.pack()
    for fmt in ["PNG", "JPG", "JPEG", "BMP", "WEBP"]:
        tk.Radiobutton(f, text=fmt, variable=format_var, value=fmt, fg="white", bg=bg, selectcolor="#333", font=FONT).pack(side=tk.LEFT, padx=5)

    def convertir():
        src = fichier_var.get()
        if src == "Aucun fichier sélectionné":
            messagebox.showwarning("Erreur", "Choisis d'abord une image !")
            return
        dest = filedialog.asksaveasfilename(defaultextension="." + format_var.get().lower(), filetypes=[(format_var.get(), "*." + format_var.get().lower())])
        if not dest:
            return
        try:
            img = Image.open(src)
            if format_var.get() in ("JPG", "JPEG") and img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(dest, format=format_var.get())
            messagebox.showinfo("Succès", "Image convertie en " + format_var.get())
        except Exception as ex:
            messagebox.showerror("Erreur", str(ex))

    tk.Button(fen, text="🔄 Convertir", font=FONT_BOLD, bg=btn_special, fg="black", padx=25, pady=10, command=convertir).pack(pady=20)

# ===== OUTIL 6 : TEST INTERNET =====
def ouvrir_test_internet():
    fen = tk.Toplevel(root)
    fen.title("Test Internet")
    fen.geometry("500x450")
    fen.configure(bg=bg)
    tk.Label(fen, text="🌐 TEST INTERNET", font=FONT_TITLE, fg=fg, bg=bg).pack(pady=(15, 5))
    tk.Label(fen, text="Clique pour lancer le test de vitesse", font=FONT_BOLD, fg="white", bg=bg).pack(pady=10)
    resultat = tk.Label(fen, text="", font=FONT, fg=fg, bg=bg, justify="left")
    resultat.pack(pady=20)

    def tester():
        resultat.config(text="⏳ Test en cours... (patientez 20-30 secondes)")
        fen.update()
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            dl = st.download() / 1_000_000
            ul = st.upload() / 1_000_000
            ping = st.results.ping
            resultat.config(text=f"✅ Résultats :\n\n📥 Téléchargement : {dl:.2f} Mbps\n📤 Envoi : {ul:.2f} Mbps\n⚡ Ping : {ping:.0f} ms")
        except Exception as e:
            resultat.config(text=f"❌ Erreur : {str(e)}")

    tk.Button(fen, text="🚀 Lancer le test", font=FONT_BOLD, bg=btn_special, fg="black", padx=25, pady=10, command=tester).pack(pady=20)

# ===== ROUTEUR =====
def ouvrir_outil(nom):
    if nom == "Générateur de mots de passe":
        ouvrir_generateur()
    elif nom == "Calculatrice":
        ouvrir_calculatrice()
    elif nom == "Bloc-notes":
        ouvrir_bloc_notes()
    elif nom == "Compresseur ZIP":
        ouvrir_compresseur()
    elif nom == "Convertisseur d'images":
        ouvrir_convertisseur()
    elif nom == "Test Internet":
        ouvrir_test_internet()
    else:
        messagebox.showinfo("Outil", nom + " bientôt disponible !")

# ===== GRILLE DES OUTILS =====
frame_outils = tk.Frame(root, bg=bg)
frame_outils.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

outils = [
    ("Générateur de mots de passe", "🔐", "Mots de passe sécurisés"),
    ("Convertisseur d'images", "🖼️", "Changer le format"),
    ("Compresseur ZIP", "📦", "Compresser / décompresser"),
    ("Calculatrice", "🧮", "Calculs avancés"),
    ("Bloc-notes", "📝", "Prendre des notes"),
    ("Test Internet", "🌐", "Mesurer la connexion"),
]

for i, (nom, emoji, desc) in enumerate(outils):
    l, c = i // 2, i % 2
    cadre = tk.Frame(frame_outils, bg="#1a1a1a", bd=0)
    cadre.grid(row=l, column=c, padx=8, pady=8, sticky="nsew")
    tk.Label(cadre, text=emoji, font=("Segoe UI", 24), bg="#1a1a1a", fg=fg).pack(pady=(8, 2))
    tk.Label(cadre, text=nom, font=FONT_TOOL, bg="#1a1a1a", fg="white").pack()
    tk.Label(cadre, text=desc, font=FONT, bg="#1a1a1a", fg="#888888").pack(pady=(0, 6))
    tk.Button(cadre, text="Ouvrir", font=FONT_BOLD, bg=btn_special, fg="black", relief="flat", padx=15, pady=4, command=lambda n=nom: ouvrir_outil(n)).pack(pady=(0, 8))

frame_outils.grid_columnconfigure(0, weight=1)
frame_outils.grid_columnconfigure(1, weight=1)

tk.Label(root, text="© 2026 Laurent Bajika - Tous droits réservés", font=("Segoe UI", 8), fg="#444444", bg=bg).pack(pady=8)

root.mainloop()