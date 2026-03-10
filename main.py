import sys
import random

# Vérification de tkinter
try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    print("Tkinter n'est pas installé sur votre système.\n")

    if sys.platform.startswith("linux"):
        print("Pour l'installer sur Linux (Debian/Ubuntu) :")
        print("sudo apt update && sudo apt install python3-tk")
    elif sys.platform == "darwin":
        print("Sur macOS, tkinter est normalement inclus avec Python officiel.")
        print("Réinstallez Python depuis le site officiel de Python.")
    elif sys.platform.startswith("win"):
        print("Sur Windows, réinstallez Python en activant l'option Tcl/Tk and IDLE.")
    else:
        print("Veuillez installer tkinter manuellement selon votre système.")

    sys.exit(1)


class JeuNombreMystere:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu du nombre mystère")
        self.root.geometry("500x500")
        self.root.resizable(False, False)

        self.scores = {}
        self.nombre_aleatoire = None
        self.max_val = 10
        self.essais = 0

        self.creer_widgets()

    def creer_widgets(self):
        titre = tk.Label(
            self.root,
            text="Jeu du nombre mystère",
            font=("Arial", 18, "bold")
        )
        titre.pack(pady=15)

        frame_joueur = tk.Frame(self.root)
        frame_joueur.pack(pady=5)

        tk.Label(frame_joueur, text="Nom du joueur :").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nom = tk.Entry(frame_joueur, width=20)
        self.entry_nom.grid(row=0, column=1, padx=5, pady=5)

        frame_niveau = tk.Frame(self.root)
        frame_niveau.pack(pady=5)

        tk.Label(frame_niveau, text="Niveau :").grid(row=0, column=0, padx=5, pady=5)

        self.niveau_var = tk.IntVar(value=1)
        tk.Radiobutton(frame_niveau, text="Facile (1-10)", variable=self.niveau_var, value=1).grid(row=0, column=1, padx=5)
        tk.Radiobutton(frame_niveau, text="Moyen (1-100)", variable=self.niveau_var, value=2).grid(row=0, column=2, padx=5)
        tk.Radiobutton(frame_niveau, text="Difficile (1-1000)", variable=self.niveau_var, value=3).grid(row=0, column=3, padx=5)

        self.btn_nouvelle_partie = tk.Button(
            self.root,
            text="Nouvelle partie",
            command=self.nouvelle_partie,
            width=20,
            bg="lightblue"
        )
        self.btn_nouvelle_partie.pack(pady=10)

        self.label_info = tk.Label(
            self.root,
            text="Choisissez un niveau puis lancez une partie.",
            font=("Arial", 11)
        )
        self.label_info.pack(pady=10)

        frame_saisie = tk.Frame(self.root)
        frame_saisie.pack(pady=10)

        tk.Label(frame_saisie, text="Votre proposition :").grid(row=0, column=0, padx=5)
        self.entry_nombre = tk.Entry(frame_saisie, width=15)
        self.entry_nombre.grid(row=0, column=1, padx=5)

        self.btn_valider = tk.Button(
            frame_saisie,
            text="Valider",
            command=self.verifier_proposition,
            state=tk.DISABLED
        )
        self.btn_valider.grid(row=0, column=2, padx=5)

        self.label_resultat = tk.Label(self.root, text="", font=("Arial", 12, "bold"))
        self.label_resultat.pack(pady=10)

        self.label_essais = tk.Label(self.root, text="Nombre d'essais : 0", font=("Arial", 11))
        self.label_essais.pack(pady=5)

        tk.Label(self.root, text="Historique des scores :", font=("Arial", 12, "bold")).pack(pady=10)

        self.listbox_scores = tk.Listbox(self.root, width=40, height=8)
        self.listbox_scores.pack(pady=5)

    def nouvelle_partie(self):
        niveau = self.niveau_var.get()

        if niveau == 1:
            self.max_val = 10
        elif niveau == 2:
            self.max_val = 100
        else:
            self.max_val = 1000

        self.nombre_aleatoire = random.randint(1, self.max_val)
        self.essais = 0

        self.label_info.config(text=f"Trouvez un nombre entre 1 et {self.max_val}.")
        self.label_resultat.config(text="")
        self.label_essais.config(text="Nombre d'essais : 0")

        self.entry_nombre.delete(0, tk.END)
        self.btn_valider.config(state=tk.NORMAL)

    def verifier_proposition(self):
        if self.nombre_aleatoire is None:
            messagebox.showwarning("Attention", "Veuillez lancer une nouvelle partie.")
            return

        try:
            num = int(self.entry_nombre.get())
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre entier.")
            return

        if not (1 <= num <= self.max_val):
            messagebox.showerror("Erreur", f"Veuillez entrer un nombre entre 1 et {self.max_val}.")
            return

        self.essais += 1
        self.label_essais.config(text=f"Nombre d'essais : {self.essais}")

        if num == self.nombre_aleatoire:
            nom_joueur = self.entry_nom.get().strip()
            if nom_joueur == "":
                nom_joueur = "Joueur"

            self.label_resultat.config(
                text=f"Victoire ! {nom_joueur} a trouvé en {self.essais} essai(s).",
                fg="green"
            )

            self.scores[nom_joueur] = self.essais
            self.mettre_a_jour_scores()

            rejouer = messagebox.askyesno("Victoire", "Bravo ! Voulez-vous rejouer ?")
            if rejouer:
                self.nouvelle_partie()
            else:
                self.btn_valider.config(state=tk.DISABLED)

        elif num > self.nombre_aleatoire:
            self.label_resultat.config(text="Plus petit", fg="red")
        else:
            self.label_resultat.config(text="Plus grand", fg="blue")

        self.entry_nombre.delete(0, tk.END)

    def mettre_a_jour_scores(self):
        self.listbox_scores.delete(0, tk.END)

        scores_tries = sorted(self.scores.items(), key=lambda x: x[1])

        for i, (nom, score) in enumerate(scores_tries, start=1):
            self.listbox_scores.insert(tk.END, f"{i}. {nom} : {score} essai(s)")


if __name__ == "__main__":
    root = tk.Tk()
    app = JeuNombreMystere(root)
    root.mainloop()
