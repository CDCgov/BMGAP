import React, { Fragment } from "react";
import { FaExclamationTriangle } from "react-icons/fa";

import "../SampleDetails/SampleDetails.scss";

const WARNING =
  "No hit above threshold from reference collection Reporting top refseq hit";

function SpeciesCard({ sampleDetails }) {
  return (
    <Fragment>
      {sampleDetails.mash && (
        <div className="card mb-4">
          <h3 className="card-header font-weight-bold">Species Information</h3>
          <div className="card-body">
            {sampleDetails.mash && sampleDetails.mash.Top_Species ? (
              <p className="card-text">
                <span className="font-weight-bold">Predicted Species </span>
                {removeUnderscores(sampleDetails.mash.Top_Species)}
              </p>
            ) : null}
            {sampleDetails.mash && sampleDetails.mash.Mash_Dist ? (
              <p className="card-text">
                <span className="font-weight-bold">Score </span>
                {Number.parseFloat(sampleDetails.mash.Mash_Dist).toFixed(4)}
              </p>
            ) : null}
            {sampleDetails.mash && sampleDetails.mash.Notes ? (
              <p className="card-text">
                <span className="font-weight-bold">Notes </span>
                {setWarning(removeUnderscores(sampleDetails.mash.Notes))}
              </p>
            ) : null}
          </div>
        </div>
      )}
    </Fragment>
  );
}

export default SpeciesCard;

function removeUnderscores(text) {
  return text.replace(/_/g, " ");
}

function setWarning(text) {
  if (text === WARNING) {
    return (
      <span>
        {text}
        <FaExclamationTriangle className="ml-2 text-warning" />
      </span>
    );
  } else return text;
}
