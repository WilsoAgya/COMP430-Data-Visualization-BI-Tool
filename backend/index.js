import express from 'express';
import cors from 'cors';
import axios from 'axios';

const app = express();
app.use(cors());
app.use(express.json());

const PYTHON_API = 'http://127.0.0.1:8000';

app.get('/api/tickers', async (req, res) => {
  try {
    const { data } = await axios.get(`${PYTHON_API}/tickers`);
    res.json(data);
  } catch (err) {
    res.status(500).send("Python Down");
  }
});

app.get('/api/stocks/:symbol', async (req, res) => {
  try {
    const { data } = await axios.get(`${PYTHON_API}/stocks/${req.params.symbol}`);
    res.json(data);
  } catch (err) {
    res.status(500).send("Python Down");
  }
});

app.listen(3001);
