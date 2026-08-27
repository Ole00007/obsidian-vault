import { Router, Request, Response } from 'express';
import { pool } from '../db';
import { createPraticheRepository } from '\.\./\.\./\.\./\.\./packages/db/repositories/pratiche.repository';

const router = Router();
const praticheRepo = createPraticheRepository(pool);

// GET /api/pratiche
router.get('/', async (req: Request, res: Response) => {
  try {
    const owner_id = (req.query.owner_id as string) || 'admin';
    const pratiche = await praticheRepo.findAll(owner_id);
    res.json({ data: pratiche });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to fetch pratiche' });
  }
});

// GET /api/pratiche/:id
router.get('/:id', async (req: Request, res: Response) => {
  try {
    const owner_id = (req.query.owner_id as string) || 'admin';
    const pratica = await praticheRepo.findById(Number(req.params.id), owner_id);
    if (!pratica) return res.status(404).json({ error: 'Not found' });
    res.json({ data: pratica });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to fetch pratica' });
  }
});

// GET /api/pratiche/client/:client_id
router.get('/client/:client_id', async (req: Request, res: Response) => {
  try {
    const owner_id = (req.query.owner_id as string) || 'admin';
    const pratiche = await praticheRepo.findByClientId(Number(req.params.client_id), owner_id);
    res.json({ data: pratiche });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to fetch pratiche by client' });
  }
});

// POST /api/pratiche
router.post('/', async (req: Request, res: Response) => {
  try {
    const pratica = await praticheRepo.create({
      owner_id: req.body.owner_id || 'admin',
      ...req.body
    });
    res.status(201).json({ data: pratica });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to create pratica' });
  }
});

// PATCH /api/pratiche/:id
router.patch('/:id', async (req: Request, res: Response) => {
  try {
    const owner_id = (req.body.owner_id as string) || 'admin';
    const updated = await praticheRepo.update(Number(req.params.id), owner_id, req.body);
    if (!updated) return res.status(404).json({ error: 'Not found' });
    res.json({ data: updated });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to update pratica' });
  }
});

// DELETE /api/pratiche/:id
router.delete('/:id', async (req: Request, res: Response) => {
  try {
    const owner_id = (req.query.owner_id as string) || 'admin';
    const deleted = await praticheRepo.delete(Number(req.params.id), owner_id);
    if (!deleted) return res.status(404).json({ error: 'Not found' });
    res.json({ success: true });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to delete pratica' });
  }
});

export default router;
