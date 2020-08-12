import * as Types from "../actions/actionTypes";

const runs = (state = {}, action) => {
  switch (action.type) {
    case Types.FETCH_RECENT_RUNS_ASYNC:
      return Object.assign({}, state, {
        fetchingRuns: action.fetchingRuns
      });
    case Types.FETCH_RECENT_RUNS_SUCCESS:
      return Object.assign({}, state, {
        runs: action.runs,
        fetchingRuns: false
      });
    case Types.FETCH_RECENT_RUNS_FAILURE:
      return Object.assign({}, state, {
        runs: null,
        fetchingRuns: false
      });
    default:
      return state;
  }
};

export default runs;
