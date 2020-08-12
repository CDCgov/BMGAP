/*
 * Title: mongodb_aggregation_commands.js
 * Description:
 * Created by: ylb9 <ylb9@ncbs-dev-09.biotech.cdc.gov>
 * Created: 2019-05-09 11:22
 * Last Modified: Tue 18 Feb 2020 01:25:54 PM EST
 */

/* eslint-disable object-curly-newline */
// Aggregation for Samples by Year
const samplesByYearAgg = [
  { $match: { 'BML_Data.year': { $exists: 1 } } },
  { $group: { _id: '$BML_Data.year', total: { $sum: 1 } } },
  { $match: { _id: { $gt: '2013' } } },
  { $project: { _id: 0, year: '$_id', count: '$total' } },
  { $sort: { year: 1 } },
];

// Aggregation for Samples by Year
const locationByYearAgg = [
  { $match: { $and: [{ 'BML_Data.year': { $exists: 1 } }, { 'BML_Data.year': { $gt: '2013' } }], 'BML_Data.location': { $exists: 1 } } },
  { $group: { _id: { Location: '$BML_Data.location', Year: '$BML_Data.year' }, locCount: { $sum: 1 } } },
  { $sort: { locCount: -1 } },
  { $group: { _id: '$_id.Year', locations: { $push: { loc_name: '$_id.Location', count: '$locCount' } }, total: { $sum: '$locCount' } } },
  { $sort: { _id: 1 } },
];

// Aggregation for Serogroup by Year
const serogroupByYearAgg = [
  { $match: { Serogroup: { $exists: 1 }, BML_Data: { $exists: 1 }, 'BML_Data.year': { $gt: '2013' } } },
  { $group: { _id: { SG: '$Serogroup.SG', Year: '$BML_Data.year' }, seroCount: { $sum: 1 } } },
  { $group: { _id: '$_id.Year', SGs: { $push: { SG_name: '$_id.SG', count: '$seroCount' } }, total: { $sum: '$seroCount' } } },
  { $sort: { _id: 1 } },
];

// Aggregation for Serotype by Year
const serotypeByYearAgg = [
  { $match: { Serotype: { $exists: 1 }, BML_Data: { $exists: 1 }, 'BML_Data.year': { $gt: '2013' } } },
  { $group: { _id: { ST: '$Serotype.ST', Year: '$BML_Data.year' }, seroCount: { $sum: 1 } } },
  { $group: { _id: '$_id.Year', STs: { $push: { ST_name: '$_id.ST', count: '$seroCount' } }, total: { $sum: '$seroCount' } } },
  { $sort: { _id: 1 } },
];

// Aggregation for Hi & Nm samples by year
const speciesByYearAgg = [
  { $match: { $or: [{ 'mash.Top_Species': 'Neisseria_meningitidis' }, { 'mash.Top_Species': 'Haemophilus_influenzae' }], BML_Data: { $exists: 1 }, 'BML_Data.year': { $gt: '2013' } } },
  { $group: { _id: { Species: '$mash.Top_Species', Year: '$BML_Data.year' }, speciesCount: { $sum: 1 } } },
  { $group: { _id: '$_id.Year', Species: { $push: { species_name: '$_id.Species', count: '$speciesCount' } }, total: { $sum: '$speciesCount' } } },
  { $project: { _id: 0, Year: '$_id', Species: 1, total: 1 } },
  { $match: { Year: { $gt: '2013' } } },
  { $sort: { Year: 1 } },
];

// Aggregation for Hi & Nm samples by location
const speciesByLocationAgg = [
  { $match: { $or: [{ 'mash.Top_Species': 'Neisseria_meningitidis' }, { 'mash.Top_Species': 'Haemophilus_influenzae' }], BML_Data: { $exists: 1 }, 'BML_Data.year': { $gt: '2013' } } },
  { $group: { _id: { Species: '$mash.Top_Species', location: '$BML_Data.location' }, speciesCount: { $sum: 1 } } },
  { $group: { _id: '$_id.location', Species: { $push: { species_name: '$_id.Species', count: '$speciesCount' } }, total: { $sum: '$speciesCount' } } },
  { $sort: { total: -1 } },
];

// Aggregation for Serogroup by location
const serogroupByLocationAgg = [
  { $match: { Serogroup: { $exists: 1 }, BML_Data: { $exists: 1 }, 'BML_Data.year': { $gt: '2013' } } },
  { $group: { _id: { SG: '$Serogroup.SG', location: '$BML_Data.location' }, seroCount: { $sum: 1 } } },
  { $group: { _id: '$_id.location', SGs: { $push: { SG_name: '$_id.SG', count: '$seroCount' } }, total: { $sum: '$seroCount' } } },
  { $sort: { total: -1 } },
];

// Aggregation for Serotype by location
const serotypeByLocationAgg = [
  { $match: { Serotype: { $exists: 1 }, BML_Data: { $exists: 1 }, 'BML_Data.year': { $gt: '2013' } } },
  { $group: { _id: { ST: '$Serotype.ST', location: '$BML_Data.location' }, seroCount: { $sum: 1 } } },
  { $group: { _id: '$_id.location', STs: { $push: { ST_name: '$_id.ST', count: '$seroCount' } }, total: { $sum: '$seroCount' } } },
  { $sort: { total: -1 } },
];

module.exports = {
  samplesByYearAgg,
  serogroupByYearAgg,
  serotypeByYearAgg,
  speciesByYearAgg,
  locationByYearAgg,
  speciesByLocationAgg,
  serogroupByLocationAgg,
  serotypeByLocationAgg,
};
