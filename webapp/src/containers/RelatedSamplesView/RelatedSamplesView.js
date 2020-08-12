import React, { Fragment, useState, useEffect } from "react";
import { connect } from "react-redux";
import { withRouter } from "react-router-dom";

import { fetchRelatedSamples } from "../../actions";
import RelatedSamplesTable from "../../components/RelatedSamplesTable/RelatedSamplesTable";
import { getIdFromUrl } from "../../utilities/regexParser";

const RelatedSamplesView = ({
  relatedSamples,
  fetchingRelatedSamples,
  fetchRelatedSamples,
  location,
  totalItems,
  token
}) => {
  const [sampleId] = useState(getIdFromUrl(location, "sample"));

  useEffect(() => {
    fetchRelatedSamples(sampleId, token, relatedSamples);
  }, [fetchRelatedSamples, sampleId, token, relatedSamples]);

  return (
    <Fragment>
      <RelatedSamplesTable
        fetchingRelatedSamples={fetchingRelatedSamples}
        relatedSamples={relatedSamples ? relatedSamples.hits : null}
        totalItems={totalItems}
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

const mapStateToProps = ({ relatedSamples, token }) => ({
  fetchingRelatedSamples: relatedSamples.fetchingRelatedSamples,
  relatedSamples: relatedSamples.relatedSamples,
  totalItems: relatedSamples.relatedSamples
    ? relatedSamples.relatedSamples.total
    : null,
  token: token
});

export default withRouter(
  connect(mapStateToProps, { fetchRelatedSamples })(RelatedSamplesView)
);
