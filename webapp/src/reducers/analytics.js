import * as Types from "../actions/actionTypes";

const analytics = (state = {}, action) => {
  switch (action.type) {
    case Types.FETCH_ANALYTICS_ASYNC:
      return Object.assign({}, state, {
        fetchingAnalytics: action.fetchingAnalytics
      });
    case Types.FETCH_ANALYTICS_SUCCESS:
      return Object.assign({}, state, {
        analytics: action.analytics,
        fetchingAnalytics: false
      });
    case Types.FETCH_ANALYTICS_FAILURE:
      return Object.assign({}, state, {
        analytics: null,
        fetchingAnalytics: false
      });
    default:
      return state;
  }
};

export default analytics;
