import express from 'express';
import cors from 'cors';
import axios from 'axios';

const back = express();
back.use(cors());
back.use(express.json());


back.get('/api/tickers', async (request, response) => {
  try {
    const {data: res} = await axios.get(`http://127.0.0.1:8000/tickers`);
    response.json(res);
  } catch (er) {
    response.status(500).send(`Error: ${er.message}`);
  }
});

back.get('/api/stocks/:symbol', async (request, response) => {
  try {
    const str = request.params.symbol
    const {data: res} = await axios.get(`http://127.0.0.1:8000/stocks/${str}`);
    response.json(res);
  } catch (er) {
    response.status(500).send(`Error: ${er.message}`);
  }
});

back.listen(3001);
