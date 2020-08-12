import React, { Fragment } from "react";
import Spinner from "../../components/Spinner/Spinner";
import { Link } from "react-router-dom";

import "../SampleTable/SampleTable.scss";

import SampleRow from "../SampleTable/SampleRow";

function RelatedSamplesTable(props) {
  return (
    <Fragment>
      <div className={`d-flex flex-row sample-container`}>
        <div className={`container d-flex flex-column`}>
          <h3 className="font-weight-bold">{`Table of Related Samples`}</h3>
          {props.relatedSamples &&
            !!props.relatedSamples.length &&
            !props.fetchingRelatedSamples && (
              <Fragment>
                <div className={`mb-4 d-flex justify-content-end`}>
                  <Link
                    to={{
                      pathname: props.isSampleFileUpload
                        ? `/sampleFileUpload`
                        : `/run/${props.runId}`,
                      state: {
                        run: props.runId,
                        isSampleFileUpload: props.isSampleFileUpload
                      },
                      search: props.search
                    }}
                  >
                    <button className="btn btn-sm btn-primary mr-2">
                      Back to Samples
                    </button>
                  </Link>
                  <Link
                    to={{
                      state: {
                        sample: props.sampleId,
                        run: props.runId,
                        isSampleFileUpload: props.isSampleFileUpload
                      },
                      pathname: `/phylo/${props.sampleId}`,
                      search: props.search
                    }}
                  >
                    <button className={`btn btn-sm btn-primary`}>
                      View Phylo Tree
                    </button>
                  </Link>
                </div>
                <table className="table table-hover">
                  <thead>
                    <tr>
                      <th scope="col">Sample Id</th>
                      <th scope="col">Location</th>
                      <th scope="col">Year</th>
                      <th scope="col">Submitter</th>
                      <th scope="col">Species</th>
                      <th scope="col">MLST</th>
                      <th scope="col">Serogrouping</th>
                      <th scope="col">Serotyping</th>
                      <th scope="col">Similarity</th>
                    </tr>
                  </thead>
                  <tbody>
                    {props.relatedSamples &&
                      props.relatedSamples.length &&
                      props.relatedSamples.map(relatedSample => (
                        <SampleRow
                          key={relatedSample.Lab_ID}
                          id={relatedSample.Lab_ID}
                          sample={relatedSample}
                          search={props.search}
                          isRelatedSample={props.relatedSamples}
                        />
                      ))}
                  </tbody>
                </table>
              </Fragment>
            )}
          {props.fetchingRelatedSamples && (
            <div className="mt-5 pt-5">
              <div className="d-flex justify-content-center">
                <Spinner />
              </div>
              <div className="d-flex justify-content-center mt-4">
                <h5>This page may take up to, and beyond 30 seconds to load</h5>
              </div>
            </div>
          )}
          {!props.fetchingRelatedSamples &&
            (!props.relatedSamples || !props.relatedSamples.length) && (
              <p>No related samples available</p>
            )}
        </div>
      </div>
    </Fragment>
  );
}

export default RelatedSamplesTable;
