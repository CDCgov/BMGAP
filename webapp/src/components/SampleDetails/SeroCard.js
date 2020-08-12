import React, { Fragment } from "react";

import "../SampleDetails/SampleDetails.scss";

const HAEMOPHILUS = "Haemophilus_influenzae";
const NEISSERIA = "Neisseria_meningitidis";

function SeroCard({ sampleDetails }) {
  return (
    <Fragment>
      {sampleDetails.mash && (
        <div className="card mb-4">
          {sampleDetails.mash &&
            sampleDetails.mash.Top_Species === HAEMOPHILUS && (
              <Fragment>
                <h3 className="card-header font-weight-bold">
                  Serotype Information
                </h3>
                <div className="card-body">
                  {sampleDetails.Serotype && sampleDetails.Serotype.ST ? (
                    <p className="card-text">
                      <span className="font-weight-bold">
                        Predicted Serotype{" "}
                      </span>
                      {sampleDetails.Serotype.ST}
                    </p>
                  ) : null}
                  {sampleDetails.Serotype && sampleDetails.Serotype.Notes ? (
                    <p className="card-text">
                      <span className="font-weight-bold">Notes </span>
                      {sampleDetails.Serotype.Notes}
                    </p>
                  ) : null}
                  {sampleDetails.Serotype &&
                  sampleDetails.Serotype.Genes_Present
                    ? generateGenes(sampleDetails.Serotype.Genes_Present)
                    : null}
                </div>
              </Fragment>
            )}
          {sampleDetails.mash && sampleDetails.mash.Top_Species === NEISSERIA && (
            <Fragment>
              <h3 className="card-header font-weight-bold">
                Serogroup Information
              </h3>
              <div className="card-body">
                {sampleDetails.Serogroup && sampleDetails.Serogroup.SG ? (
                  <p className="card-text">
                    <span className="font-weight-bold">
                      Predicted Serogroup{" "}
                    </span>
                    {sampleDetails.Serogroup.SG}
                  </p>
                ) : null}
                {sampleDetails.Serogroup && sampleDetails.Serogroup.Notes ? (
                  <p className="card-text">
                    <span className="font-weight-bold">Notes </span>
                    {sampleDetails.Serogroup.Notes}
                  </p>
                ) : null}
                {sampleDetails.Serogroup &&
                sampleDetails.Serogroup.Genes_Present
                  ? generateGenes(sampleDetails.Serogroup.Genes_Present)
                  : null}
              </div>
            </Fragment>
          )}
        </div>
      )}
    </Fragment>
  );
}

export default SeroCard;

function generateGenes(genes) {
  const geneList = genes.split(",");
  if (!geneList.length) {
    return null;
  }
  return (
    <Fragment>
      <hr />
      <p className="card-text">
        <span className="font-weight-bold">Genes Present </span>
      </p>
      <div className="container">
        <div className="row">
          {geneList.map(gene => (
            <div key={gene} className="col">
              {gene}
            </div>
          ))}
        </div>
      </div>
    </Fragment>
  );
}
