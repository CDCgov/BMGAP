import * as Types from "../actions/actionTypes";

const samplesFromFile = (state = {}, action) => {
  switch (action.type) {
    case Types.FETCH_SAMPLES_FROM_FILE_ASYNC:
      return Object.assign({}, state, {
        fetchingSamplesFromFile: action.fetchingSamplesFromFile
      });
    case Types.FETCH_SAMPLES_FROM_FILE_SUCCESS:
      return Object.assign({}, state, {
        samplesFromFile: action.samplesFromFile,
        fetchingSamplesFromFile: false
      });
    case Types.FETCH_SAMPLES_FROM_FILE_FAILURE:
      return Object.assign({}, state, {
        samplesFromFile: null,
        fetchingSamplesFromFile: false
      });
    default:
      return state;
  }
};

export default samplesFromFile;
