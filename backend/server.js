const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');

const app = express();
const port = 5000;

app.use(cors());

mongoose.connect('mongodb://localhost:27017/sportsbook', { useNewUrlParser: true, useUnifiedTopology: true });

const oddsSchema = new mongoose.Schema({
    sportsbook: String,
    odds: String
});

const Odd = mongoose.model('Odd', oddsSchema);

app.get('/odds', async (req, res) => {
    try {
        const odds = await Odd.find();
        res.json(odds);
    } catch (err) {
        res.status(500).send('Error fetching data');
    }
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});