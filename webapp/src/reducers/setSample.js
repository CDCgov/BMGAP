import * as Types from "../actions/actionTypes";

const setSample = (state = {}, action) => {
  switch (action.type) {
    case Types.SET_SAMPLE_ID:
      return Object.assign({}, state, {
        // this sets the state locally for set sample only... need to find a way to set state globally
        setSample: action.sampleId,
        phyloTree: null,
        relatedSamples: null
      });
    default:
      return state;
  }
};

export default setSample;
