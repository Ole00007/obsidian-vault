import { Pool } from 'pg';
import { config } from './config';

export const pool = new Pool({
  connectionString: config.databaseUrl,
  ssl: config.nodeEnv === 'production' ? { rejectUnauthorized: false } : false,
});

export async function testConnection(): Promise<void> {
  const client = await pool.connect();
  console.log('✅ Database connected successfully');
  client.release();
}
