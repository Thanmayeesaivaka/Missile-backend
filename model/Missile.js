const mongoose = require('mongoose');

const missileSchema = new mongoose.Schema({
  title: String,
  content: String,
  category: String
});

module.exports = mongoose.model('Missile', missileSchema);
