import React, { Fragment } from "react";
import { FaRegCheckSquare, FaRegSquare } from "react-icons/fa";

import "./SampleTable.scss";

const sampleDownloadTypes = [
  { type: "meta", text: "Sample Information" },
  { type: "cleanData", text: "Assembly Statistics" },
  { type: "Serotype", text: "Serotype Information" },
  { type: "Serogroup", text: "Serogroup Information" },
  { type: "mash", text: "Species Information" },
  { type: "MLST", text: "Molecular Typing" }
];

const sampleAdvancedDownloadTypes = [
  ...sampleDownloadTypes,
  { type: "fasta", text: "Assembled Contigs (fasta)" },
  { type: "gff", text: "Genome Annotation Results (GFF)" }
];

function SampleDownload({
  handleSampleTypeClick,
  selectedSampleTypes,
  viewDownloadOptions,
  handleViewDownloadOptions
}) {
  return (
    <Fragment>
      {(!viewDownloadOptions && (
        <Fragment>
          <p className="font-weight-bold mb-2">Select download options</p>
          {sampleDownloadTypes.map(sampleType => {
            return (
              <div className={`mb-1`} key={sampleType.type}>
                <span
                  onClick={handleSampleTypeClick.bind(this, sampleType.type)}
                >
                  {selectedSampleTypes[sampleType.type] ? (
                    <FaRegCheckSquare />
                  ) : (
                    <FaRegSquare />
                  )}
                </span>
                <span className="ml-2">{sampleType.text}</span>
              </div>
            );
          })}
          <button
            className="btn btn-primary btn-sm download-options-link mt-2"
            onClick={handleViewDownloadOptions.bind(this, true)}
          >
            View advanced options
          </button>
        </Fragment>
      )) || (
        <Fragment>
          <p className="font-weight-bold mb-2">Select download options</p>
          {sampleAdvancedDownloadTypes.map(sampleType => {
            return (
              <div className={`mb-1`} key={sampleType.type}>
                <span
                  onClick={handleSampleTypeClick.bind(this, sampleType.type)}
                >
                  {selectedSampleTypes[sampleType.type] ? (
                    <FaRegCheckSquare />
                  ) : (
                    <FaRegSquare />
                  )}
                </span>
                <span className="ml-2">{sampleType.text}</span>
              </div>
            );
          })}
          <button
            className="btn btn-primary btn-sm download-options-link mt-2"
            onClick={handleViewDownloadOptions.bind(this, false)}
          >
            Hide advanced options
          </button>
        </Fragment>
      )}
    </Fragment>
  );
}

export default SampleDownload;
