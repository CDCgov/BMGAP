import React, { Fragment } from "react";
import {
  FaRegCheckSquare,
  FaRegSquare,
  FaChevronUp,
  FaChevronDown
} from "react-icons/fa";

import "./SampleTable.scss";

const sortMap = {
  sampleId: { text: "Sample Id", query: "Lab_ID" },
  location: { text: "Location", query: "location" },
  year: { text: "Year", query: "year" },
  submitter: { text: "Submitter", query: "Submitter" },
  mlst: { text: "MLST", query: "MLST" },
  serogrouping: {
    text: "Serogrouping",
    query: "Serogroup"
  },
  serotyping: {
    text: "Serotyping",
    query: "Serotype"
  }
};

function SampleHeaders(props) {
  return (
    <Fragment>
      <thead>
        <tr>
          <th scope="col">
            <span
              onClick={props.handleCheckAll.bind(
                this,
                props.samples.map(sample => sample.identifier)
              )}
            >
              {props.selectedSamples.length === props.samples.length ? (
                <FaRegCheckSquare />
              ) : (
                <FaRegSquare />
              )}
            </span>
          </th>
          <th
            scope="col"
            onClick={props.handleSortClick.bind(
              this,
              calculateSortValue(props.sortType, sortMap.sampleId.query)
            )}
          >
            {calculateSortHeader(props.sortType, sortMap.sampleId)}
          </th>
          <th
            scope="col"
            onClick={props.handleSortClick.bind(
              this,
              calculateSortValue(props.sortType, sortMap.location.query)
            )}
          >
            {calculateSortHeader(props.sortType, sortMap.location)}
          </th>
          <th
            scope="col"
            onClick={props.handleSortClick.bind(
              this,
              calculateSortValue(props.sortType, sortMap.year.query)
            )}
          >
            {calculateSortHeader(props.sortType, sortMap.year)}
          </th>
          <th
            scope="col"
            onClick={props.handleSortClick.bind(
              this,
              calculateSortValue(props.sortType, sortMap.submitter.query)
            )}
          >
            {calculateSortHeader(props.sortType, sortMap.submitter)}
          </th>
          <th scope="col">Species</th>
          <th
            scope="col"
            onClick={props.handleSortClick.bind(
              this,
              calculateSortValue(props.sortType, sortMap.mlst.query)
            )}
          >
            {calculateSortHeader(props.sortType, sortMap.mlst)}
          </th>
          <th
            scope="col"
            onClick={props.handleSortClick.bind(
              this,
              calculateSortValue(props.sortType, sortMap.serogrouping.query)
            )}
          >
            {calculateSortHeader(props.sortType, sortMap.serogrouping)}
          </th>
          <th
            scope="col"
            onClick={props.handleSortClick.bind(
              this,
              calculateSortValue(props.sortType, sortMap.serotyping.query)
            )}
          >
            {calculateSortHeader(props.sortType, sortMap.serotyping)}
          </th>
        </tr>
      </thead>
    </Fragment>
  );
}

function calculateSortValue(sortType, sortValue) {
  if (sortType && sortType === sortValue) {
    return "-" + sortValue;
  } else return sortValue;
}

function calculateSortHeader(sortType, sortValue) {
  return (
    <div className="d-inline-flex flex-wrap sample-header">
      <div className="d-inline-flex>">{`${sortValue.text}`}</div>
      <div className="pl-2 d-inline-flex flex-column sort-icons">
        {sortType && sortType === sortValue.query && (
          <Fragment>
            <FaChevronUp className={`sort-icon-on`} />
            <FaChevronDown className={`sort-icon-off`} />
          </Fragment>
        )}
        {sortType && sortType === "-" + sortValue.query && (
          <Fragment>
            <FaChevronUp className={`sort-icon-off`} />
            <FaChevronDown className={`sort-icon-on`} />
          </Fragment>
        )}
        {(!sortType ||
          (sortType !== sortValue.query &&
            sortType !== "-" + sortValue.query)) && (
          <Fragment>
            <FaChevronUp className={`sort-icon-off`} />
            <FaChevronDown className={`sort-icon-off`} />
          </Fragment>
        )}
      </div>
    </div>
  );
}

export default SampleHeaders;
