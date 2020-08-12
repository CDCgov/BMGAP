import React, { Fragment, useState, useEffect } from "react";
import { connect } from "react-redux";
import { withRouter } from "react-router-dom";

import { fetchPhyloTree } from "../../actions";
import PhyloTree from "../../components/PhyloTree/PhyloTree";
import Spinner from "../../components/Spinner/Spinner";
import { getIdFromUrl } from "../../utilities/regexParser";

const PhyloView = ({
  relatedSamples,
  fetchPhyloTree,
  fetchingPhyloTree,
  phyloTree,
  location
}) => {
  const [sampleId] = useState(getIdFromUrl(location, "phylo"));

  useEffect(() => {
    fetchPhyloTree(relatedSamples, sampleId, phyloTree);
  }, [fetchPhyloTree, relatedSamples, sampleId, phyloTree]);

  return (
    <Fragment>
      {(phyloTree && !fetchingPhyloTree && (
        <PhyloTree
          phyloTree={phyloTree}
          sampleId={sampleId}
          runId={location.state ? location.state.run : []}
          search={location.search || location.hash}
          isSampleFileUpload={
            location.state ? location.state.isSampleFileUpload : false
          }
        />
      )) ||
        (fetchingPhyloTree && (
          <div className="mt-5 container pt-5 d-flex flex-column">
            <div className="d-flex justify-content-center mt-5">
              <Spinner />
            </div>
            <div className="d-flex justify-content-center mt-4">
              <h5>This page may take up to, and beyond 30 seconds to load</h5>
            </div>
          </div>
        ))}
    </Fragment>
  );
};

const mapStateToProps = ({ relatedSamples, phyloTree }) => ({
  fetchingPhyloTree: phyloTree.fetchingPhyloTree,
  phyloTree: phyloTree.phyloTree,
  relatedSamples: relatedSamples.relatedSamples
    ? relatedSamples.relatedSamples
    : null
});

export default withRouter(
  connect(mapStateToProps, { fetchPhyloTree })(PhyloView)
);
