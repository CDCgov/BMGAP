import React, { Fragment } from "react";
import { FaTimes } from "react-icons/fa";

import "./SampleModal.scss";

class SampleModal extends React.Component {
  render() {
    return (
      <Fragment>
        <div
          className={
            this.props.show
              ? `modal-back-drop d-flex justify-content-center`
              : ``
          }
        >
          <div
            className={
              this.props.show
                ? `card modal-wrapper`
                : `card modal-hide modal-wrapper`
            }
          >
            <div className={`card-body download-card-body py-0`}>
              <div className={`card-title modal-header d-flex flex-row mb-0`}>
                <div>
                  <h4 className="font-weight-bold m-0">Sample Download</h4>
                </div>
                {!this.props.downloadingSamples && (
                  <div>
                    <span
                      className={`close-modal-btn`}
                      onClick={this.props.close}
                    >
                      <FaTimes />
                    </span>
                  </div>
                )}
              </div>
              <div className={`modal-body`}>{this.props.children}</div>
              {!this.props.downloadingSamples && (
                <div className={`modal-footer`}>
                  <button
                    className={`btn btn-primary btn-sm btn-continue`}
                    onClick={this.props.handleSampleZipDownload}
                  >
                    Download
                  </button>
                  <button
                    className={`ml-2 btn btn-secondary btn-sm
                  btn-cancel`}
                    onClick={this.props.close}
                  >
                    Close
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </Fragment>
    );
  }
}

export default SampleModal;
