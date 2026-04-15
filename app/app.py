from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from adapter import run_search


class DocumentSearchApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Iskanje po dokumentih")
        self.root.geometry("980x760")
        self.root.minsize(900, 680)

        self.folder_path: str = ""

        self.weighted_var = tk.BooleanVar(value=True)
        self.has_existing_matrices_var = tk.BooleanVar(value=False)

        self.k_var = tk.StringVar(value="2")
        self.cosine_var = tk.StringVar(value="0.1")
        self.query_var = tk.StringVar()

        self.matrix_a_var = tk.StringVar()
        self.matrix_s_var = tk.StringVar()
        self.matrix_g_var = tk.StringVar()

        self._build_ui()
        self._toggle_matrix_fields()

    def _build_ui(self) -> None:
        outer = ttk.Frame(self.root, padding=16)
        outer.pack(fill="both", expand=True)

        title = ttk.Label(
            outer,
            text="Aplikacija za iskanje po zbirki dokumentov",
            font=("Segoe UI", 16, "bold"),
        )
        title.pack(anchor="w")

        subtitle = ttk.Label(
            outer,
            text="Izberi mapo z .txt dokumenti, nastavi parametre in zaženi iskanje.",
        )
        subtitle.pack(anchor="w", pady=(4, 14))

        docs_frame = ttk.LabelFrame(outer, text="1. Dokumenti", padding=12)
        docs_frame.pack(fill="x", pady=(0, 12))

        btns = ttk.Frame(docs_frame)
        btns.pack(fill="x")

        ttk.Button(btns, text="Dodaj mapo", command=self._add_folder).pack(side="left")
        ttk.Button(btns, text="Počisti izbor", command=self._clear_folder).pack(side="left", padx=(8, 0))

        self.folder_label = ttk.Label(docs_frame, text="Ni izbrane mape.")
        self.folder_label.pack(anchor="w", pady=(10, 6))

        self.docs_list = tk.Listbox(docs_frame, height=8)
        self.docs_list.pack(fill="x", pady=(4, 0))

        options_frame = ttk.LabelFrame(outer, text="2. Nastavitve", padding=12)
        options_frame.pack(fill="x", pady=(0, 12))

        matrix_type_frame = ttk.Frame(options_frame)
        matrix_type_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(matrix_type_frame, text="Vrsta matrike:").pack(side="left")
        ttk.Radiobutton(
            matrix_type_frame,
            text="Utežena",
            variable=self.weighted_var,
            value=True,
        ).pack(side="left", padx=(12, 0))
        ttk.Radiobutton(
            matrix_type_frame,
            text="Neutežena",
            variable=self.weighted_var,
            value=False,
        ).pack(side="left", padx=(12, 0))

        existing_frame = ttk.Frame(options_frame)
        existing_frame.pack(fill="x")

        ttk.Checkbutton(
            existing_frame,
            text="Matrike A, S in G že obstajajo (zaenkrat se ignorira)",
            variable=self.has_existing_matrices_var,
            command=self._toggle_matrix_fields,
        ).pack(anchor="w")

        self.matrices_frame = ttk.Frame(options_frame)
        self.matrices_frame.pack(fill="x", pady=(10, 0))

        self._build_matrix_row(self.matrices_frame, "Matrika A:", self.matrix_a_var)
        self._build_matrix_row(self.matrices_frame, "Matrika S:", self.matrix_s_var)
        self._build_matrix_row(self.matrices_frame, "Matrika G:", self.matrix_g_var)

        params_frame = ttk.LabelFrame(outer, text="3. Parametri iskanja", padding=12)
        params_frame.pack(fill="x", pady=(0, 12))

        form = ttk.Frame(params_frame)
        form.pack(fill="x")

        ttk.Label(form, text="k:", width=18).grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(form, textvariable=self.k_var, width=20).grid(row=0, column=1, sticky="w", pady=4)

        ttk.Label(form, text="Meja kosinusa:", width=18).grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(form, textvariable=self.cosine_var, width=20).grid(row=1, column=1, sticky="w", pady=4)

        ttk.Label(form, text="Iskalni niz:", width=18).grid(row=2, column=0, sticky="w", pady=4)
        ttk.Entry(form, textvariable=self.query_var, width=60).grid(row=2, column=1, sticky="we", pady=4)
        form.columnconfigure(1, weight=1)

        actions = ttk.Frame(outer)
        actions.pack(fill="x", pady=(0, 12))
        ttk.Button(actions, text="Zaženi iskanje", command=self._search).pack(side="left")

        results_frame = ttk.LabelFrame(outer, text="4. Rezultati", padding=12)
        results_frame.pack(fill="both", expand=True)

        self.output = tk.Text(results_frame, wrap="word", height=18)
        self.output.pack(fill="both", expand=True)

    def _build_matrix_row(self, parent: ttk.Frame, label: str, variable: tk.StringVar) -> None:
        row = ttk.Frame(parent)
        row.pack(fill="x", pady=4)
        ttk.Label(row, text=label, width=18).pack(side="left")
        ttk.Entry(row, textvariable=variable).pack(side="left", fill="x", expand=True)
        ttk.Button(row, text="Prebrskaj", command=lambda v=variable: self._pick_file(v)).pack(side="left", padx=(8, 0))

    def _pick_file(self, variable: tk.StringVar) -> None:
        path = filedialog.askopenfilename()
        if path:
            variable.set(path)

    def _add_folder(self) -> None:
        folder = filedialog.askdirectory()
        if not folder:
            return

        self.folder_path = folder
        self.folder_label.config(text=f"Izbrana mapa: {folder}")

        self.docs_list.delete(0, tk.END)
        txt_files = sorted(Path(folder).glob("*.txt"))

        for path in txt_files:
            self.docs_list.insert(tk.END, str(path))

        if not txt_files:
            messagebox.showinfo("Mapa", "V izbrani mapi ni .txt dokumentov.")

    def _clear_folder(self) -> None:
        self.folder_path = ""
        self.folder_label.config(text="Ni izbrane mape.")
        self.docs_list.delete(0, tk.END)

    def _toggle_matrix_fields(self) -> None:
        state = "disabled"
        for child in self.matrices_frame.winfo_children():
            self._set_widget_state_recursive(child, state)

    def _set_widget_state_recursive(self, widget: tk.Widget, state: str) -> None:
        try:
            widget.configure(state=state)
        except tk.TclError:
            pass
        for child in widget.winfo_children():
            self._set_widget_state_recursive(child, state)

    def _validate(self) -> bool:
        if not self.folder_path:
            messagebox.showerror("Napaka", "Najprej izberi mapo z dokumenti.")
            return False

        txt_files = list(Path(self.folder_path).glob("*.txt"))
        if not txt_files:
            messagebox.showerror("Napaka", "V izbrani mapi ni .txt dokumentov.")
            return False

        try:
            k = int(self.k_var.get())
            if k <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Napaka", "Vrednost k mora biti pozitivno celo število.")
            return False

        try:
            cosine = float(self.cosine_var.get())
            if not (0 <= cosine <= 1):
                raise ValueError
        except ValueError:
            messagebox.showerror("Napaka", "Meja kosinusa mora biti med 0 in 1.")
            return False

        if not self.query_var.get().strip():
            messagebox.showerror("Napaka", "Vnesi iskalni niz.")
            return False

        return True

    def _search(self) -> None:
        if not self._validate():
            return

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "Zaganjam iskanje...\n\n")
        self.root.update_idletasks()

        try:
            result = run_search(
                folder_path=self.folder_path,
                weighted=self.weighted_var.get(),
                has_existing_matrices=self.has_existing_matrices_var.get(),
                matrix_paths={
                    "A": self.matrix_a_var.get().strip(),
                    "S": self.matrix_s_var.get().strip(),
                    "G": self.matrix_g_var.get().strip(),
                },
                k=int(self.k_var.get()),
                cosine_threshold=float(self.cosine_var.get()),
                query=self.query_var.get().strip(),
            )
        except Exception as exc:
            self.output.insert(tk.END, f"Napaka pri iskanju:\n{exc}\n")
            return

        rezultati = result.get("rezultati", [])

        if not rezultati:
            self.output.insert(tk.END, "Ni zadetkov.\n")
            return

        self.output.insert(tk.END, "Najbolj relevantni dokumenti:\n\n")
        for i, item in enumerate(rezultati, start=1):
            indeks = item.get("indeks", "?")
            datoteka = item.get("datoteka", "neznana datoteka")
            self.output.insert(tk.END, f"{i}. dokument #{indeks}: {datoteka}\n")


def main() -> None:
    root = tk.Tk()
    try:
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
    except tk.TclError:
        pass
    DocumentSearchApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()