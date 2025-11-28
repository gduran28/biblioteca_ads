import tkinter as tk
from tkinter import ttk, messagebox
import requests

# ------------------------------
# Función para cambiar pantallas
# ------------------------------

def mostrar_frame(frame):
    frame.tkraise()


# =======================
# CONFIGURACIÓN DE LA API
# =======================

BASE_URL = "https://biblioteca-ads.onrender.com"

# Pega aquí un token válido (obtenido por /auth/login)
TOKEN = "TU_TOKEN_JWT_AQUI"

def get_headers():
    if not TOKEN:
        return {}
    return {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

# =======================
# FUNCIONES DE LA API
# =======================

def api_get_libros():
    url = f"{BASE_URL}/libros"
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    return r.json()

def api_get_libro(isbn: str):
    url = f"{BASE_URL}/libros/{isbn}"
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    return r.json()

def api_update_libro(isbn: str, libro: dict):
    url = f"{BASE_URL}/libros/{isbn}"
    r = requests.put(url, json=libro, headers=get_headers(), timeout=20)
    r.raise_for_status()
    return r.json()
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

#-------------procesos---

def solicitar_ejemplar(usuario_id: int, isbn: str):
    libro = api_get_libro(isbn)
    stock_disp = libro.get("stock_disponible", 0)

    if stock_disp <= 0:
        raise Exception("No hay ejemplares disponibles para préstamo.")

    libro["stock_disponible"] = stock_disp - 1
    libro_act = api_update_libro(isbn, libro)

    return {
        "usuario_id": usuario_id,
        "isbn": isbn,
        "titulo": libro_act.get("titulo"),
        "mensaje": "Préstamo registrado correctamente."
    }

def devolver_ejemplar(usuario_id: int, isbn: str):
    libro = api_get_libro(isbn)
    stock_disp = libro.get("stock_disponible", 0)
    stock_total = libro.get("stock_total", 0)

    if stock_disp >= stock_total:
        raise Exception("El stock disponible ya es igual al stock total.")

    libro["stock_disponible"] = stock_disp + 1
    libro_act = api_update_libro(isbn, libro)

    return {
        "usuario_id": usuario_id,
        "isbn": isbn,
        "titulo": libro_act.get("titulo"),
        "mensaje": "Devolución registrada correctamente."
    }

# =======================
# VENTANAS SECUNDARIAS
# =======================

def ventana_solicitud(root):
    win = tk.Toplevel(root)
    win.title("Solicitud de ejemplar")
    win.geometry("400x200")

    tk.Label(win, text="Solicitud de ejemplar", font=("Arial", 14)).pack(pady=10)

    frame = tk.Frame(win)
    frame.pack(pady=10)

    tk.Label(frame, text="ID Usuario:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    tk.Label(frame, text="ISBN:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

    e_usuario = tk.Entry(frame, width=20)
    e_isbn = tk.Entry(frame, width=20)

    e_usuario.grid(row=0, column=1, padx=5, pady=5)
    e_isbn.grid(row=1, column=1, padx=5, pady=5)

    def hacer_solicitud():
        try:
            usuario_id = int(e_usuario.get())
            isbn = e_isbn.get().strip()
            if not isbn:
                raise Exception("Ingresa un ISBN.")
            resultado = solicitar_ejemplar(usuario_id, isbn)
            messagebox.showinfo("Préstamo", f"{resultado['mensaje']}\nTítulo: {resultado['titulo']}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el préstamo:\n{e}")

    tk.Button(win, text="Solicitar", command=hacer_solicitud).pack(pady=10)


def ventana_devolucion(root):
    win = tk.Toplevel(root)
    win.title("Devolución de ejemplar")
    win.geometry("400x200")

    tk.Label(win, text="Devolución de ejemplar", font=("Arial", 14)).pack(pady=10)

    frame = tk.Frame(win)
    frame.pack(pady=10)

    tk.Label(frame, text="ID Usuario:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    tk.Label(frame, text="ISBN:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

    e_usuario = tk.Entry(frame, width=20)
    e_isbn = tk.Entry(frame, width=20)

    e_usuario.grid(row=0, column=1, padx=5, pady=5)
    e_isbn.grid(row=1, column=1, padx=5, pady=5)

    def hacer_devolucion():
        try:
            usuario_id = int(e_usuario.get())
            isbn = e_isbn.get().strip()
            if not isbn:
                raise Exception("Ingresa un ISBN.")
            resultado = devolver_ejemplar(usuario_id, isbn)
            messagebox.showinfo("Devolución", f"{resultado['mensaje']}\nTítulo: {resultado['titulo']}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la devolución:\n{e}")

    tk.Button(win, text="Devolver", command=hacer_devolucion).pack(pady=10)
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
        libro = api_get_libro(isbn)
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


# =======================
# VENTANA PRINCIPAL (MENÚ USUARIO)
# =======================

def main():
    root = tk.Tk()
    root.title("SG Biblioteca - Usuario")
    root.geometry("400x250")

    tk.Label(root, text="Menú Usuario", font=("Arial", 16)).pack(pady=20)

    tk.Button(
        root,
        text="Solicitud de ejemplar",
        width=25,
        command=lambda: ventana_solicitud(root)
    ).pack(pady=5)

    tk.Button(
        root,
        text="Devolución de ejemplar",
        width=25,
        command=lambda: ventana_devolucion(root)
    ).pack(pady=5)

    tk.Button(
        root,
        text="Consulta del catálogo",
        width=25,
        command=lambda: cargar_catalogo(root)
    ).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
