/*
 * Title: download.js
 * Description:
 * Created by: ylb9 <ylb9@ncbs-dev-09>
 * Created: 2017-12-18 11:16
 * Last Modified: Wed 18 Mar 2020 02:26:00 PM EDT
 */
const mongoose = require('mongoose');
const fs = require('fs');
const path = require('path');
const archiver = require('archiver-promise');
const tmp = require('tmp');
const json2csv = require('json2csv');
const flatten = require('flat');
const XLSX = require('xlsx');
const downloader = require('./fileDownloader');
const constants = require('./constants.js');
const Sample = require('../models/Sample.js');
const FullSchema = require('../models/FullSchema.js');

mongoose.Promise = require('bluebird');

module.exports = (app) => {
  const buildFieldList = (fields) => {
    const display = {
      _id: 0,
      identifier: 1,
      Run_ID: 1,
      Assembly_ID: 1,
      Lab_ID: 1,
      Submitter: 1,
    };

    const Allfields = constants.allFields;

    fields.forEach((f) => {
      const data = Object.keys(Allfields);
      if (data.indexOf(f) > -1) {
        Allfields[f].forEach((fieldName) => {
          if (constants.downloadFieldList.indexOf(fieldName) > -1) {
            display[fieldName] = 1;
          }
        });
      }
    });

    return display;
  };

  const buildQuery = (ids) => {
    const queryObj = {
      $and: [
        { Submitter: { $exists: 1 } },
        {
          $or: [
            { identifier: { $in: ids } },
            { Lab_ID: { $in: ids } },
          ],
        },
      ],
    };
    return queryObj;
  };

  const renameHeaders = (object, oldHeaders, newHeaders) => {
    let n = oldHeaders.length;
    const newObject = {};
    /* eslint-disable-next-line no-plusplus */
    while (n--) {
      newObject[newHeaders[n]] = object[oldHeaders[n]];
    }
    return newObject;
  };

  const getMetadataCsv = (ids, displayFields, outFields, fileBase) => {
    const csvPromise = new Promise(((resolve, reject) => {
      const queryObj = buildQuery(ids);
      const query = FullSchema.find(queryObj, displayFields);
      query.exec((err, data) => {
        if (err) {
          reject(err);
        }
        const dataHolder = [];
        data.forEach((item) => {
          /* eslint-disable no-prototype-builtins */
          if (item && item.hasOwnProperty('_doc')) {
            const docu = flatten(item._doc);
            if (docu && docu.hasOwnProperty('Lab_ID')) {
              const splitId = docu.Lab_ID.split('_');
              /* eslint-disable camelcase */
              const [Lab_ID1, Lab_ID2] = splitId;
              docu.Lab_ID1 = Lab_ID1;
              docu.Lab_ID2 = Lab_ID2;
              /* eslint-enable camelcase */
            }
            dataHolder.push(docu);
          }
          /* eslint-enable no-prototype-builtins */
        });
        const csv = json2csv({ data: dataHolder, fields: outFields });
        fs.writeFileSync(path.join(__dirname, `${fileBase}.csv`), csv);
        const filePath = path.join(__dirname, `${fileBase}.csv`);
        const csvEntry = { path: filePath, name: `${fileBase}.csv` };
        resolve(csvEntry);
      });
    }));
    return csvPromise;
  };

  const getMetadataXls = (ids, displayFields, outFields, fileBase) => {
    const metadataPromise = new Promise(((resolve, reject) => {
      const queryObj = buildQuery(ids);
      const query = FullSchema.find(queryObj, displayFields);
      query.exec((err, data) => {
        if (err) {
          reject(err);
        }
        const dataHolder = [];
        data.forEach((item) => {
          /* eslint-disable no-prototype-builtins */
          if (item && item.hasOwnProperty('_doc')) {
            const docu = flatten(item._doc);
            if (docu && docu.hasOwnProperty('Lab_ID')) {
              const splitId = docu.Lab_ID.split('_');
              /* eslint-disable camelcase */
              const [Lab_ID1, Lab_ID2] = splitId;
              docu.Lab_ID1 = Lab_ID1;
              docu.Lab_ID2 = Lab_ID2;
              /* eslint-disable camelcase */
            }
            dataHolder.push(docu);
          }
          /* eslint-enable no-prototype-builtins */
        });
        const xls = XLSX.utils.book_new();
        const updatedData = [];
        dataHolder.forEach((dataRow) => {
          const newRow = renameHeaders(
            dataRow,
            constants.downloadFieldList,
            constants.downloadFieldNames,
          );
          updatedData.push(newRow);
        });
        const metasheet = XLSX.utils.json_to_sheet(
          updatedData,
          { header: constants.downloadFieldNames },
        );
        XLSX.utils.book_append_sheet(xls, metasheet, 'BMGAP Data');
        const dictionary_data = XLSX.readFile(path.join(__dirname, 'BMGAP_data_dictionary.xlsx'));
        const dictjson = XLSX.utils.sheet_to_json(dictionary_data.Sheets['Data Dictionary']);
        const dictsheet = XLSX.utils.json_to_sheet(dictjson, { header: ['Column Name', 'Definition'] });
        XLSX.utils.book_append_sheet(xls, dictsheet, 'Data Dictionary');
        const filePath = path.join(__dirname, `${fileBase}.xlsx`);
        XLSX.writeFile(xls, filePath);
        const xlsEntry = { path: filePath, name: `${fileBase}.xlsx` };
        resolve(xlsEntry);
      });
    }));
    return metadataPromise;
  };

  const getFastaFilename = (id) => {
    const fastaPromise = new Promise(((resolve, reject) => {
      const query = Sample.findOne({ $or: [{ identifier: id }, { Lab_ID: id }] }, 'Run_ID MLST.Filename');
      query.then((data, err) => {
        if (data) {
          const fastaRes = downloader.retrieveFastaFilename(data.Run_ID, data.MLST.Filename);
          resolve(fastaRes);
        } else if (err) {
          reject(err);
        }
      });
    }));
    return fastaPromise;
  };
  const getGffFilename = (id) => {
    const gffPromise = new Promise(((resolve, reject) => {
      const query = Sample.findOne({ $or: [{ identifier: id }, { Lab_ID: id }] }, 'Run_ID PMGA');
      query.then((data, err) => {
        if (data) {
          const gffRes = downloader.retrievePmgaFilename(data.PMGA.filegff);
          resolve(gffRes);
        } else if (err) {
          reject(err);
        }
      });
    }));
    return gffPromise;
  };
  const getJsonFilename = (id) => {
    const jsonFilenamePromise = new Promise(((resolve, reject) => {
      const query = Sample.findOne({ $or: [{ identifier: id }, { Lab_ID: id }] }, 'Run_ID PMGA');
      query.then((data, err) => {
        if (data) {
          const jsonRes = downloader.retrievePmgaFilename(data.PMGA.filejson);
          resolve(jsonRes);
        } else if (err) {
          reject(err);
        }
      });
    }));
    return jsonFilenamePromise;
  };
  const getJson = (ids) => {
    const jsonPromise = new Promise(((resolve, reject) => {
      const queryObj = buildQuery(ids);
      const query = FullSchema.find(queryObj);
      query.exec((err, data) => {
        if (err) {
          reject(err);
        }
        resolve(data);
      });
    }));
    return jsonPromise;
  };

  const makeFilelist = (ids, fields, fieldSet, fileBase) => {
    const filelist = [];
    if (fields.includes('fasta')) {
      ids.forEach((el) => {
        filelist.push(getFastaFilename(el));
      });
    }
    if (fields.includes('gff')) {
      ids.forEach((el) => {
        filelist.push(getGffFilename(el));
      });
    }
    if (fields.includes('json')) {
      ids.forEach((el) => {
        filelist.push(getJsonFilename(el));
      });
    }

    if (fields.filter(e => e !== 'fasta' && e !== 'gff' && e !== 'json').length > 0) {
      filelist.push(getMetadataCsv(ids, fieldSet.display, fieldSet.outFields, fileBase));
      filelist.push(getMetadataXls(ids, fieldSet.display, fieldSet.outFields, fileBase));
    }
    const paths = Promise.all(filelist).then(data => data);
    return paths;
  };


  /**
   * @swagger
   * /download:
   *   post:
   *      description: Returns a zip file with a CSV containing selected fields and optionally a
   *                   fasta file for each sample
   *      parameters:
   *          - name: ids
   *            description: Comma-separated list of ids to download information for
   *            in: query
   *            type: string
   *          - name: fields
   *            description: Comma-separated list of fields to include for each id
   *            in: query
   *            type: string
   *      produces:
   *          - application/zip
   *      responses:
   *          200:
   *              description: OK
   *              schema:
   *                type: file
   */
  app.post('/api/v1/download', (req, res, next) => {
    const timestamp = Date.now();
    const fileBase = `BMGAP_Metadata_${timestamp}`;
    const archive = archiver(`${fileBase}.zip`);
    // const { ids, fields } = req.body;
    const fieldSet = {
      display: buildFieldList(req.body.fields),
      outFields: constants.downloadFieldList,
    };

    try {
      const filelist = makeFilelist(req.body.ids, req.body.fields, fieldSet, fileBase);
      filelist.then((data) => {
        const missingFiles = [];
        data.forEach((el) => {
          if (fs.existsSync(el.path)) {
            archive.file(el.path, { name: el.name });
          } else {
            missingFiles.push(`${el.path}\n`);
          }
        });
        if (missingFiles.length > 0) {
          const tmpFile = tmp.fileSync();
          missingFiles.forEach((file) => {
            fs.writeSync(tmpFile.fd, `${file}\n`);
          });
          archive.file(tmpFile.name, { name: 'missingFiles.txt' });
        }
      }).then(() => {
        archive.finalize().then(() => {
          res.download(`${fileBase}.zip`);
        });
      });
    } catch (err) {
      next(err);
    }
  });

  /**
   * @swagger
   * /download/json:
   *   get:
   *      description: Returns a JSON file with all of the data for the specified samples
   *      parameters:
   *          - name: ids
   *            description: Comma-separated list of ids to download information for
   *            in: query
   *            type: string
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
  app.get('/api/v1/download/json', (req, res, next) => {
    const ids = req.query.ids.split(',');

    try {
      const jsonData = getJson(ids);
      jsonData.then((data, err) => {
        if (data) {
          res.json(data);
        } else if (err) {
          next(err);
        }
      });
    } catch (err) {
      next(err);
    }
  });
};
