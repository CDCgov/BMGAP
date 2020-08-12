import React, { Fragment, useEffect } from "react";
import Phylocanvas from "phylocanvas";
import { Link } from "react-router-dom";

import "./PhyloTree.scss";

function PhyloTree({ phyloTree, sampleId, runId, search, isSampleFileUpload }) {
  useEffect(() => {
    let tree = Phylocanvas.createTree("phylocanvas", {
      fillCanvas: false,
      textSize: 16,
      hoverLabels: true
    });
    tree.load(phyloTree);
    tree.setTreeType("rectangular");
  }, [phyloTree]);

  return (
    <Fragment>
      <div className={`d-flex flex-row phylo-container`}>
        <div className={`container-fluid d-flex flex-column px-5`}>
          <h3 className="font-weight-bold">{`Phylogenetic Tree`}</h3>
          <div className={`mb-2 d-flex justify-content-end`}>
            <Link
              to={{
                pathname: `/sample/${sampleId}`,
                state: { run: runId, sample: sampleId, isSampleFileUpload },
                search: search
              }}
            >
              <button className="btn btn-sm btn-primary">
                Back to Related Samples
              </button>
            </Link>
          </div>
          <div className="phylocanvas border rounded mb-4" id="phylocanvas" />
          <h3 className="font-weight-bold">{`Newick String`}</h3>
          <div className="mb-4">
            <textarea
              readOnly
              value={phyloTree}
              className={`form-control`}
              id="validationTextarea"
              placeholder="Newick string will go here"
              rows="10"
            />
          </div>
        </div>
      </div>
    </Fragment>
  );
}

export default PhyloTree;
