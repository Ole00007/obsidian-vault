import { Router, Request, Response } from 'express';
import { pool } from '../db';
import { createRegistroRepository } from '\.\./\.\./\.\./\.\./packages/db/repositories/registro.repository';

const router = Router();
const registroRepo = createRegistroRepository(pool);

// GET /api/registro
router.get('/', async (req: Request, res: Response) => {
  try {
    const owner_id = (req.query.owner_id as string) || 'admin';
    const entries = await registroRepo.findAll(owner_id);
    res.json({ data: entries });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to fetch registro' });
  }
});

// GET /api/registro/:entity_type/:entity_id
router.get('/:entity_type/:entity_id', async (req: Request, res: Response) => {
  try {
    const owner_id = (req.query.owner_id as string) || 'admin';
    const entries = await registroRepo.findByEntity(
      req.params.entity_type,
      Number(req.params.entity_id),
      owner_id
    );
    res.json({ data: entries });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to fetch registro by entity' });
  }
});

// POST /api/registro
router.post('/', async (req: Request, res: Response) => {
  try {
    const entry = await registroRepo.log({
      owner_id: req.body.owner_id || 'admin',
      ...req.body
    });
    res.status(201).json({ data: entry });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to log registro entry' });
  }
});

export default router;
