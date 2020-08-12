import React, { Fragment } from "react";
import { Link } from "react-router-dom";

import "./SampleDetails.scss";

const CustomSideBar = ({
  link,
  state,
  search,
  sampleId,
  runId,
  buttonText,
  currentView
}) => {
  return (
    <Fragment>
      <div
        className={`container sample-control-container mx-0 px-5 d-flex flex-column`}
      >
        <Link
          to={{
            pathname: link,
            state: state,
            search: search
          }}
        >
          <button className={`btn btn-primary back-btn btn-block`}>
            {buttonText}
          </button>
        </Link>
        {currentView === "related-samples" && (
          <Link
            to={{
              state: { sample: sampleId, run: runId },
              pathname: `/phylo/${sampleId}`,
              search: search
            }}
          >
            <button className={`btn btn-primary back-btn mt-3 btn-block`}>
              View Phylo Tree
            </button>
          </Link>
        )}
      </div>
    </Fragment>
  );
};

export default CustomSideBar;
