export const setRedirectUrl = () => {
  if (process.env.NODE_ENV === "test")
    return process.env.REACT_APP_AMD_TEST_URL;
  if (process.env.NODE_ENV === "development")
    return process.env.REACT_APP_AMD_DEV_URL;
  if (process.env.NODE_ENV === "production")
    return process.env.REACT_APP_AMD_PROD_URL;
};
