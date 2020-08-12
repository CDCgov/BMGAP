import React, { Fragment } from "react";

import "./SampleTable.scss";

import Pagination from "../Pagination/Pagination";
import PageInfo from "../Pagination/PageInfo";
import SampleRow from "./SampleRow";
import SampleHeaders from "./SampleHeaders";
// import DownloadButton from "../Button/DownloadButton";
import Spinner from "../../components/Spinner/Spinner";

function SampleTable(props) {
  return (
    <Fragment>
      <div className={`d-flex flex-row sample-container`}>
        <div className="ghost-box invisible">Ghost box</div>
        <div className={`d-flex flex-column container sample-box`}>
          {props.samples && !!props.samples.length && !props.fetchingSamples && (
            <Fragment>
              <h3 className="font-weight-bold">{`Table of Samples`}</h3>
              {props.run && (
                <Fragment>
                  {((Array.isArray(props.run) &&
                    props.run.length === 1 &&
                    props.run[0] !== "") ||
                    typeof props.run === "string") && (
                    <p className="mb-2">
                      <span className="font-weight-bold mr-2">{`Displaying samples for Run ID`}</span>
                      <span>{`${props.run}`}</span>
                    </p>
                  )}
                </Fragment>
              )}
              {(!props.run ||
                (Array.isArray(props.run) && props.run.length === 0) ||
                (Array.isArray(props.run) &&
                  props.run.length === 1 &&
                  props.run[0] === "")) && (
                <p className="mb-2 font-weight-bold">{`Displaying samples from all Runs`}</p>
              )}
              {Array.isArray(props.run) && props.run.length > 1 && (
                <p className="mb-2 font-weight-bold">{`Displaying samples from multiple Runs`}</p>
              )}
              <p className="mb-2">
                <span className="font-weight-bold mr-1">{`Total samples`}</span>
                <span>{`${props.totalItems}`}</span>
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
                {props.samples.length > 10 && (
                  <Pagination
                    onPageClick={props.onPageClick}
                    totalPages={Math.ceil(
                      props.totalItems / props.itemNumberFilter
                    )}
                    currentPage={props.currentPage}
                    totalItems={props.totalItems}
                    itemsPerPage={props.samples.length}
                  />
                )}
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
                      />
                    ))}
                </tbody>
              </table>
              <Pagination
                onPageClick={props.onPageClick}
                totalPages={Math.ceil(
                  props.totalItems / props.itemNumberFilter
                )}
                currentPage={props.currentPage}
                totalItems={props.totalItems}
                itemsPerPage={props.samples.length}
              />
              <PageInfo
                currentPage={props.currentPage}
                totalItems={props.totalItems}
                itemNumberFilter={props.itemNumberFilter}
              />
            </Fragment>
          )}
          {props.fetchingSamples && <Spinner />}
          {!props.fetchingSamples &&
            (!props.samples || !props.samples.length) && (
              <p>No samples available</p>
            )}
        </div>
      </div>
      {/* {!!props.selectedSamples.length && !props.downloadModal && (
        <DownloadButton handleClick={props.handleDownloadClick} />
      )} */}
    </Fragment>
  );
}

export default SampleTable;
