const express = require('express');
const { exec } = require('child_process');
const path = require('path');
const app = express();

app.use(express.static(__dirname));

app.get('/peterWish', (req, res) => {
  res.sendFile(path.join(__dirname, 'wishPeter.html'));
});

app.get('/samWish', (req, res) => {
  res.sendFile(path.join(__dirname, 'wishSam.html'));
});

app.get('/searchSam', (req, res) => {
  const keyword = req.query.keyword;
  if (!keyword) return res.send("Please enter a keyword.");
  const cmd = `node topProductSam.js "${keyword}"`;
  exec(cmd, (err, stdout, stderr) => {
    if (err) {
      console.error(stderr);
      return res.send("Something went wrong.");
    }
    res.sendFile(path.join(__dirname, 'wishlist_search_sam.html'));
  });
});

app.get('/searchPeter', (req, res) => {
  const keyword = req.query.keyword;
  if (!keyword) return res.send("Please enter a keyword.");
  const cmd = `node topProductPeter.js "${keyword}"`;
  exec(cmd, (err, stdout, stderr) => {
    if (err) {
      console.error(stderr);
      return res.send("Something went wrong.");
    }
    res.sendFile(path.join(__dirname, 'wishlist_search_peter.html'));
  });
});

app.listen(3000, () => {
  console.log('✅ Server running at http://localhost:3000');
});
