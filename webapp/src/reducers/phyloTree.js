import * as Types from "../actions/actionTypes";

const phyloTree = (state = {}, action) => {
  switch (action.type) {
    case Types.FETCH_PHYLOTREE_ASYNC:
      return Object.assign({}, state, {
        fetchingPhyloTree: action.fetchingPhyloTree
      });
    case Types.FETCH_PHYLOTREE_SUCCESS:
      return Object.assign({}, state, {
        phyloTree: action.phyloTree,
        fetchingPhyloTree: false
      });
    case Types.FETCH_PHYLOTREE_FAILURE:
      return Object.assign({}, state, {
        phyloTree: null,
        fetchingPhyloTree: false
      });
    default:
      return state;
  }
};

export default phyloTree;
