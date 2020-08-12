import React, { Fragment } from "react";
import {
  FaRegCheckSquare,
  FaRegSquare,
  FaSearch,
  FaExclamationCircle,
  FaTimesCircle
} from "react-icons/fa";
import { Link } from "react-router-dom";

import "./SampleTable.scss";

const HAEMOPHILUS = "Haemophilus_influenzae";
const NEISSERIA = "Neisseria_meningitidis";

function SampleRow({
  sample,
  handleCheckClick,
  isChecked,
  id,
  run,
  search,
  isRelatedSample,
  isSampleFileUpload
}) {
  return (
    <Fragment key={id}>
      {(!isRelatedSample && (
        <tr>
          {handleCheckClick && (
            <td>
              <div className="d-inline-flex">
                <div
                  className="mr-2"
                  onClick={handleCheckClick.bind(this, sample.identifier)}
                >
                  {isChecked ? <FaRegCheckSquare /> : <FaRegSquare />}
                </div>
                <Link
                  to={{
                    pathname: `/sample/${sample.identifier}`,
                    state: {
                      sample: sample.identifier,
                      run: run,
                      isSampleFileUpload
                    },
                    search: search
                  }}
                >
                  <button className="btn-sm btn-primary py-0 px-1">
                    <FaSearch />
                  </button>
                </Link>
              </div>
            </td>
          )}
          <td className="sample-row-m">
            {sample.identifier && sample.Lab_ID ? (
              <Fragment>
                <Link
                  to={{
                    pathname: `/sampleDetails/${sample.identifier}`,
                    state: {
                      sample: sample.identifier,
                      run: run,
                      isSampleFileUpload
                    },
                    search: search
                  }}
                >
                  <span className="sample-name">{sample.Lab_ID}</span>
                </Link>
                {sample["sequence_flagged"] && (
                  <span
                    data-toggle="tooltip"
                    data-placement="top"
                    title={`Possible Sample Contamination`}
                  >
                    <FaTimesCircle className="ml-2 text-danger icon-warning" />
                  </span>
                )}
                {sample["assembly_flagged"] && (
                  <span
                    data-toggle="tooltip"
                    data-placement="top"
                    title={`Low Assembly Coverage`}
                  >
                    <FaExclamationCircle className="ml-2 text-warning icon-warning" />
                  </span>
                )}
              </Fragment>
            ) : (
              " "
            )}
          </td>
          <td className="sample-row-m">
            {sample.location ? sample.location : " "}
          </td>
          <td className="sample-row-s">{sample.year ? sample.year : " "}</td>
          <td className="sample-row-m">
            {sample.Submitter ? sample.Submitter : " "}
          </td>
          <td className="font-italic">{generateSpecies(sample)}</td>
          <td className="sample-row-m">{generateMLST(sample)}</td>
          <td className="sample-row-l">{generateSerogroup(sample)}</td>
          <td className="sample-row-l">{generateSerotype(sample)}</td>
        </tr>
      )) || (
        <tr>
          <td className="">
            {sample.identifier && sample.Lab_ID ? (
              <Fragment>
                <span className="">{sample.Lab_ID}</span>
                {sample["sequence_flagged"] && (
                  <span
                    data-toggle="tooltip"
                    data-placement="top"
                    title={`Possible Sample Contamination`}
                  >
                    <FaTimesCircle className="ml-2 text-danger icon-warning" />
                  </span>
                )}
                {sample["assembly_flagged"] && (
                  <span
                    data-toggle="tooltip"
                    data-placement="top"
                    title={`Low Assembly Coverage`}
                  >
                    <FaExclamationCircle className="ml-2 text-warning icon-warning" />
                  </span>
                )}
              </Fragment>
            ) : (
              " "
            )}
          </td>
          <td className="">{sample.location ? sample.location : " "}</td>
          <td className="">{sample.year ? sample.year : " "}</td>
          <td className="">{sample.Submitter ? sample.Submitter : " "}</td>
          <td className="font-italic">{generateSpecies(sample)}</td>
          <td className="">{generateMLST(sample)}</td>
          <td className="">{generateSerogroup(sample)}</td>
          <td className="">{generateSerotype(sample)}</td>
          <td className="">{sample.distance}</td>
        </tr>
      )}
    </Fragment>
  );
}

function generateMLST(sample) {
  if (!sample.MLST || !sample.Species) {
    return " ";
  }
  if (sample.MLST.toString().includes("New")) {
    return "New";
  }
  if (sample.MLST.toString().includes("Error")) {
    return "Error";
  }
  if (sample.MLST.toString().includes("Not applicable")) {
    return "Not applicable";
  }
  if (sample.Species !== NEISSERIA) {
    return `ST-${sample.MLST}`;
  }
  if (sample.cc && sample.Species === NEISSERIA) {
    return `ST-${sample.MLST} ${sample.cc}`;
  } else {
    return " ";
  }
}

function generateSerogroup(sample) {
  if (sample.Serogroup && sample.Species && sample.Species === NEISSERIA) {
    return sample.Serogroup;
  } else {
    return " ";
  }
}

function generateSerotype(sample) {
  if (sample.Serotype && sample.Species && sample.Species === HAEMOPHILUS) {
    return sample.Serotype;
  } else {
    return " ";
  }
}

function generateSpecies(sample) {
  if (sample.Species) {
    return sample.Species.replace(/_/g, " ");
  } else {
    return " ";
  }
}

export default SampleRow;
