import * as React from "react";
import './Spinner.scss';

const Spinner = (props) => {
  return (
    <div className={`row justify-content-center spinner-container`}>
      <div className={`DNA_cont`}>
        <div className={`nucleobase`}></div>
        <div className={`nucleobase`}></div>
        <div className={`nucleobase`}></div>
        <div className={`nucleobase`}></div>
        <div className={`nucleobase`}></div>
        <div className={`nucleobase`}></div>
        <div className={`nucleobase`}></div>
        <div className={`nucleobase`}></div>
        <div className={`nucleobase`}></div>
        <div className={`nucleobase`}></div>
      </div>
    </div>
  );
};

export default Spinner;
