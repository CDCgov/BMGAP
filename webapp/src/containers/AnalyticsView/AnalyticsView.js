import React, { Fragment, useState, useEffect } from "react";
import { connect } from "react-redux";
import { withRouter } from "react-router-dom";

import { fetchAnalytics } from "../../actions";
import AnalyticsBox from "../../components/AnalyticsBox/AnalyticsBox";
import { getToken } from "../../utilities/regexParser";
import Spinner from "../../components/Spinner/Spinner";

const AnalyticsView = ({
  fetchAnalytics,
  fetchingAnalytics,
  analytics,
  location
}) => {
  const [sampleId] = useState(location.state ? location.state.sample : null);

  useEffect(() => {
    fetchAnalytics(getToken(location));
  }, [fetchAnalytics, location]);

  return (
    <Fragment>
      <div className={`d-flex flex-row align-items-start`}>
        {analytics && !fetchingAnalytics && (
          <AnalyticsBox
            analytics={analytics}
            sampleId={sampleId}
            runId={location.state ? location.state.run : null}
            search={location.search || location.hash}
          />
        )}
        {fetchingAnalytics && (
          <div
            className={`container-fluid run-table-container d-flex flex-column justify-content-center`}
          >
            <Spinner />
          </div>
        )}
        {!fetchingAnalytics && !analytics && (
          <div
            className={`container-fluid run-table-container d-flex justify-content-center`}
          >
            <h5 className="mt-4">No analytics data available</h5>
          </div>
        )}
      </div>
    </Fragment>
  );
};

const mapStateToProps = ({ analytics }) => ({
  fetchingAnalytics: analytics.fetchingAnalytics,
  analytics: analytics.analytics
});

export default withRouter(
  connect(mapStateToProps, { fetchAnalytics })(AnalyticsView)
);
