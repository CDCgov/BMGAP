import * as React from "react";
import { Link } from "react-router-dom";

import "./Button.scss";

const BackToButton = ({ link, state, name, position, search }) => {
  return (
    <Link
      to={{
        pathname: link,
        state: state,
        search: search
      }}
    >
      <button className={`btn btn-primary back-btn ${position}`}>{name}</button>
    </Link>
  );
};

export default BackToButton;
