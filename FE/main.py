import requests
import tkinter as tk
from tkinter import ttk, messagebox


BASE_URL = "https://biblioteca-ads.onrender.com"
TOKEN ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZW1haWwiOiJhZG1pbkBiaWJsaW90ZWNhLmNvbSIsInJvbCI6ImFkbWluIiwiaWF0IjoxNzY0MTI3NDg5LCJleHAiOjE3NjQxMzQ2ODl9.OtEo7p7y_rWOGANyMLACyw1FvRk03q4nEP5PqFNV6m4"
# ------------------------------
# Funciones de acceso a la API
# ------------------------------

def api_get_libros():
    url = f"{BASE_URL}/libros"
    r = requests.get(url, timeout=5)
    r.raise_for_status()
    return r.json()

def api_get_libro_por_isbn(isbn):
    url = f"{BASE_URL}/libros/{isbn}"
    r = requests.get(url, timeout=5)
    r.raise_for_status()
    return r.json()

def api_crear_libro(data):
    url = f"{BASE_URL}/libros"
    r = requests.post(url, json=data, timeout=5)
    r.raise_for_status()
    return r.json()

# ------------------------------
# Función para cambiar pantallas
# ------------------------------

def mostrar_frame(frame):
    frame.tkraise()

# ------------------------------
# Ventana principal
# ------------------------------

ventana = tk.Tk()
ventana.title("SG Biblioteca")
ventana.geometry("900x500")

contenedor = tk.Frame(ventana)
contenedor.pack(fill="both", expand=True)

contenedor.grid_rowconfigure(0, weight=1)
contenedor.grid_columnconfigure(0, weight=1)

pantalla_usuario = tk.Frame(contenedor, bg="white")
pantalla_bibliotecario = tk.Frame(contenedor, bg="white")
pantalla_direccion = tk.Frame(contenedor, bg="white")

for frame in (pantalla_usuario, pantalla_bibliotecario, pantalla_direccion):
    frame.grid(row=0, column=0, sticky="nsew")

# ------------------------------
# PANTALLA USUARIO
# ------------------------------

tk.Label(
    pantalla_usuario,
    text="Panel Usuario - Consulta de Catálogo",
    font=("Arial", 18)
).pack(pady=10)

frame_busqueda = tk.Frame(pantalla_usuario, bg="white")
frame_busqueda.pack(pady=5)

tk.Label(frame_busqueda, text="ISBN:", bg="white").grid(row=0, column=0, padx=5)
entry_isbn = tk.Entry(frame_busqueda, width=20)
entry_isbn.grid(row=0, column=1, padx=5)

def cargar_catalogo():
    try:
        libros = api_get_libros()
        tabla_libros.delete(*tabla_libros.get_children())
        for libro in libros:
            tabla_libros.insert(
                "",
                "end",
                values=(
                    libro.get("isbn", ""),
                    libro.get("titulo", ""),
                    libro.get("anio_publicacion", ""),
                    libro.get("stock_disponible", "")
                )
            )
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el catálogo:\n{e}")

def buscar_isbn():
    isbn = entry_isbn.get().strip()
    if not isbn:
        messagebox.showwarning("Aviso", "Ingresa un ISBN.")
        return
    try:
        libro = api_get_libro_por_isbn(isbn)
        tabla_libros.delete(*tabla_libros.get_children())
        # si la API devuelve un solo objeto
        if isinstance(libro, dict):
            tabla_libros.insert(
                "",
                "end",
                values=(
                    libro.get("isbn", ""),
                    libro.get("titulo", ""),
                    libro.get("anio_publicacion", ""),
                    libro.get("stock_disponible", "")
                )
            )
        # si devuelve lista
        elif isinstance(libro, list):
            for l in libro:
                tabla_libros.insert(
                    "",
                    "end",
                    values=(
                        l.get("isbn", ""),
                        l.get("titulo", ""),
                        l.get("anio_publicacion", ""),
                        l.get("stock_disponible", "")
                    )
                )
    except Exception as e:
        messagebox.showerror("Error", f"No se encontró el libro:\n{e}")

tk.Button(frame_busqueda, text="Buscar por ISBN", command=buscar_isbn).grid(row=0, column=2, padx=5)
tk.Button(frame_busqueda, text="Cargar catálogo completo", command=cargar_catalogo).grid(row=0, column=3, padx=5)

# Tabla para mostrar libros
tabla_libros = ttk.Treeview(
    pantalla_usuario,
    columns=("isbn", "titulo", "anio", "stock"),
    show="headings",
    height=15
)
tabla_libros.heading("isbn", text="ISBN")
tabla_libros.heading("titulo", text="Título")
tabla_libros.heading("anio", text="Año")
tabla_libros.heading("stock", text="Stock disp.")

tabla_libros.column("isbn", width=120)
tabla_libros.column("titulo", width=350)
tabla_libros.column("anio", width=60, anchor="center")
tabla_libros.column("stock", width=80, anchor="center")

tabla_libros.pack(fill="both", expand=True, padx=10, pady=10)


# ------------------------------
# PANTALLA BIBLIOTECARIO
# ------------------------------


tk.Label(
    pantalla_bibliotecario,
    text="Panel Bibliotecario - Gestión de Libros",
    font=("Arial", 18)
).pack(pady=10)

form = tk.Frame(pantalla_bibliotecario, bg="white")
form.pack(pady=10)

tk.Label(form, text="Título:", bg="white").grid(row=0, column=0, sticky="e", padx=5, pady=2)
tk.Label(form, text="Descripción:", bg="white").grid(row=1, column=0, sticky="e", padx=5, pady=2)
tk.Label(form, text="Año publicación:", bg="white").grid(row=2, column=0, sticky="e", padx=5, pady=2)
tk.Label(form, text="Autor ID:", bg="white").grid(row=3, column=0, sticky="e", padx=5, pady=2)
tk.Label(form, text="Categoría ID:", bg="white").grid(row=4, column=0, sticky="e", padx=5, pady=2)
tk.Label(form, text="Stock total:", bg="white").grid(row=5, column=0, sticky="e", padx=5, pady=2)
tk.Label(form, text="ISBN:", bg="white").grid(row=6, column=0, sticky="e", padx=5, pady=2)

e_titulo = tk.Entry(form, width=40)
e_desc = tk.Entry(form, width=40)
e_anio = tk.Entry(form, width=10)
e_autor = tk.Entry(form, width=10)
e_categoria = tk.Entry(form, width=10)
e_stock = tk.Entry(form, width=10)
e_isbn = tk.Entry(form, width=20)

e_titulo.grid(row=0, column=1, padx=5, pady=2)
e_desc.grid(row=1, column=1, padx=5, pady=2)
e_anio.grid(row=2, column=1, padx=5, pady=2)
e_autor.grid(row=3, column=1, padx=5, pady=2)
e_categoria.grid(row=4, column=1, padx=5, pady=2)
e_stock.grid(row=5, column=1, padx=5, pady=2)
e_isbn.grid(row=6, column=1, padx=5, pady=2)


def api_crear_libro(data):
    if not TOKEN:
        # Por si acaso te olvidas de poner el token
        raise RuntimeError("")

    url = f"{BASE_URL}/libros"
    headers = {
        "Authorization": f"Bearer {TOKEN}",   # aquí va el token
        "Content-Type": "application/json"
    }

   
    r = requests.post(url, json=data, headers=headers, timeout=20)
    if r.status_code >= 400:
        try:
            detalle =r.json()
        except ValueError:
            detalle =r.text
            raise Exception(f"Error {r.status_code}:\n{detalle}")
    try:
          return r.json()
    except ValueError:
        return{"mensaje": r.text}

def crear_libro_desde_form():
    try:
        data = {
            "titulo": e_titulo.get(),
            "descripcion": e_desc.get(),
            "anio_publicacion": int(e_anio.get()),
            "autor_id": int(e_autor.get()),
            "categoria_id": int(e_categoria.get()),
            "stock_total": int(e_stock.get()),
            "stock_disponible": int(e_stock.get()),
            "isbn": e_isbn.get()
        }
        nuevo = api_crear_libro(data)
        messagebox.showinfo("Éxito", f"Libro creado\n")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo crear el libro:\n{e}")
   
tk.Button(pantalla_bibliotecario, text="Guardar libro", command=crear_libro_desde_form).pack(pady=10)
cargar_catalogo()
# ------------------------------
# PANTALLA DIRECCIÓN
# ------------------------------

tk.Label(
    pantalla_direccion,
    text="Panel Dirección - Reportes y KPIs",
    font=("Arial", 18)
).pack(pady=60)

tk.Label(
    pantalla_direccion,
    text=" llamar a endpoints de reportes\npara mostrar estadísticas y gráficas.",
    bg="white"
).pack(pady=60)

# ------------------------------
# MENÚ SUPERIOR
# ------------------------------

menu = tk.Frame(ventana, bg="#792222")
menu.place(x=0, y=0, width=900, height=40)

tk.Button(menu, text="Usuario", command=lambda: mostrar_frame(pantalla_usuario)).pack(side="left", padx=10)
tk.Button(menu, text="Bibliotecario", command=lambda: mostrar_frame(pantalla_bibliotecario)).pack(side="left", padx=10)
tk.Button(menu, text="Dirección", command=lambda: mostrar_frame(pantalla_direccion)).pack(side="left", padx=10)

# Pantalla inicial
mostrar_frame(pantalla_usuario)

ventana.mainloop()
