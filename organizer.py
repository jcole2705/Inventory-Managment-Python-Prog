from tkinter import *
from tkinter import messagebox, filedialog
from pathlib import Path
import re
import shutil

# =========================================================
# COLORS
# =========================================================
BG = "#0b0b0b"
PANEL = "#111111"
PANEL_2 = "#101010"
RED = "#ff2a2a"
GRAY = "#b0b0b0"


# =========================================================
# DATA
# =========================================================
base_folder = None
serial_folder = None
selected_files = []


# =========================================================
# CLEAN
# =========================================================
def clean(text):
    text = text.strip()
    text = re.sub(r'[\\/:*?"<>|]', "_", text)
    return text


# =========================================================
# FILE SELECT
# =========================================================
def select_files():
    global selected_files

    files = filedialog.askopenfilenames(title="Select files")

    if files:
        selected_files = list(files)

        output_box.insert(END, "\nFILES SELECTED\n")
        for f in selected_files:
            output_box.insert(END, f"{f}\n")


# =========================================================
# TRANSFER
# =========================================================
def transfer_files():
    if not selected_files:
        messagebox.showwarning("Error", "No files selected")
        return

    if serial_folder is None:
        messagebox.showwarning("Error", "No target folder selected")
        return

    output_box.insert(END, "\nTRANSFER STARTED\n")

    for f in selected_files:
        try:
            dest = serial_folder / Path(f).name
            shutil.copy2(f, dest)
            output_box.insert(END, f"SENT -> {dest}\n")
        except Exception as e:
            output_box.insert(END, f"ERROR -> {e}\n")

    output_box.insert(END, "TRANSFER COMPLETE\n")


# =========================================================
# FOLDERS
# =========================================================
def select_main_folder():
    global base_folder
    folder = filedialog.askdirectory()

    if folder:
        base_folder = Path(folder)
        main_folder_label.config(text=f"MAIN: {base_folder}")


def select_serial_folder():
    global serial_folder
    folder = filedialog.askdirectory()

    if folder:
        serial_folder = Path(folder)
        serial_folder_label.config(text=f"TARGET: {serial_folder}")


# =========================================================
# INVENTORY
# =========================================================
def create_inventory():
    if base_folder is None:
        messagebox.showwarning("Error", "Select main folder first")
        return

    serials = [clean(s) for s in serial_entry.get("1.0", END).splitlines() if s.strip()]
    names = [clean(n) for n in name_entry.get("1.0", END).splitlines()]
    models = [clean(m) for m in model_entry.get("1.0", END).splitlines()]

    output_box.delete("1.0", END)

    if not serials:
        return

    surplus = surplus_var.get()
    located = located_var.get()
    instock = instock_var.get()

    if not (surplus or located or instock):
        messagebox.showwarning("Error", "Select a mode")
        return


    # ---------------- SURPLUS ----------------
    if surplus:
        while len(models) < len(serials):
            models.append("Unknown")

        for i, s in enumerate(serials):
            folder = base_folder / s
            folder.mkdir(parents=True, exist_ok=True)

            (folder / "info.txt").write_text(
                f"Serial: {s}\nModel: {models[i]}\nStatus: Surplus"
            )

            output_box.insert(END, f"SURPLUS -> {s}\n")


    # ---------------- LOCATED ----------------
    if located:
        while len(names) < len(serials):
            names.append("Unknown")
        while len(models) < len(serials):
            models.append("Unknown")

        for i, s in enumerate(serials):
            folder = base_folder / s
            folder.mkdir(parents=True, exist_ok=True)

            (folder / "info.txt").write_text(
                f"Serial: {s}\nName: {names[i]}\nModel: {models[i]}\nStatus: Located"
            )

            output_box.insert(END, f"LOCATED -> {s}\n")


    # ---------------- IN STOCK ----------------
    if instock:
        while len(models) < len(serials):
            models.append("Unknown")

        for i, s in enumerate(serials):
            folder = base_folder / s
            folder.mkdir(parents=True, exist_ok=True)

            (folder / "info.txt").write_text(
                f"Serial: {s}\nModel: {models[i]}\nStatus: In Stock"
            )

            output_box.insert(END, f"IN STOCK -> {s}\n")

    output_box.insert(END, "\nDONE\n")


# =========================================================
# UI
# =========================================================
root = Tk()
root.title("Inventory Control System")
root.geometry("1200x850")
root.configure(bg=BG)


# =========================================================
# TITLE
# =========================================================
title_frame = Frame(root, bg=PANEL_2, relief=RAISED, bd=3)
title_frame.pack(fill=X, padx=10, pady=10)

Label(
    title_frame,
    text="INVENTORY CONTROL SYSTEM",
    font=("Helvetica", 20, "bold"),
    bg=PANEL_2,
    fg=RED
).pack(pady=5)


# =========================================================
# LEFT: INVENTORY PANEL
# =========================================================
inventory_outer = Frame(root, bg=PANEL, relief=RIDGE, bd=3)
inventory_outer.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

inventory_panel = Frame(inventory_outer, bg=PANEL_2, relief=SUNKEN, bd=3)
inventory_panel.pack(fill=BOTH, expand=True)


Label(
    inventory_panel,
    text="INVENTORY PANEL",
    bg=PANEL_2,
    fg=RED,
    font=("Helvetica", 13, "bold")
).pack(pady=5)


# ---------------- FOLDERS ----------------
main_folder_label = Label(inventory_panel, text="MAIN: NONE", bg=PANEL_2, fg="white")
main_folder_label.pack()

Button(
    inventory_panel,
    text="Select Main Folder",
    command=select_main_folder,
    bg="#1e1e1e",
    fg="white",
    relief=RAISED,
    bd=2
).pack(pady=5)


# =========================================================
# INPUTS (CENTERED FIXED)
# =========================================================
input_frame = Frame(inventory_panel, bg=PANEL_2)
input_frame.pack(pady=10)

header = Frame(input_frame, bg=PANEL_2)
header.pack(fill=X)

Label(header, text="SERIALS", bg=PANEL_2, fg=GRAY, width=25).pack(side=LEFT, expand=True)
Label(header, text="NAMES", bg=PANEL_2, fg=GRAY, width=25).pack(side=LEFT, expand=True)
Label(header, text="MODELS", bg=PANEL_2, fg=GRAY, width=25).pack(side=LEFT, expand=True)

box_row = Frame(input_frame, bg=PANEL_2)
box_row.pack(fill=X)

serial_entry = Text(box_row, width=25, height=6, bg="#0d0d0d", fg=GRAY, insertbackground=GRAY)
serial_entry.pack(side=LEFT, expand=True, padx=5)

name_entry = Text(box_row, width=25, height=6, bg="#0d0d0d", fg=GRAY, insertbackground=GRAY)
name_entry.pack(side=LEFT, expand=True, padx=5)

model_entry = Text(box_row, width=25, height=6, bg="#0d0d0d", fg=GRAY, insertbackground=GRAY)
model_entry.pack(side=LEFT, expand=True, padx=5)


# =========================================================
# CHECKBOXES
# =========================================================
options = Frame(inventory_panel, bg=PANEL_2)
options.pack(pady=10)

surplus_var = BooleanVar()
located_var = BooleanVar()
instock_var = BooleanVar()

def cb(text, var):
    return Checkbutton(
        options,
        text=text,
        variable=var,
        bg=PANEL_2,
        fg="white",
        selectcolor=RED
    )

cb("SURPLUS", surplus_var).pack(side=LEFT, padx=10)
cb("LOCATED", located_var).pack(side=LEFT, padx=10)
cb("IN STOCK", instock_var).pack(side=LEFT, padx=10)


Button(
    inventory_panel,
    text="EXECUTE INVENTORY",
    command=create_inventory,
    bg=RED,
    fg="black",
    relief=RAISED,
    bd=3,
    font=("Helvetica", 11, "bold")
).pack(pady=10)


# =========================================================
# OUTPUT
# =========================================================
Label(
    inventory_panel,
    text="OUTPUT CONSOLE",
    bg=PANEL_2,
    fg=RED
).pack()

output_frame = Frame(inventory_panel, bg=BG, relief=SUNKEN, bd=3)
output_frame.pack(fill=BOTH, expand=True, pady=10)

scroll = Scrollbar(output_frame)
scroll.pack(side=RIGHT, fill=Y)

output_box = Text(
    output_frame,
    bg=BG,
    fg="white",
    insertbackground="white",
    yscrollcommand=scroll.set
)
output_box.pack(fill=BOTH, expand=True)

scroll.config(command=output_box.yview)


# =========================================================
# RIGHT: TRANSFER PANEL
# =========================================================
transfer_outer = Frame(root, bg=PANEL, relief=RIDGE, bd=3)
transfer_outer.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

transfer_panel = Frame(transfer_outer, bg=PANEL_2, relief=SUNKEN, bd=3)
transfer_panel.pack(fill=BOTH, expand=True)

Label(
    transfer_panel,
    text="TRANSFER PANEL",
    bg=PANEL_2,
    fg=RED,
    font=("Helvetica", 13, "bold")
).pack(pady=5)


serial_folder_label = Label(transfer_panel, text="TARGET: NONE", bg=PANEL_2, fg="white")
serial_folder_label.pack()

Button(
    transfer_panel,
    text="Select Target Folder",
    command=select_serial_folder,
    bg="#1e1e1e",
    fg="white"
).pack(pady=5)

Button(
    transfer_panel,
    text="Select Files",
    command=select_files,
    bg="#2a2a2a",
    fg="white"
).pack(pady=5)

Button(
    transfer_panel,
    text="TRANSFER FILES",
    command=transfer_files,
    bg=RED,
    fg="black",
    font=("Helvetica", 10, "bold"),
    relief=RAISED,
    bd=3
).pack(pady=10)


root.mainloop()