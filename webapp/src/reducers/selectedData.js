import * as Types from "../actions/actionTypes";

const selectedData = (
  state = { runs: [], sample: null, phyloTree: null },
  action
) => {
  switch (action.type) {
    case Types.SET_CURRENT_RUN:
      return Object.assign({}, state, {
        runs: action.runs
      });
    case Types.SET_CURRENT_SAMPLE:
      return Object.assign({}, state, {
        sample: action.sample
      });
    case Types.SET_CURRENT_PHYLO:
      return Object.assign({}, state, {
        phyloTree: action.phyloTree
      });
    default:
      return state;
  }
};

export default selectedData;
