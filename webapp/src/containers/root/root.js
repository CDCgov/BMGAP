import React, { Fragment } from "react";
import PropTypes from "prop-types";
import { Provider } from "react-redux";
import { BrowserRouter as Router } from "react-router-dom";
import { createBrowserHistory } from "history";

import App from "../app/App";

const history = createBrowserHistory();

const Root = ({ store }) => (
  <Provider store={store}>
    <Router basename="/bmgap">
      <Fragment>
        <App history={history} />
      </Fragment>
    </Router>
  </Provider>
);

Root.propTypes = {
  store: PropTypes.object.isRequired
};

export default Root;
