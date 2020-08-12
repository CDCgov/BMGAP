/*
 * Title: SampleSummary.js
 * Description:
 * Created by: ylb9 <ylb9@ncbs-dev-09.biotech.cdc.gov>
 * Created: 2019-05-16 11:49
 * Last Modified: Mon 03 Jun 2019 09:15:03 AM EDT
 */
const mongoose = require('mongoose');
const paginator = require('mongoose-paginate');

const SampleSummary = mongoose.Schema({
  identifier: String,
  Lab_ID: String,
  Assembly_ID: String,
  Run_ID: String,
  QC_flagged: Boolean,
  Submitter: String,
  assemblyPath: String,
  MLST: String,
  cc: String,
  Serotype: String,
  Serogroup: String,
  Species: String,
  year: String,
  location: String,
  sample_type: String,
  sequencer: String,
}, { collection: 'sample_summary' });

SampleSummary.index({ identifier: 1 });
SampleSummary.index({ Lab_ID: 1 });
SampleSummary.index({ Assembly_ID: 1 });
SampleSummary.index({ Run_ID: 1 });
SampleSummary.index({ Submitter: 1 });
SampleSummary.index({ assemblyPath: 1 });
SampleSummary.index({ MLST: 1 });
SampleSummary.index({ cc: 1 });
SampleSummary.index({ Serotype: 1 });
SampleSummary.index({ Species: 1 });
SampleSummary.index({ year: 1 });
SampleSummary.index({ location: 1 });
SampleSummary.index({ sample_type: 1 });
SampleSummary.index({ sequencer: 1 });
SampleSummary.index({ identifier: -1 });
SampleSummary.index({ Lab_ID: -1 });
SampleSummary.index({ Assembly_ID: -1 });
SampleSummary.index({ Run_ID: -1 });
SampleSummary.index({ Submitter: -1 });
SampleSummary.index({ assemblyPath: -1 });
SampleSummary.index({ MLST: -1 });
SampleSummary.index({ cc: -1 });
SampleSummary.index({ Serotype: -1 });
SampleSummary.index({ Species: -1 });
SampleSummary.index({ year: -1 });
SampleSummary.index({ location: -1 });
SampleSummary.index({ sample_type: -1 });
SampleSummary.index({ sequencer: -1 });
SampleSummary.plugin(paginator);
module.exports = mongoose.model('SampleSummary', SampleSummary);
