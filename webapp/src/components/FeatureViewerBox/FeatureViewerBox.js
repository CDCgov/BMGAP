import React, { Fragment, useEffect } from "react";

// import "../FeatureViewer/FeatureViewer.scss";

function FeatureViewerBox({ data }) {
  useEffect(() => {
    let ft = null;
    if (hasFeatureViewer(data)) {
      ft = new window.FeatureViewer(
        data.viewerObj.offset.end - data.viewerObj.offset.start,
        "#fv1",
        data.viewerObj
      );

      data.features.forEach(element => {
        ft.addFeature(element);
      });
    }
    return function() {
      ft.clearInstance();
      document.getElementById("fv1").innerHTML = "";
    };
  }, [data]);

  return (
    <Fragment>
      {hasFeatureViewer(data) && (
        <Fragment>
          <div className="">
            <h5 className="font-weight-bold">Feature Viewer</h5>
          </div>
          <div id="fv1" />
        </Fragment>
      )}
    </Fragment>
  );
}

const hasFeatureViewer = data => {
  return data && data.viewerObj && data.viewerObj.offset && data.features
    ? true
    : false;
};

export default FeatureViewerBox;
