import * as Types from "../actions/actionTypes";

const featureViewer = (state = {}, action) => {
  switch (action.type) {
    case Types.FETCH_FEATURE_VIEWER_ASYNC:
      return Object.assign({}, state, {
        fetchingFeatureViewer: action.fetchingFeatureViewer
      });
    case Types.FETCH_FEATURE_VIEWER_SUCCESS:
      return Object.assign({}, state, {
        featureViewer: action.featureViewer,
        fetchingFeatureViewer: false
      });
    case Types.FETCH_FEATURE_VIEWER_FAILURE:
      return Object.assign({}, state, {
        featureViewer: null,
        fetchingFeatureViewer: false
      });
    default:
      return state;
  }
};

export default featureViewer;
