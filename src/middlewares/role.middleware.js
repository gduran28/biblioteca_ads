export const requireRole = (roles = []) => {
  return (req, res, next) => {
    const allowed = Array.isArray(roles) ? roles : [roles];

    if(!req.user) {
      return res.status(401).json({ error: "Usuario no autenticado." });
    }

    if(!allowed.includes(req.user.rol)) {
      return res.status(403).json({ error: "Acceso denegado." });
    }

    next();
  }
}