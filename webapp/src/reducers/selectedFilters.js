import * as Types from "../actions/actionTypes";

const defaultFilters = {
  numberOfSamples: 50,
  sampleId: null,
  runs: [],
  location: null,
  species: null,
  serogroup: null,
  serotyping: null,
  sequencer: null,
  numberOfRuns: 10,
  submitter: null,
  runSequencer: null,
  startDate: null,
  endDate: null
};

const selectedFilters = (state = defaultFilters, action) => {
  switch (action.type) {
    case Types.SET_SELECTED_FILTERS:
      return Object.assign({}, state, action.selectedFilters);
    default:
      return state;
  }
};

export default selectedFilters;
