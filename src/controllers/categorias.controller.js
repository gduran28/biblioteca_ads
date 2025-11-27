import { db } from "../../db/db.js";

export const getCategorias = async (_, res) => {
  try {
    const {rows} = await db.execute("SELECT * FROM categorias");
    res.json(rows);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Error al obtener las categorías"});
  }
};

export const getCategoriaById = async (req, res) => {
  const { id } = req.params;
  try {
    const {rows} = await db.execute("SELECT * FROM categorias WHERE id = ?", [id]);
    if (rows.length === 0) {
      return res.status(404).json({ error: "Categoría no encontrada" });
    }
  } catch (error) {
    res.json(rows[0]);
    res.status(500).json({ error: "Error al obtener la categoría" });
  }
};

export const createCategoria = async (req, res) => {
  const { nombre } = req.body;
  try {
    await db.execute(
      "INSERT INTO categorias (nombre) VALUES (?)",
      [nombre]
    );
    res.status(201).json({ message: "Categoría creada exitosamente" });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Error al crear la categoría" });
  }
};

export const updateCategoria = async (req, res) => {
  const { id } = req.params;
  const { nombre } = req.body;
  try {
    const result = await db.execute("UPDATE categorias SET nombre = ? WHERE id = ?", [nombre, id]);
    if (result.affectedRows === 0) {
      return res.status(404).json({ error: "Categoría no encontrada" });
    }
    res.json({ message: "Categoría actualizada exitosamente" });
  } catch (error) {
    res.status(500).json({ error: "Error al actualizar la categoría", });
  }
};