import React from "react";
import { Link } from "react-router-dom";

import "./Header.scss";
import haemophilus from "../../haemophilus_circ_small.png";
import neisseria from "../../neisseria_circ_small.png";

function Header(props) {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark main-header">
      <Link
        to={{
          pathname: `/`,
          search: props.search
        }}
        style={{ textDecoration: "none" }}
      >
        <span className="mb-0 h1 header-text py-2">{props.name}</span>
      </Link>
      <span className="mb-0 ml-3 h5 header-subtext">
        Bacterial Meningitis Genome Analysis Platform
      </span>
      <img
        className="ml-3 logo"
        src={haemophilus}
        height="50"
        alt="Haemophilus"
      />
      <img className="ml-3 logo" src={neisseria} height="50" alt="Neisseria" />
    </nav>
  );
}

export default Header;
