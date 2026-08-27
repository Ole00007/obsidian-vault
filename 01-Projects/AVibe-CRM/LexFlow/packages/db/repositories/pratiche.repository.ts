import { Pool } from 'pg';

export interface Pratica {
  id?: number;
  client_id: number;
  owner_id: string;
  titolo: string;
  valore_stimato?: number;
  fase?: string;
  scadenza?: Date;
  created_at?: Date;
  updated_at?: Date;
}

export function createPraticheRepository(pool: Pool) {
  return {
    async findAll(owner_id: string): Promise<Pratica[]> {
      const res = await pool.query(
        'SELECT * FROM pratiche WHERE owner_id = $1 ORDER BY created_at DESC',
        [owner_id]
      );
      return res.rows;
    },

    async findByClientId(client_id: number, owner_id: string): Promise<Pratica[]> {
      const res = await pool.query(
        'SELECT * FROM pratiche WHERE client_id = $1 AND owner_id = $2 ORDER BY created_at DESC',
        [client_id, owner_id]
      );
      return res.rows;
    },

    async findById(id: number, owner_id: string): Promise<Pratica | null> {
      const res = await pool.query(
        'SELECT * FROM pratiche WHERE id = $1 AND owner_id = $2',
        [id, owner_id]
      );
      return res.rows[0] || null;
    },

    async create(data: Pratica): Promise<Pratica> {
      const res = await pool.query(
        `INSERT INTO pratiche (client_id, owner_id, titolo, valore_stimato, fase, scadenza)
         VALUES ($1, $2, $3, $4, $5, $6)
         RETURNING *`,
        [data.client_id, data.owner_id, data.titolo,
         data.valore_stimato || null, data.fase || 'nuovo_incarico', data.scadenza || null]
      );
      return res.rows[0];
    },

    async update(id: number, owner_id: string, data: Partial<Pratica>): Promise<Pratica | null> {
      const res = await pool.query(
        `UPDATE pratiche SET
           titolo = COALESCE($3, titolo),
           valore_stimato = COALESCE($4, valore_stimato),
           fase = COALESCE($5, fase),
           scadenza = COALESCE($6, scadenza),
           updated_at = now()
         WHERE id = $1 AND owner_id = $2
         RETURNING *`,
        [id, owner_id, data.titolo, data.valore_stimato, data.fase, data.scadenza]
      );
      return res.rows[0] || null;
    },

    async delete(id: number, owner_id: string): Promise<boolean> {
      const res = await pool.query(
        'DELETE FROM pratiche WHERE id = $1 AND owner_id = $2',
        [id, owner_id]
      );
      return (res.rowCount ?? 0) > 0;
    }
  };
}
