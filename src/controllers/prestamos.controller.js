import { db } from "../../db/db.js";

export const getPrestamos = async (_, res) => {
	try {
		const { rows } = await db.execute("SELECT * FROM prestamos");
		res.json(rows);
	} catch (error) {
		return res.status(500).json({ error: "Error retrieving prestamos" });
	}
};

export const getPrestamosById = async (req, res) => {
	const { id } = req.params;
	try {
		const { rows } = await db.execute("SELECT * FROM prestamos WHERE id = ?", [
			id,
		]);
		if (rows.length <= 0) {
			return res.status(404).json({ error: "Prestamo not found" });
		}
		const prestamo = rows[0];
		const fechaEntrega = new Date(prestamo.fecha_entrega);
		const mora = calcularMora(fechaEntrega, new Date());

		if (mora > 0) {
			prestamo.mora = mora;
      const updated = await setMoraForPrestamo(prestamo, mora);
      return res.json({ id: updated.id, usuario_id: updated.usuario_id, libro_id: updated.libro_id, fecha_prestamo: updated.fecha_prestamo, fecha_entrega: updated.fecha_entrega, fecha_devolucion: updated.fecha_devolucion, estado: updated.estado, mora });
		}
		res.json(rows[0]);
	} catch (error) {
		return res.status(500).json({ error: "Error retrieving prestamo" });
	}
};

export const getPrestamosByUserId = async (req, res) => {
	const { userId } = req.params;
	try {
		const { rows } = await db.execute(
			"SELECT * FROM prestamos WHERE usuario_id = ?",
			[userId]
		);
    for (let i = 0; i < rows.length; i++) {
      const prestamo = rows[i];
      const fechaEntrega = new Date(prestamo.fecha_entrega);
      const mora = calcularMora(fechaEntrega, new Date());
      if (mora > 0) {
        prestamo.mora = mora;
        const updated = await setMoraForPrestamo(prestamo, mora);
        rows[i] = { ...updated, mora };
      }
    }
		res.json(rows);
	} catch (error) {
    console.log(error);
		return res
			.status(500)
			.json({ error: "Error retrieving prestamos for user" });
	}
};

export const createPrestamo = async (req, res) => {
	const { usuario_id, libro_id } = req.body;
	const fecha_prestamos = new Date();
	const fecha_entrega = new Date();
	fecha_entrega.setDate(fecha_prestamos.getDate() + 14);
	try {
    const libroCheck = await db.execute("SELECT stock_disponible FROM libros WHERE id = ?", [libro_id]);
    if (libroCheck.rows.length === 0) {
      return res.status(404).json({ error: "Libro no encontrado" });
    }
    if (libroCheck.rows[0].stock_disponible <= 0) {
      return res.status(400).json({ error: "No hay stock disponible" });
    }
		await db.execute(
			`INSERT INTO prestamos (usuario_id, libro_id, fecha_prestamo, fecha_entrega, estado) VALUES (?, ?, ?, ?, 'activo')`,
			[usuario_id, libro_id, fecha_prestamos, fecha_entrega]
		);
    await db.execute("UPDATE libros SET stock_disponible = stock_disponible - 1 WHERE id = ?", [libro_id]);
		res.status(201).json({ message: "Prestamo creado" });
	} catch (error) {
		console.error(error);
		return res.status(500).json({ error: "Error creating prestamo" });
	}
};

export const devolverLibro = async (req, res) => {
	const { id } = req.params;
	const fecha_devolucion = new Date();
	try {
    const prestamoLookup = await db.execute("SELECT * FROM prestamos WHERE id = ?", [id]);
    if (prestamoLookup.rows.length === 0) {
      return res.status(404).json({ error: "Prestamo not found" });
    }
    const libro_id = prestamoLookup.rows[0].libro_id;

		const result = await db.execute(
			`UPDATE prestamos SET fecha_devolucion = ?, estado = 'devuelto' WHERE id = ?`,
			[fecha_devolucion, id]
		);
		if (result.rowsAffected === 0) {
			return res.status(404).json({ error: "Prestamo not found" });
		}
    await db.execute("UPDATE libros SET stock_disponible = stock_disponible + 1 WHERE id = ?", [libro_id]);
		res.json({ message: "Libro devuelto exitosamente" });
	} catch (error) {
		console.error(error);
		return res.status(500).json({ error: "Error updating prestamo" });
	}
};

const calcularMora = (fechaEntrega, fechaDevolucion) => {
	const unDia = 24 * 60 * 60 * 1000;
	const diferenciaDias = Math.ceil((fechaDevolucion - fechaEntrega) / unDia);
	return diferenciaDias > 0 ? diferenciaDias * 1 : 0;
};

const setMoraForPrestamo = async (prestamo, mora) => {
	const fecha_entrega = new Date(prestamo.fecha_entrega);
	const fecha_devolucion = prestamo.fecha_devolucion
		? new Date(prestamo.fecha_devolucion)
		: new Date();
	try {
		const result = await db.execute(`UPDATE prestamos SET estado = 'atrasado' WHERE id = ? RETURNING *`, [
			prestamo.id,
		]);
    console.log(result);
    return result.rows[0];
	} catch (error) {
		console.error("Error updating prestamo with mora:", error);
	}
};
