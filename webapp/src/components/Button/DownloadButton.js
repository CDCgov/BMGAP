import * as React from "react";

import "./Button.scss";

const DownloadButton = ({ data, handleClick }) => {
  return (
    <div
      className={`btn-lg btn-primary download-btn`}
      onClick={handleClick.bind(this)}
    >
      Download
    </div>
  );
};

export default DownloadButton;
