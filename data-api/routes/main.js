const mongoose = require('mongoose');
const path = require('path');
const childProc = require('child_process');
const https = require('https');
const User = require('../models/User');
mongoose.Promise = require('bluebird');

module.exports = (app, tokenHost) => {
  const getSubmitterFromToken = (token) => {
    const validateUrl = `https://${tokenHost}/id/validate/${token}`;
    const submitterRequest = new Promise((resolve, reject) => {
      https.get(validateUrl, (res) => {
        const bodyHolder = [];
        res.on('data', (chunk) => {
          bodyHolder.push(chunk);
        }).on('end', () => {
          const body = Buffer.concat(bodyHolder);
          const userProfile = JSON.parse(body.toString());
          if (userProfile.result.result) {
            resolve(userProfile.result.result.username);
          } else {
            reject(new Error('No user associated with this token'));
          }
        });
      });
    });
    return submitterRequest;
  };

  const getSubmitterState = (username) => {
    const userResult = User.findOne({ username });
    const userState = new Promise((resolve, reject) => {
      userResult.then((data) => {
        if (data && data !== '') {
          resolve(data.state);
        } else {
          reject(new Error('User not found in database'));
        }
      });
    });
    return userState;
  };

  const runProgram = (command) => {
    const execute = childProc.execSync;
    const result = execute(command);
    const resultStr = result.toString();
    return resultStr;
  };

  // routes ================================
  app.use((req, res, next) => {
    const tokenHeader = req.header('Authorization');
    const token = tokenHeader;
    if (!req.query) {
      req.query = {};
    }
    if (token) {
      const onlyToken = token.split(' ')[1];
      const tokenPromise = getSubmitterFromToken(onlyToken);
      tokenPromise.then((data) => {
        if (data && data !== '') {
          const subState = getSubmitterState(data);
          subState.then((sdata) => {
            if (Object.prototype.hasOwnProperty.call(req.query, 'filter')) {
              if (sdata === 'BML') {
                const holderObj = JSON.parse(req.query.filter);
                req.query.filter = JSON.stringify(holderObj);
                req.query.Submitter = sdata;
              } else if (sdata !== 'BML') {
                req.query.filter = {};
                req.query.filter.state = [sdata];
                req.query.Submitter = sdata;
              }
            } else if (sdata !== 'BML') {
              req.query.filter = {};
              req.query.filter.state = [sdata];
              req.query.Submitter = sdata;
            }
            next();
          })
            .catch((error) => {
              res.status(401).send(error);
            });
        }
      })
        .catch((error) => {
          res.status(401).send(error);
        });
    } else {
      next();
    }
  });

  app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
    next();
  });


  /* GET home page. */
  app.get('/', (req, res) => {
    res.json({ message: 'Welcome to the BMGAP data API' });
  });

  app.get('/api/v1/users/:userid/', (req, res) => {
    const output = User.findOne({ username: req.params.userid });
    output.then((data) => {
      res.send(data);
    });
  });

  app.get('/api/v1/id/validate/:token', (req, res) => {
    /* eslint-disable no-console */
    console.log(req.params.token);
    /* eslint-enable no-console */
    getSubmitterFromToken(req.params.token).then((response) => {
      const username = response;
      const query = User.findOne({ username }, { _id: 0 });
      query.then((data, err) => {
        if (err) {
          res.send(err);
        } else if (!data) {
          res.status('404').send(null); // json({message: "No BMGAP User associated with that token"});
        } else if (data) {
          res.send(data.state);
        }
      });
    });
  });

  /**
   * @swagger
   * definitions:
   *   filters:
   *     type: object
   *     properties:
   *       run_filters:
   *         type: object
   *         properties:
   *           submitter:
   *             type: array
   *           sequencer:
   *             type: array
   *           year:
   *             type: array
   *       sample_filters:
   *         type: object
   *         properties:
   *           mash-species:
   *             type: array
   *           Hi_MLST:
   *             type: array
   *           Nm_MLST:
   *             type: array
   *           serotyping:
   *             type: array
   *           serogrouping:
   *            type: array
   *           run_id:
   *             type: array
   *           state:
   *             type: array
   *           location:
   *             type: array
   *   Run:
   *      type: object
   *      properties:
   *        run:
   *          type: string
   *        date:
   *          type: date
   *        samples:
   *          type: number
   *        submitter:
   *          type: string
   *        sequencer:
   *          type: string
   *   SampleSummary:
   *      type: object
   *      required: ['identifier', 'Run_ID', 'Assembly_ID', 'Lab_ID']
   *      properties:
   *         identifier:
   *          type: string
   *         Run_ID:
   *          type: string
   *         Assembly_ID:
   *          type: string
   *         Lab_ID:
   *          type: string
   *         MLST:
   *          type: string
   *         cc:
   *          type: string
   *         QC_flagged:
   *          type: boolean
   *         Serogroup:
   *          type: string
   *         Serotype:
   *          type: string
   *         assemblyPath:
   *          type: string
   *         Submitter:
   *          type: string
   *         Species:
   *           type: string
   *         sequencer:
   *           type: string
   *         assembly_flagged:
   *           type: string
   *         sequence_flagged:
   *           type: string
   *   Sample:
   *      type: object
   *      required: ['identifier', 'Run_ID', 'Assembly_ID', 'Lab_ID']
   *      properties:
   *         identifier:
   *          type: string
   *         Run_ID:
   *          type: string
   *         Assembly_ID:
   *          type: string
   *         Lab_ID:
   *          type: string
   *         MLST:
   *          type: object
   *          properties:
   *            MLST.Analysis_Time:
   *                type: string
   *            MLST.Analysis_User:
   *                type: string
   *            MLST.Analysis_Version:
   *                type: string
   *            MLST.FHbp_protein_subletiant_Novartis:
   *                type: string
   *            MLST.FHbp_protein_subletiant_Oxford:
   *                type: string
   *            MLST.FHbp_protein_subletiant_Pfizer:
   *                type: string
   *            MLST.FHbp_subfamily:
   *                type: string
   *            MLST.FetA:
   *                type: string
   *            MLST.Filename:
   *                type: string
   *            MLST.Hi_MLST_ST:
   *                type: string
   *            MLST.Hi_MLST_adk:
   *                type: string
   *            MLST.Hi_MLST_atpG:
   *                type: string
   *            MLST.Hi_MLST_frdB:
   *                type: string
   *            MLST.Hi_MLST_fucK:
   *                type: string
   *            MLST.Hi_MLST_mdh:
   *                type: string
   *            MLST.Hi_MLST_pgi:
   *                type: string
   *            MLST.Hi_MLST_recA:
   *                type: string
   *            MLST.Lab_ID:
   *                type: string
   *            MLST.NadA_Protein_subletiant_Novartis:
   *                type: string
   *            MLST.NhbA_Protein_subletiant_Novartis:
   *                type: string
   *            MLST.Nm_MLST_ST:
   *                type: string
   *            MLST.Nm_MLST_abcZ:
   *                type: string
   *            MLST.Nm_MLST_adk:
   *                type: string
   *            MLST.Nm_MLST_aroE:
   *                type: string
   *            MLST.Nm_MLST_cc:
   *                type: string
   *            MLST.Nm_MLST_fumC:
   *                type: string
   *            MLST.Nm_MLST_gdh:
   *                type: string
   *            MLST.Nm_MLST_pdhC:
   *                type: string
   *            MLST.Nm_MLST_pgm:
   *                type: string
   *            MLST.PorA_VR1:
   *                type: string
   *            MLST.PorA_VR2:
   *                type: string
   *            MLST.PorA_type:
   *                type: string
   *            MLST.PorB_type:
   *                type: string
   *            MLST.Unique_ID:
   *                type: string
   *            MLST.fHbp_DNA_allele_Nolettis:
   *                type: string
   *            MLST.fHbp_DNA_allele_Oxford:
   *                type: string
   *            MLST.fHbp_DNA_allele_Pfizer:
   *                type: string
   *            MLST.nadA_PCR:
   *              type: string
   *         mash:
   *          type: object
   *          properties:
   *            mash.Mash_Dist:
   *                type: string
   *            mash.Mash_Entry:
   *                type: string
   *            mash.Mash_Entry_Source:
   *                type: string
   *            mash.Mash_Hash:
   *                type: string
   *            mash.Mash_P_value:
   *                type: string
   *            mash.Notes:
   *                type: string
   *            mash.Top_Species:
   *              type: string
   *         meta:
   *          type: object
   *          properties:
   *            meta.Submitter_Country:
   *                type: string
   *            meta.Submitter_State:
   *              type: string
   *         serogrouping:
   *          type: object
   *          properties:
   *            serogrouping.Infer:
   *                type: string
   *            serogrouping.baseSG:
   *                type: string
   *            serogrouping.gene1:
   *                type: string
   *            serogrouping.gene2:
   *                type: string
   *            serogrouping.gene3:
   *                type: string
   *            serogrouping.gene4:
   *                type: string
   *            serogrouping.gene5:
   *                type: string
   *            serogrouping.gene6:
   *                type: string
   *            serogrouping.gene7:
   *              type: string
   *         serotyping:
   *          type: object
   *          properties:
   *            serotyping.ST:
   *                type: string
   *            serotyping.bexA:
   *                type: string
   *            serotyping.bexB:
   *                type: string
   *            serotyping.bexC:
   *                type: string
   *            serotyping.bexD:
   *                type: string
   *            serotyping.hcsA:
   *                type: string
   *            serotyping.hcsB:
   *                type: string
   *            serotyping._cs1:
   *                type: string
   *            serotyping._cs2:
   *                type: string
   *            serotyping._cs3:
   *                type: string
   *            serotyping._cs4:
   *                type: string
   *            serotyping._cs5:
   *                type: string
   *            serotyping._cs6:
   *                type: string
   *            serotyping._cs7:
   *                type: string
   *            serotyping._cs8:
   *              type: string
   */
};
