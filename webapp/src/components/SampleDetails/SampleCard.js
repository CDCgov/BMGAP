import React, { Fragment } from "react";

import "../SampleDetails/SampleDetails.scss";
import FeatureViewerBox from "../FeatureViewerBox/FeatureViewerBox";

const HAEMOPHILUS = "Haemophilus_influenzae";
const NEISSERIA = "Neisseria_meningitidis";

function SampleCard({ sampleDetails, featureViewer }) {
  return (
    <Fragment>
      <div className="card mb-4">
        <h3 className="card-header font-weight-bold">Sample Details</h3>
        <div className="card-body">
          {!!sampleDetails.QC_flagged && (
            <Fragment>
              <p className="card-text">
                <span className="font-weight-bold text-danger">
                  The QC process has flagged this sample
                </span>
              </p>
              <p className="card-text">
                <span className="font-weight-bold">
                  Mean Assembly Coverage{" "}
                </span>
                {sampleDetails.cleanData
                  ? Number.parseFloat(
                      sampleDetails.cleanData.Mean_Coverage
                    ).toFixed(4)
                  : "-"}
              </p>
              <p className="card-text">
                <span className="font-weight-bold">Discarded % </span>
                {sampleDetails.cleanData
                  ? Number.parseFloat(
                      sampleDetails.cleanData.Discarded_Percent
                    ).toFixed(4)
                  : "-"}
              </p>
              <p className="card-text">
                <span className="font-weight-bold">HalfCov % </span>
                {sampleDetails.cleanData
                  ? Number.parseFloat(
                      sampleDetails.cleanData.HalfCov_Percent
                    ).toFixed(4)
                  : "-"}
              </p>
              <hr />
            </Fragment>
          )}
          {sampleDetails.Lab_ID ? (
            <p className="card-text">
              <span className="font-weight-bold">Lab ID </span>
              {sampleDetails.Lab_ID}
            </p>
          ) : null}
          {sampleDetails.Assembly_ID ? (
            <p className="card-text">
              <span className="font-weight-bold">Assembly ID </span>
              {sampleDetails.Assembly_ID}
            </p>
          ) : null}
          {sampleDetails.Run_ID ? (
            <p className="card-text">
              <span className="font-weight-bold">Run ID </span>
              {sampleDetails.Run_ID}
            </p>
          ) : null}
          {sampleDetails.mash && sampleDetails.mash.Top_Species ? (
            <p className="card-text">
              <span className="font-weight-bold">Species </span>
              {sampleDetails.mash.Top_Species.replace(/_/g, " ")}
            </p>
          ) : null}
          {generateSero(sampleDetails)}
          {generateMLST(sampleDetails)}
          {generateLocation(sampleDetails)}
          {sampleDetails.BML_Data && sampleDetails.BML_Data.year ? (
            <p className="card-text">
              <span className="font-weight-bold">Year Collected </span>
              {sampleDetails.BML_Data.year}
            </p>
          ) : null}
          {sampleDetails.BML_Data && sampleDetails.BML_Data.sample_type ? (
            <p className="card-text">
              <span className="font-weight-bold">Sample Type </span>
              {sampleDetails.BML_Data.sample_type}
            </p>
          ) : null}
          {generateLabSero(sampleDetails)}
          {generatePCRSero(sampleDetails)}

          {sampleDetails.mash &&
            (sampleDetails.mash.Top_Species === NEISSERIA ||
              sampleDetails.mash.Top_Species === HAEMOPHILUS) &&
            featureViewer && (
              <Fragment>
                <hr />
                <FeatureViewerBox data={featureViewer} />
              </Fragment>
            )}
        </div>
      </div>
    </Fragment>
  );
}

export default SampleCard;

function generateSero(sample) {
  if (
    sample.Serogroup &&
    sample.mash &&
    sample.mash.Top_Species === NEISSERIA
  ) {
    return (
      <p className="card-text">
        <span className="font-weight-bold">Predicted Serogroup </span>
        {sample.Serogroup.SG}
      </p>
    );
  } else if (
    sample.Serotype &&
    sample.mash &&
    sample.mash.Top_Species === HAEMOPHILUS
  ) {
    return (
      <p className="card-text">
        <span className="font-weight-bold">Predicted Serotype </span>
        {sample.Serotype.ST}
      </p>
    );
  } else {
    return null;
  }
}

function generateMLST(sample) {
  if (
    sample.MLST &&
    sample.MLST.ST &&
    sample.MLST.Nm_MLST_cc &&
    sample.mash &&
    sample.mash.Top_Species === NEISSERIA
  ) {
    return (
      <p className="card-text">
        <span className="font-weight-bold">Sequence Type </span>
        {sample.MLST.ST} ({sample.MLST.Nm_MLST_cc})
      </p>
    );
  } else if (
    sample.MLST &&
    sample.mash &&
    sample.mash.Top_Species === HAEMOPHILUS
  ) {
    return (
      <p className="card-text">
        <span className="font-weight-bold">Sequence Type </span>
        {sample.MLST.ST}
      </p>
    );
  } else {
    return null;
  }
}

function generateLocation(sample) {
  if (sample.BML_Data && sample.BML_Data.country && sample.BML_Data.state) {
    return (
      <p className="card-text">
        <span className="font-weight-bold">Country - State </span>
        {sample.BML_Data.country} - {sample.BML_Data.state}
      </p>
    );
  } else if (
    sample.BML_Data &&
    sample.BML_Data.country &&
    !sample.BML_Data.state
  ) {
    return (
      <p className="card-text">
        <span className="font-weight-bold">Country </span>
        {sample.BML_Data.country}
      </p>
    );
  } else {
    return null;
  }
}

function generateLabSero(sample) {
  if (
    sample.BML_Data &&
    sample.BML_Data.lab_sg &&
    sample.mash &&
    sample.mash.Top_Species === NEISSERIA
  ) {
    return (
      <p className="card-text">
        <span className="font-weight-bold">Lab Serogroup </span>
        {sample.BML_Data.lab_sg}
      </p>
    );
  } else if (
    sample.BML_Data &&
    sample.BML_Data.lab_st &&
    sample.mash &&
    sample.mash.Top_Species === HAEMOPHILUS
  ) {
    return (
      <p className="card-text">
        <span className="font-weight-bold">Lab Serotype </span>
        {sample.BML_Data.lab_st}
      </p>
    );
  } else {
    return null;
  }
}

function generatePCRSero(sample) {
  if (
    sample.BML_Data &&
    sample.BML_Data.pcr_sg &&
    sample.mash &&
    sample.mash.Top_Species === NEISSERIA
  ) {
    return (
      <p className="card-text">
        <span className="font-weight-bold">PCR Serogroup </span>
        {sample.BML_Data.pcr_sg}
      </p>
    );
  } else if (
    sample.BML_Data &&
    sample.BML_Data.pcr_st &&
    sample.mash &&
    sample.mash.Top_Species === HAEMOPHILUS
  ) {
    return (
      <p className="card-text">
        <span className="font-weight-bold">PCR Serotype </span>
        {sample.BML_Data.pcr_st}
      </p>
    );
  } else {
    return null;
  }
}
