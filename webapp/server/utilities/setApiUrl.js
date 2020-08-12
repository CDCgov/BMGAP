module.exports = () => {
  if (process.env.NODE_ENV === "test")
    return "https://bmgap-test.biotech.cdc.gov:3000/api/v1";
  if (process.env.NODE_ENV === "development")
    return "https://ncbs-dev-09.biotech.cdc.gov:3000/api/v1";
    //return "https://bmgap-dev.biotech.cdc.gov:3000/api/v1";
  if (process.env.NODE_ENV === "production")
    return "https://bmgap-poc.biotech.cdc.gov:3000/api/v1";
};
