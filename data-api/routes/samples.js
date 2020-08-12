/*
 * Title: samples.js
 * Description:
 * Created by: ylb9 <ylb9@ncbs-dev-09>
 * Created: 2017-12-18 11:12
 * Last Modified: Wed 18 Mar 2020 02:51:09 PM EDT
 */
const mongoose = require('mongoose');
const path = require('path');
const fs = require('fs');
const multer = require('multer');
mongoose.Promise = require('bluebird');
const downloader = require('./fileDownloader');
const Sample = require('../models/Sample');
const SampleSummary = require('../models/SampleSummary');
const helpers = require('./query_helpers');
const sampleHelpers = require('./sample_helpers');
const idFileParser = require('./id_file_parser');
const sero = require('./sero');

const upload = multer({ dest: './uploads' });
const mashSketchPath = '/scicomp/groups/OID/NCIRD-OD/OI/ncbs/projects/Meningitis/by-instrument/full_mash_sketch/BMGAP_DATA_MASH_DB.msh';

module.exports = (app) => {
  /**
     * @swagger
     * /samples:
     *  get:
     *      description: Returns samples
     *      parameters:
     *          - name: page
     *            description: Number of page to return
     *            in: query
     *            type: number
     *          - name: perPage
     *            description: Number of entries to include per returned page
     *            in: query
     *            type: number
     *          - name: sortField
     *            description: Field name to sort results by
     *            in: query
     *            type: string
     *          - name: filter
     *            in: query
     *            type: object
     *            properties:
     *              identifiers:
     *                  type: array
     *                  items:
     *                      type: string
     *              runs:
     *                  type: array
     *                  items:
     *                      type: string
     *              state:
     *                  type: array
     *                  items:
     *                      type: string
     *              mashSpecies:
     *                  type: array
     *                  items:
     *                      type: string
     *              serogrouping:
     *                  type: array
     *                  items:
     *                      type: string
     *              serotyping:
     *                  type: array
     *                  items:
     *                      type: string
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
     *                              $ref: '#/definitions/Sample'
     *                      total:
     *                          type: number
     *                      limit:
     *                          type: number
     */

  app.get('/api/v1/samples', (req, res) => {
    const parsedQuery = helpers.parseSamplesQuery(req.query);
    if (parsedQuery.perPage === 'all') {
      sampleHelpers.getAllSamples(parsedQuery, res);
    } else {
      sampleHelpers.runQuery(parsedQuery, res);
    }
  });

  /**
     * @swagger
     * /sample_summaries:
     *  get:
     *      description: Returns sample_summaries
     *      parameters:
     *          - name: page
     *            description: Number of page to return
     *            in: query
     *            type: number
     *          - name: perPage
     *            description: Number of entries to include per returned page
     *            in: query
     *            type: number
     *          - name: sortField
     *            description: Field name to sort results by
     *            in: query
     *            type: string
     *          - name: filter
     *            in: query
     *            type: object
     *            properties:
     *              runs:
     *                  type: array
     *                  items:
     *                      type: string
     *              state:
     *                  type: array
     *                  items:
     *                      type: string
     *              mashSpecies:
     *                  type: array
     *                  items:
     *                      type: string
     *              serogrouping:
     *                  type: array
     *                  items:
     *                      type: string
     *              serotyping:
     *                  type: array
     *                  items:
     *                      type: string
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
     *                              $ref: '#/definitions/SampleSummary'
     *                      total:
     *                          type: number
     *                      limit:
     *                          type: number
     */
  app.get('/api/v1/sample_summaries', (req, res) => {
    const parsedQuery = helpers.parseSamplesQuery(req.query);
    if (parsedQuery.perPage === 'all') {
      sampleHelpers.getAllSampleSummaries(parsedQuery, res);
    } else {
      sampleHelpers.runSummaryQuery(parsedQuery, res);
    }
  });

  /**
     * @swagger
     * /samples/{sampleId}:
     *  get:
     *      description: Returns a specific sample
     *      parameters:
     *          - name: sampleId
     *            description: ID of sample to return
     *            in: path
     *            type: string
     *            required: true
     *      produces:
     *          - application/json
     *      responses:
     *          200:
     *              description: OK
     *              schema:
     *                  $ref: '#/definitions/Sample'
     *
     */

  app.get('/api/v1/samples/:sampleId/', (req, res) => {
    const queryObj = sampleHelpers.makeSampleQueryObj(req.params.sampleId);
    const query = Sample.findOne(queryObj, { MLST_allele: 0, location: 0, PMGA: 0 });
    query.then((err, data) => {
      if (err) {
        res.send(err);
      } else if (data) {
        res.status(200).json(data);
      } else {
        const errMessage = helpers.send404Error(queryObj);
        res.status(404).send(errMessage);
      }
    });
  });

  /**
     * @swagger
     * /samples/{sampleId}/fasta:
     *  get:
     *      description: Returns a specific sample's cleaned assembly
     *      parameters:
     *          - name: sampleId
     *            description: ID of sample to return
     *            in: path
     *            type: string
     *            required: true
     *      produces:
     *          - text/fasta
     *      responses:
     *          200:
     *              description: OK
     *              content:
     *                  schema:
     *                      type: file
     *
     */

  app.get('/api/v1/samples/:sampleId/fasta', (req, res) => {
    const queryObj = sampleHelpers.makeSampleQueryObj(req.params.sampleId);
    const query = Sample.findOne(queryObj);
    query.then((data, err) => {
      if (err) {
        res.send(err);
      }
      if (data) {
        const fastaSequence = downloader.retrieveFastaData(data.Run_ID, data.MLST.Filename);
        res.set('Content-Disposition', `attachment; filename=${data.MLST.Filename}`);
        res.set('Content-Type', 'text/fasta');
        res.send(fastaSequence);
      }
    });
  });

  /**
     * @swagger
     * /samples/{sampleId}/pmga-gff:
     *  get:
     *      description: Returns a specific sample's PMGA GFF File
     *      parameters:
     *          - name: sampleId
     *            description: ID of sample to return
     *            in: path
     *            type: string
     *            required: true
     *      produces:
     *          - text/gff
     *      responses:
     *          200:
     *              description: OK
     *              content:
     *                  schema:
     *                      type: file
     *
     */

  app.get('/api/v1/samples/:sampleId/pmga-gff', (req, res) => {
    const queryObj = sampleHelpers.makeSampleQueryObj(req.params.sampleId);
    const query = Sample.findOne(queryObj);
    query.then((data, err) => {
      if (err) {
        res.send(err);
      }
      if (data) {
        const gffFile = downloader.retrievePmgaData(data.PMGA.filegff);
        const gffFileName = downloader.retrievePmgaFilename(data.PMGA.filegff);
        res.set('Content-Disposition', `attachment; filename=${gffFileName.name}`);
        res.set('Content-Type', 'text/plain');
        res.send(gffFile);
      }
    });
  });

  /**
     * @swagger
     * /samples/{sampleId}/pmga-json:
     *  get:
     *      description: Returns a specific sample's PMGA JSON file
     *      parameters:
     *          - name: sampleId
     *            description: ID of sample to return
     *            in: path
     *            type: string
     *            required: true
     *      produces:
     *          - application/json
     *      responses:
     *          200:
     *              description: OK
     *              content:
     *                  schema:
     *                      type: file
     *
     */

  app.get('/api/v1/samples/:sampleId/pmga-json', (req, res) => {
    const queryObj = sampleHelpers.makeSampleQueryObj(req.params.sampleId);
    const query = Sample.findOne(queryObj);
    query.then((data, err) => {
      if (err) {
        res.send(err);
      }
      if (data) {
        const jsonFile = downloader.retrievePmgaData(data.PMGA.filejson);
        const jsonFileName = downloader.retrievePmgaFilename(data.PMGA.filejson);
        res.set('Content-Disposition', `attachment; filename=${jsonFileName.name}`);
        res.set('Content-Type', 'application/json');
        res.send(jsonFile);
      }
    });
  });

  /**
     * @swagger
     * /samples/{sampleId}/alleles:
     *  get:
     *      description: Returns a FASTA file with novel alleles
     *      parameters:
     *          - name: sampleId
     *            description: ID of sample to return
     *            in: path
     *            type: string
     *            required: true
     *      produces:
     *          - text/fasta
     *      responses:
     *          200:
     *              description: OK
     *
     */

  app.get('/api/v1/samples/:sampleId/alleles', (req, res) => {
    const queryObj = sampleHelpers.makeSampleQueryObj(req.params.sampleId);
    const query = Sample.findOne(queryObj, { _id: 0, mismatched_DNA: 1 });
    query.then((data, err) => {
      if (err) {
        res.send(err);
      }
      if (data) {
        res.json(data);
      } else {
        const errMessage = helpers.send404Error(queryObj);
        res.status(404).send(errMessage);
      }
    });
  });

  /**
     * @swagger
     * /samples/{sampleId}/alleles_peptide:
     *  get:
     *      description: Returns a FASTA file with novel alleles in amino acid format
     *      parameters:
     *          - name: sampleId
     *            description: ID of sample to return
     *            in: path
     *            type: string
     *            required: true
     *      produces:
     *          - text/fasta
     *      responses:
     *          200:
     *              description: OK
     *
     */

  app.get('/api/v1/samples/:sampleId/alleles_peptide', (req, res) => {
    const queryObj = sampleHelpers.makeSampleQueryObj(req.params.sampleId);
    const query = Sample.findOne(queryObj, { _id: 0, mismatched_peptide: 1 });
    query.then((data, err) => {
      if (err) {
        res.send(err);
      }
      if (data) {
        res.json(data);
      } else {
        const errMessage = helpers.send404Error(queryObj);
        res.status(404).send(errMessage);
      }
    });
  });

  /**
     * @swagger
     * /samples/{sampleId}/mash_sort:
     *  get:
     *      description: Returns a JSON object showing the most closely related samples
     *      parameters:
     *          - name: sampleId
     *            description: ID of sample to find related samples for
     *            in: path
     *            type: string
     *            required: true
     *      produces:
     *          - application/json
     *      responses:
     *          200:
     *            description: OK
     *
     */
  app.get('/api/v1/samples/:sampleId/mash_sort', (req, res) => {
    let submitter = req.query.Submitter;
    if (!submitter) {
      submitter = 'BML';
    }
    const queryObj = sampleHelpers.makeSampleQueryObj(req.params.sampleId);
    const query = Sample.findOne(queryObj, { _id: 0, assemblyPath: 1 });
    query.then((data, err) => {
      if (err) {
        res.send(err);
      }
      if (data) {
        const results = data.toObject();
        const executable = path.join(__dirname, '../get_closest_hits.sh');
        const command = `${executable} ${results.assemblyPath} ${mashSketchPath}`;
        const resultStr = sampleHelpers.runProgram(command);
        const resultObj = JSON.parse(resultStr);
        // console.log(resultStr);
        const mashPaths = resultObj.map(a => a.hit);
        const querySet = { assemblyPath: { $in: mashPaths } };
        const mashQuery = SampleSummary.find(querySet, {
          _id: 0,
        });
        mashQuery.then((mashData, mashErr) => {
          if (mashErr) {
            res.send(mashErr);
          }
          if (mashData) {
            const finalObj = sampleHelpers.processMashResults(resultObj, mashData,
              submitter);
            res.json(finalObj);
          }
        });
      }
    });
  });

  /**
     * @swagger
     * /samples/{sampleId}/phylo:
     *  post:
     *      description: Returns a JSON object showing the most closely related samples
     *      parameters:
     *          - name: sampleId
     *            description: ID of sample to find related samples for
     *            in: path
     *            type: string
     *            required: true
     *          - name: hit
     *            description: an array of assembly paths for related samples
     *            in: body
     *            required: true
     *      produces:
     *          - text/plain
     *      responses:
     *        200:
     *          description: OK
     *
     */
  app.post('/api/v1/samples/:sampleId/phylo', (req, res) => {
    const hitAssemblies = req.body.hits.map(a => a.assemblyPath);
    const assemblyList = hitAssemblies.join('\n');
    const assemblyFofn = 'assembly_fofn_file';
    fs.writeFileSync(assemblyFofn, assemblyList);
    const executable = path.join(__dirname, '../make_phylo_tree.sh');
    const command = `${executable} ${assemblyFofn}`;
    const resultStr = sampleHelpers.runProgram(command);
    const correctedResultsStr = resultStr.replace(/_cleaned/g, '');
    res.send(correctedResultsStr);
  });

  /**
     * @swagger
     * /samples/{sampleId}/sero:
     *  get:
     *      description: Returns a JSON representation of sero genes
     *      parameters:
     *          - name: sampleId
     *            description: ID of sample to return
     *            in: path
     *            type: string
     *            required: true
     *      produces:
     *          - application/
     *      responses:
     *          200:
     *              description: OK
     *
     */

  app.get('/api/v1/samples/:sampleId/sero', (req, res) => {
    const queryObj = sampleHelpers.makeSampleQueryObj(req.params.sampleId);
    const query = Sample.findOne(queryObj, { _id: 0, PMGATyping: 1 });
    query.then((data, err) => {
      const seroObj = sero.getSeroData(data);
      if (err) {
        res.send(err);
      }
      if (seroObj) {
        res.json(seroObj);
      } else {
        const errMessage = helpers.send404Error(queryObj);
        res.status(404).send(errMessage);
      }
    });
  });

  /**
     * @swagger
     * /samples/by-id:
     *  post:
     *      description: Returns samples from list
     */

  app.post('/api/v1/sample_summaries/by-id', upload.single('file'), (req, res) => {
    const idQueryObj = idFileParser.parse(req.file);
    const parsedIdQuery = {
      query: idQueryObj,
      sort: '-identifier',
      page: 1,
      perPage: 50,
    };
    sampleHelpers.runSummaryQuery(parsedIdQuery, res);
  });
};
