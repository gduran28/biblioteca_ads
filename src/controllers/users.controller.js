import { db } from "../../db/db.js";

export const getUsers = async (_, res) => {
  try {
    const result = await db.execute("SELECT id, email, rol FROM usuarios");
    res.json(result.rows);
  } catch (error) {
    res.status(500).json({ error: "Error retrieving users" });
  }
}