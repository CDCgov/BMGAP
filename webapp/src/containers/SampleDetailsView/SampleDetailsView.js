import React, { Fragment, useState, useEffect } from "react";
import { connect } from "react-redux";
import { withRouter } from "react-router-dom";

import {
  fetchSampleDetails,
  fetchFeatureViewer,
  setToken
} from "../../actions";
import { getToken, getIdFromUrl } from "../../utilities/regexParser";
import SampleDetails from "../../components/SampleDetails/SampleDetails";

const SampleDetailsView = ({
  sampleDetails,
  fetchingSampleDetails,
  fetchSampleDetails,
  fetchFeatureViewer,
  fetchingFeatureViewer,
  featureViewer,
  location,
  setToken,
  token
}) => {
  const [sampleId] = useState(getIdFromUrl(location, "sampleDetails"));

  useEffect(() => {
    setToken(getToken(location));
  }, [setToken, location]);

  useEffect(() => {
    fetchSampleDetails(sampleId, token);
  }, [fetchSampleDetails, sampleId, token]);

  useEffect(() => {
    fetchFeatureViewer(sampleId, token);
  }, [fetchFeatureViewer, sampleId, token]);

  return (
    <Fragment>
      <SampleDetails
        sampleDetails={sampleDetails}
        featureViewer={featureViewer}
        fetchingSampleDetails={fetchingSampleDetails}
        fetchingFeatureViewer={fetchingFeatureViewer}
        sampleId={sampleId}
        runId={location.state ? location.state.run : []}
        search={location.search || location.hash}
        isSampleFileUpload={
          location.state ? location.state.isSampleFileUpload : false
        }
      />
    </Fragment>
  );
};

const mapStateToProps = ({ sampleDetails, token, featureViewer }) => ({
  fetchingSampleDetails: sampleDetails.fetchingSampleDetails,
  sampleDetails: sampleDetails.sampleDetails,
  featureViewer: featureViewer.featureViewer,
  fetchingFeatureViewer: featureViewer.fetchingFeatureViewer,
  token: token
});

export default withRouter(
  connect(mapStateToProps, {
    fetchSampleDetails,
    fetchFeatureViewer,
    setToken
  })(SampleDetailsView)
);
