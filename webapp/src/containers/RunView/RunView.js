import React, { Fragment, useState, useEffect } from "react";
import { connect } from "react-redux";
import {
  fetchRecentRuns,
  fetchFilters,
  setToken,
  setSelectedFilters,
  fetchSamplesFromFile
} from "../../actions";
import { getToken } from "../../utilities/regexParser";

import RunTable from "../../components/RunTable/RunTable";
import RunControls from "../../components/RunControls/RunControls";
import SideBar from "../../components/SideBar/SideBar";

const RunView = ({
  runs,
  filters,
  fetchRecentRuns,
  fetchFilters,
  totalItems,
  fetchingRuns,
  location,
  setToken,
  setSelectedFilters,
  selectedFilters,
  fetchSamplesFromFile
}) => {
  const [currentFilters, setCurrentFilters] = useState({
    numberOfRuns: 10,
    submitter: null,
    runSequencer: null,
    startDate: null,
    endDate: null
  });

  const [currentPage, setCurrentPage] = useState(1);

  const [token] = useState(getToken(location));

  useEffect(() => {
    setToken(token);
  }, [setToken, token]);

  useEffect(() => {
    fetchRecentRuns(selectedFilters, currentPage, token);
  }, [fetchRecentRuns, selectedFilters, currentPage, token]);

  useEffect(() => {
    fetchFilters(token);
  }, [fetchFilters, token]);

  const handleFilterChange = (filterType, filterValue) => {
    setCurrentPage(1);
    setCurrentFilters(
      Object.assign({}, currentFilters, { [filterType]: filterValue })
    );
    setSelectedFilters({ [filterType]: filterValue });
  };

  const handleClearRunFilters = () => {
    setCurrentPage(1);
    setSelectedFilters(
      Object.assign({}, selectedFilters, {
        numberOfRuns: 10,
        submitter: null,
        runSequencer: null,
        startDate: null,
        endDate: null
      })
    );
  };

  const handleFileUpload = file => {
    fetchSamplesFromFile(file);
  };

  const onPageClick = currentPage => {
    setCurrentPage(currentPage);
  };

  return (
    <Fragment>
      <SideBar>
        <RunControls
          numberOfRuns={selectedFilters.numberOfRuns}
          runFilters={filters.runs}
          onHandleChange={handleFilterChange}
          runCount={runs ? runs.length : null}
          search={location.search || location.hash}
          selectedFilters={selectedFilters}
          handleClearRunFilters={handleClearRunFilters}
          handleFileUpload={handleFileUpload}
        />
      </SideBar>
      <RunTable
        fetchingRuns={fetchingRuns}
        runs={runs}
        totalItems={totalItems}
        currentPage={currentPage}
        onPageClick={onPageClick}
        itemNumberFilter={selectedFilters.numberOfRuns}
        search={location.search || location.hash}
      />
    </Fragment>
  );
};

const mapStateToProps = ({
  runs,
  filters,
  token,
  selectedFilters,
  samplesFromFile
}) => ({
  fetchingRuns: runs.fetchingRuns,
  runs: runs.runs ? runs.runs.docs : null,
  filters: filters,
  totalItems: runs.runs ? runs.runs.total : null,
  token: token,
  selectedFilters: selectedFilters,
  samplesFromFile: samplesFromFile.samplesFromFile
});

export default connect(mapStateToProps, {
  fetchRecentRuns,
  fetchFilters,
  setToken,
  setSelectedFilters,
  fetchSamplesFromFile
})(RunView);
