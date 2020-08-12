const mongoose = require('mongoose');
const _ = require('lodash');
const SampleSummary = require('../models/SampleSummary');
const Run = require('../models/Run');
const constants = require('./constants');
mongoose.Promise = require('bluebird');


module.exports = (app) => {
  // Helper functions
  const getYears = (query) => {
    const startYear = Run.findOne(query, { _id: 0, date: 1 }).sort('date').limit(1);
    const endYear = Run.findOne(query, { _id: 0, date: 1 }).sort('-date').limit(1);
    return Promise.all([startYear, endYear]);
  };

  const getSpeciesFilters = (filterList) => {
    const neisIndex = filterList.indexOf('Neisseria_meningitidis');
    if (neisIndex !== -1) {
      filterList.splice(neisIndex, 1);
      filterList.unshift('Neisseria_meningitidis');
    }
    const haemoIndex = filterList.indexOf('Haemophilus_influenzae');
    if (haemoIndex !== -1) {
      filterList.splice(haemoIndex, 1);
      filterList.unshift('Haemophilus_influenzae');
    }
    return filterList;
  };

  const getSampleFilterQueries = (submitter) => {
    console.log(submitter);
    const sampleFilterQueries = [];
    const fields = constants.sampleFilterFields;
    const baseQuery = {};
    if (submitter) {
      baseQuery.Submitter = submitter;
    }
    fields.forEach((f) => {
      const filterValues = SampleSummary.find(baseQuery).distinct(f.id);
      sampleFilterQueries.push(filterValues);
    });
    return Promise.all(sampleFilterQueries);
  };

  const getRunFilterQueries = (submitter) => {
    const runFilterQueries = [];
    const fields = constants.runFilterFields;
    const baseQuery = { date: { $exists: true } };
    if (submitter) {
      baseQuery.Submitter = submitter;
    }
    fields.forEach((f) => {
      if (f.id !== 'date') {
        runFilterQueries.push(Run.find(baseQuery).distinct(f.id));
      } else {
        const yearArray = getYears(baseQuery);
        runFilterQueries.push(yearArray);
      }
    });
    return Promise.all(runFilterQueries);
  };

  const cleanArray = (array) => {
    const newArray = array.filter(n => n !== undefined && n !== null);
    const sortedArray = newArray.sort();
    return sortedArray;
  };

  const processSampleFilters = (data) => {
    const allFilters = {};
    Object.keys(data).forEach((d) => {
      if (constants.sampleFilterFields[d].display === 'mash-species') {
        const cleanedArray = cleanArray(data[d]);
        const filterValues = getSpeciesFilters(cleanedArray);
        allFilters[constants.sampleFilterFields[d].display] = filterValues;
      } else {
        allFilters[constants.sampleFilterFields[d].display] = cleanArray(data[d]);
      }
    });
    return allFilters;
  };

  const processRunFilters = (data) => {
    const allFilters = {};
    for (let d = 0; d < data.length; d += 1) {
      const varName = constants.runFilterFields[d].display;
      if (data[d][0] && data[d][0].date && constants.runFilterFields[d].id === 'date') {
        const startYear = data[d][0].date.getYear();
        const endYear = data[d][1].date.getYear();
        allFilters[varName] = _.range(startYear + 1900, endYear + 1901);
      } else {
        allFilters[varName] = cleanArray(data[d]);
      }
    }
    return allFilters;
  };

  /**
   * @swagger
   * /filters:
   *  get:
   *      description: Returns available filters
   *      produces:
   *          - application/json
   *      responses:
   *          200:
   *              description: OK
   *              schema:
   *                $ref: '#/definitions/filters'
   */

  app.get('/api/v1/filters', (req, res) => {
    console.log('Starting to look for filters');
    let submitter = '';
    if (req.query && req.query.filter && req.query.filter.state) {
      submitter = req.query.filter.state;
    }
    const sampleFilters = getSampleFilterQueries(submitter);
    sampleFilters.then((data) => {
      console.log(data);
      const filterObj = processSampleFilters(data);
      return filterObj;
    })
      .then((data) => {
        console.log(data);
        const sampleFilterObj = data;
        const runFilters = getRunFilterQueries(submitter);
        runFilters.then(runFiltersData => processRunFilters(runFiltersData))
          .then((runFilterObj) => {
            console.log(runFilterObj);
            const finalFilterObj = {
              samples: sampleFilterObj,
              runs: runFilterObj,
            };
            res.json(finalFilterObj);
          });
      });
  });

  /**
   * @swagger
   * /filters/samples:
   *  get:
   *      description: Returns available filters for samples
   *      produces:
   *          - application/json
   *      responses:
   *          200:
   *              description: OK
   *              schema:
   *                $ref: '#/definitions/filters/sample_filters'
   */

  app.get('/api/v1/filters/samples', (req, res) => {
    const sampleFilters = getSampleFilterQueries(req.query.Submitter);
    sampleFilters.then(processSampleFilters)
      .then(data => res.json(data));
  });

  /**
   * @swagger
   * /filters/runs:
   *  get:
   *      description: Returns available filters for runs
   *      produces:
   *          - application/json
   *      responses:
   *          200:
   *              description: OK
   *              schema:
   *                $ref: '#/definitions/filters/run_filters'
   */

  app.get('/api/v1/filters/runs', (req, res) => {
    const runFilters = getRunFilterQueries(req.query.Submitter);
    runFilters.then(processRunFilters)
      .then((data) => {
        res.json(data);
      });
  });
};
