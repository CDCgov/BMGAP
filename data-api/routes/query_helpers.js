/*
 * Title: query_helpers.js
 * Description:
 * Created by: ylb9 <ylb9@ncbs-dev-09.biotech.cdc.gov>
 * Created: 2019-02-12 09:23
 * Last Modified: Wed 18 Mar 2020 02:50:25 PM EDT
 */

const getIdQuery = (searchTerm) => {
  // console.log(`get IDs from ${searchTerm}`);
  // const idList = searchTerm.split(',');
  const idQueryList = [];
  let idQuery = [];
  if (searchTerm.indexOf(',') !== -1) {
    const termList = searchTerm.split(',');
    if (termList[0] === /^BM\d+/) {
      idQuery = { identifier: { $in: termList } };
    }
  } else {
    searchTerm.forEach((idValue) => {
      idQueryList.push({ Lab_ID: { $regex: new RegExp(idValue) } });
      idQueryList.push({ Assembly_ID: { $regex: new RegExp(idValue) } });
      idQueryList.push({ Run_ID: { $regex: new RegExp(idValue) } });
    });
    idQuery = {
      $or: idQueryList,
    };
  }
  return idQuery;
};

const getIdQueryFromFile = (searchTerm) => {
  // console.log(`get IDs from ${searchTerm}`);
  // const idList = searchTerm.split(',');
  const idQueryList = [];
  let idQuery = [];
  searchTerm.forEach((idValue) => {
    if (idValue !== '') {
      idQueryList.push({ Lab_ID: { $regex: new RegExp(idValue) } });
      idQueryList.push({ Assembly_ID: { $regex: new RegExp(idValue) } });
    }
  });
  idQuery = {
    $or: idQueryList,
  };
  return idQuery;
};

const parseFilter = (filterObj) => {
  const querySet = [];
  const filter = JSON.parse(filterObj);
  // console.log(JSON.parse(filterObj));
  if (filter.runs && filter.runs.length > 0) {
    querySet.push({ Run_ID: { $in: filter.runs } });
  }
  if (filter.mashSpecies && filter.mashSpecies.length > 0) {
    querySet.push({ Species: { $in: filter.mashSpecies } });
  }
  if (filter.serogrouping && filter.serogrouping.length > 0) {
    querySet.push({ Serogroup: { $in: filter.serogrouping } });
  }
  if (filter.serotyping && filter.serotyping.length > 0) {
    querySet.push({ Serotype: { $in: filter.serotyping } });
  }
  if (filter.state && filter.state.length > 0) {
    querySet.push({ Submitter: { $in: filter.state } });
  }
  if (filter.location && filter.location.length > 0) {
    querySet.push({ location: { $in: filter.location } });
  }
  if (filter.sequencer && filter.sequencer.length > 0) {
    querySet.push({ sequencer: { $in: filter.sequencer } });
  }
  if (filter.identifiers && filter.identifiers.length > 0) {
    // console.log(filter.identifiers);
    const identifierObj = getIdQuery(filter.identifiers);
    querySet.push(identifierObj);
  }
  return querySet;
};

const parseSortField = (sortField) => {
  let isNeg = false;
  let newSortField = null;
  if (sortField.charAt(0) === '-') {
    isNeg = true;
    newSortField = sortField.substr(1);
  }
  if (sortField === 'PMGATyping.Serotype[0].predicted_st') {
    newSortField = 'PMGATyping.Serotype.predicted_st';
  } else if (sortField === 'PMGATyping.Serogroup[0].predicted_sg') {
    newSortField = 'PMGATyping.Serogroup.predicted_sg';
  }
  if (isNeg) {
    newSortField = String.prototype.concat('-', sortField);
  }
  return newSortField;
};

const parseSamplesQuery = (query) => {
  // console.log(query);
  const parsedQuery = {
    perPage: 50,
    page: 1,
    sortField: '',
    query: {},
  };
  const pageNumber = query.page;
  if (query.perPage) {
    if (query.perPage === 'all') {
      parsedQuery.perPage = 'all';
    } else {
      parsedQuery.perPage = parseInt(query.perPage, 10);
    }
  }
  if (pageNumber === null) {
    parsedQuery.page = 1;
  } else {
    parsedQuery.page = pageNumber;
  }
  if (query.sortField) {
    if (query.sortField === '-') {
      parsedQuery.sortField = 'identifier';
    } else {
      parsedQuery.sortField = parseSortField(query.sortField);
    }
  } else {
    parsedQuery.sortField = '-identifier';
  }
  let querySet = [];
  if (query.filter && query.filter !== 'none') {
    querySet = parseFilter(query.filter);
  } else {
    querySet = [];
  }
  if (query.filter && query.filter.state && query.filter.state !== '') {
    const submitterQuery = { Submitter: { $in: query.filter.state } };
    querySet.push(submitterQuery);
  } else if (query.submitter && query.submitter !== '') {
    const submitterQuery = { Submitter: { $in: query.submitter.split(',') } };
    querySet.push(submitterQuery);
  }
  if (querySet && querySet.length > 0) {
    if (querySet.length > 1) {
      parsedQuery.query = { $and: querySet };
    } else {
      [parsedQuery.query] = querySet;
      if (querySet[0].Run_ID && querySet[0].Run_ID.$in.length === 1) {
        if (parsedQuery.sortField && parsedQuery.sortField.match(/identifier$/)) {
          parsedQuery.sortField = 'sample_order';
        }
      }
    }
  } else {
    parsedQuery.query = {};
  }
  return parsedQuery;
};


const parseRunsQuery = (query) => {
  // console.log(query);
  const parsedQuery = {
    perPage: 5,
    page: 1,
    query: {},
  };
  const pageNumber = query.page;
  if (query.perPage) {
    if (query.perPage === 'all') {
      parsedQuery.perPage = 'all';
    } else {
      parsedQuery.perPage = parseInt(query.perPage, 10);
    }
  }
  if (pageNumber !== null) {
    parsedQuery.page = pageNumber;
  }
  const querySet = [];
  if (query.filter && query.filter.state && query.filter.state !== '') {
    const submitterQuery = { submitter: { $in: query.filter.state } };
    querySet.push(submitterQuery);
  } else if (query.submitter && query.submitter !== '') {
    const submitterQuery = { submitter: { $in: query.submitter.split(',') } };
    querySet.push(submitterQuery);
  }
  if (query.sequencer && query.sequencer !== '') {
    const sequencerQuery = { sequencer: { $in: query.sequencer.split(',') } };
    querySet.push(sequencerQuery);
  }
  if (query.start_year && query.start_year !== null) {
    const startYearDateObj = new Date(query.start_year, 1, 1);
    querySet.push({ date: { $gte: startYearDateObj.toISOString() } });
  }
  if (query.end_year && query.end_year !== null) {
    const endYearDateObj = new Date(query.end_year, 11, 31);
    querySet.push({ date: { $lte: endYearDateObj.toISOString() } });
  }
  if (querySet.length > 0) {
    if (querySet.length === 1) {
      [parsedQuery.query] = querySet;
    } else {
      parsedQuery.query = { $and: querySet };
    }
  }
  return parsedQuery;
};

const send404Error = (res, queryObj) => {
  const errorMessage = { error: 404, message: 'Query returned no results', query: queryObj };
  return errorMessage;
};

module.exports = {
  parseFilter,
  parseSamplesQuery,
  parseRunsQuery,
  send404Error,
  getIdQueryFromFile,
  getIdQuery,
};
