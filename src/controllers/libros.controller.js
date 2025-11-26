import { db } from "../../db/db";

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