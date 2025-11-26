import { db } from "../../db/db.js";
import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";

export const login = async (req, res) => {  
  console.log("Login attempt:", req.body);
  const { email, password } = req.body;
  try {
    const result = await db.execute("SELECT * FROM usuarios WHERE email = ?", [email]);
    if (result.rows.length === 0) {
      return res.status(401).json({ error: "Contraseña o correo incorrecto." });
    }

    const user = result.rows[0];
    console.log("🚀 ~ login ~ user:", user.password_hash);
    
    const isPasswordValid = bcrypt.compareSync(password, user.password_hash);
    if (!isPasswordValid) {
      return res.status(401).json({ error: "Contraseña incorrecta." });
    }

    const token = jwt.sign({
      id: user.id,
      email: user.email,
      rol: user.rol
    },
    process.env.JWT_SECRET, 
    { expiresIn: "2h" });

    res.json({
      message: "Inicio de sesión exitoso.",
      token,
      user: {
        id: user.id,
        email: user.email,
        rol: user.rol
      }
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Error al iniciar sesión." });
  }
}

export const register = async (req, res) => {
  const { nombre, email, password, rol } = req.body;
  try {
    if(!nombre || !email || !password) {
      return res.status(400).json({ error: "Faltan datos obligatorios." });
    }

    const existingUser = await db.execute("SELECT * FROM usuarios WHERE email = ?", [email]);
    if (existingUser.rows.length > 0) {
      return res.status(409).json({ error: "El correo ya está registrado." });
    }

    const passwordHash = bcrypt.hashSync(password, 10);

    await db.execute(
      "INSERT INTO usuarios (nombre, email, password_hash, rol) VALUES (?, ?, ?, ?)",
      [nombre, email, passwordHash, rol || 'usuario']
    );

    res.status(201).json({ message: "Usuario registrado exitosamente." });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Error al registrar usuario." }); 
  }
}

export const getProfile = async (req, res) => {
  try {
    console.log("Fetching profile for user ID:", req);
    const userId = req.user.id;
    const result = await db.execute("SELECT id, nombre, email, rol FROM usuarios WHERE id = ?", [userId]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: "Usuario no encontrado." });
    }
    
    const user = result.rows[0];
    res.json({ user });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Error al obtener el perfil del usuario." });
  }
}