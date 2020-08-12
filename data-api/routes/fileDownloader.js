/*
 * Title: fileDownloader.js
 * Description:
 * Created by: ylb9 <ylb9@ncbs-dev-09>
 * Created: 2017-12-16 13:45
 * Last Modified: Thu 02 Jul 2020 03:52:45 PM EDT
 */


const fs = require('fs');

const downloader = {
  findRunDir: (runName) => {
    const basePath = './BMGAP/Instruments/';
    // Update this line to include a list of all of the folders data is stored in
    // const sequencers = [];
    for (let j = 0; j < sequencers.length; j += 1) {
      const seq = sequencers[j];
      const seqFolder = basePath + seq;
      const allRuns = fs.readdirSync(seqFolder);
      for (let i = 0; i < allRuns.length; i += 1) {
        if (allRuns[i] === runName) {
          const finalPath = `${seqFolder}/${runName}`;
          return finalPath;
        }
      }
    }
    return null;
  },
  retrieveFastaData(runName, fileName) {
    const finalPath = this.findRunDir(runName);
    const filePath = `${finalPath}/AssemblyCleanup/${fileName}`;
    try {
      const file = fs.readFileSync(filePath);
      return file;
    } catch (err) {
      return null;
    }
  },
  retrieveFastaFilename(runName, fileName) {
    const finalPath = this.findRunDir(runName);
    const filePath = `${finalPath}/AssemblyCleanup/${fileName}`;
    return { name: fileName, path: filePath };
  },
  retrievePmgaFilename(filePath) {
    const fileName = filePath.split('/').pop(); // I worry this is too clever - it takes the last element of the array formed when split
    return { name: fileName, path: filePath };
  },
  retrievePmgaData(filepath) {
    try {
      const file = fs.readFileSync(filepath);
      return file;
    } catch (err) {
      return null;
    }
  },
};

module.exports = downloader;
