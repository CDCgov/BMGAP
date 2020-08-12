/*
 * Title: sample_helpers.js
 * Description:
 * Created by: ylb9 <ylb9@ncbs-dev-09>
 * Created: 2019-07-26 12:12
 * Last Modified: Thu 31 Oct 2019 09:30:09 AM EDT
 */

const childProc = require('child_process');
const Sample = require('../models/Sample');
const SampleSummary = require('../models/SampleSummary');

const runQuery = (parsedQuery, res) => {
  const query = Sample.paginate(parsedQuery.query, {
    select: '-MLST_allele -location', sort: parsedQuery.sortField, page: parsedQuery.page, limit: parsedQuery.perPage,
  });
  query.then((data, err) => {
    if (err) {
      res.send(err);
    } else {
      res.json(data);
    }
  });
};
const runSummaryQuery = (parsedQuery, res) => {
  const query = SampleSummary.paginate(parsedQuery.query, {
    sort: parsedQuery.sortField, page: parsedQuery.page, limit: parsedQuery.perPage,
  });
  query.then((data, err) => {
    if (err) {
      res.send(err);
    } else {
      res.json(data);
    }
  });
};
const getAllSamples = (parsedQuery, res) => {
  const totalCount = Sample.countDocuments(parsedQuery.query);
  totalCount.then((data) => {
    parsedQuery.page = 1;
    parsedQuery.perPage = data;
    runQuery(parsedQuery, res);
  });
};
const getAllSampleSummaries = (parsedQuery, res) => {
  const totalCount = SampleSummary.countDocuments(parsedQuery.query);
  totalCount.then((data) => {
    parsedQuery.page = 1;
    parsedQuery.perPage = data;
    runSummaryQuery(parsedQuery, res);
  });
};
const runProgram = (command) => {
  const execute = childProc.execSync;
  const result = execute(command);
  const resultStr = result.toString();
  return resultStr;
};
const makeSampleQueryObj = (id) => {
  let criteria = {};
  if (id.match(/BM\d+/)) {
    criteria = { identifier: id };
  } else {
    criteria = { Lab_ID: { $regex: id } };
  }
  return criteria;
};
const processMashResults = (resultObj, mashData, submitter) => {
  const finalObj = {};
  finalObj.query = resultObj;
  finalObj.hits = [];
  resultObj.forEach((x) => {
    const record = mashData.find((y) => {
      if (submitter !== 'BML') {
        if (y._doc.Submitter !== submitter) {
          y._doc.Lab_ID = y._doc.identifier;
          y._doc.Assembly_ID = y._doc.identifier;
          y._doc.location = y._doc.country;
          y._doc.sample_type = '';
          if (y._doc.assemblyPath === x.hit) {
            x.hit = y._doc.identifier;
            return y;
          }
        }
        if (y._doc.assemblyPath === x.hit) {
          return y;
        }
      } else if (y._doc.assemblyPath === x.hit) {
        return y;
      }
      return null;
    });
    const distPercent = (1 - x.distance) * 100;
    record._doc.distance = Math.round(distPercent * 10000) / 10000;
    finalObj.hits.push(record);
  });
  return finalObj;
};
module.exports = {
  runQuery,
  runSummaryQuery,
  getAllSamples,
  getAllSampleSummaries,
  runProgram,
  processMashResults,
  makeSampleQueryObj,
};
