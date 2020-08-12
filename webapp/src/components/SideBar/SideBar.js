import React, { Fragment } from "react";
import "./SideBar.scss";

function SideBar(props) {
  return <Fragment>{props.children}</Fragment>;
}

export default SideBar;
