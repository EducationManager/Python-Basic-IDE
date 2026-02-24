#Este Ide lo hice con el propósito de aprendizaje y proyectos reales, me pasare a PySide Pronto, aprendiendo POO de tkinter y demás#
#Gracias por ver mi proyecto, no olvides arreglar algunos bugs que veas por ahi, Suerte!
# esta basado en tkinter, pero me olvide de agregar que en def de savefile no solo llame al filedialog. xd, use una ia de agente para arreglar algunos problemas y de paso 
# evitar cosas reptitivas eh inecesarias (NO VIBECODING)#

from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext, ttk
import os
from tkinter import filedialog, messagebox, font
import tkinter as tk
import keyword
import re

root = Tk()
root.title("PySimpleIDE")
root.geometry("800x600")

icon_path = os.path.join(os.path.dirname(__file__), "LOGO.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)
# Clase para los números 
menubar = Menu(root)

root.config(menu=menubar)


text = scrolledtext.ScrolledText(root, width=70, height=50, font=("Cascadia Code", 12, "italic bold"), undo=True)
text.pack(expand=True, fill='both')


print("This is a Console, here showing for you a resolts from you python program")

def openfile():
    file = filedialog.askopenfilename(title="Open Python File", filetypes=[("Python File", "*.py"), ("All Files", "*.*")] )
    if file:
        with open(file, "r") as f:
            text.delete(1.0, END)   
            text.insert(1.0, f.read())
def savefile():
    file = filedialog.asksaveasfilename(title="Python Files", filetypes=[("Python File", "*.py"), ("All Files", "*.*")] )
    if file:
        with open(file, "w") as f:
            f.write(text.get(1.0, END))
def copy():
    text.clipboard_clear()
    text.clipboard_append(text.get(1.0, END))
def cut():
    text.clipboard_clear()
    text.clipboard_append(text.get(1.0, END))
    text.delete(1.0, END)
def paste():
    text.insert(1.0, text.clipboard_get())
def color():
    text.config(bg="#1e1e1e", fg="white", insertbackground="white")
def clickderecho(event):
    menu_contextual = Menu(root, tearoff=0)
    menu_contextual.add_command(label="Copy", command=copy)
    menu_contextual.add_command(label="Cut", command=cut)
    menu_contextual.add_command(label="Paste", command=paste)
    menu_contextual.tk_popup(event.x_root, event.y_root)

text.bind("<Button-3>", clickderecho)


search_window = None

def find_text(event=None):
    global search_window
    
    if search_window and search_window.winfo_exists():
        search_window.focus()
        return

    search_window = tk.Toplevel(root)
    search_window.title("Buscar")
    search_window.geometry("300x60")
    search_window.resizable(False, False)
    search_window.transient(root)

    tk.Label(search_window, text="Buscar:").pack(side="left", padx=5)

    entry = tk.Entry(search_window, width=25)
    entry.pack(side="left", padx=5)
    entry.focus()

    def search_next(event=None):
        text.tag_remove("search", "1.0", "end")

        word = entry.get()
        if not word:
            return

        start_pos = text.search(word, text.index("insert"), stopindex="end")

        if not start_pos:
            start_pos = text.search(word, "1.0", stopindex="end")
            if not start_pos:
                return

        end_pos = f"{start_pos}+{len(word)}c"

        text.tag_add("search", start_pos, end_pos)
        text.tag_config("search", background="yellow", foreground="black")

        text.mark_set("insert", end_pos)
        text.see(start_pos)

    entry.bind("<Return>", search_next)

    search_window.bind("<Escape>", lambda e: search_window.destroy())
frame = Frame(root)
frame.pack(fill="both", expand=True)

line_numbers = Text(frame, width=4, padx=5, takefocus=0, border=0,
                    background="#1e1e1e", foreground="gray",
                    state="disabled")

line_numbers.pack(side="left", fill="y")
# Atajo teclado
root.bind("<Control-f>", find_text)
def changelanguage():
    if messagebox.askyesno("Language", "Do you want to change the language to Spanish?"):
        messagebox.showinfo("Language", "El lenguaje ha sido cambiado al español!")
        root.title("Python Editor de Texto")
        file.entryconfig(0, label="Archivo")
        file.entryconfig(1, label="Guardar")
        file.entryconfig(2, label="Salir")
        edit.entryconfig(0, label="Copiar")
        edit.entryconfig(1, label="Cortar")
        edit.entryconfig(2, label="Pegar")
        run_menu.entryconfig(0, label="Ejecutar")
        config.entryconfig(0, label="Cambiar Color")
        config.entryconfig(1, label="Idioma")

    else:
        messagebox.showinfo("Language", "The language has not been changed")
text.tag_config("keyword", foreground="#680094")   # azul
text.tag_config("string", foreground="#CE9178")    # naranja
text.tag_config("comment", foreground="#6A9955")   # verde
text.tag_config("brackets", foreground="#164494")  # amarillo


def completions(event):
    
    texto = text.get(1.0, END)
    if event.char == "(":
        text.insert("insert", ")")
        text.mark_set("insert", "insert-1c")
    if event.char == '"':
        text.insert("insert", '"')
        text.mark_set("insert", "insert-1c")
    if event.char == "'":
        text.insert("insert", "'")
        text.mark_set("insert", "insert-1c")
    if event.char == "[":
        text.insert("insert", "]")
        text.mark_set("insert", "insert-1c")
    if event.char == "{":
        text.insert("insert", "}")
        text.mark_set("insert", "insert-1c")
    if event.char == "<":
        text.insert("insert", ">")
        text.mark_set("insert", "insert-1c")
def completionstwo(event):
    line_start = text.index("insert linestart")
    line_end = text.index("insert lineend")
    line = text.get(line_start, line_end)

    for tag in ["keyword", "string", "comment", "brackets"]:
        text.tag_remove(tag, line_start, line_end)

    # keywords
    keywords = ["import", "def", "class", "return", "if", "else", "elif", "for", "while"]
    for word in keywords:
        idx = line.find(word)
        if idx != -1:
            start = f"{line_start}+{idx}c"
            end = f"{start}+{len(word)}c"
            text.tag_add("keyword", start, end)

    # strings
    inside_string = False
    string_start = None
    for i, char in enumerate(line):
        if char in ['"', "'"]:
            if not inside_string:
                inside_string = True
                string_start = i
            else:
                start = f"{line_start}+{string_start}c"
                end = f"{line_start}+{i+1}c"
                text.tag_add("string", start, end)
                inside_string = False

    if "#" in line:
        idx = line.index("#")
        start = f"{line_start}+{idx}c"
        text.tag_add("comment", start, line_end)

    # paréntesis y llaves
    for i, char in enumerate(line):
        if char in "(){}[]":
            pos = f"{line_start}+{i}c"
            text.tag_add("brackets", pos, f"{pos}+1c")
    # No autocompletar si es tecla de borrado XD
    if event.keysym in ["BackSpace", "Delete"]:
        return

    # Solo autocompletar si no estamos seleccionando :V
    try:
        sel_start = text.index("sel.first")
        sel_end = text.index("sel.last")
        if sel_start != sel_end:
            return
    except tk.TclError:
        pass  # No selection, sigue

    # Solo autocompletar si no hay Ctrl/Alt/Meta
    if (event.state & 0x4) or (event.state & 0x8):
        return

    cursor_pos = text.index("insert")

    # Para cada clave, revisa los requisitos y completa si aplica
    # Clave: (lo que debe estar antes del cursor, lo que se insertará)
    completions = [
        ("impo", "rt"),
        ("def", ""),
        ("de", "f"),
        ("tkin", "ter"),
        ("pysi", "side6"),
        ("text=", '""'),
        ("customtk", "inter"),
        ("pri", 'nt("")')
    ]

    # Para evitar problema con over-autocomplete, chequea de mayor a menor
    maxlen = max(len(k) for k, v in completions)
    prev_chars = text.get(f"{cursor_pos} -{maxlen}c", cursor_pos)

    for before, completion in completions:
        if prev_chars.endswith(before):
            # Checa si no estamos dentro de una cadena (no autocomplete en strings)
            curr_tags = text.tag_names(cursor_pos)
            if "string" in curr_tags or "comment" in curr_tags:
                return
            # Si el completion inserta paréntesis/cadena, coloca el cursor dentro donde corresponde
            if before == "pri" and completion == 'nt("")':
                text.insert("insert", completion)
                text.mark_set("insert", f"{cursor_pos}+4c") # Entre las comillas
            elif before == "text=" and completion == '""':
                text.insert("insert", completion)
                text.mark_set("insert", f"{cursor_pos}+1c") # Entre las comillas
            else:
                text.insert("insert", completion)
            break
text.bind("<KeyRelease>", completionstwo)
def run():
    
    code = text.get("1.0", "end-1c")
    try:
        exec(code)
    except Exception as e:
        messagebox.showerror("Error in you code", str(e))
def config():
    config = Tk()
    config.title("PyIDE Configure")
    config.mainloop()
text.bind("<Key>", completions)
file = Menu(menubar, tearoff=0)
def newfile():
    textox = text.get("1.0", END).strip()
    if textox:
        respuesta = messagebox.askquestion("Confirmar", "¿Seguro quieres crear otro archivo de texto?")
        if respuesta == "yes":
            text.delete("1.0", END)
        else:
            return
    else:
        text.delete("1.0", END)
#Menu bars simples 
menubar.add_cascade(label="File", menu=file)
file.add_command(label="New File", command=newfile)
file.add_command(label="Open", command=openfile)
file.add_command(label="Save", command=savefile)
file.add_separator()
file.add_command(label="Exit", command=root.quit)

edit = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=edit)
edit.add_command(label="Copy", command=copy)
edit.add_command(label="Cut", command=cut)
edit.add_command(label="Paste", command=paste)

run_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Run(F5)", menu=run_menu)
run_menu.add_command(label="Run", command=run)

root.bind("<F5>", run())
config = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Configure", menu=config)
config.add_command(label="Change Color", command=color)
config.add_command(label="Language", command=changelanguage)
config.add_command(label="More...", command=config)
root.config(menu=menubar)

programmer = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Programming language", menu=programmer)
programmer.add_command(label="Python", command= None)
programmer.add_command(label="C", command=None)
programmer.add_command(label="JavaScript", command=None)



help = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=help)
help.add_command(label="About", command=lambda: messagebox.showinfo("About", "PyIDE for Low PC, This IDE was made completely by me, to use it properly you must analyze its main functions. It has 5 menus, the first is File, Edit, Run Configure, each of them has its own functions such as copy, cut or paste, open files, save, create etc. If you want more information, go to my GitHub! "))


def run():
    exec(text.get(1.0, END))

lambda e: text.edit_redo()
root.bind("<Control-s>", lambda e: savefile())
root.bind("<Control-o>", lambda e: openfile())
root.bind("<Control-x>", lambda e: cut())
root.bind("<Control-v>", lambda e: paste())
root.bind("<Key-Release>", )
root.bind("<F5>", lambda e: run())
root.mainloop()

#----- FIN DEL IDE -----#
