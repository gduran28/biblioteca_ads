import tkinter as tk
from tkinter import ttk, messagebox
import requests

# =======================
# CONFIGURACIÓN API
# =======================

BASE_URL = "https://biblioteca-ads.onrender.com"

# Pega aquí un token JWT de admin obtenido con /auth/login
# Ejemplo en tu colección Postman (pero probablemente ya está vencido, genera uno nuevo si hace falta).
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZW1haWwiOiJhZG1pbkBiaWJsaW90ZWNhLmNvbSIsInJvbCI6ImFkbWluIiwiaWF0IjoxNzY0Mjg4ODQ2LCJleHAiOjE3NjQyOTYwNDZ9.DNZBdhr4uXEiAHAL8izHNhMXiLvzlftoHR_gnmJfXL0"


def get_headers():
    if not TOKEN:
        raise RuntimeError("Configura la variable TOKEN con un JWT válido.")
    return {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }


# =======================
# FUNCIONES API
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


def api_get_users():
    url = f"{BASE_URL}/users"
    r = requests.get(url, headers=get_headers(), timeout=20)
    r.raise_for_status()
    return r.json()


# ========= NUEVAS FUNCIONES API PARA MORA / SANCIONES =========

def api_get_sanciones_usuario(usuario_id: int):
    """
    Obtiene las sanciones (mora) de un usuario.
    GET /sanciones/usuario/{id}
    """
    url = f"{BASE_URL}/sanciones/usuario/{usuario_id}"
    r = requests.get(url, headers=get_headers(), timeout=20)
    r.raise_for_status()
    return r.json()


def api_pagar_sancion(sancion_id: int):
    """
    Marca una sanción como pagada.
    POST /sanciones/pagar/{id}
    """
    url = f"{BASE_URL}/sanciones/pagar/{sancion_id}"
    r = requests.post(url, headers=get_headers(), timeout=20)
    r.raise_for_status()
    return r.json()


# =======================
# LÓGICA: PRÉSTAMO / DEVOLUCIÓN
# =======================

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
# VENTANAS USUARIO
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


def ventana_catalogo(root):
    win = tk.Toplevel(root)
    win.title("Consulta de catálogo")
    win.geometry("700x400")

    tk.Label(win, text="Catálogo de la biblioteca", font=("Arial", 14)).pack(pady=10)

    cols = ("isbn", "titulo", "anio", "stock")
    tabla = ttk.Treeview(win, columns=cols, show="headings", height=15)
    tabla.heading("isbn", text="ISBN")
    tabla.heading("titulo", text="Título")
    tabla.heading("anio", text="Año")
    tabla.heading("stock", text="Stock disp.")

    tabla.column("isbn", width=120)
    tabla.column("titulo", width=340)
    tabla.column("anio", width=60, anchor="center")
    tabla.column("stock", width=100, anchor="center")

    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    def cargar_catalogo():
        try:
            data = api_get_libros()
            # puede venir como lista o como dict {"libros":[...]}
            if isinstance(data, dict):
                libros = data.get("libros", [])
            else:
                libros = data

            tabla.delete(*tabla.get_children())
            for libro in libros:
                tabla.insert(
                    "",
                    "end",
                    values=(
                        libro.get("isbn", ""),
                        libro.get("titulo", ""),
                        libro.get("anio_publicacion", libro.get("anio", "")),
                        libro.get("stock_disponible", libro.get("stock", ""))
                    )
                )
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el catálogo:\n{e}")

    # Cargar automáticamente al abrir
    cargar_catalogo()

    # Dejas el botón por si quieren refrescar
    tk.Button(win, text="Actualizar catálogo", command=cargar_catalogo).pack(pady=5)


# ========= NUEVA VENTANA: MORA / SANCIONES =========

def ventana_sanciones_usuario(root):
    win = tk.Toplevel(root)
    win.title("Mora / Sanciones del usuario")
    win.geometry("700x400")

    tk.Label(win, text="Sanciones por mora", font=("Arial", 14)).pack(pady=10)

    top_frame = tk.Frame(win)
    top_frame.pack(pady=5)

    tk.Label(top_frame, text="ID Usuario:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    e_usuario = tk.Entry(top_frame, width=10)
    e_usuario.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    cols = ("id", "descripcion", "monto", "pagada")
    tabla = ttk.Treeview(win, columns=cols, show="headings", height=15)
    tabla.heading("id", text="ID")
    tabla.heading("descripcion", text="Descripción")
    tabla.heading("monto", text="Monto")
    tabla.heading("pagada", text="Pagada")

    tabla.column("id", width=50, anchor="center")
    tabla.column("descripcion", width=360)
    tabla.column("monto", width=100, anchor="center")
    tabla.column("pagada", width=80, anchor="center")

    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    def cargar_sanciones():
        try:
            usuario_txt = e_usuario.get().strip()
            if not usuario_txt:
                raise Exception("Ingresa el ID de usuario.")
            usuario_id = int(usuario_txt)

            data = api_get_sanciones_usuario(usuario_id)

            if isinstance(data, dict):
                sanciones = data.get("sanciones", data.get("data", []))
            else:
                sanciones = data

            tabla.delete(*tabla.get_children())
            for s in sanciones:
                tabla.insert(
                    "",
                    "end",
                    values=(
                        s.get("id", ""),
                        s.get("descripcion", s.get("motivo", "")),
                        s.get("monto", s.get("valor", "")),
                        "Sí" if s.get("pagada", False) else "No"
                    )
                )
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las sanciones:\n{e}")

    def pagar_sancion():
        try:
            seleccion = tabla.selection()
            if not seleccion:
                raise Exception("Selecciona una sanción de la tabla.")

            item = tabla.item(seleccion[0])
            sancion_id = item["values"][0]
            if not sancion_id:
                raise Exception("No se encontró el ID de la sanción seleccionada.")

            api_pagar_sancion(int(sancion_id))
            messagebox.showinfo("Pago de mora", "La sanción seleccionada ha sido marcada como pagada.")

            # Refrescar lista
            cargar_sanciones()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo pagar la sanción:\n{e}")

    botones_frame = tk.Frame(win)
    botones_frame.pack(pady=5)

    tk.Button(botones_frame, text="Cargar sanciones", command=cargar_sanciones).grid(row=0, column=0, padx=5)
    tk.Button(botones_frame, text="Pagar sanción seleccionada", command=pagar_sancion).grid(row=0, column=1, padx=5)


# =======================
# VENTANAS BIBLIOTECARIO
# =======================

def ventana_gestion_usuarios(root):
    win = tk.Toplevel(root)
    win.title("Gestión de usuarios")
    win.geometry("700x400")

    tk.Label(win, text="Usuarios del sistema", font=("Arial", 14)).pack(pady=10)

    cols = ("id", "nombre", "email", "rol")
    tabla = ttk.Treeview(win, columns=cols, show="headings", height=15)
    tabla.heading("id", text="ID")
    tabla.heading("nombre", text="Nombre")
    tabla.heading("email", text="Email")
    tabla.heading("rol", text="Rol")

    tabla.column("id", width=50, anchor="center")
    tabla.column("nombre", width=180)
    tabla.column("email", width=250)
    tabla.column("rol", width=80, anchor="center")

    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    def cargar_usuarios():
        try:
            usuarios = api_get_users()
            tabla.delete(*tabla.get_children())
            for u in usuarios:
                tabla.insert(
                    "",
                    "end",
                    values=(
                        u.get("id", ""),
                        u.get("nombre", ""),
                        u.get("email", ""),
                        u.get("rol", "")
                    )
                )
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los usuarios:\n{e}")

    tk.Button(win, text="Cargar usuarios", command=cargar_usuarios).pack(pady=5)


def ventana_actualizar_ejemplares(root):
    win = tk.Toplevel(root)
    win.title("Actualización de ejemplares")
    win.geometry("500x320")

    tk.Label(win, text="Actualización de ejemplares", font=("Arial", 14)).pack(pady=10)

    frame = tk.Frame(win)
    frame.pack(pady=10)

    # Etiquetas
    tk.Label(frame, text="ISBN:", anchor="e").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    tk.Label(frame, text="Título:", anchor="e").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    tk.Label(frame, text="Año publicación:", anchor="e").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    tk.Label(frame, text="Autor:", anchor="e").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    tk.Label(frame, text="Stock total:", anchor="e").grid(row=4, column=0, padx=5, pady=5, sticky="e")
    tk.Label(frame, text="Stock disponible:", anchor="e").grid(row=5, column=0, padx=5, pady=5, sticky="e")

    # Entradas
    e_isbn = tk.Entry(frame, width=20)
    e_titulo = tk.Entry(frame, width=40)
    e_anio = tk.Entry(frame, width=10)
    e_autor = tk.Entry(frame, width=25)   # aquí mostraremos nombre o autor_id
    e_stock_total = tk.Entry(frame, width=10)
    e_stock_disp = tk.Entry(frame, width=10)

    e_isbn.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    e_titulo.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    e_anio.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    e_autor.grid(row=3, column=1, padx=5, pady=5, sticky="w")
    e_stock_total.grid(row=4, column=1, padx=5, pady=5, sticky="w")
    e_stock_disp.grid(row=5, column=1, padx=5, pady=5, sticky="w")

    def cargar_datos():
        try:
            isbn = e_isbn.get().strip()
            if not isbn:
                raise Exception("Ingresa un ISBN.")
            libro = api_get_libro(isbn)

            # Limpiar entradas
            for entry in (e_titulo, e_anio, e_autor, e_stock_total, e_stock_disp):
                entry.delete(0, tk.END)

            # Rellenar con lo que venga de la API
            e_titulo.insert(0, libro.get("titulo", ""))
            e_anio.insert(0, libro.get("anio_publicacion", ""))
            # Si la API trae autor como objeto, usamos su nombre; si no, usamos autor_id
            autor_nombre = ""
            if isinstance(libro.get("autor"), dict):
                autor_nombre = libro["autor"].get("nombre", "")
            else:
                autor_nombre = str(libro.get("autor_id", ""))

            e_autor.insert(0, autor_nombre)
            e_stock_total.insert(0, libro.get("stock_total", 0))
            e_stock_disp.insert(0, libro.get("stock_disponible", 0))

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el libro:\n{e}")

    def guardar_cambios():
        try:
            isbn = e_isbn.get().strip()
            if not isbn:
                raise Exception("Ingresa un ISBN.")

            # Traemos el libro actual para no perder otros campos (descripcion, categoria_id, etc.)
            libro = api_get_libro(isbn)

            libro["titulo"] = e_titulo.get()
            # Si no cambias el año, dejamos el existente; si lo cambias, lo convertimos a int
            libro["anio_publicacion"] = int(e_anio.get()) if e_anio.get().strip() else libro.get("anio_publicacion", 0)

            libro["stock_total"] = int(e_stock_total.get())
            libro["stock_disponible"] = int(e_stock_disp.get())

            libro_act = api_update_libro(isbn, libro)
            messagebox.showinfo(
                "Actualización",
                f"Ejemplares actualizados para:\n{libro_act.get('titulo', '')}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el ejemplar:\n{e}")

    tk.Button(win, text="Cargar datos", command=cargar_datos).pack(pady=5)
    tk.Button(win, text="Guardar cambios", command=guardar_cambios).pack(pady=5)


# =======================
# VENTANA DIRECCIÓN ACADÉMICA
# =======================

def ventana_reportes(root):
    win = tk.Toplevel(root)
    win.title("Reportes y KPIs")
    win.geometry("400x250")

    tk.Label(win, text="Reportes Académicos", font=("Arial", 14)).pack(pady=40)

    info_label = tk.Label(win, text="", justify="left")
    info_label.pack(pady=40)

    def cargar_reportes():
        try:
            libros = api_get_libros()
            if isinstance(libros, dict):
                libros_list = libros.get("libros", [])
            else:
                libros_list = libros

            total_libros = len(libros_list)
            sin_stock = sum(1 for l in libros_list if l.get("stock_disponible", 0) == 0)
            with_stock = total_libros - sin_stock

            texto = (
                f"Total de libros en catálogo: {total_libros}\n"
                f"Libros con stock disponible: {with_stock}\n"
                f"Libros sin stock: {sin_stock}"
            )
            info_label.config(text=texto)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron generar los reportes:\n{e}")

    tk.Button(win, text="Mostrar reportes", command=cargar_reportes).pack(pady=40)


# =======================
# FRAMES POR ROL
# =======================

def construir_pantalla_usuario(contenedor, root):
    frame = tk.Frame(contenedor, bg="white")
    tk.Label(frame, text="Menú Usuario", font=("Arial", 16), bg="white").pack(pady=40)

    tk.Button(
        frame,
        text="Solicitud de ejemplar",
        width=25,
        command=lambda: ventana_solicitud(root)
    ).pack(pady=5)

    tk.Button(
        frame,
        text="Devolución de ejemplar",
        width=25,
        command=lambda: ventana_devolucion(root)
    ).pack(pady=5)

    tk.Button(
        frame,
        text="Consulta del catálogo",
        width=25,
        command=lambda: ventana_catalogo(root)
    ).pack(pady=5)

    # NUEVO: ver mora / sanciones del usuario
    tk.Button(
        frame,
        text="Ver mora / sanciones",
        width=25,
        command=lambda: ventana_sanciones_usuario(root)
    ).pack(pady=5)

    return frame


def construir_pantalla_bibliotecario(contenedor, root):
    frame = tk.Frame(contenedor, bg="white")
    tk.Label(frame, text="Menú Bibliotecario", font=("Arial", 16), bg="white").pack(pady=40)

    tk.Button(
        frame,
        text="Gestión de usuarios",
        width=25,
        command=lambda: ventana_gestion_usuarios(root)
    ).pack(pady=5)

    tk.Button(
        frame,
        text="Actualización de ejemplares",
        width=25,
        command=lambda: ventana_actualizar_ejemplares(root)
    ).pack(pady=5)

    # NUEVO: gestión/consulta de mora por usuario (usa la misma ventana)
    tk.Button(
        frame,
        text="Mora / sanciones por usuario",
        width=25,
        command=lambda: ventana_sanciones_usuario(root)
    ).pack(pady=5)

    return frame


def construir_pantalla_direccion(contenedor, root):
    frame = tk.Frame(contenedor, bg="white")
    tk.Label(frame, text="Dirección Académica", font=("Arial", 16), bg="white").pack(pady=40)

    tk.Button(
        frame,
        text="Mostrar reportes",
        width=25,
        command=lambda: ventana_reportes(root)
    ).pack(pady=5)

    return frame


# =======================
# APP PRINCIPAL
# =======================

def mostrar_frame(frame):
    frame.tkraise()


def main():
    root = tk.Tk()
    root.title("SG Biblioteca")
    root.geometry("500x300")

    contenedor = tk.Frame(root)
    contenedor.pack(fill="both", expand=True)

    contenedor.grid_rowconfigure(0, weight=1)
    contenedor.grid_columnconfigure(0, weight=1)

    pantalla_usuario = construir_pantalla_usuario(contenedor, root)
    pantalla_biblio = construir_pantalla_bibliotecario(contenedor, root)
    pantalla_dir = construir_pantalla_direccion(contenedor, root)

    for frame in (pantalla_usuario, pantalla_biblio, pantalla_dir):
        frame.grid(row=0, column=0, sticky="nsew")

    # Menú superior para cambiar de rol
    menu = tk.Frame(root, bg="#dddddd")
    menu.place(x=0, y=0, width=500, height=40)

    tk.Button(menu, text="Usuario", command=lambda: mostrar_frame(pantalla_usuario)).pack(side="left", padx=10)
    tk.Button(menu, text="Bibliotecario", command=lambda: mostrar_frame(pantalla_biblio)).pack(side="left", padx=10)
    tk.Button(menu, text="Dirección Académica", command=lambda: mostrar_frame(pantalla_dir)).pack(side="left", padx=10)

    mostrar_frame(pantalla_usuario)

    root.mainloop()


if __name__ == "__main__":
    main()
