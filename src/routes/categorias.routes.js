import { Router } from 'express';
import {
  getCategorias,
  getCategoriaById,
  createCategoria,
  updateCategoria,
} from '../controllers/categorias.controller.js';
import { authMiddleware } from '../middlewares/auth.middleware.js';
import { requireRole } from '../middlewares/role.middleware';

const router = Router();

router.get('/', getCategorias);
router.get('/:id', getCategoriaById);
router.post('/', authMiddleware, requireRole(["admin", "bibliotecario"]), createCategoria);
router.put('/:id', authMiddleware, requireRole(["admin", "bibliotecario"]), updateCategoria);

export default router;