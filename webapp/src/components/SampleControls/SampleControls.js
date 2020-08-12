import React, { Fragment, useState } from "react";
import { isEmpty } from "lodash";
import Select from "react-select";
import { Link } from "react-router-dom";

import "./SampleControls.scss";

const SampleControls = (props) => {
  const [sampleValue, setSampleValue] = useState("");

  function onHandleFilterChange(filterType, event) {
    const result = handleEventObject(event);
    props.onHandleChange(filterType, result);
  }

  function handleEventObject(event) {
    if (event.length && Array.isArray(event)) {
      if (event.find((item) => item.label === "All")) return [""];
      return event.map((filter) => filter.value);
    }
    if (event.target) return event.target.value;
    if (event.value) return event.value;
    return null;
  }

  function handleInputChange(event) {
    setSampleValue(event.target.value);
  }

  function handleInputSubmit(event) {
    if (event.key === "Enter") {
      props.onHandleChange("sampleId", sampleValue.split(","));
    }
  }

  function createSelectArray(items) {
    return items.map((item) => {
      return {
        value: item,
        label: item,
      };
    });
  }

  function clearFilters() {
    setSampleValue("");
    props.handleClearSampleFilters();
  }

  function mapToObject(value) {
    if (typeof value === "string" || typeof value === "number") {
      return { value: value, label: value };
    }
    if (Array.isArray(value)) {
      return createSelectArray(value);
    }
    return null;
  }

  if (isEmpty(props.sampleFilters)) return <div />;
  return (
    <Fragment>
      <div className={`container sample-control-container mx-0`}>
        <div className={`form-row justify-content-center`}>
          <div
            className="btn-group btn-group-toggle mb-4"
            data-toggle="buttons"
          >
            <Link
              to={{
                pathname: "/",
                state: { run: null },
                search: props.search,
              }}
            >
              <button className="btn btn-sm btn-light toggle-left">Runs</button>
            </Link>
            <button className="btn btn-sm btn-primary active empty-toggle">
              Samples
            </button>
          </div>
        </div>
        <div className={`form-row run-filter-form`}>
          <div className={`col font-weight-bold filter-title`}>Filters</div>
          <button className="btn btn-sm btn-link mr-2" onClick={clearFilters}>
            Clear Filters
          </button>
        </div>
        <div className={`form-row run-filter-form`}>
          <div className={`col mt-3`}>
            <label className="filter-label"># of Samples</label>
            <Select
              options={[
                { value: "25", label: "25" },
                { value: "50", label: "50" },
                { value: "100", label: "100" },
                { value: "250", label: "250" },
                { value: "500", label: "500" },
                { value: "1000", label: "1000" },
              ]}
              isSearchable={false}
              defaultValue={
                props.selectedFilters.numberOfSamples
                  ? {
                      value: props.selectedFilters.numberOfSamples,
                      label: props.selectedFilters.numberOfSamples,
                    }
                  : { value: "50", label: "50" }
              }
              value={
                props.selectedFilters.numberOfSamples
                  ? {
                      value: props.selectedFilters.numberOfSamples,
                      label: props.selectedFilters.numberOfSamples,
                    }
                  : { value: "50", label: "50" }
              }
              onChange={onHandleFilterChange.bind(this, "numberOfSamples")}
            />
          </div>
        </div>
        <div className={`form-row run-filter-form mt-3`}>
          <div className={`col`}>
            <label className="filter-label">Search</label>
            <input
              className="form-control"
              type="text"
              value={sampleValue}
              onChange={handleInputChange.bind(this)}
              onKeyDown={handleInputSubmit.bind(this)}
              onBlur={handleInputSubmit.bind(this)}
            />
            {(props.selectedFilters.sampleId &&
              props.selectedFilters.sampleId[0] !== "" && (
                <span className="search-filter-info">
                  Searching on: {props.selectedFilters.sampleId}
                </span>
              )) || (
              <span className="search-filter-info">No search term applied</span>
            )}
          </div>
        </div>
        <div className={`form-row run-filter-form mt-3`}>
          <div className={`col`}>
            <label className="filter-label">Run ID</label>
            <Select
              isMulti
              options={createSelectArray([...props.sampleFilters["run_id"]])}
              isSearchable={true}
              onChange={onHandleFilterChange.bind(this, "runs")}
              defaultValue={mapToObject(props.runs)}
              value={mapToObject(props.runs)}
            />
          </div>
        </div>
        <div className={`form-row run-filter-form mt-3`}>
          <div className={`col`}>
            <label className="filter-label">Serogroup</label>
            <Select
              isMulti
              options={createSelectArray([...props.sampleFilters.serogroup])}
              isSearchable={false}
              onChange={onHandleFilterChange.bind(this, "serogroup")}
              defaultValue={mapToObject(props.selectedFilters.serogroup)}
              value={mapToObject(props.selectedFilters.serogroup)}
            />
          </div>
        </div>
        <div className={`form-row run-filter-form mt-3`}>
          <div className={`col`}>
            <label className="filter-label">Serotyping</label>
            <Select
              isMulti
              options={createSelectArray([...props.sampleFilters.serotyping])}
              isSearchable={false}
              onChange={onHandleFilterChange.bind(this, "serotyping")}
              defaultValue={mapToObject(props.selectedFilters.serotyping)}
              value={mapToObject(props.selectedFilters.serotyping)}
            />
          </div>
        </div>
        <div className={`form-row run-filter-form mt-3`}>
          <div className={`col`}>
            <label className="filter-label">Location</label>
            <Select
              isMulti
              options={createSelectArray([...props.sampleFilters.location])}
              isSearchable={true}
              onChange={onHandleFilterChange.bind(this, "location")}
              defaultValue={mapToObject(props.selectedFilters.location)}
              value={mapToObject(props.selectedFilters.location)}
            />
          </div>
        </div>
        <div className={`form-row run-filter-form mt-3`}>
          <div className={`col`}>
            <label className="filter-label">Species</label>
            <Select
              isMulti
              styles={{ fontSize: 10 }}
              options={createSelectArray([
                ...props.sampleFilters["mash-species"],
              ])}
              isSearchable={true}
              onChange={onHandleFilterChange.bind(this, "species")}
              defaultValue={mapToObject(props.selectedFilters.species)}
              value={mapToObject(props.selectedFilters.species)}
            />
          </div>
        </div>
        <div className={`form-row run-filter-form mt-3`}>
          <div className={`col`}>
            <label className="filter-label">Sequencer</label>
            <Select
              isMulti
              styles={{ fontSize: 10 }}
              options={createSelectArray([...props.sampleFilters["sequencer"]])}
              isSearchable={true}
              onChange={onHandleFilterChange.bind(this, "sequencer")}
              defaultValue={mapToObject(props.selectedFilters.sequencer)}
              value={mapToObject(props.selectedFilters.sequencer)}
            />
          </div>
        </div>
        <div className={`form-row run-filter-form mt-3`}>
          <div className={`col`}>
            <Link
              to={{
                pathname: "/sampleFileUpload",
                state: { run: [] },
                search: props.search,
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

export default SampleControls;
