// server.js

// set up ========================
const express = require('express');
const mongoose = require('mongoose');
const swaggerJSDoc = require('swagger-jsdoc');
const morgan = require('morgan');
const bodyParser = require('body-parser');
const methodOverride = require('method-override');
const https = require('https');
const fs = require('fs');
const config = require('./config');

const sslOptions = {
  cert: fs.readFileSync('certs/ssl-cert.pem'),
  key: fs.readFileSync('certs/ssl-key.pem'),
};

const app = express();
// configuration =================
const swaggerDefinition = {
  swaggerDefinition: {
    info: {
      title: 'BMGAP API',
      version: module.exports.version,
      description: 'An API that serves data from the BMGAP MongoDB',
    },
    host: config.app.host,
  },
  apis: ['./routes/main.js', './routes/samples.js', './routes/download.js', './routes/runs.js', './routes/filters.js'],
};

const swaggerSpec = swaggerJSDoc(swaggerDefinition);

// serve swagger
app.get('/api/v1/swagger.json', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  res.send(swaggerSpec);
});

app.options('/*', (req, res) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization, Content-Length, X-Requested-With');
  res.sendStatus(200);
});

const {
  db: {
    host, port, name, user, pass,
  },
} = config;
const connectionString = `mongodb://${user}:${pass}@${host}:${port}/${name}`;
mongoose.connect(connectionString);

app.use(morgan('dev'));
app.use(bodyParser.urlencoded({ limit: '50mb', extended: 'true' }));
app.use(bodyParser.json());
app.use(methodOverride());

require('./routes')(app, config.app.token_host);

app.all('*', (req, res) => {
  res.status(404).json({ message: 'Endpoint does not exist' });
});

// listen (start app with node server.js) ======================================
https.createServer(sslOptions, app).listen(config.app.port);
console.log(`App listening on port ${config.app.port}`); // eslint-disable-line no-console
