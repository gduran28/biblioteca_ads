import { Router } from "express";
import { getUsers } from "../controllers/users.controller.js";
import { authMiddleware } from "../middlewares/auth.middleware.js";
import { requireRole } from "../middlewares/role.middleware.js";

const router = Router();

router.get("/", 
  authMiddleware,
  requireRole("admin"),
  getUsers
);

export default router;  