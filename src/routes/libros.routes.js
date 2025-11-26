import { Router } from "express";
import { getLibros, getLibroByISBN } from "../controllers/libros.controller.js";

const router = Router();

router.get("/", getLibros);

router.get("/:isbn", getLibroByISBN);

export default router;