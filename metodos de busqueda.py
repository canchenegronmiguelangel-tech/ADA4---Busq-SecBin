"""
Unidad 5 - Métodos de Ordenamiento y Búsqueda
Programa con menú gráfico (tkinter) que ejecuta 3 métodos de búsqueda:
  1. Secuencial   2. Binaria   3. Hash
Un solo archivo. Requiere solo Python 3 (tkinter viene incluido).
"""

import random
import tkinter as tk
from tkinter import ttk, messagebox

# ----------------------------------------------------------------------
#  Colores de la animación
# ----------------------------------------------------------------------
BASE, REVISANDO, DESCARTADO, RANGO, ENCONTRADO = (
    "#ffffff", "#ffd54f", "#cfcfcf", "#bbdefb", "#81c784")


# ----------------------------------------------------------------------
#  Algoritmos (devuelven los pasos para poder animarlos)
# ----------------------------------------------------------------------
def pasos_secuencial(datos, objetivo):
    """Devuelve (indice, lista de (colores, mensaje))."""
    n, frames = len(datos), []
    for i, valor in enumerate(datos):
        colores = [DESCARTADO] * i + [REVISANDO] + [BASE] * (n - i - 1)
        msg = f"Comparación {i + 1}: ¿{valor} == {objetivo}?"
        if valor == objetivo:
            colores[i] = ENCONTRADO
            frames.append((colores, msg + "  ¡Sí! Encontrado."))
            return i, frames
        frames.append((colores, msg + "  No."))
    return -1, frames


def pasos_binaria(datos, objetivo):
    """Lista ya ordenada. Devuelve (indice, lista de (colores, mensaje))."""
    n, frames = len(datos), []
    inicio, fin, comps = 0, n - 1, 0
    while inicio <= fin:
        medio = (inicio + fin) // 2
        comps += 1
        colores = [DESCARTADO] * n
        for k in range(inicio, fin + 1):
            colores[k] = RANGO
        colores[medio] = REVISANDO
        msg = (f"Comparación {comps}: rango [{inicio}..{fin}], medio = {medio} "
               f"(valor {datos[medio]}).")
        if datos[medio] == objetivo:
            colores[medio] = ENCONTRADO
            frames.append((colores, msg + "  ¡Encontrado!"))
            return medio, frames
        if datos[medio] < objetivo:
            msg += f"  {datos[medio]} < {objetivo}: descarto la izquierda."
            inicio = medio + 1
        else:
            msg += f"  {datos[medio]} > {objetivo}: descarto la derecha."
            fin = medio - 1
        frames.append((colores, msg))
    return -1, frames


class TablaHash:
    """Tabla hash con encadenamiento para resolver colisiones."""

    def __init__(self, tamano=10):
        self.tamano = tamano
        self.tabla = [[] for _ in range(tamano)]

    def funcion_hash(self, clave):
        return clave % self.tamano

    def insertar(self, clave, valor):
        cubeta = self.tabla[self.funcion_hash(clave)]
        for par in cubeta:
            if par[0] == clave:
                par[1] = valor
                return
        cubeta.append([clave, valor])

    def buscar(self, clave):
        """Devuelve (valor o None, indice de cubeta, posición en la cubeta)."""
        idx = self.funcion_hash(clave)
        for pos, (k, v) in enumerate(self.tabla[idx]):
            if k == clave:
                return v, idx, pos
        return None, idx, -1


# ----------------------------------------------------------------------
#  Pestaña para búsqueda secuencial y binaria
# ----------------------------------------------------------------------
class TabLista(ttk.Frame):
    def __init__(self, master, binaria):
        super().__init__(master, padding=10)
        self.binaria = binaria
        self.datos = []
        self.job = None

        texto = ("Divide la lista a la mitad en cada paso. La lista se ordena "
                 "automáticamente." if binaria else
                 "Recorre la lista elemento por elemento hasta encontrar el valor.")
        ttk.Label(self, text=texto, wraplength=860).pack(anchor="w")

        f1 = ttk.Frame(self)
        f1.pack(fill="x", pady=8)
        ttk.Label(f1, text="Lista (separada por comas):").pack(side="left")
        self.var_lista = tk.StringVar(value="45, 12, 78, 33, 5, 90, 21, 67, 3, 54")
        ttk.Entry(f1, textvariable=self.var_lista, width=48).pack(side="left", padx=6)
        ttk.Button(f1, text="Aleatoria", command=self.aleatoria).pack(side="left")

        f2 = ttk.Frame(self)
        f2.pack(fill="x")
        ttk.Label(f2, text="Número a buscar:").pack(side="left")
        self.var_obj = tk.StringVar()
        e = ttk.Entry(f2, textvariable=self.var_obj, width=10)
        e.pack(side="left", padx=6)
        e.bind("<Return>", lambda ev: self.buscar())
        ttk.Button(f2, text="Buscar", command=self.buscar).pack(side="left")

        self.canvas = tk.Canvas(self, height=90, bg="white", highlightthickness=1,
                                highlightbackground="#999")
        self.canvas.pack(fill="x", pady=12)

        self.lbl_res = ttk.Label(self, text="", font=("Segoe UI", 11, "bold"))
        self.lbl_res.pack(anchor="w")

        self.log = tk.Text(self, height=9, state="disabled", wrap="word")
        self.log.pack(fill="both", expand=True, pady=(6, 0))

        self.leer_datos(mostrar_error=False)

    # -- utilidades ------------------------------------------------------
    def aleatoria(self):
        nums = random.sample(range(1, 100), 12)
        self.var_lista.set(", ".join(map(str, nums)))
        self.leer_datos()

    def leer_datos(self, mostrar_error=True):
        try:
            nums = [int(x) for x in self.var_lista.get().replace(",", " ").split()]
            if not nums or len(nums) > 20:
                raise ValueError
        except ValueError:
            if mostrar_error:
                messagebox.showerror("Error", "Escribe de 1 a 20 números enteros "
                                              "separados por comas.")
            return False
        if self.binaria:
            nums.sort()
            self.var_lista.set(", ".join(map(str, nums)))
        self.datos = nums
        self.dibujar([BASE] * len(nums))
        return True

    def dibujar(self, colores):
        self.canvas.delete("all")
        w, x0 = 44, 10
        for i, (v, c) in enumerate(zip(self.datos, colores)):
            x = x0 + i * (w + 4)
            self.canvas.create_rectangle(x, 12, x + w, 56, fill=c, outline="black")
            self.canvas.create_text(x + w / 2, 34, text=str(v), fill="black",
                                    font=("Segoe UI", 11, "bold"))
            self.canvas.create_text(x + w / 2, 70, text=str(i), fill="#555")

    def escribir(self, texto, limpiar=False):
        self.log.config(state="normal")
        if limpiar:
            self.log.delete("1.0", "end")
        self.log.insert("end", texto + "\n")
        self.log.see("end")
        self.log.config(state="disabled")

    # -- búsqueda --------------------------------------------------------
    def buscar(self):
        if self.job:
            self.after_cancel(self.job)
            self.job = None
        if not self.leer_datos():
            return
        try:
            objetivo = int(self.var_obj.get())
        except ValueError:
            messagebox.showerror("Error", "El número a buscar debe ser entero.")
            return
        funcion = pasos_binaria if self.binaria else pasos_secuencial
        idx, frames = funcion(self.datos, objetivo)
        self.lbl_res.config(text="Buscando...")
        self.escribir("", limpiar=True)
        self.animar(frames, 0, idx, objetivo)

    def animar(self, frames, i, idx, objetivo):
        if i < len(frames):
            colores, msg = frames[i]
            self.dibujar(colores)
            self.escribir(msg)
            self.job = self.after(800, self.animar, frames, i + 1, idx, objetivo)
            return
        self.job = None
        if idx == -1:
            self.dibujar([DESCARTADO] * len(self.datos))
            self.lbl_res.config(text=f"{objetivo} NO está en la lista "
                                     f"({len(frames)} comparaciones).")
        else:
            self.lbl_res.config(text=f"{objetivo} encontrado en la posición {idx} "
                                     f"({len(frames)} comparaciones).")


# ----------------------------------------------------------------------
#  Pestaña para búsqueda hash
# ----------------------------------------------------------------------
class TabHash(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self.tabla = TablaHash(10)
        for mat, nom in {101: "Ana", 205: "Luis", 312: "María", 415: "Pedro",
                         520: "Sofía", 633: "Carlos", 741: "Elena", 855: "Jorge"}.items():
            self.tabla.insertar(mat, nom)

        ttk.Label(self, text="Tabla hash de 10 cubetas (matrícula → nombre). "
                  "Función hash: matrícula % 10. Las colisiones se guardan "
                  "en la misma cubeta.", wraplength=860).pack(anchor="w")

        f1 = ttk.Frame(self)
        f1.pack(fill="x", pady=8)
        ttk.Label(f1, text="Matrícula:").pack(side="left")
        self.var_mat = tk.StringVar()
        ttk.Entry(f1, textvariable=self.var_mat, width=8).pack(side="left", padx=4)
        ttk.Label(f1, text="Nombre:").pack(side="left")
        self.var_nom = tk.StringVar()
        ttk.Entry(f1, textvariable=self.var_nom, width=14).pack(side="left", padx=4)
        ttk.Button(f1, text="Insertar", command=self.insertar).pack(side="left")

        f2 = ttk.Frame(self)
        f2.pack(fill="x")
        ttk.Label(f2, text="Matrícula a buscar:").pack(side="left")
        self.var_obj = tk.StringVar()
        e = ttk.Entry(f2, textvariable=self.var_obj, width=10)
        e.pack(side="left", padx=6)
        e.bind("<Return>", lambda ev: self.buscar())
        ttk.Button(f2, text="Buscar", command=self.buscar).pack(side="left")

        self.tree = ttk.Treeview(self, columns=("cubeta", "contenido"),
                                 show="headings", height=10)
        self.tree.heading("cubeta", text="Cubeta")
        self.tree.heading("contenido", text="Contenido (matrícula: nombre)")
        self.tree.column("cubeta", width=80, anchor="center")
        self.tree.column("contenido", width=700)
        self.tree.tag_configure("hallado", background=ENCONTRADO)
        self.tree.pack(fill="x", pady=10)

        self.lbl_res = ttk.Label(self, text="", font=("Segoe UI", 11, "bold"),
                                 wraplength=860)
        self.lbl_res.pack(anchor="w")
        self.refrescar()

    def refrescar(self, resaltar=None):
        self.tree.delete(*self.tree.get_children())
        for i, cubeta in enumerate(self.tabla.tabla):
            txt = "   |   ".join(f"{k}: {v}" for k, v in cubeta) or "(vacía)"
            self.tree.insert("", "end", iid=str(i), values=(i, txt),
                             tags=("hallado",) if i == resaltar else ())

    def leer_int(self, texto):
        try:
            return int(texto)
        except ValueError:
            messagebox.showerror("Error", "La matrícula debe ser un número entero.")
            return None

    def insertar(self):
        mat = self.leer_int(self.var_mat.get())
        if mat is None:
            return
        nombre = self.var_nom.get().strip()
        if not nombre:
            messagebox.showerror("Error", "Escribe un nombre.")
            return
        self.tabla.insertar(mat, nombre)
        idx = self.tabla.funcion_hash(mat)
        self.lbl_res.config(text=f"Insertado en la cubeta {idx}  ({mat} % 10 = {idx}).")
        self.refrescar(idx)

    def buscar(self):
        mat = self.leer_int(self.var_obj.get())
        if mat is None:
            return
        nombre, idx, pos = self.tabla.buscar(mat)
        calculo = f"hash({mat}) = {mat} % 10 = {idx}.  "
        if nombre is not None:
            self.lbl_res.config(text=calculo + f"Encontrado: {nombre} "
                                f"(cubeta {idx}, posición {pos + 1} de la cubeta).")
            self.refrescar(idx)
        else:
            self.lbl_res.config(text=calculo + f"No se encontró la matrícula {mat}.")
            self.refrescar()


# ----------------------------------------------------------------------
#  Ventana principal con menú gráfico
# ----------------------------------------------------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Unidad 5 - Métodos de Búsqueda")
        self.geometry("920x620")
        self.minsize(820, 560)

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=6, pady=6)
        self.nb.add(TabLista(self.nb, binaria=False), text="  1. Secuencial  ")
        self.nb.add(TabLista(self.nb, binaria=True), text="  2. Binaria  ")
        self.nb.add(TabHash(self.nb), text="  3. Hash  ")

        barra = tk.Menu(self)
        m_bus = tk.Menu(barra, tearoff=0)
        m_bus.add_command(label="Búsqueda secuencial", command=lambda: self.nb.select(0))
        m_bus.add_command(label="Búsqueda binaria", command=lambda: self.nb.select(1))
        m_bus.add_command(label="Búsqueda hash", command=lambda: self.nb.select(2))
        m_bus.add_separator()
        m_bus.add_command(label="Salir", command=self.destroy)
        barra.add_cascade(label="Búsqueda", menu=m_bus)

        m_ayuda = tk.Menu(barra, tearoff=0)
        m_ayuda.add_command(label="Acerca de", command=lambda: messagebox.showinfo(
            "Acerca de", "Unidad 5 - Métodos de Ordenamiento y Búsqueda\n"
                         "Secuencial, Binaria y Hash en Python (tkinter)."))
        barra.add_cascade(label="Ayuda", menu=m_ayuda)
        self.config(menu=barra)


if __name__ == "__main__":
    App().mainloop()