import { db } from "../../db/db.js";

export const getAutores = async (_, res) => {
  try {
    const result = await db.execute("SELECT * FROM autores");
    res.json(result.rows);
  } catch (error) {
    res.status(500).json({ error: "Error retrieving authors" });
  }
};

export const getAutorById = async (req, res) => {
  const { id } = req.params;
  try {
    const result = await db.execute("SELECT * FROM autores WHERE id = ?", [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: "Author not found" });
    }
    res.json(result.rows[0]);
  } catch (error) {
    res.status(500).json({ error: "Error retrieving author" });
  }
};

export const createAutor = async (req, res) => {
  const { nombre } = req.body;
  try {
    await db.execute(
      "INSERT INTO autores (nombre) VALUES (?)",
      [nombre]
    );
    res.status(201).json({ message: "Author created successfully" });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Error creating author" });
  }
};

export const updateAutor = async (req, res) => {
  const { id } = req.params;
  const { nombre } = req.body;
  try {
    const result = await db.execute(
      "UPDATE autores SET nombre = ? WHERE id = ?",
      [nombre, id]
    );
    if (result.affectedRows === 0) {
      return res.status(404).json({ error: "Author not found" });
    }
    res.json({ message: "Author updated successfully" });
  } catch (error) {
    res.status(500).json({ error: "Error updating author" });
  }
};