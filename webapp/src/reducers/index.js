import { combineReducers } from "redux";
import runs from "./runs";
import filters from "./filters";
import samples from "./samples";
import relatedSamples from "./relatedSamples";
import phyloTree from "./phyloTree";
import sampleDetails from "./sampleDetails";
import user from "./user";
import token from "./token";
import selectedData from "./selectedData";
import featureViewer from "./featureViewer";
import analytics from "./analytics";
import selectedFilters from "./selectedFilters";
import samplesFromFile from "./samplesFromFile";

export default combineReducers({
  filters,
  runs,
  samples,
  relatedSamples,
  phyloTree,
  sampleDetails,
  user,
  token,
  selectedData,
  featureViewer,
  analytics,
  selectedFilters,
  samplesFromFile
});
