import { db } from "../../db/db.js";

export const crearSancion = async (usuario_id, prestamo_id, monto, motivo = "Devolución tardía") => {
  try {
    await db.execute(
      `INSERT INTO sanciones (usuario_id, prestamo_id, monto, motivo)
       VALUES (?, ?, ?, ?)`,
      [usuario_id, prestamo_id, monto, motivo]
    );
  } catch (error) {
    console.error("Error creando sanción:", error);
  }
};

export const getSanciones = async (req, res) => {
  try {
    const { rows } = await db.execute(`SELECT * FROM sanciones`);
    res.json(rows);
  } catch (error) {
    console.error(error);
    return res.status(500).json({ error: "Error retrieving sanciones" });
  }
};

export const getSancionesByUser = async (req, res) => {
  const { id } = req.params;
  try {
    const { rows } = await db.execute(
      `SELECT * FROM sanciones WHERE usuario_id = ?`,
      [id]
    );
    res.json(rows);
  } catch (error) {
    console.error(error);
    return res.status(500).json({ error: "Error retrieving user sanciones" });
  }
};

export const pagarSancion = async (req, res) => {
  const { id } = req.params;
  try {
    const result = await db.execute(
      `UPDATE sanciones SET pagado = 1 WHERE id = ?`,
      [id]
    );

    if (result.rowsAffected === 0) {
      return res.status(404).json({ error: "Sanción no encontrada" });
    }

    const { rows: sancionData } = await db.execute(
      "SELECT prestamo_id FROM sanciones WHERE id = ?",
      [id]
    );

    const prestamoId = sancionData[0].prestamo_id;

    const { rows: prestamoRows } = await db.execute(
      "SELECT fecha_devolucion FROM prestamos WHERE id = ?",
      [prestamoId]
    );

    const prestamo = prestamoRows[0];

    if (prestamo.fecha_devolucion) {
      await db.execute(
        "UPDATE prestamos SET estado = 'devuelto', fecha_entrega = fecha_devolucion WHERE id = ?",
        [prestamoId]
      );
    }

    res.json({ message: "Sanción pagada correctamente" });
  } catch (error) {
    console.error(error);
    return res.status(500).json({ error: "Error paying sancion" });
  }
};