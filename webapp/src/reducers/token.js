import * as Types from "../actions/actionTypes";

const token = (state = null, action) => {
  switch (action.type) {
    case Types.SET_TOKEN:
      return action.token;
    default:
      return state;
  }
};

export default token;
