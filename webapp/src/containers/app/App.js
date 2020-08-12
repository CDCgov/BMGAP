import React, { Component, Fragment } from "react";
import { Route, withRouter } from "react-router-dom";

import Header from "../../components/Header/Header";
import RunView from "../RunView/RunView";
import SampleView from "../SampleView/SampleView";
import RelatedSamplesView from "../RelatedSamplesView/RelatedSamplesView";
import PhyloView from "../PhyloView/PhyloView";
import SampleDetailsView from "../SampleDetailsView/SampleDetailsView";
import AnalyticsView from "../AnalyticsView/AnalyticsView";
import SampleFileUploadView from "../SampleFileUploadView/SampleFileUploadView";
import { getToken } from "../../utilities/regexParser";
import "./App.scss";
import { setRedirectUrl } from "../../utilities/setRedirectUrl";

class App extends Component {
  render() {
    return getToken(this.props.location) ? (
      <Fragment>
        <Route
          path="/"
          component={() => (
            <Header
              name="BMGAP"
              search={this.props.location.search || this.props.location.hash}
            />
          )}
        />
        <Route exact path="/" component={RunView} />
        <Route exact path="/run" component={SampleView} />
        <Route path="/run/:id" component={SampleView} />
        <Route path="/sample/:sampleId" component={RelatedSamplesView} />
        <Route path="/phylo/:sampleId" component={PhyloView} />
        <Route path="/analytics" component={AnalyticsView} />
        <Route path="/sampleDetails/:sampleId" component={SampleDetailsView} />
        <Route path="/sampleFileUpload" component={SampleFileUploadView} />
      </Fragment>
    ) : (
      <Fragment>
        Not authorized, redirecting to log in page...
        <Route
          path="/"
          component={() => {
            window.location = setRedirectUrl();
            return null;
          }}
        />
      </Fragment>
    );
  }
}

export default withRouter(App);
