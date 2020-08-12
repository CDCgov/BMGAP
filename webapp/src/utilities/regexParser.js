export const getTokenFromQuery = query => {
  if (/.*access_token=/gi.test(query))
    return query.replace(/.*access_token=/gi, "");
  return null;
};

export const getTokenFromHash = query => {
  return /.*access_token=/gi.test(query)
    ? query.replace(/.*access_token=/gi, "")
    : null;
};

export const getToken = location => {
  if (location.search) {
    return getTokenFromQuery(location.search);
  }
  if (location.hash) {
    return getTokenFromQuery(location.hash);
  }
  return null;
};

export const getIdFromUrl = (location, path) => {
  const regex = new RegExp("(/" + path + "/?)");
  const result = location.pathname && location.pathname.replace(regex, "")
  ? location.pathname.replace(regex, "")
  : [];
  if(result && result === "null") {
    return [];
  }
  if(typeof result === "string" && result !== "null") {
    return result.split(',');
  }
  return [];
};
