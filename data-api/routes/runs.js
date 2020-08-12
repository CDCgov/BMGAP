/*
 * Title: run.js
 * Description:
 * Created by: ylb9 <ylb9@ncbs-dev-09.biotech.cdc.gov>
 * Created: 2019-02-11 18:00
 * Last Modified: Tue 26 Feb 2019 04:47:36 PM EST
 */
const Run = require('../models/Run');
const helpers = require('./query_helpers');

module.exports = (app) => {
  const runQuery = (parsedQuery, res) => {
    const query = Run.paginate(parsedQuery.query, {
      sort: '-date', page: parsedQuery.page, limit: parsedQuery.perPage,
    });
    query.then((data, err) => {
      if (err) {
        res.send(err);
      } else {
        res.json(data);
      }
    });
  };

  const getAllRun = (parsedQuery, res) => {
    const totalCount = Run.count(parsedQuery.query);
    totalCount.then((data) => {
      parsedQuery.page = 1;
      parsedQuery.perPage = data;
      runQuery(parsedQuery, res);
    });
  };

  /**
     * @swagger
     * /runs:
     *  get:
     *      description: Returns runs
     *      parameters:
     *          - name: perPage
     *            description: Number of records per page
     *            in: query
     *            type: number
     *          - name: page
     *            description: The specific page to return
     *            in: query
     *            type: number
     *          - name: submitter
     *            description: Submitters to find runs from
     *            in: query
     *            type: object
     *          - name: sequencer
     *            description: Sequencer to find runs from
     *            in: query
     *            type: object
     *          - name: start_year
     *            description: Earliest year to find runs from
     *            in: query
     *            type: object
     *          - name: end_year
     *            description: Latest year to find runs from
     *            in: query
     *            type: object
     *      produces:
     *          - application/json
     *      responses:
     *          200:
     *              description: OK
     *              schema:
     *                  type: object
     *                  properties:
     *                      docs:
     *                          type: array
     *                          items:
     *                              $ref: '#/definitions/Runs'
     *                      total:
     *                          type: number
     *                      limit:
     *                          type: number
     */
  app.get('/api/v1/runs', (req, res) => {
    const runsQuery = helpers.parseRunsQuery(req.query);
    if (runsQuery.perPage === 'all') {
      getAllRun(runsQuery, res);
    } else {
      if (runsQuery.perPage === 50) {
        runsQuery.perPage = 5;
      }
      runQuery(runsQuery, res);
    }
  });

  /**
     * @swagger
     * /runs/{runId}:
     *  get:
     *      description: Returns a specific run
     *      parameters:
     *          - name: runId
     *            description: ID of run to return
     *            in: path
     *            type: string
     *            required: true
     *      produces:
     *          - application/json
     *      responses:
     *          200:
     *              description: OK
     *              schema:
     *                  $ref: '#/definitions/Run'
     *
     */
  app.get('/api/v1/runs/:runId/', (req, res) => {
    const runIdVal = req.params.runId;
    const query = Run.findOne({ run: runIdVal });
    query.then((err, data) => {
      if (err) {
        res.send(err);
      } else if (data) {
        res.status(200).json(data);
      } else {
        const errMessage = helpers.send404Error(query);
        res.status(404).send(errMessage);
      }
    });
  });
};
