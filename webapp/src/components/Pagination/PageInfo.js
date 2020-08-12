import * as React from "react";

const PageInfo = ({ currentPage, totalItems, itemNumberFilter }) => {
  function calculateResults() {
    if (
      totalItems < itemNumberFilter ||
      totalItems < currentPage * itemNumberFilter
    ) {
      return totalItems;
    } else return currentPage * itemNumberFilter;
  }

  return (
    <div className="row justify-content-between mt-2">
      <div className="justify-content-start col-4 d-flex results-text">
        <span className="pages-text">
          <span className="font-weight-bold mr-1">Results</span>{" "}
          {currentPage * itemNumberFilter - itemNumberFilter + 1}-
          {calculateResults()} of {totalItems}
        </span>
      </div>
    </div>
  );
};

export default PageInfo;
