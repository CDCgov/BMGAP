import React, { Fragment } from "react";
import Dropzone from "react-dropzone";

import "../SampleTable/SampleTable.scss";

import SampleRow from "../SampleTable/SampleRow";
import SampleHeaders from "../SampleTable/SampleHeaders";
import Spinner from "../../components/Spinner/Spinner";

function SampleFileUpload(props) {
  return (
    <Fragment>
      <div className={`d-flex flex-row sample-container`}>
        <div className={`d-flex flex-column container sample-box`}>
          <div className="d-flex flex-row">
            <Dropzone onDrop={props.handleFileUpload}>
              {({ getRootProps, getInputProps }) => (
                <section className="mb-4">
                  <div {...getRootProps()}>
                    <input {...getInputProps()} />
                    <button className="btn btn-primary btn-sm px-2">
                      {props.samples
                        ? "Upload another file"
                        : "Click to select file"}
                    </button>
                  </div>
                </section>
              )}
            </Dropzone>
          </div>
          {props.samples &&
            !!props.samples.length &&
            !props.fetchingSamplesFromFile && (
              <Fragment>
                <h3 className="font-weight-bold">{`Table of Samples from File Upload`}</h3>
                <p className="mb-2">
                  <span className="font-weight-bold mr-1">{`Total samples`}</span>
                  <span>{`${props.samples.length}`}</span>
                </p>
                {!!props.selectedSamples.length && (
                  <p className="mb-2">
                    <span className="font-weight-bold mr-1">{`Selected samples for download`}</span>
                    <span>{`${props.selectedSamples.length}`}</span>
                  </p>
                )}
                <div
                  className={
                    `mb-2 d-flex ` +
                    (props.samples.length > 10
                      ? `justify-content-between`
                      : `justify-content-end`)
                  }
                >
                  <div>
                    {!!props.selectedSamples.length && !props.downloadModal && (
                      <button
                        className={`btn btn-sm btn-primary mr-2`}
                        onClick={props.handleDownloadClick}
                      >
                        Download
                      </button>
                    )}
                  </div>
                </div>
                <table className="table table-hover flex-column">
                  <SampleHeaders
                    samples={props.samples}
                    handleCheckAll={props.handleCheckAll}
                    selectedSamples={props.selectedSamples}
                    handleSortClick={props.handleSortClick}
                    sortType={props.sortType}
                  />
                  <tbody>
                    {props.samples &&
                      props.samples.length &&
                      props.samples.map(sample => (
                        <SampleRow
                          key={sample._id}
                          run={props.run}
                          id={sample._id}
                          sample={sample}
                          handleCheckClick={props.handleCheckClick}
                          isChecked={props.selectedSamples.includes(
                            sample.identifier
                          )}
                          search={props.search}
                          isSampleFileUpload={props.isSampleFileUpload}
                        />
                      ))}
                  </tbody>
                </table>
              </Fragment>
            )}
          {props.fetchingSamplesFromFile && <Spinner />}
          {!props.fetchingSamplesFromFile &&
            (!props.samples || !props.samples.length) && (
              <p>No samples available</p>
            )}
        </div>
      </div>
    </Fragment>
  );
}

export default SampleFileUpload;
