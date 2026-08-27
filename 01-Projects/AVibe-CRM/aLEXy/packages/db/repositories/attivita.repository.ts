import { Pool } from 'pg';

export interface Attivita {
  id?: number;
  pratica_id?: number;
  client_id?: number;
  owner_id: string;
  tipo: string;
  descrizione?: string;
  data_attivita?: Date;
  completata?: boolean;
  created_at?: Date;
}

export function createAttivitaRepository(pool: Pool) {
  return {
    async findAll(owner_id: string): Promise<Attivita[]> {
      const res = await pool.query(
        'SELECT * FROM attivita WHERE owner_id = $1 ORDER BY data_attivita DESC',
        [owner_id]
      );
      return res.rows;
    },

    async findByPraticaId(pratica_id: number, owner_id: string): Promise<Attivita[]> {
      const res = await pool.query(
        'SELECT * FROM attivita WHERE pratica_id = $1 AND owner_id = $2 ORDER BY data_attivita DESC',
        [pratica_id, owner_id]
      );
      return res.rows;
    },

    async findByClientId(client_id: number, owner_id: string): Promise<Attivita[]> {
      const res = await pool.query(
        'SELECT * FROM attivita WHERE client_id = $1 AND owner_id = $2 ORDER BY data_attivita DESC',
        [client_id, owner_id]
      );
      return res.rows;
    },

    async findById(id: number, owner_id: string): Promise<Attivita | null> {
      const res = await pool.query(
        'SELECT * FROM attivita WHERE id = $1 AND owner_id = $2',
        [id, owner_id]
      );
      return res.rows[0] || null;
    },

    async create(data: Attivita): Promise<Attivita> {
      const res = await pool.query(
        `INSERT INTO attivita (pratica_id, client_id, owner_id, tipo, descrizione, data_attivita, completata)
         VALUES ($1, $2, $3, $4, $5, $6, $7)
         RETURNING *`,
        [data.pratica_id || null, data.client_id || null, data.owner_id,
         data.tipo, data.descrizione || null,
         data.data_attivita || new Date(), data.completata ?? false]
      );
      return res.rows[0];
    },

    async markComplete(id: number, owner_id: string): Promise<Attivita | null> {
      const res = await pool.query(
        `UPDATE attivita SET completata = true
         WHERE id = $1 AND owner_id = $2
         RETURNING *`,
        [id, owner_id]
      );
      return res.rows[0] || null;
    },

    async delete(id: number, owner_id: string): Promise<boolean> {
      const res = await pool.query(
        'DELETE FROM attivita WHERE id = $1 AND owner_id = $2',
        [id, owner_id]
      );
      return (res.rowCount ?? 0) > 0;
    }
  };
}
