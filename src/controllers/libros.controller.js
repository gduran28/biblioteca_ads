import { db } from "../../db/db.js";

export const getLibros = async (_, res) => {
  try {
    const result = await db.execute("SELECT * FROM libros");
    res.json(result.rows);
  } catch (error) {
    res.status(500).json({ error: "Error retrieving books" });
  }
};

export const getLibroByISBN = async (req, res) => {
  const { isbn } = req.params;
  try {
    const result = await db.execute("SELECT * FROM libros WHERE isbn = ?", [isbn]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: "Book not found" });
    }
    res.json(result.rows[0]);
  } catch (error) {
    res.status(500).json({ error: "Error retrieving book" });
  }
};

export const createLibro = async (req, res) => {
  const { titulo, descripcion, anio_publicacion, autor_id, categoria_id, stock_total, stock_disponible, isbn } = req.body;
  try {
    await db.execute(
      "INSERT INTO libros (titulo, descripcion, anio_publicacion, autor_id, categoria_id, stock_total, stock_disponible, isbn) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
      [titulo, descripcion, anio_publicacion, autor_id, categoria_id, stock_total, stock_disponible, isbn]
    );
    res.status(201).json({ message: "Book created successfully" });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Error creating book" });
  }
};

export const updateLibro = async (req, res) => {
  const { isbn } = req.params;
  const { titulo, descripcion, anio_publicacion, autor_id, categoria_id, stock_total, stock_disponible } = req.body;
  try {
    const result = await db.execute(
      "UPDATE libros SET titulo = ?, descripcion = ?, anio_publicacion = ?, autor_id = ?, categoria_id = ?, stock_total = ?, stock_disponible = ? WHERE isbn = ?",
      [titulo, descripcion, anio_publicacion, autor_id, categoria_id, stock_total, stock_disponible, isbn]
    );
    if (result.affectedRows === 0) {
      return res.status(404).json({ error: "Book not found" });
    }
    res.json({ message: "Book updated successfully" });
  } catch (error) {
    res.status(500).json({ error: "Error updating book" });
  }
};

export const deactivateLibro = async (req, res) => {
  const { isbn } = req.params;
  try {
    const result = await db.execute(
      "UPDATE libros SET activo = 0 WHERE isbn = ?",
      [isbn]
    );
    if (result.affectedRows === 0) {
      return res.status(404).json({ error: "Book not found" });
    }
    res.json({ message: "Book deactivated successfully" });
  } catch (error) {
    res.status(500).json({ error: "Error deactivating book" });
  }
};

export const activateLibro = async (req, res) => {
  const { isbn } = req.params;
  try {
    const result = await db.execute(
      "UPDATE libros SET activo = 1 WHERE isbn = ?",
      [isbn]
    );
    if (result.affectedRows === 0) {
      return res.status(404).json({ error: "Book not found" });
    }
    res.json({ message: "Book activated successfully" });
  } catch (error) {
    res.status(500).json({ error: "Error activating book" });
  }
};