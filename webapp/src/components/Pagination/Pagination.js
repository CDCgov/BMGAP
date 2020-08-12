import React, { Fragment, Component } from "react";
import "./Pagination.scss";

class Pagination extends Component {
  constructor(props) {
    super(props);

    this.generatePages = this.generatePages.bind(this);
  }

  generatePages(totalPages, currentPage, onPageClick) {
    return (
      <Fragment>
        {currentPage === totalPages && totalPages > 2 && (
          <li className="page-item">
            <button
              className="page-link"
              onClick={() => {
                onPageClick(currentPage - 2);
              }}
            >
              {currentPage - 2}
            </button>
          </li>
        )}
        {currentPage > 1 && (
          <li className="page-item">
            <button
              className="page-link"
              onClick={() => {
                onPageClick(currentPage - 1);
              }}
            >
              {currentPage - 1}
            </button>
          </li>
        )}
        <li className="page-item active">
          <button
            className="page-link active-page"
            onClick={() => {
              onPageClick(currentPage);
            }}
          >
            {currentPage}
          </button>
        </li>
        {currentPage < totalPages && (
          <li className="page-item">
            <button
              className="page-link"
              onClick={() => {
                onPageClick(currentPage + 1);
              }}
            >
              {currentPage + 1}
            </button>
          </li>
        )}
        {currentPage === 1 && totalPages > 2 && (
          <li className="page-item">
            <button
              className="page-link"
              onClick={() => {
                onPageClick(currentPage + 2);
              }}
            >
              {currentPage + 2}
            </button>
          </li>
        )}
      </Fragment>
    );
  }

  render() {
    let { totalPages, currentPage, onPageClick } = this.props;

    return (
      <div className="">
        <nav>
          <ul className="pagination page-ul mb-0">
            <li
              key={"<<"}
              className={`page-item ${currentPage === 1 ? "disabled" : ""}`}
            >
              <button
                className="page-link"
                onClick={() => {
                  onPageClick(1);
                }}
              >
                &laquo;
              </button>
            </li>
            <li
              key={"<"}
              className={`page-item ${currentPage === 1 ? "disabled" : ""}`}
            >
              <button
                className="page-link"
                onClick={() => {
                  onPageClick(--currentPage);
                }}
              >
                &lsaquo;
              </button>
            </li>
            {this.generatePages(totalPages, currentPage, onPageClick)}
            <li
              key={">"}
              className={`page-item ${
                currentPage === totalPages ? "disabled" : ""
              }`}
            >
              <button
                className="page-link"
                onClick={() => {
                  onPageClick(++currentPage);
                }}
              >
                &rsaquo;
              </button>
            </li>
            <li
              key={">>"}
              className={`page-item ${
                currentPage === totalPages ? "disabled" : ""
              }`}
            >
              <button
                className="page-link"
                onClick={() => {
                  onPageClick(totalPages);
                }}
              >
                &raquo;
              </button>
            </li>
          </ul>
        </nav>
      </div>
    );
  }
}

export default Pagination;
