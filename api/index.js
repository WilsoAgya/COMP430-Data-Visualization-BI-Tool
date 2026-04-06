import express from 'express';
import cors from 'cors';
import pg from 'pg';


const app = express();

app.use(cors());

app.use(express.json());



const pool = new pg.Pool({
  user: 'redacted',
  host: 'redacted',
  database: 'redacted',
  password: 'redacted',
  port: 5432,
});



app.get('/api/tickers', async (req, res) => {
  try {
    const result = await pool.query('SELECT DISTINCT ticker_symbol, company_name FROM dim_ticker ORDER BY ticker_symbol ASC');
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});



app.get('/api/stocks/:symbol', async (req, res) => {
  const { symbol } = req.params;
  try {
    const query = `
      SELECT
        t.ticker_symbol as symbol,
        t.company_name as name,
        AVG(f.closing_price) as close,
        MIN(f.low_price) as low,
        AVG(f.open_price) as open,
        MAX(f.high_price) as high,
        SUM(f.revenue_total_actual) as revenue,
        TO_CHAR(date_trunc('hour', tm.full_date), 'Mon DD, HH24:00') as month,
        date_trunc('hour', tm.full_date) as hourB
      FROM facts_table f
      JOIN dim_ticker t ON f.ticker_id = t.ticker_id
      JOIN dim_time tm ON f.time_id = tm.time_key
      WHERE t.ticker_symbol = $1
        AND tm.full_date >= NOW() - INTERVAL '6 months'
      GROUP BY symbol, name, hourB
      ORDER BY hourB ASC;
    `;

    const ret = await pool.query(query, [symbol.toUpperCase()]);
    res.json(ret.rows);

  } catch (err) {
    res.status(500).json({ error: "Database query failed" });
  }
});
app.listen(3001, () => console.log('Backend running on http://localhost:3001'));