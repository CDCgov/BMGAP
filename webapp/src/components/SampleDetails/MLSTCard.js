import React, { Fragment } from "react";

import "../SampleDetails/SampleDetails.scss";

const HAEMOPHILUS = "Haemophilus_influenzae";
const NEISSERIA = "Neisseria_meningitidis";

function MLSTCard({ sampleDetails }) {
  return (
    <Fragment>
      {sampleDetails.mash && (
        <div className="card mb-4">
          <h3 className="card-header font-weight-bold">Molecular Typing</h3>
          <div className="card-body">
            {sampleDetails.mash &&
              sampleDetails.mash.Top_Species === HAEMOPHILUS && (
                <Fragment>
                  {sampleDetails.MLST && sampleDetails.MLST.Hi_MLST_ST ? (
                    <p className="card-text">
                      <span className="font-weight-bold">Sequence Type </span>
                      {sampleDetails.MLST.Hi_MLST_ST}
                    </p>
                  ) : null}
                  <hr />
                  <table className="table table-borderless">
                    <thead>
                      <tr>
                        <th scope="col">adk</th>
                        <th scope="col">atpG</th>
                        <th scope="col">frdB</th>
                        <th scope="col">fucK</th>
                        <th scope="col">mdh</th>
                        <th scope="col">pgi</th>
                        <th scope="col">recA</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td className="pt-0">
                          {sampleDetails.MLST && sampleDetails.MLST.Hi_MLST_adk
                            ? sampleDetails.MLST.Hi_MLST_adk
                            : "-"}
                        </td>
                        <td className="pt-0">
                          {sampleDetails.MLST && sampleDetails.MLST.Hi_MLST_atpG
                            ? sampleDetails.MLST.Hi_MLST_atpG
                            : "-"}
                        </td>
                        <td className="pt-0">
                          {sampleDetails.MLST && sampleDetails.MLST.Hi_MLST_frdB
                            ? sampleDetails.MLST.Hi_MLST_frdB
                            : "-"}
                        </td>
                        <td className="pt-0">
                          {sampleDetails.MLST && sampleDetails.MLST.Hi_MLST_fucK
                            ? sampleDetails.MLST.Hi_MLST_fucK
                            : "-"}
                        </td>
                        <td className="pt-0">
                          {sampleDetails.MLST && sampleDetails.MLST.Hi_MLST_mdh
                            ? sampleDetails.MLST.Hi_MLST_mdh
                            : "-"}
                        </td>
                        <td className="pt-0">
                          {sampleDetails.MLST && sampleDetails.MLST.Hi_MLST_pgi
                            ? sampleDetails.MLST.Hi_MLST_pgi
                            : "-"}
                        </td>
                        <td className="pt-0">
                          {sampleDetails.MLST && sampleDetails.MLST.Hi_MLST_recA
                            ? sampleDetails.MLST.Hi_MLST_recA
                            : "-"}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </Fragment>
              )}
            {sampleDetails.mash &&
              sampleDetails.mash.Top_Species === NEISSERIA && (
                <Fragment>
                  {sampleDetails.MLST &&
                  sampleDetails.MLST.Nm_MLST_ST &&
                  sampleDetails.MLST.Nm_MLST_cc ? (
                    <p className="card-text">
                      <span className="font-weight-bold">Sequence Type </span>
                      {sampleDetails.MLST.Nm_MLST_ST} (
                      {sampleDetails.MLST.Nm_MLST_cc})
                    </p>
                  ) : null}
                  <hr />
                  <table className="table table-borderless">
                    <thead>
                      <tr>
                        <th scope="col">abcZ</th>
                        <th scope="col">adk</th>
                        <th scope="col">aroE</th>
                        <th scope="col">fumC</th>
                        <th scope="col">gdh</th>
                        <th scope="col">pdhC</th>
                        <th scope="col">pgm</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td className="pt-0">
                          {sampleDetails.MLST && sampleDetails.MLST.Nm_MLST_abcZ
                            ? sampleDetails.MLST.Nm_MLST_abcZ
                            : "-"}
                        </td>
                        <td className="pt-0">
                          {sampleDetails.MLST && sampleDetails.MLST.Nm_MLST_adk
                            ? sampleDetails.MLST.Nm_MLST_adk
                            : "-"}
                        </td>
                        <td className="pt-0">
                          {sampleDetails.MLST && sampleDetails.MLST.Nm_MLST_aroE
                            ? sampleDetails.MLST.Nm_MLST_aroE
                            : "-"}
                        </td>
                        <td className="pt-0">
                          {sampleDetails.MLST && sampleDetails.MLST.Nm_MLST_fumC
                            ? sampleDetails.MLST.Nm_MLST_fumC
                            : "-"}
                        </td>
                        <td className="pt-0">
                          {sampleDetails.MLST && sampleDetails.MLST.Nm_MLST_gdh
                            ? sampleDetails.MLST.Nm_MLST_gdh
                            : "-"}
                        </td>
                        <td className="pt-0">
                          {sampleDetails.MLST && sampleDetails.MLST.Nm_MLST_pdhC
                            ? sampleDetails.MLST.Nm_MLST_pdhC
                            : "-"}
                        </td>
                        <td className="pt-0">
                          {sampleDetails.MLST && sampleDetails.MLST.Nm_MLST_pgm
                            ? sampleDetails.MLST.Nm_MLST_pgm
                            : "-"}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                  <hr />
                  <table className="table table-borderless">
                    <thead>
                      <tr>
                        <th scope="col">PorA type</th>
                        <th scope="col">PorB type</th>
                        <th scope="col">FetA</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td className="pt-0">
                          {sampleDetails.MLST && sampleDetails.MLST.PorA_type
                            ? sampleDetails.MLST.PorA_type
                            : "-"}
                        </td>
                        <td className="pt-0">
                          {sampleDetails.MLST && sampleDetails.MLST.PorB_type
                            ? sampleDetails.MLST.PorB_type
                            : "-"}
                        </td>
                        <td className="pt-0">
                          {sampleDetails.MLST && sampleDetails.MLST.FetA
                            ? sampleDetails.MLST.FetA
                            : "-"}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                  <table className="table table-bordered my-4">
                    <thead>
                      <tr>
                        <th colSpan="7" scope="col" className="text-center">
                          FHbp
                        </th>
                      </tr>
                    </thead>
                    <thead>
                      <tr>
                        <th colSpan="2" scope="col" className="text-center">
                          Oxford
                        </th>
                        <th colSpan="2" scope="col" className="text-center">
                          Novartis
                        </th>
                        <th colSpan="3" scope="col" className="text-center">
                          Pfizer
                        </th>
                      </tr>
                    </thead>
                    <thead>
                      <tr>
                        <th>Protein Variant</th>
                        <th>DNA Allele</th>
                        <th>Protein Variant</th>
                        <th>DNA Allele</th>
                        <th>Subfamily</th>
                        <th>Protein Variant</th>
                        <th>DNA Allele</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td className="pt-0">
                          {sampleDetails.MLST &&
                          sampleDetails.MLST.FHbp_protein_subvariant_Oxford
                            ? sampleDetails.MLST.FHbp_protein_subvariant_Oxford
                            : "-"}
                        </td>
                        <td className="pt-0">
                          {sampleDetails.MLST &&
                          sampleDetails.MLST.fHbp_DNA_allele_Oxford
                            ? sampleDetails.MLST.fHbp_DNA_allele_Oxford
                            : "-"}
                        </td>
                        <td className="pt-0">
                          {sampleDetails.MLST &&
                          sampleDetails.MLST.FHbp_protein_subvariant_Novartis
                            ? sampleDetails.MLST
                                .FHbp_protein_subvariant_Novartis
                            : "-"}
                        </td>
                        <td className="pt-0">
                          {sampleDetails.MLST &&
                          sampleDetails.MLST.fHbp_DNA_allele_Novartis
                            ? sampleDetails.MLST.fHbp_DNA_allele_Novartis
                            : "-"}
                        </td>
                        <td className="pt-0">
                          {sampleDetails.MLST &&
                          sampleDetails.MLST.FHbp_subfamily
                            ? sampleDetails.MLST.FHbp_subfamily
                            : "-"}
                        </td>
                        <td className="pt-0">
                          {sampleDetails.MLST &&
                          sampleDetails.MLST.FHbp_protein_subvariant_Pfizer
                            ? sampleDetails.MLST.FHbp_protein_subvariant_Pfizer
                            : "-"}
                        </td>
                        <td className="pt-0">
                          {sampleDetails.MLST &&
                          sampleDetails.MLST.fHbp_DNA_allele_Pfizer
                            ? sampleDetails.MLST.fHbp_DNA_allele_Pfizer
                            : "-"}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                  <table className="table table-borderless">
                    <thead>
                      <tr>
                        <th scope="col">nadA PCR</th>
                        <th scope="col">NadA Protein subvariant Novartis</th>
                        <th scope="col">NhbA Protein subvariant Novartis</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td className="pt-0">
                          {sampleDetails.MLST && sampleDetails.MLST.nadA_PCR
                            ? sampleDetails.MLST.nadA_PCR
                            : "-"}
                        </td>
                        <td className="pt-0">
                          {sampleDetails.MLST &&
                          sampleDetails.MLST.NadA_Protein_subvariant_Novartis
                            ? sampleDetails.MLST
                                .NadA_Protein_subvariant_Novartis
                            : "-"}
                        </td>
                        <td className="pt-0">
                          {sampleDetails.MLST &&
                          sampleDetails.MLST.NhbA_Protein_subvariant_Novartis
                            ? sampleDetails.MLST
                                .NhbA_Protein_subvariant_Novartis
                            : "-"}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </Fragment>
              )}
          </div>
        </div>
      )}
    </Fragment>
  );
}

export default MLSTCard;
