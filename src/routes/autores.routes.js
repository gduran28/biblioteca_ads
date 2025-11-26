import { Router } from "express";
import { getAutores, getAutorById, updateAutor, createAutor } from "../controllers/autores.routes";
import { authMiddleware } from "../middlewares/auth.middleware.js";
import { requireRole } from "../middlewares/role.middleware.js";

const router = Router();

router.get("/", getAutores);

router.get("/:id", getAutorById);

router.post("/", authMiddleware, requireRole(["admin", "bibliotecario"]),createAutor);

router.put("/:id", authMiddleware, requireRole(["admin", "bibliotecario"]), updateAutor);

export default router;
