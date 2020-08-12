/*
 * Title: Runs.js
 * Description:
 * Created by: ylb9 <ylb9@ncbs-dev-09.biotech.cdc.gov>
 * Created: 2019-02-11 18:12
 * Last Modified: Mon 11 Feb 2019 06:55:23 PM EST
 */
const mongoose = require('mongoose');
const paginator = require('mongoose-paginate');

const Runs = mongoose.Schema({
  run: String,
  samples: Number,
  date: Date,
  sequencer: String,
}, { collection: 'runs' });

Runs.index({ run: 1 });
Runs.index({ date: 1 });
Runs.index({ sequencer: 1 });
Runs.plugin(paginator);
module.exports = mongoose.model('Runs', Runs);
