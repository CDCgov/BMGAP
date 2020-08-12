import React, { Fragment, useState, useEffect } from "react";
import { connect } from "react-redux";
import { withRouter } from "react-router-dom";
import _ from "lodash";

import {
  fetchRecentSamples,
  fetchFilters,
  downloadSamples,
  setToken,
  setSelectedFilters,
  fetchSamplesFromFile
} from "../../actions";
import { getToken } from "../../utilities/regexParser";
import SampleFileUpload from "../../components/SampleFileUpload/SampleFileUpload";
import SampleModal from "../../components/SampleTable/SampleModal";
import SampleDownload from "../../components/SampleTable/SampleDownload";

const SampleFileUploadView = ({
  downloadingSamples,
  fetchRecentSamples,
  downloadSamples,
  fetchFilters,
  location,
  totalItems,
  setToken,
  token,
  setSelectedFilters,
  selectedFilters,
  samplesFromFile,
  fetchSamplesFromFile,
  fetchingSamplesFromFile
}) => {
  const [currentFilters, setCurrentFilters] = useState({
    numberOfSamples: 50,
    sampleId: null,
    runs: [],
    location: null,
    species: null,
    serogroup: null,
    serotyping: null,
    sequencer: null
  });

  const [runs, setRuns] = useState(
    location.state && location.state.run ? location.state.run : []
  );

  const [sampleTypes, setSampleTypes] = useState({
    meta: true,
    cleanData: true,
    Serotype: true,
    Serogroup: true,
    mash: true,
    MLST: true,
    fasta: false,
    gff: false
  });

  const [sortType, setSortType] = useState("");

  const [currentPage, setCurrentPage] = useState(1);

  const [selectedSamples, setSelectedSamples] = useState([]);

  const [downloadModal, setDownloadModal] = useState(false);

  const [viewDownloadOptions, setViewDownloadOptions] = useState(false);

  const handleFilterChange = (filterType, filterValue) => {
    setSelectedSamples([]);
    setCurrentPage(1);
    setCurrentFilters(
      Object.assign({}, currentFilters, { [filterType]: filterValue })
    );
    setSelectedFilters({ [filterType]: filterValue });
    if (filterType === "runs") setRuns(filterValue);
  };

  const handleSortClick = sortValue => {
    setSortType(sortValue);
    handleFilterChange("sortBy", sortValue);
  };

  useEffect(() => {
    setToken(getToken(location));
  }, [setToken, location]);

  useEffect(() => {
    fetchRecentSamples(selectedFilters, runs, currentPage, token);
  }, [fetchRecentSamples, runs, selectedFilters, currentPage, token]);

  useEffect(() => {
    fetchFilters(token);
  }, [fetchFilters, token]);

  const onPageClick = currentPage => {
    setSelectedSamples([]);
    setCurrentPage(currentPage);
  };

  const handleCheckClick = sampleId => {
    if (!selectedSamples.includes(sampleId)) {
      setSelectedSamples([...selectedSamples, sampleId]);
    } else {
      setSelectedSamples(
        _.filter(selectedSamples, id => {
          return id !== sampleId;
        })
      );
    }
  };

  const handleDownloadClick = e => {
    e.stopPropagation();
    setDownloadModal(true);
  };

  const handleDismissModal = () => {
    setViewDownloadOptions(false);
    setDownloadModal(false);
  };

  const handleCheckAll = allSamples => {
    if (selectedSamples.length) {
      setSelectedSamples([]);
    } else {
      setSelectedSamples(allSamples);
    }
  };

  const handleSampleTypeClick = type => {
    setSampleTypes(
      Object.assign({}, sampleTypes, { [type]: !sampleTypes[type] })
    );
  };

  const handleSampleZipDownload = async () => {
    await downloadSamples(selectedSamples, getListOfSampleOptions(sampleTypes));
    await setDownloadModal(false);
  };

  const getListOfSampleOptions = types => {
    return Object.keys(types).filter(key => {
      return types[key];
    });
  };

  const handleViewDownloadOptions = (showOptions, e) => {
    e.stopPropagation();
    setViewDownloadOptions(showOptions);
  };

  const handleFileUpload = file => {
    fetchSamplesFromFile(file);
  };

  return (
    <Fragment>
      <SampleFileUpload
        fetchingSamplesFromFile={fetchingSamplesFromFile}
        samples={samplesFromFile}
        totalItems={totalItems}
        currentPage={currentPage}
        itemNumberFilter={selectedFilters.numberOfSamples}
        onPageClick={onPageClick}
        run={runs}
        handleCheckClick={handleCheckClick}
        selectedSamples={selectedSamples}
        handleCheckAll={handleCheckAll}
        handleDownloadClick={handleDownloadClick}
        handleDismissModal={handleDismissModal}
        downloadModal={downloadModal}
        handleSortClick={handleSortClick}
        sortType={sortType}
        search={location.search || location.hash}
        handleFileUpload={handleFileUpload}
        isSampleFileUpload={true}
      />
      <SampleModal
        show={downloadModal}
        close={handleDismissModal}
        handleSampleZipDownload={handleSampleZipDownload}
        downloadingSamples={downloadingSamples}
      >
        {!downloadingSamples && (
          <SampleDownload
            handleSampleTypeClick={handleSampleTypeClick}
            selectedSampleTypes={sampleTypes}
            handleViewDownloadOptions={handleViewDownloadOptions}
            viewDownloadOptions={viewDownloadOptions}
          />
        )}
        {downloadingSamples && (
          <div className="font-weight-bold h5">Download in progress...</div>
        )}
      </SampleModal>
    </Fragment>
  );
};

const mapStateToProps = ({
  samples,
  filters,
  token,
  selectedFilters,
  samplesFromFile
}) => ({
  fetchingSamplesFromFile: samplesFromFile.fetchingSamplesFromFile,
  downloadingSamples: samples.downloadingSamples,
  samples: samples.samples ? samples.samples.docs : null,
  filters: filters,
  totalItems: samples.samples ? samples.samples.total : null,
  token: token,
  selectedFilters: selectedFilters,
  samplesFromFile: samplesFromFile.samplesFromFile
    ? samplesFromFile.samplesFromFile.docs
    : null
});

export default withRouter(
  connect(mapStateToProps, {
    fetchRecentSamples,
    fetchFilters,
    downloadSamples,
    setToken,
    setSelectedFilters,
    fetchSamplesFromFile
  })(SampleFileUploadView)
);
