import * as Types from '../actions/actionTypes';

const filters = (state = {}, action) => {
  switch (action.type) {
    case Types.FETCH_FILTERS_SUCCESS:
      return action.filters;
    default:
      return state;
  }
};

export default filters;
