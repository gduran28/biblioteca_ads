PRAGMA foreign_keys = ON;

-- ============================================
-- USUARIOS
-- ============================================
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    rol TEXT NOT NULL CHECK (rol IN ('admin', 'bibliotecario', 'usuario')),
    estado TEXT NOT NULL DEFAULT 'activo' CHECK (estado IN ('activo', 'suspendido')),
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- AUTORES
-- ============================================
CREATE TABLE autores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL
);

-- ============================================
-- CATEGORÍAS
-- ============================================
CREATE TABLE categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE
);

-- ============================================
-- LIBROS
-- ============================================
CREATE TABLE libros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descripcion TEXT,
    anio_publicacion INTEGER,
    autor_id INTEGER NOT NULL,
    categoria_id INTEGER NOT NULL,
    stock_total INTEGER NOT NULL DEFAULT 1,
    stock_disponible INTEGER NOT NULL DEFAULT 1,

    FOREIGN KEY (autor_id) REFERENCES autores(id) ON DELETE CASCADE,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE CASCADE
);

CREATE INDEX idx_libros_titulo ON libros(titulo);
CREATE INDEX idx_libros_categoria ON libros(categoria_id);

-- ============================================
-- PRÉSTAMOS
-- ============================================
CREATE TABLE prestamos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    libro_id INTEGER NOT NULL,
    fecha_prestamo DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_entrega DATETIME NOT NULL,
    fecha_devolucion DATETIME,

    estado TEXT NOT NULL CHECK (estado IN ('activo', 'devuelto', 'atrasado')),

    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (libro_id) REFERENCES libros(id) ON DELETE CASCADE
);

CREATE INDEX idx_prestamos_usuario ON prestamos(usuario_id);
CREATE INDEX idx_prestamos_libro ON prestamos(libro_id);

-- ============================================
-- RESERVAS
-- ============================================
CREATE TABLE reservas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    libro_id INTEGER NOT NULL,
    fecha_reserva DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado TEXT NOT NULL CHECK (estado IN ('pendiente', 'notificado', 'cancelado')),

    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (libro_id) REFERENCES libros(id)
);

CREATE INDEX idx_reservas_usuario ON reservas(usuario_id);

-- ============================================
-- SANCIONES
-- ============================================
CREATE TABLE sanciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    prestamo_id INTEGER NOT NULL,
    monto REAL NOT NULL,
    motivo TEXT NOT NULL,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    pagado INTEGER NOT NULL DEFAULT 0 CHECK (pagado IN (0, 1)),

    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (prestamo_id) REFERENCES prestamos(id)
);

-- ============================================
-- DATOS INICIALES
-- ============================================

INSERT INTO usuarios (nombre, email, password_hash, rol)
VALUES
('Admin General', 'admin@biblioteca.com', 'hash_admin', 'admin'),
('Bibliotecario 1', 'bibliotecario@biblioteca.com', 'hash_biblio', 'bibliotecario'),
('Usuario Prueba', 'usuario@correo.com', 'hash_usuario', 'usuario');

INSERT INTO autores (nombre) VALUES
('Gabriel García Márquez'),
('J. K. Rowling'),
('George Orwell');

INSERT INTO categorias (nombre) VALUES
('Ficción'),
('Ciencia Ficción'),
('Literatura'),
('Fantasía');

INSERT INTO libros (titulo, descripcion, anio_publicacion, autor_id, categoria_id, stock_total, stock_disponible)
VALUES
('Cien Años de Soledad', 'Obra maestra del realismo mágico', 1967, 1, 3, 5, 5),
('1984', 'Distopía clásica', 1949, 3, 2, 3, 3),
('Harry Potter y la Piedra Filosofal', 'Libro 1', 1997, 2, 4, 10, 10);