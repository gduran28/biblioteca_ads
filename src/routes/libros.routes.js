import { Router } from "express";
import { getLibros, getLibroByISBN, createLibro, updateLibro, deactivateLibro, activateLibro } from "../controllers/libros.controller.js";
import { authMiddleware } from "../middlewares/auth.middleware.js";
import { requireRole } from "../middlewares/role.middleware.js";
const router = Router();

router.get("/", getLibros);

router.get("/:isbn", getLibroByISBN);

router.post("/", authMiddleware, requireRole("admin"), createLibro);

router.put("/:isbn", authMiddleware, requireRole("admin"), updateLibro);

router.delete("/:isbn", authMiddleware, requireRole("admin"), deactivateLibro);

router.put("/:isbn/activate", authMiddleware, requireRole("admin"), activateLibro);

export default router;