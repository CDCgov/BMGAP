const express = require("express");
const path = require("path");
const morgan = require("morgan");
const bodyParser = require("body-parser");
const axios = require("axios");
const https = require("https");
const fs = require("fs");
const history = require("connect-history-api-fallback");
const multer = require("multer");
const FormData = require("form-data");
const storage = multer.memoryStorage();
const upload = multer({ storage }).single("sample-data");

const setApiUrl = require("./utilities/setApiUrl");

const privateKey = fs.readFileSync(
  `${__dirname}/cert/bmgap_ssl_certificate.key`,
  "utf8"
);
const certificate = fs.readFileSync(
  `${__dirname}/cert/bmgap_ssl_certificate.crt`,
  "utf8"
);
const credentials = { key: privateKey, cert: certificate };

process.env["NODE_TLS_REJECT_UNAUTHORIZED"] = "0";
let agent = new https.Agent({
  ca: fs.readFileSync(`${__dirname}/cert/CDC_internal_CA_chain.pem`)
});

const app = express();

const apiUrl = setApiUrl();

app.use(bodyParser.json({ limit: "50mb" }));
app.use(morgan("short"));
app.use("/bmgap", history());

app.get("/bmgap/api/runs", (req, res) => {
  console.log("The /runs endpoint has been hit");
  console.log(req.query);
  console.log(req.headers && req.headers.authorization);
  axios
    .get(`${apiUrl}/runs`, {
      httpsAgent: agent,
      params: req.query,
      headers: req.headers &&
        req.headers.authorization && {
          Authorization: req.headers.authorization
        }
    })
    .then(apiRes => {
      res.send(apiRes.data);
    })
    .catch(error => {
      handleError(res, error, "/runs");
    });
});

app.get("/bmgap/api/samples", (req, res) => {
  console.log("The /samples endpoint has been hit");
  console.log(req.query);
  console.log(req.headers && req.headers.authorization);
  axios
    .get(`${apiUrl}/sample_summaries`, {
      httpsAgent: agent,
      params: req.query,
      headers: req.headers &&
        req.headers.authorization && {
          Authorization: req.headers.authorization
        }
    })
    .then(apiRes => {
      res.send(apiRes.data);
    })
    .catch(error => {
      handleError(res, error, "/samples");
    });
});

app.get("/bmgap/api/filters", (req, res) => {
  console.log("The /filters endpoint has been hit");
  console.log(req.headers && req.headers.authorization);
  axios
    .get(`${apiUrl}/filters`, {
      httpsAgent: agent,
      params: req.query,
      headers: req.headers &&
        req.headers.authorization && {
          Authorization: req.headers.authorization
        }
    })
    .then(apiRes => {
      res.send(apiRes.data);
    })
    .catch(error => {
      handleError(res, error, "/filters");
    });
});

// Download read data
app.post("/bmgap/api/download", (req, res) => {
  console.log("The /download endpoint has been hit");
  axios
    .post(`${apiUrl}/download`, req.body, { responseType: "arraybuffer" })
    .then(apiRes => {
      res.contentType("application/zip");
      res.send(apiRes.data);
    })
    .catch(error => {
      handleError(res, error, "/download");
    });
});

app.get("/bmgap/api/samples/:sampleId/mash_sort", (req, res) => {
  console.log("The /mash_sort endpoint has been hit");
  console.log(req.headers && req.headers.authorization);
  axios
    .get(`${apiUrl}/samples/${req.params.sampleId}/mash_sort`, {
      params: req.query,
      headers: req.headers &&
        req.headers.authorization && {
          Authorization: req.headers.authorization
        }
    })
    .then(apiRes => {
      res.send(apiRes.data);
    })
    .catch(error => {
      handleError(res, error, "/mash_sort");
    });
});

app.post("/bmgap/api/samples/:sampleId/phylo", (req, res) => {
  console.log("The /phylo endpoint has been hit");
  axios
    .post(`${apiUrl}/samples/${req.params.sampleId}/phylo`, req.body)
    .then(apiRes => {
      res.send(apiRes.data);
    })
    .catch(error => {
      handleError(res, error, "/samples/:sampleId/phylo");
    });
});

app.get("/bmgap/api/samples/:sampleId", (req, res) => {
  console.log("The /samples/:sampleId endpoint has been hit");
  axios
    .get(`${apiUrl}/samples/${req.params.sampleId}`, {
      params: req.query
    })
    .then(apiRes => {
      res.send(apiRes.data);
    })
    .catch(error => {
      handleError(res, error, "/samples/:sampleId");
    });
});

app.get("/bmgap/api/id/validate/:token", (req, res) => {
  console.log("The id/validate/:token endpoint has been hit");
  axios
    .get(`${apiUrl}/id/validate/${req.params.token}`, {
      params: req.query
    })
    .then(apiRes => {
      res.send(apiRes.data);
    })
    .catch(error => {
      handleError(res, error, "/id/validate/:token");
    });
});

app.get("/bmgap/api/samples/:sampleId/sero", (req, res) => {
  console.log("The /samples/:sampleId/sero endpoint has been hit");
  axios
    .get(`${apiUrl}/samples/${req.params.sampleId}/sero`, {
      params: req.query
    })
    .then(apiRes => {
      res.send(apiRes.data);
    })
    .catch(error => {
      handleError(res, error, "/samples/:sampleId/sero");
    });
});

app.get("/bmgap/api/analytics", (req, res) => {
  console.log("The /analytics endpoint has been hit");
  axios
    .get(`${apiUrl}/analytics`, {
      params: req.query,
      headers: req.headers &&
        req.headers.authorization && {
          Authorization: req.headers.authorization
        }
    })
    .then(apiRes => {
      res.send(apiRes.data);
    })
    .catch(error => {
      handleError(res, error, "/analytics");
    });
});

app.post("/bmgap/api/samplesFromFile", upload, (req, res) => {
  console.log("The /samplesFromFile endpoint has been hit");
  const dataBuffer = req.file.buffer;
  let form = new FormData();
  form.append("file", dataBuffer, "samples.txt");
  axios
    .post(`${apiUrl}/sample_summaries/by-id`, form, {
      headers: form.getHeaders()
    })
    .then(apiRes => {
      console.log('\n\n\n', apiRes.data, '\n\n\n')
      res.send(apiRes.data);
    })
    .catch(error => {
      handleError(res, error, "/samplesFromFile");
    });
});

const handleError = (res, error, endpoint) => {
  if (error.response && error.response.status) {
    console.log(
      "Error Status:",
      error.response.status,
      "Error Text:",
      error.response.statusText,
      "Endpoint:",
      endpoint
    );
    res.status(error.response.status).send();
  } else {
    console.log(
      "Error Message:",
      error ? error.message : "Unknown",
      "Endpoint:",
      endpoint
    );
    res.status(500).send();
  }
};

if (process.env.NODE_ENV === "production") {
  app.use("/bmgap", express.static(path.join(__dirname, "..", "build")));
} else {
  app.use(express.static(path.join(__dirname, "..", "build")));
  app.get("/*", (req, res) => {
    res.sendFile(path.join(__dirname, "..", "build", "index.html"));
  });
}

let httpsServer = https.createServer(credentials, app);
httpsServer.listen(4000, () => {
  console.log("BMGAP App listening on port 4000!\n");
});
