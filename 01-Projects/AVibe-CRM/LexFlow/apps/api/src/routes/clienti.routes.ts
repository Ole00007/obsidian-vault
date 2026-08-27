import { Router, Request, Response } from 'express';
import { pool } from '../db';
import { createClientiRepository } from '\.\./\.\./\.\./\.\./packages/db/repositories/clienti.repository';

const router = Router();
const clientiRepo = createClientiRepository(pool);

// GET /api/clienti
router.get('/', async (req: Request, res: Response) => {
  try {
    const owner_id = (req.query.owner_id as string) || 'admin';
    const clienti = await clientiRepo.findAll(owner_id);
    res.json({ data: clienti });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to fetch clienti' });
  }
});

// GET /api/clienti/:id
router.get('/:id', async (req: Request, res: Response) => {
  try {
    const owner_id = (req.query.owner_id as string) || 'admin';
    const cliente = await clientiRepo.findById(Number(req.params.id), owner_id);
    if (!cliente) return res.status(404).json({ error: 'Not found' });
    res.json({ data: cliente });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to fetch cliente' });
  }
});

// POST /api/clienti
router.post('/', async (req: Request, res: Response) => {
  try {
    const cliente = await clientiRepo.create({
      owner_id: req.body.owner_id || 'admin',
      ...req.body
    });
    res.status(201).json({ data: cliente });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to create cliente' });
  }
});

// PATCH /api/clienti/:id
router.patch('/:id', async (req: Request, res: Response) => {
  try {
    const owner_id = (req.body.owner_id as string) || 'admin';
    const updated = await clientiRepo.update(Number(req.params.id), owner_id, req.body);
    if (!updated) return res.status(404).json({ error: 'Not found' });
    res.json({ data: updated });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to update cliente' });
  }
});

// DELETE /api/clienti/:id
router.delete('/:id', async (req: Request, res: Response) => {
  try {
    const owner_id = (req.query.owner_id as string) || 'admin';
    const deleted = await clientiRepo.delete(Number(req.params.id), owner_id);
    if (!deleted) return res.status(404).json({ error: 'Not found' });
    res.json({ success: true });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to delete cliente' });
  }
});

export default router;
