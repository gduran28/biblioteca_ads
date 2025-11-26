import { Router } from "express";
import { login, register, getProfile } from "../controllers/auth.controller.js";
import { authMiddleware } from "../middlewares/auth.middleware.js";

const router = Router();

router.post("/login", login);
router.post("/register", register);
router.get("/me", authMiddleware, getProfile);

export default router;