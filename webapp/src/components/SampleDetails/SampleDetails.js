import React, { Fragment } from "react";
import Spinner from "../../components/Spinner/Spinner";
import { Link } from "react-router-dom";

import "./SampleDetails.scss";
import SampleCard from "./SampleCard";
import SpeciesCard from "./SpeciesCard";
import MLSTCard from "./MLSTCard";
import SeroCard from "./SeroCard";

function SampleDetails({
  sampleDetails,
  fetchingSampleDetails,
  featureViewer,
  fetchingFeatureViewer,
  runId,
  search,
  isSampleFileUpload,
}) {
  return (
    <Fragment>
      <div className={`sample-container`}>
        <div className={`container`}>
          {sampleDetails && !fetchingSampleDetails && !fetchingFeatureViewer && (
            <Fragment>
              <div className={`mb-4 d-flex justify-content-end back-button`}>
                <Link
                  to={{
                    pathname: isSampleFileUpload
                      ? `/sampleFileUpload`
                      : `/run/${runId}`,
                    state: { run: runId, isSampleFileUpload },
                    search: search,
                  }}
                >
                  <button className="btn btn-sm btn-primary">
                    Back to Samples
                  </button>
                </Link>
              </div>
              <SampleCard
                sampleDetails={sampleDetails}
                featureViewer={featureViewer}
              />
              <SpeciesCard sampleDetails={sampleDetails} />
              <SeroCard sampleDetails={sampleDetails} />
              <MLSTCard sampleDetails={sampleDetails} />
            </Fragment>
          )}
          {(fetchingSampleDetails || fetchingFeatureViewer) && <Spinner />}
          {!fetchingSampleDetails &&
            !fetchingFeatureViewer &&
            !sampleDetails && <p>No sample details available</p>}
        </div>
      </div>
    </Fragment>
  );
}

export default SampleDetails;
