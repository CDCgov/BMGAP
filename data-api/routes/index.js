/*
 * Title: index.js
 * Description:
 * Created by: ylb9 <ylb9@ncbs-dev-09>
 * Created: 2017-12-19 08:37
 * Last Modified: Mon 26 Aug 2019 06:01:23 PM EDT
 */

const main = require('./main');
const download = require('./download');
const samples = require('./samples');
const filters = require('./filters');
const runs = require('./runs');
const analytics = require('./analytics');

module.exports = (app, tokenHost) => {
  main(app, tokenHost);
  download(app);
  samples(app);
  filters(app);
  runs(app);
  analytics(app);
};
