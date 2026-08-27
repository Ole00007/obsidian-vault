import { Pool } from 'pg';

export interface RegistroEntry {
  id?: number;
  owner_id: string;
  entity_type: string;
  entity_id: number;
  azione: string;
  dettagli?: Record<string, unknown>;
  created_at?: Date;
}

export function createRegistroRepository(pool: Pool) {
  return {
    async findAll(owner_id: string): Promise<RegistroEntry[]> {
      const res = await pool.query(
        'SELECT * FROM registro WHERE owner_id = $1 ORDER BY created_at DESC',
        [owner_id]
      );
      return res.rows;
    },

    async findByEntity(entity_type: string, entity_id: number, owner_id: string): Promise<RegistroEntry[]> {
      const res = await pool.query(
        `SELECT * FROM registro
         WHERE entity_type = $1 AND entity_id = $2 AND owner_id = $3
         ORDER BY created_at DESC`,
        [entity_type, entity_id, owner_id]
      );
      return res.rows;
    },

    async log(data: RegistroEntry): Promise<RegistroEntry> {
      const res = await pool.query(
        `INSERT INTO registro (owner_id, entity_type, entity_id, azione, dettagli)
         VALUES ($1, $2, $3, $4, $5)
         RETURNING *`,
        [data.owner_id, data.entity_type, data.entity_id,
         data.azione, data.dettagli ? JSON.stringify(data.dettagli) : null]
      );
      return res.rows[0];
    }
  };
}
