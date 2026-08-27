import express from 'express';
import cors from 'cors';
import { config } from './config';
import { testConnection } from './db';
import clientiRoutes from './routes/clienti.routes';
import praticheRoutes from './routes/pratiche.routes';
import attivitaRoutes from './routes/attivita.routes';
import registroRoutes from './routes/registro.routes';

const app = express();

app.use(cors());
app.use(express.json());

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', env: config.nodeEnv });
});

// Routes
app.use('/api/clienti', clientiRoutes);
app.use('/api/pratiche', praticheRoutes);
app.use('/api/attivita', attivitaRoutes);
app.use('/api/registro', registroRoutes);

// Start
app.listen(config.port, async () => {
  console.log(`🚀 API running on port ${config.port}`);
  await testConnection();
});

export default app;
