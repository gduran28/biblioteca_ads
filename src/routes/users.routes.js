import { Router } from "express";
import { getUsers, getUserById, updateUser, deactivateUser, activateUser } from "../controllers/users.controller.js";
import { authMiddleware } from "../middlewares/auth.middleware.js";
import { requireRole } from "../middlewares/role.middleware.js";

const router = Router();

router.get("/", authMiddleware, requireRole("admin"), getUsers);

router.get("/:id", authMiddleware, requireRole("admin"), getUserById);

router.put("/:id", authMiddleware, requireRole("admin"), updateUser);

router.delete("/:id", authMiddleware, requireRole("admin"), deactivateUser);

router.put("/:id/activate", authMiddleware, requireRole("admin"), activateUser);

export default router;