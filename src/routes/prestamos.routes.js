import { Router } from "express";
import { createPrestamo, getPrestamos, getPrestamosById, getPrestamosByUserId, devolverLibro } from "../controllers/prestamos.controller.js";
import { authMiddleware } from "../middlewares/auth.middleware.js";
import { requireRole } from "../middlewares/role.middleware.js";

const router = Router();

router.get("/", authMiddleware, requireRole(["admin", "user"]), getPrestamos);
router.get("/:id", authMiddleware, requireRole(["admin", "user"]), getPrestamosById);
router.get("/usuario/:userId", authMiddleware, requireRole(["admin", "user"]), getPrestamosByUserId);
router.post("/", authMiddleware, requireRole(["admin", "user"]), createPrestamo);
router.put("/devolver/:id", authMiddleware, requireRole(["admin", "user"]), devolverLibro);

export default router;