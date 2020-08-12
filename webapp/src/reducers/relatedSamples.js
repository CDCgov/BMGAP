import * as Types from "../actions/actionTypes";

const relatedSamples = (state = {}, action) => {
  switch (action.type) {
    case Types.FETCH_RELATED_SAMPLES_ASYNC:
      return Object.assign({}, state, {
        fetchingRelatedSamples: action.fetchingRelatedSamples
      });
    case Types.FETCH_RELATED_SAMPLES_SUCCESS:
      return Object.assign({}, state, {
        relatedSamples: action.relatedSamples,
        fetchingRelatedSamples: false
      });
    case Types.FETCH_RELATED_SAMPLES_FAILURE:
      return Object.assign({}, state, {
        relatedSamples: null,
        fetchingRelatedSamples: false
      });
    default:
      return state;
  }
};

export default relatedSamples;
