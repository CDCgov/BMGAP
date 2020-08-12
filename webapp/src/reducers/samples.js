import * as Types from "../actions/actionTypes";

const samples = (state = {}, action) => {
  switch (action.type) {
    case Types.FETCH_RECENT_SAMPLES_ASYNC:
      return Object.assign({}, state, {
        fetchingSamples: action.fetchingSamples
      });
    case Types.FETCH_RECENT_SAMPLES_SUCCESS:
      return Object.assign({}, state, {
        samples: action.samples,
        fetchingSamples: false
      });
    case Types.FETCH_RECENT_SAMPLES_FAILURE:
      return Object.assign({}, state, {
        samples: null,
        fetchingSamples: false
      });
    case Types.DOWNLOAD_SAMPLES_ASYNC:
      return Object.assign({}, state, {
        downloadingSamples: true
      });
    case Types.DOWNLOAD_SAMPLES_SUCCESS:
      return Object.assign({}, state, {
        downloadingSamples: false
      });
    case Types.DOWNLOAD_SAMPLES_FAILURE:
      return Object.assign({}, state, {
        downloadingSamples: false
      });
    default:
      return state;
  }
};

export default samples;
