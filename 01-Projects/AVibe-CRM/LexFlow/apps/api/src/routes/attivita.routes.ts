import { Router, Request, Response } from 'express';
import { pool } from '../db';
import { createAttivitaRepository } from '\.\./\.\./\.\./\.\./packages/db/repositories/attivita.repository';

const router = Router();
const attivitaRepo = createAttivitaRepository(pool);

// GET /api/attivita
router.get('/', async (req: Request, res: Response) => {
  try {
    const owner_id = (req.query.owner_id as string) || 'admin';
    const attivita = await attivitaRepo.findAll(owner_id);
    res.json({ data: attivita });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to fetch attivita' });
  }
});

// GET /api/attivita/:id
router.get('/:id', async (req: Request, res: Response) => {
  try {
    const owner_id = (req.query.owner_id as string) || 'admin';
    const attivita = await attivitaRepo.findById(Number(req.params.id), owner_id);
    if (!attivita) return res.status(404).json({ error: 'Not found' });
    res.json({ data: attivita });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to fetch attivita item' });
  }
});

// GET /api/attivita/pratica/:pratica_id
router.get('/pratica/:pratica_id', async (req: Request, res: Response) => {
  try {
    const owner_id = (req.query.owner_id as string) || 'admin';
    const attivita = await attivitaRepo.findByPraticaId(Number(req.params.pratica_id), owner_id);
    res.json({ data: attivita });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to fetch attivita by pratica' });
  }
});

// GET /api/attivita/client/:client_id
router.get('/client/:client_id', async (req: Request, res: Response) => {
  try {
    const owner_id = (req.query.owner_id as string) || 'admin';
    const attivita = await attivitaRepo.findByClientId(Number(req.params.client_id), owner_id);
    res.json({ data: attivita });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to fetch attivita by client' });
  }
});

// POST /api/attivita
router.post('/', async (req: Request, res: Response) => {
  try {
    const attivita = await attivitaRepo.create({
      owner_id: req.body.owner_id || 'admin',
      ...req.body
    });
    res.status(201).json({ data: attivita });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to create attivita' });
  }
});

// PATCH /api/attivita/:id/complete
router.patch('/:id/complete', async (req: Request, res: Response) => {
  try {
    const owner_id = (req.body.owner_id as string) || 'admin';
    const updated = await attivitaRepo.markComplete(Number(req.params.id), owner_id);
    if (!updated) return res.status(404).json({ error: 'Not found' });
    res.json({ data: updated });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to complete attivita' });
  }
});

// DELETE /api/attivita/:id
router.delete('/:id', async (req: Request, res: Response) => {
  try {
    const owner_id = (req.query.owner_id as string) || 'admin';
    const deleted = await attivitaRepo.delete(Number(req.params.id), owner_id);
    if (!deleted) return res.status(404).json({ error: 'Not found' });
    res.json({ success: true });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to delete attivita' });
  }
});

export default router;
