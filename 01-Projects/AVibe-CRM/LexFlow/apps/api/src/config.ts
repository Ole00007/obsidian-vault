export const config = {
  port: process.env.PORT ? parseInt(process.env.PORT) : 3001,
  databaseUrl: process.env.DATABASE_URL || '',
  nodeEnv: process.env.NODE_ENV || 'development',
  resendApiKey: process.env.RESEND_API_KEY || '',
};
