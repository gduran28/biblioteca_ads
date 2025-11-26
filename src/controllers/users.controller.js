import { db } from "../../db/db.js";

export const getUsers = async (_, res) => {
  try {
    const result = await db.execute("SELECT id, email, rol FROM usuarios");
    res.json(result.rows);
  } catch (error) {
    res.status(500).json({ error: "Error retrieving users" });
  }
}

export const getUserById = async (req, res) => {  
  const { id } = req.params; 
  try {
    const result = await db.execute(
      "SELECT id, email, rol FROM usuarios WHERE id = :id",
      { id }
    );
    if (result.rows.length === 0) {
      return res.status(404).json({ error: "User not found" });
    }
    res.json(result.rows[0]);
  } catch (error) {
    res.status(500).json({ error: "Error retrieving user" });
  }
}

export const updateUser = async (req, res) => {
  const { id } = req.params;
  const { email, rol } = req.body;
  try {
    const result = await db.execute(
      "UPDATE usuarios SET email = :email, rol = :rol WHERE id = :id",
      { id, email, rol }
    );
    if (result.rowsAffected === 0) {
      return res.status(404).json({ error: "User not found" });
    }
    res.json({ message: "User updated successfully" });
  } catch (error) {
    res.status(500).json({ error: "Error updating user" });
  }
}

export const deactivateUser = async (req, res) => {
  const { id } = req.params;
  try {
    const result = await db.execute(
      "UPDATE usuarios SET estado = 'suspendido' WHERE id = :id",
      { id }
    );
    if (result.rowsAffected === 0) {
      return res.status(404).json({ error: "User not found" });
    }
    res.json({ message: "User deactivated successfully" });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Error deactivating user" });
  }
}

export const activateUser = async (req, res) => {
  const { id } = req.params;
  try {
    const result = await db.execute(
      "UPDATE usuarios SET estado = 'activo' WHERE id = :id",
      { id }
    );
    if (result.rowsAffected === 0) {
      return res.status(404).json({ error: "User not found" });
    }
    res.json({ message: "User activated successfully" });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Error activating user" });
  }
}