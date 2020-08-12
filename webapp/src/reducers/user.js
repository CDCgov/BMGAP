import * as Types from "../actions/actionTypes";

const user = (state = {}, action) => {
  switch (action.type) {
    case Types.FETCH_USER_SUCCESS:
      return action.user;
    default:
      return state;
  }
};

export default user;
