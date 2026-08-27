import { Pool } from 'pg';

export interface Cliente {
  id?: number;
  owner_id: string;
  nome: string;
  email?: string;
  telefono?: string;
  azienda?: string;
  status?: string;
  tags?: string[];
  note?: string;
  created_at?: Date;
  updated_at?: Date;
}

export function createClientiRepository(pool: Pool) {
  return {
    async findAll(owner_id: string): Promise<Cliente[]> {
      const res = await pool.query(
        'SELECT * FROM clienti WHERE owner_id = $1 ORDER BY created_at DESC',
        [owner_id]
      );
      return res.rows;
    },

    async findById(id: number, owner_id: string): Promise<Cliente | null> {
      const res = await pool.query(
        'SELECT * FROM clienti WHERE id = $1 AND owner_id = $2',
        [id, owner_id]
      );
      return res.rows[0] || null;
    },

    async create(data: Cliente): Promise<Cliente> {
      const res = await pool.query(
        `INSERT INTO clienti (owner_id, nome, email, telefono, azienda, status, tags, note)
         VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
         RETURNING *`,
        [data.owner_id, data.nome, data.email, data.telefono,
         data.azienda, data.status || 'lead', data.tags || [], data.note]
      );
      return res.rows[0];
    },

    async update(id: number, owner_id: string, data: Partial<Cliente>): Promise<Cliente | null> {
      const res = await pool.query(
        `UPDATE clienti SET
           nome = COALESCE($3, nome),
           email = COALESCE($4, email),
           telefono = COALESCE($5, telefono),
           azienda = COALESCE($6, azienda),
           status = COALESCE($7, status),
           tags = COALESCE($8, tags),
           note = COALESCE($9, note),
           updated_at = now()
         WHERE id = $1 AND owner_id = $2
         RETURNING *`,
        [id, owner_id, data.nome, data.email, data.telefono,
         data.azienda, data.status, data.tags, data.note]
      );
      return res.rows[0] || null;
    },

    async delete(id: number, owner_id: string): Promise<boolean> {
      const res = await pool.query(
        'DELETE FROM clienti WHERE id = $1 AND owner_id = $2',
        [id, owner_id]
      );
      return (res.rowCount ?? 0) > 0;
    }
  };
}
