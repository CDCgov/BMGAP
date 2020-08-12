import * as Types from "../actions/actionTypes";

const sampleDetails = (state = {}, action) => {
  switch (action.type) {
    case Types.FETCH_SAMPLE_DETAILS_ASYNC:
      return Object.assign({}, state, {
        fetchingSampleDetails: action.fetchingSampleDetails
      });
    case Types.FETCH_SAMPLE_DETAILS_SUCCESS:
      return Object.assign({}, state, {
        sampleDetails: action.sampleDetails,
        fetchingSampleDetails: false
      });
    case Types.FETCH_SAMPLE_DETAILS_FAILURE:
      return Object.assign({}, state, {
        sampleDetails: null,
        fetchingSampleDetails: false
      });
    default:
      return state;
  }
};

export default sampleDetails;
