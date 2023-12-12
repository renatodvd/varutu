import tkinter as tk
import tkinter.simpledialog as tk_simpledialog
from tkinter import messagebox

class AplicatieDepozit(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Aplicație Depozit Materiale")
        self.geometry("800x400")

        # Dicționar pentru a stoca materialele și cantitățile disponibile
        self.depozit_materiale = {}

        # Listă pentru a stoca rețetele
        self.lista_retele = []

        # Dicționar pentru a stoca materialele și cantitățile utilizate în rețete
        self.materiale_utilizate_in_retele = {}

        self.creare_interfata()

    def creare_interfata(self):
        # Partea pentru materiale
        lbl_nume = tk.Label(self, text="Nume material:")
        lbl_nume.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_nume = tk.Entry(self)
        self.entry_nume.grid(row=0, column=1, padx=10, pady=10)

        lbl_cantitate = tk.Label(self, text="Cantitate:")
        lbl_cantitate.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_cantitate = tk.Entry(self)
        self.entry_cantitate.grid(row=1, column=1, padx=10, pady=10)

        btn_adauga = tk.Button(self, text="Adaugă Material", command=self.adauga_material)
        btn_adauga.grid(row=2, column=0, columnspan=2, pady=10)

        # Buton pentru a șterge material
        btn_sterge_material = tk.Button(self, text="Șterge Material", command=self.sterge_material)
        btn_sterge_material.grid(row=2, column=2, columnspan=1, pady=10, padx=(10, 0))

        # Partea pentru rețete
        lbl_reteta = tk.Label(self, text="Nume Rețetă:")
        lbl_reteta.grid(row=0, column=3, padx=10, pady=10, sticky="w")
        self.entry_reteta = tk.Entry(self)
        self.entry_reteta.grid(row=0, column=4, padx=10, pady=10)

        lbl_cantitate_reteta = tk.Label(self, text="Materiale în Retetă:")
        lbl_cantitate_reteta.grid(row=1, column=3, padx=10, pady=10, sticky="w")

        # Lista pentru a stoca materialele disponibile în depozit
        self.lista_materiale_disponibile = tk.Listbox(self, selectmode=tk.MULTIPLE)
        self.lista_materiale_disponibile.grid(row=1, column=4, padx=10, pady=10)

        btn_adauga_reteta = tk.Button(self, text="Adaugă Rețetă", command=self.adauga_reteta)
        btn_adauga_reteta.grid(row=2, column=3, columnspan=2, pady=10, padx=(10, 0))

        # Listbox pentru afișarea materialelor din depozit
        self.lista_box_materiale = tk.Listbox(self)
        self.lista_box_materiale.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Adaugă configurare pentru coloane în lista de materiale
        self.columnconfigure(0, weight=2)  # Prima coloană să fie mai mare
        self.columnconfigure(1, weight=1)  # A doua coloană

        # Listbox pentru afișarea rețetelor
        self.lista_box_retele = tk.Listbox(self)
        self.lista_box_retele.grid(row=3, column=2, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Adaugă configurare pentru coloane în lista de rețete
        self.columnconfigure(2, weight=2)  # Prima coloană să fie mai mare
        self.columnconfigure(3, weight=1)  # A doua coloană

    def adauga_material(self):
        nume = self.entry_nume.get()
        cantitate = self.entry_cantitate.get()

        if nume and cantitate:
            cantitate = int(cantitate)

            if nume in self.depozit_materiale:
                self.depozit_materiale[nume] += cantitate
            else:
                self.depozit_materiale[nume] = cantitate

            self.actualizeaza_lista_materiale()

            self.entry_nume.delete(0, tk.END)
            self.entry_cantitate.delete(0, tk.END)
        else:
            messagebox.showwarning("Avertizare", "Te rog completează toate câmpurile pentru materiale.")

    def sterge_material(self):
        materiale_selectate = self.lista_materiale_disponibile.curselection()

        for index in materiale_selectate:
            material = self.lista_materiale_disponibile.get(index)
            nume_material = material.split(" - ")[0]

            cantitate_material = tk_simpledialog.askinteger("Șterge Cantitate", f"Introdu cantitatea pentru {nume_material}:", parent=self)
            if cantitate_material is not None and cantitate_material > 0:
                if nume_material in self.depozit_materiale and self.depozit_materiale[nume_material] >= cantitate_material:
                    self.depozit_materiale[nume_material] -= cantitate_material
                else:
                    messagebox.showwarning("Avertizare", f"Cantitatea pentru {nume_material} este insuficientă.")
        
        self.actualizeaza_lista_materiale()

    def adauga_reteta(self):
        nume_reteta = self.entry_reteta.get()

        if nume_reteta:
            # Obține toate materialele din depozit
            materiale_disponibile = list(self.depozit_materiale.keys())

            # Verifică dacă există materiale în depozit
            if not materiale_disponibile:
                messagebox.showwarning("Avertizare", "Nu există materiale disponibile în depozit.")
                return

            # Crează un dicționar pentru a stoca materialele și cantitățile din rețetă
            materiale_reteta = {}

            for material in materiale_disponibile:
                cantitate_material = tk_simpledialog.askinteger("Cantitate", f"Introdu cantitatea pentru {material}:", parent=self)
                if cantitate_material is not None and cantitate_material > 0:
                    materiale_reteta[material] = cantitate_material

            # Adaugă rețeta în listă și actualizează listbox-ul pentru rețete
            self.lista_retele.append({nume_reteta: materiale_reteta})
            self.lista_box_retele.delete(0, tk.END)
            for reteta in self.lista_retele:
                for nume_reteta, materiale_reteta in reteta.items():
                    self.lista_box_retele.insert(tk.END, f"{nume_reteta} - Materiale: {materiale_reteta}")

            # Actualizează lista de materiale în interfață
            self.actualizeaza_lista_materiale()

            # Resetează câmpurile de introducere pentru rețete
            self.entry_reteta.delete(0, tk.END)
        else:
            messagebox.showwarning("Avertizare", "Te rog completează toate câmpurile pentru rețete.")

    def actualizeaza_lista_materiale(self):
        self.lista_box_materiale.delete(0, tk.END)
        for material, cantitate in self.depozit_materiale.items():
            self.lista_box_materiale.insert(tk.END, f"{material} - {cantitate} buc")

        # Actualizează lista de materiale disponibile pentru ștergere
        self.lista_materiale_disponibile.delete(0, tk.END)
        for material in self.depozit_materiale.keys():
            self.lista_materiale_disponibile.insert(tk.END, material)

if __name__ == "__main__":
    app = AplicatieDepozit()
    app.mainloop()
