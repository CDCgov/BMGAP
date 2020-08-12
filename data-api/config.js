const config = {
  app: {
    host: 'bmgap-poc.biotech.cdc.gov',
    token_host: 'amdportal-sams.cdc.gov',
    port: 3000,
  },
  db: {
    host: 'bmgap-poc.biotech.cdc.gov',
    port: 27017,
    name: 'BMGAP',
    user: 'bmgap-reader',
    pass: <user password for read only account>
  },
};

module.exports = config;
