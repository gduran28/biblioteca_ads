import express from 'express';
import  librosRoutes from './src/routes/libros.routes.js';
const app = express();

app.get('/', (req, res) => {
  res.send('Hello, World!');
});

app.use('/libros', librosRoutes);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
