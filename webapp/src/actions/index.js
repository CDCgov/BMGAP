import * as Types from "./actionTypes";
import * as axios from "axios";
import FormData from "form-data";

/**
 * Action Creators
 */

export const setToken = token => ({
  type: Types.SET_TOKEN,
  token
});

export const fetchUserSuccess = user => ({
  type: Types.FETCH_USER_SUCCESS,
  user
});

export const fetchRecentRunsSuccess = runs => ({
  type: Types.FETCH_RECENT_RUNS_SUCCESS,
  runs
});

export const fetchRecentRunsFailure = () => ({
  type: Types.FETCH_RECENT_RUNS_FAILURE
});

export const fetchRecentRunsAsync = fetchingRuns => ({
  type: Types.FETCH_RECENT_RUNS_ASYNC,
  fetchingRuns
});

export const fetchRecentSamplesSuccess = samples => ({
  type: Types.FETCH_RECENT_SAMPLES_SUCCESS,
  samples
});

export const fetchRecentSamplesFailure = () => ({
  type: Types.FETCH_RECENT_SAMPLES_FAILURE
});

export const fetchRecentSamplesAsync = fetchingSamples => ({
  type: Types.FETCH_RECENT_SAMPLES_ASYNC,
  fetchingSamples
});

export const fetchFiltersSuccess = filters => ({
  type: Types.FETCH_FILTERS_SUCCESS,
  filters
});

export const downloadSamplesSuccess = () => ({
  type: Types.DOWNLOAD_SAMPLES_SUCCESS
});

export const downloadSamplesFailure = () => ({
  type: Types.DOWNLOAD_SAMPLES_FAILURE
});

export const downloadSamplesAsync = () => ({
  type: Types.DOWNLOAD_SAMPLES_ASYNC
});

export const fetchRelatedSamplesSuccess = relatedSamples => ({
  type: Types.FETCH_RELATED_SAMPLES_SUCCESS,
  relatedSamples
});

export const fetchRelatedSamplesFailure = () => ({
  type: Types.FETCH_RELATED_SAMPLES_FAILURE
});

export const fetchRelatedSamplesAsync = fetchingRelatedSamples => ({
  type: Types.FETCH_RELATED_SAMPLES_ASYNC,
  fetchingRelatedSamples
});

export const fetchPhyloTreeSuccess = phyloTree => ({
  type: Types.FETCH_PHYLOTREE_SUCCESS,
  phyloTree
});

export const fetchPhyloTreeFailure = () => ({
  type: Types.FETCH_PHYLOTREE_FAILURE
});

export const fetchPhyloTreeAsync = fetchingPhyloTree => ({
  type: Types.FETCH_PHYLOTREE_ASYNC,
  fetchingPhyloTree
});

export const fetchSampleDetailsSuccess = sampleDetails => ({
  type: Types.FETCH_SAMPLE_DETAILS_SUCCESS,
  sampleDetails
});

export const fetchSampleDetailsFailure = () => ({
  type: Types.FETCH_SAMPLE_DETAILS_FAILURE
});

export const fetchSampleDetailsAsync = fetchingSampleDetails => ({
  type: Types.FETCH_SAMPLE_DETAILS_ASYNC,
  fetchingSampleDetails
});

export const setRuns = runs => ({
  type: Types.SET_CURRENT_RUN,
  runs
});

export const setSample = sample => ({
  type: Types.SET_CURRENT_SAMPLE,
  sample
});

export const setPhyloTree = phyloTree => ({
  type: Types.SET_CURRENT_PHYLO,
  phyloTree
});

export const setFeatureViewer = featureViewer => ({
  type: Types.SET_FEATURE_VIEWER,
  featureViewer
});

export const fetchFeatureViewerSuccess = featureViewer => ({
  type: Types.FETCH_FEATURE_VIEWER_SUCCESS,
  featureViewer
});

export const fetchFeatureViewerFailure = () => ({
  type: Types.FETCH_FEATURE_VIEWER_FAILURE
});

export const fetchFeatureViewerAsync = fetchingFeatureViewer => ({
  type: Types.FETCH_FEATURE_VIEWER_ASYNC,
  fetchingFeatureViewer
});

export const fetchAnalyticsSuccess = analytics => ({
  type: Types.FETCH_ANALYTICS_SUCCESS,
  analytics
});

export const fetchAnalyticsFailure = () => ({
  type: Types.FETCH_ANALYTICS_FAILURE
});

export const fetchAnalyticsAsync = fetchingAnalytics => ({
  type: Types.FETCH_ANALYTICS_ASYNC,
  fetchingAnalytics
});

export const setSelectedFilters = selectedFilters => ({
  type: Types.SET_SELECTED_FILTERS,
  selectedFilters
});

export const fetchSamplesFromFileSuccess = samplesFromFile => ({
  type: Types.FETCH_SAMPLES_FROM_FILE_SUCCESS,
  samplesFromFile
});

export const fetchSamplesFromFileFailure = () => ({
  type: Types.FETCH_SAMPLES_FROM_FILE_FAILURE
});

export const fetchSamplesFromFileAsync = fetchingSamplesFromFile => ({
  type: Types.FETCH_SAMPLES_FROM_FILE_ASYNC,
  fetchingSamplesFromFile
});

export const clearSamplesFromFile = () => ({
  type: Types.FETCH_SAMPLES_FROM_FILE_SUCCESS,
  fetchingSamplesFromFile: null
});

/**
 * Thunks
 */

export const fetchUser = token => {
  return dispatch => {
    return axios
      .get(`/bmgap/api/id/validate/${token}`)
      .then(res => {
        dispatch(fetchUserSuccess(res.data));
      })
      .catch(error => {
        // TODO - handle error
        console.log(error);
      });
  };
};

export const fetchRecentRuns = (filter, page, token) => {
  return (dispatch, getState) => {
    dispatch(fetchRecentRunsAsync(true));
    return axios
      .get(
        "/bmgap/api/runs",
        filter && page
          ? {
              params: {
                perPage: filter.numberOfRuns
                  ? filter.numberOfRuns.toString()
                  : "",
                submitter: filter.submitter ? filter.submitter.toString() : "",
                sequencer: filter.runSequencer
                  ? filter.runSequencer.toString()
                  : "",
                start_year: filter.startDate ? filter.startDate.toString() : "",
                end_year: filter.endDate ? filter.endDate.toString() : "",
                page: page
              },
              headers: token && { Authorization: `Bearer ${token}` }
            }
          : null
      )
      .then(res => {
        dispatch(fetchRecentRunsSuccess(res.data));
      })
      .catch(error => {
        dispatch(fetchRecentRunsFailure());
      });
  };
};

export const fetchRecentSamples = (filter, runs, page, token) => {
  return (dispatch, getState) => {
    dispatch(fetchRecentSamplesAsync(true));
    return axios
      .get(
        "/bmgap/api/samples",
        filter && page
          ? {
              params: {
                perPage: filter.numberOfSamples,
                page: page,
                sortField: filter.sortBy,
                filter: {
                  identifiers: getValidFilterValue(filter.sampleId),
                  runs: getValidFilterValue(runs),
                  location: getValidFilterValue(filter.location),
                  mashSpecies: getValidFilterValue(filter.species),
                  serogrouping: getValidFilterValue(filter.serogroup),
                  serotyping: getValidFilterValue(filter.serotyping),
                  sequencer: getValidFilterValue(filter.sequencer),
                  state: []
                }
              },
              headers: token && { Authorization: `Bearer ${token}` }
            }
          : null
      )
      .then(res => {
        dispatch(fetchRecentSamplesSuccess(res.data));
      })
      .catch(error => {
        dispatch(fetchRecentSamplesFailure());
      });
  };
};

export const fetchFilters = token => {
  return (dispatch, getState) => {
    if (getState().filters.samples && getState().filters.samples)
      return Promise.resolve();
    return axios
      .get("/bmgap/api/filters", {
        headers: token && { Authorization: `Bearer ${token}` }
      })
      .then(res => {
        dispatch(fetchFiltersSuccess(res.data));
      })
      .catch(error => {});
  };
};

export const downloadSamples = (samples, types) => {
  return dispatch => {
    dispatch(downloadSamplesAsync());
    return axios
      .post(
        "/bmgap/api/download",
        { ids: samples, fields: types },
        { responseType: "arraybuffer" }
      )
      .then(res => {
        if (window.navigator && window.navigator.msSaveOrOpenBlob) {
          window.navigator.msSaveOrOpenBlob(
            new Blob([res.data], { type: "application/zip" }),
            "BMGAP_metadata.zip"
          );
        } else {
          let url = window.URL.createObjectURL(
            new Blob([res.data], { type: "application/zip" })
          );
          const link = document.createElement("a");
          link.href = url;
          link.setAttribute("download", `BMGAP_metadata.zip`);
          document.body.appendChild(link);
          link.click();
          link.parentNode.removeChild(link);
          window.URL.revokeObjectURL(url);
        }
        dispatch(downloadSamplesSuccess());
      })
      .catch(error => {
        dispatch(downloadSamplesFailure());
      });
  };
};

export const fetchRelatedSamples = (sampleId, token) => {
  return (dispatch, getState) => {
    if (
      sampleId === getState().selectedData.sample &&
      getState().relatedSamples.relatedSamples &&
      getState().relatedSamples.relatedSamples.query
    ) {
      return Promise.resolve();
    }

    dispatch(setSample(sampleId));
    dispatch(setPhyloTree(null));
    dispatch(fetchRelatedSamplesAsync(true));
    return axios
      .get(`/bmgap/api/samples/${sampleId}/mash_sort`, {
        headers: token && { Authorization: `Bearer ${token}` }
      })
      .then(res => {
        dispatch(fetchRelatedSamplesSuccess(res.data));
      })
      .catch(error => {
        dispatch(fetchRelatedSamplesFailure());
      });
  };
};

export const fetchPhyloTree = (relatedSamples, sampleId, phyloTree) => {
  return (dispatch, getState) => {
    if (
      sampleId === getState().selectedData.sample &&
      phyloTree &&
      phyloTree.localeCompare(getState().selectedData.phyloTree) === 0 &&
      typeof getState().phyloTree.phyloTree === "string"
    )
      return Promise.resolve();
    dispatch(setPhyloTree(phyloTree));
    dispatch(fetchPhyloTreeAsync(true));
    return axios
      .post(`/bmgap/api/samples/${sampleId}/phylo`, relatedSamples)
      .then(res => {
        dispatch(fetchPhyloTreeSuccess(res.data));
        dispatch(setPhyloTree(res.data));
      })
      .catch(error => {
        dispatch(fetchPhyloTreeFailure());
      });
  };
};

export const fetchSampleDetails = sampleId => {
  return (dispatch, getState) => {
    dispatch(setFeatureViewer(null));
    dispatch(fetchSampleDetailsAsync(true));
    return axios
      .get(`/bmgap/api/samples/${sampleId}`)
      .then(res => {
        dispatch(fetchSampleDetailsSuccess(res.data));
      })
      .catch(error => {
        dispatch(fetchSampleDetailsFailure());
      });
  };
};

export const fetchFeatureViewer = sampleId => {
  return (dispatch, getState) => {
    dispatch(setFeatureViewer(null));
    dispatch(fetchFeatureViewerAsync(true));
    return axios
      .get(`/bmgap/api/samples/${sampleId}/sero`)
      .then(res => {
        dispatch(fetchFeatureViewerSuccess(res.data));
      })
      .catch(error => {
        dispatch(fetchFeatureViewerFailure());
      });
  };
};

export const fetchAnalytics = token => {
  return (dispatch, getState) => {
    dispatch(fetchAnalyticsAsync(true));
    return axios
      .get(`/bmgap/api/analytics`)
      .then(res => {
        dispatch(fetchAnalyticsSuccess(res.data));
      })
      .catch(error => {
        dispatch(fetchAnalyticsFailure());
      });
  };
};

export const fetchSamplesFromFile = file => {
  return (dispatch, getState) => {
    dispatch(clearSamplesFromFile());
    let formData = new FormData();
    formData.append("sample-data", file[0]);
    dispatch(fetchSamplesFromFileAsync(true));
    return axios
      .post(`/bmgap/api/samplesFromFile`, formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      })
      .then(res => {
        dispatch(fetchSamplesFromFileSuccess(res.data));
      })
      .catch(error => {
        dispatch(fetchAnalyticsFailure());
      });
  };
};

const getValidFilterValue = filter => {
  // TODO: check behavior when filter = [""] inside CDC network
  if (filter && Array.isArray(filter)) return filter;
  if (filter && !Array.isArray(filter)) return [filter];
  return [];
};
