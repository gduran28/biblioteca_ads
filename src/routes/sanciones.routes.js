import { Router } from "express";
import { getSanciones, getSancionesByUser, pagarSancion } from "../controllers/sanciones.controller.js";

const router = Router();

router.get("/", getSanciones);
router.get("/usuario/:id", getSancionesByUser);
router.post("/pagar/:id", pagarSancion);

export default router;