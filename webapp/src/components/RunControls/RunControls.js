import React, { Fragment, useEffect } from "react";
import { isEmpty } from "lodash";
import Select from "react-select";
import { Link } from "react-router-dom";

import "./RunControls.scss";

const RunControls = props => {
  useEffect(() => {}, [props.selectedFilters]);

  const onHandleFilterChange = (filterType, event) => {
    const result = handleEventObject(event);
    props.onHandleChange(filterType, result);
  };

  const handleEventObject = event => {
    if (event.length && Array.isArray(event)) {
      if (event.find(item => item.label === "All")) return [""];
      return event.map(filter => filter.value);
    }
    if (event.target) return event.target.value;
    if (event.value) return event.value;
    return null;
  };

  const createSelectArray = items => {
    return items.map(item => {
      return {
        value: item,
        label: item
      };
    });
  };

  const mapToObject = value => {
    if (typeof value === "string" || typeof value === "number") {
      return { value: value, label: value };
    }
    if (Array.isArray(value)) {
      return createSelectArray(value);
    }
    return [];
  };

  if (isEmpty(props.runFilters)) return <div />;
  return (
    <Fragment>
      <div className={`container run-control-container mx-0`}>
        <div className={`form-row justify-content-center`}>
          <div
            className="btn-group btn-group-toggle mb-4"
            data-toggle="buttons"
          >
            <button className="btn btn-sm btn-primary active empty-toggle">
              Runs
            </button>
            <Link
              to={{
                pathname: "/run",
                state: { run: [] },
                search: props.search
              }}
            >
              <button className="btn btn-sm btn-light toggle-right">
                Samples
              </button>
            </Link>
          </div>
        </div>
        <div className={`form-row`}>
          <div className={`col font-weight-bold filter-title`}>Filters</div>
          <button
            className="btn btn-sm btn-link mr-2"
            onClick={props.handleClearRunFilters.bind(this, null)}
          >
            Clear Filters
          </button>
        </div>
        <div className={`form-row run-filter-form mt-3`}>
          <div className={`col`}>
            <label className="filter-label"># of Runs</label>
            <Select
              options={[
                { value: "5", label: "5" },
                { value: "10", label: "10" },
                { value: "25", label: "25" }
              ]}
              isSearchable={false}
              defaultValue={
                props.selectedFilters.numberOfRuns
                  ? {
                      value: props.selectedFilters.numberOfRuns,
                      label: props.selectedFilters.numberOfRuns
                    }
                  : { value: "10", label: "10" }
              }
              value={
                props.selectedFilters.numberOfRuns
                  ? {
                      value: props.selectedFilters.numberOfRuns,
                      label: props.selectedFilters.numberOfRuns
                    }
                  : { value: "10", label: "10" }
              }
              onChange={onHandleFilterChange.bind(this, "numberOfRuns")}
            />
          </div>
        </div>

        <div className={`form-row run-filter-form mt-3`}>
          <div className={`col`}>
            <label className="filter-label">Submitter</label>
            <Select
              isMulti
              options={createSelectArray([...props.runFilters.submitter])}
              isSearchable={false}
              onChange={onHandleFilterChange.bind(this, "submitter")}
              defaultValue={mapToObject(props.selectedFilters.submitter)}
              value={mapToObject(props.selectedFilters.submitter)}
            />
          </div>
        </div>
        <div className={`form-row run-filter-form mt-3`}>
          <div className={`col`}>
            <label className="filter-label">Sequencer</label>
            <Select
              isMulti
              options={createSelectArray([...props.runFilters.sequencer])}
              isSearchable={false}
              onChange={onHandleFilterChange.bind(this, "runSequencer")}
              defaultValue={mapToObject(props.selectedFilters.runSequencer)}
              value={mapToObject(props.selectedFilters.runSequencer)}
            />
          </div>
        </div>
        <div className={`form-row run-filter-form mt-3`}>
          <div className={`col`}>
            <label className="filter-label">Start Date</label>
            <Select
              options={createSelectArray([...props.runFilters.year])}
              isSearchable={false}
              onChange={onHandleFilterChange.bind(this, "startDate")}
              defaultValue={mapToObject(props.selectedFilters.startDate)}
              value={mapToObject(props.selectedFilters.startDate)}
            />
          </div>
        </div>
        <div className={`form-row run-filter-form mt-3`}>
          <div className={`col`}>
            <label className="filter-label">End Date</label>
            <Select
              options={createSelectArray([...props.runFilters.year])}
              isSearchable={false}
              onChange={onHandleFilterChange.bind(this, "endDate")}
              defaultValue={mapToObject(props.selectedFilters.endDate)}
              value={mapToObject(props.selectedFilters.endDate)}
            />
          </div>
        </div>
        <div className={`form-row run-filter-form mt-3`}>
          <div className={`col`}>
            <Link
              to={{
                pathname: "/sampleFileUpload",
                state: { run: [] },
                search: props.search
              }}
            >
              <button className="btn btn-sm btn-primary">
                Sample File Upload
              </button>
            </Link>
          </div>
        </div>
      </div>
    </Fragment>
  );
};

export default RunControls;
