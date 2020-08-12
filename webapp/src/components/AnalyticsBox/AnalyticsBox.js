import React, { Fragment } from "react";
import { Bar } from "react-chartjs-2";
import { Link } from "react-router-dom";

function AnalyticsBox({ analytics, search }) {
  const sampleYears = analytics.samples
    .filter(value => value.year !== null && value.year !== "")
    .map(value => value.year);

  const sampleCounts = analytics.samples
    .filter(value => value.year !== null && value.year !== "")
    .map(value => value.count);

  const species = analytics.species.filter(
    value => value.Year !== null && value.Year !== ""
  );

  const speciesYears = species.map(value => value.Year);

  let speciesNeisseria = [];

  let speciesHaemophilus = [];

  species.forEach(specia => {
    specia.Species.forEach(someSpecies => {
      if (someSpecies.species_name === "Neisseria_meningitidis") {
        speciesNeisseria.push({ count: someSpecies.count, year: specia.Year });
      }
      if (someSpecies.species_name === "Haemophilus_influenzae") {
        speciesHaemophilus.push({
          count: someSpecies.count,
          year: specia.Year
        });
      }
    });
  });

  const samplesData = {
    labels: sampleYears,
    datasets: [
      {
        label: "# of Samples",
        backgroundColor: "rgba(255,99,132,0.2)",
        borderColor: "rgba(255,99,132,1)",
        borderWidth: 1,
        hoverBackgroundColor: "rgba(255,99,132,0.4)",
        hoverBorderColor: "rgba(255,99,132,1)",
        data: sampleCounts
      }
    ]
  };

  const speciesData = {
    labels: speciesYears,
    datasets: [
      {
        label: "Neisseria meningitidis",
        backgroundColor: "rgba(99,132,255,0.2)",
        borderColor: "rgba(99,132,255,1)",
        borderWidth: 1,
        hoverBackgroundColor: "rgba(99,132,255,0.4)",
        hoverBorderColor: "rgba(99,132,255,1)",
        data: speciesNeisseria.map(value => value.count)
      },
      {
        label: "Haemophilus influenzae",
        backgroundColor: "rgba(255,99,132,0.2)",
        borderColor: "rgba(255,99,132,1)",
        borderWidth: 1,
        hoverBackgroundColor: "rgba(255,99,132,0.4)",
        hoverBorderColor: "rgba(255,99,132,1)",
        data: speciesHaemophilus.map(value => value.count)
      }
    ]
  };

  return (
    <Fragment>
      <div
        className={`container-fluid run-table-container d-flex flex-column justify-content-center`}
      >
        <div className={`d-flex justify-content-end`}>
          <Link
            to={{
              pathname: `/`,
              state: {},
              search: search
            }}
          >
            <button className="btn btn-sm btn-primary">Back to Runs</button>
          </Link>
        </div>
        <div className="d-flex justify-content-center flex-grow-1">
          <h3 className="text-center font-weight-bold">Analytics Page</h3>
        </div>
        <h5 className="mt-4 text-center">Samples per Year</h5>
        <div className="ct-chart mt-1" id="chart"></div>
        <Bar
          data={samplesData}
          width={80}
          height={30}
          options={{
            maintainAspectRatio: true
          }}
        />
        <h5 className="mt-5 text-center">Species per Year</h5>
        <div className="ct-chart mt-1" id="chart"></div>
        <Bar
          data={speciesData}
          width={80}
          height={30}
          options={{
            maintainAspectRatio: true
          }}
        />
      </div>
    </Fragment>
  );
}

export default AnalyticsBox;
