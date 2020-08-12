/*
 * Title: analytics.js
 * Description: routes to return analytics about BMGAP data
 * Created by: ylb9 <ylb9@ncbs-dev-09>
 * Created: 2019-08-26 11:15
 * Last Modified: Wed 18 Mar 2020 02:50:51 PM EDT
 */

const mongoose = require('mongoose');
const analyticsQueries = require('../mongodb_aggregation_commands');
const Sample = require('../models/Sample');
mongoose.Promise = require('bluebird');

module.exports = (app) => {
  app.get('/api/v1/analytics/samples', (req, res) => {
    const query = Sample.aggregate(analyticsQueries.samplesByYearAgg);
    query.then((data, err) => {
      if (err) {
        res.send(err);
      }
      res.send(data);
    });
  });
  app.get('/api/v1/analytics/species', (req, res) => {
    const query = Sample.aggregate(analyticsQueries.speciesByYearAgg);
    query.then((data, err) => {
      if (err) {
        res.send(err);
      }
      res.send(data);
    });
  });
  app.get('/api/v1/analytics/serogroup', (req, res) => {
    const query = Sample.aggregate(analyticsQueries.serogroupByYearAgg);
    query.then((data, err) => {
      if (err) {
        res.send(err);
      }
      res.send(data);
    });
  });
  app.get('/api/v1/analytics/serotype', (req, res) => {
    const query = Sample.aggregate(analyticsQueries.serotypeByYearAgg);
    query.then((data, err) => {
      if (err) {
        res.send(err);
      }
      res.send(data);
    });
  });
  app.get('/api/v1/analytics/locationByYear', (req, res) => {
    const query = Sample.aggregate(analyticsQueries.locationByYearAgg);
    query.then((data, err) => {
      if (err) {
        res.send(err);
      }
      res.send(data);
    });
  });
  app.get('/api/v1/analytics/speciesByLocation', (req, res) => {
    const query = Sample.aggregate(analyticsQueries.speciesByLocationAgg);
    query.then((data, err) => {
      if (err) {
        res.send(err);
      }
      res.send(data);
    });
  });
  app.get('/api/v1/analytics/serotypeByLocation', (req, res) => {
    const query = Sample.aggregate(analyticsQueries.serotypeByLocationAgg);
    query.then((data, err) => {
      if (err) {
        res.send(err);
      }
      res.send(data);
    });
  });
  app.get('/api/v1/analytics/serogroupByLocation', (req, res) => {
    const query = Sample.aggregate(analyticsQueries.serogroupByLocationAgg);
    query.then((data, err) => {
      if (err) {
        res.send(err);
      }
      res.send(data);
    });
  });
  app.get('/api/v1/analytics', (req, res) => {
    const analyticsResults = {};
    const samplesQuery = Sample.aggregate(analyticsQueries.samplesByYearAgg);
    const speciesQuery = Sample.aggregate(analyticsQueries.speciesByYearAgg);
    const serogroupQuery = Sample.aggregate(analyticsQueries.serogroupByYearAgg);
    const serotypeQuery = Sample.aggregate(analyticsQueries.serotypeByYearAgg);
    const locationByYearQuery = Sample.aggregate(analyticsQueries.locationByYearAgg);
    const speciesByLocationQuery = Sample.aggregate(analyticsQueries.speciesByLocationAgg);
    const serogroupByLocationQuery = Sample.aggregate(analyticsQueries.serogroupByLocationAgg);
    const serotypeByLocationQuery = Sample.aggregate(analyticsQueries.serotypeByLocationAgg);
    Promise.all([samplesQuery, speciesQuery, serogroupQuery, serotypeQuery, speciesByLocationQuery,
      serogroupByLocationQuery, serotypeByLocationQuery, locationByYearQuery]).then((values) => {
      /* eslint-disable prefer-destructuring */
      analyticsResults.samples = values[0];
      analyticsResults.species = values[1];
      analyticsResults.serogroups = values[2];
      analyticsResults.serotypes = values[3];
      analyticsResults.speciesByLocation = values[4];
      analyticsResults.serogroupByLocation = values[5];
      analyticsResults.serotypeByLocation = values[6];
      analyticsResults.locationByYear = values[7];
      res.send(analyticsResults);
    });
  });
};
