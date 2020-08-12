import React, { Fragment } from "react";
import moment from "moment";
import { Link } from "react-router-dom";
import { FaSyncAlt } from "react-icons/fa";

import Pagination from "../Pagination/Pagination";
import PageInfo from "../Pagination/PageInfo";
import Spinner from "../../components/Spinner/Spinner";

import "./RunTable.scss";

function RunTable(props) {
  return (
    <Fragment>
      <div className={`d-flex flex-row run-container`}>
        <div className="ghost-box invisible">Ghost box</div>
        <div className={`d-flex flex-column container run-box`}>
          {props.runs && props.runs.length && !props.fetchingRuns && (
            <Fragment>
              <h3 className="font-weight-bold mb-2">Table of Runs</h3>
              <div
                className={
                  `mb-2 d-flex ` +
                  (props.runs.length > 10
                    ? `justify-content-between`
                    : `justify-content-end`)
                }
              >
                {props.runs.length > 10 && (
                  <Pagination
                    onPageClick={props.onPageClick}
                    totalPages={Math.ceil(
                      props.totalItems / props.itemNumberFilter
                    )}
                    currentPage={props.currentPage}
                    totalItems={props.totalItems}
                    itemsPerPage={props.runs.length}
                  />
                )}
                <div>
                  <Link
                    to={{
                      pathname: "/analytics",
                      state: { run: [] },
                      search: props.search,
                    }}
                  >
                    <button className="btn btn-sm btn-primary">
                      Analytics
                    </button>
                  </Link>
                </div>
              </div>
              <table className="table table-hover flex-column">
                <thead>
                  <tr>
                    <th>Run name</th>
                    <th># of samples</th>
                    <th>Sequencer</th>
                    <th>Submitter</th>
                    <th># of running samples</th>
                    <th>Date</th>
                  </tr>
                </thead>
                <tbody>
                  {props.runs &&
                    props.runs.map((run) => (
                      <tr key={run._id}>
                        <td className="">
                          <Link
                            to={{
                              pathname: `/run/${run.run}`,
                              state: { run: run.run },
                              search: props.search,
                            }}
                          >
                            <span className="run-name mr-2">{run.run}</span>
                          </Link>
                          {typeof run.analysis_running === "boolean" &&
                            run.analysis_running === true && (
                              <span
                                data-toggle="tooltip"
                                data-placement="top"
                                title="This run is currently being analyzed"
                              >
                                <FaSyncAlt />
                              </span>
                            )}
                        </td>
                        <td className="">{run.samples}</td>
                        <td className="">{run.sequencer}</td>
                        <td className="">{run.submitter}</td>
                        <td className="">{run.samples_running || "-"}</td>
                        <td className="">
                          {moment(run.date).format("MM-DD-YYYY")}
                        </td>
                      </tr>
                    ))}
                </tbody>
              </table>
              <Pagination
                onPageClick={props.onPageClick}
                totalPages={Math.ceil(
                  props.totalItems / props.itemNumberFilter
                )}
                currentPage={props.currentPage}
                totalItems={props.totalItems}
                itemsPerPage={props.runs.length}
              />
              <PageInfo
                currentPage={props.currentPage}
                totalItems={props.totalItems}
                itemNumberFilter={props.itemNumberFilter}
              />
            </Fragment>
          )}
          {props.fetchingRuns && <Spinner />}
          {!props.fetchingRuns && !props.runs && (
            <p>Sorry, you aren’t authorized to see any data</p>
          )}
        </div>
      </div>
    </Fragment>
  );
}

export default RunTable;
