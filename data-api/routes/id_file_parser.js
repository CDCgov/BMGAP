const fs = require('fs');
const queryHelpers = require('./query_helpers.js');
/* eslint-disable no-console */

const getListFromIdFile = (inputFile) => {
  const idList = fs.readFileSync(inputFile.path, { encoding: 'utf-8' });
  console.log(idList.split(/\r?\n/g));
  return idList.split(/\r?\n/g);
};

const parse = (idFile) => {
  const idList = getListFromIdFile(idFile);
  const idQuery = queryHelpers.getIdQueryFromFile(idList);
  return idQuery;
};

/* eslint-enable no-console */
module.exports = { parse };
