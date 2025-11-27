import express from 'express';
import librosRoutes from './src/routes/libros.routes.js';
import authRoutes from './src/routes/auth.routes.js';
import userRoutes from './src/routes/users.routes.js';
import autoresRoutes from './src/routes/autores.routes.js';
import categoriasRoutes from './src/routes/categorias.routes.js';
import prestamosRoutes from './src/routes/prestamos.routes.js';
import cors from 'cors';
const app = express();

app.use(express.json());
app.use(cors());

app.get('/', (req, res) => {
  res.send('Biblioteca!');
});

app.use('/libros', librosRoutes);
app.use('/auth', authRoutes);
app.use('/users', userRoutes); 
app.use("/autores", autoresRoutes)
app.use("/categorias", categoriasRoutes);
app.use("/prestamos", prestamosRoutes);

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
