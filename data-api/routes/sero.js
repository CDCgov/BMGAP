const geneSet = require('./colorfile');

const getFeatureColors = (geneName) => {
  let geneColor = null;
  geneColor = geneSet.colors.serogroupingGenes.filter(a => a.name === geneName);
  if (geneColor[0]) {
    return geneColor[0].color;
  }
  geneColor = geneSet.colors.serotypingGenes.filter(a => a.name === geneName);
  if (geneColor[0]) {
    return geneColor[0].color;
  }
  return null;
};

const makeFeatures = (features, featName) => {
  const newFeature = {
    data: features,
    type: 'rect',
    name: featName,
    height: 24,
  };
  return newFeature;
};

const getTypingGenes = (typing) => {
  if (typing.Serogroup.length > 0) {
    const geneList = typing.Serogroup[0]._doc.genes;
    return geneList;
  }
  if (typing.Serotype.length > 0) {
    const geneList = typing.Serotype[0]._doc.genes;
    return geneList;
  }
  return [];
};


const getContigName = (contig) => {
  const contigParts = contig.split('_');
  return `ctg_${contigParts.pop()}`;
};

const getUniqueContigs = (typingGenes) => {
  // console.log(typingGenes);
  const contigs = [];
  if (typingGenes) {
    typingGenes.forEach((gene) => {
      if (gene.contig && !contigs.includes(gene.contig)) {
        contigs.push(gene.contig);
      }
    });
  }
  return contigs;
};

const getOffset = (featureGenes) => {
  const points = [];
  featureGenes.forEach((item) => {
    points.push(item.x);
    points.push(item.y);
  });
  const filteredPoints = points.filter(Boolean);
  const start = Number.parseInt(Math.min.apply(null, filteredPoints), 10);
  const startThousands = start / 1000;
  const startRoundDown = Math.floor(startThousands) * 1000;
  const end = Number.parseInt(Math.max.apply(null, filteredPoints), 10);
  const endThousands = end / 1000;
  const endRoundUp = (Math.ceil(endThousands)) * 1000;

  const offsetObj = { start: startRoundDown, end: endRoundUp };
  return offsetObj;
};

const getContigLength = (featureGenes) => {
  const coordinates = getOffset(featureGenes);
  return coordinates.start + coordinates.end;
};

const extractGeneInfo = (typingGenes) => {
  const contigs = getUniqueContigs(typingGenes);
  const features = [];
  if (contigs) {
    contigs.forEach((c) => {
      const geneList = [];
      const geneNames = [];
      const contigGenes = typingGenes.filter(gene => c === gene.contig);
      contigGenes.forEach((gene) => {
        if (gene.allele_name && !geneNames.includes(gene.allele_name)) {
          const entry = {
            x: Number.parseInt(gene.qstart, 10),
            y: Number.parseInt(gene.qend, 10),
            description: gene.allele_name,
            color: getFeatureColors(gene.allele_name),
          };
          geneList.push(entry);
          geneNames.push(gene.allele_name);
        }
      });
      if (geneList.length > 0) {
        const ctgName = getContigName(c);
        features[ctgName] = { length: getContigLength(geneList), genes: geneList };
      }
    });
  }
  return features;
};

const getSeroData = (record) => {
  const typingGenes = getTypingGenes(record.PMGATyping);
  const features = extractGeneInfo(typingGenes);
  const viewerObj = {
    showAxis: true,
    showSequence: false,
    brushActive: true, // zoom
    toolbar: true, // current zoom & mouse position
    bubbleHelp: true,
    zoomMax: 10,
  };
  const genesObj = [];
  Object.keys(features).forEach((f) => {
    if (f.length > 0) {
      genesObj.push(makeFeatures(features[f].genes, f));
      // console.log(genesObj);
      return genesObj;
    }
    return null;
  });
  let finalGeneList = [];
  Object.keys(genesObj).forEach((m) => {
    // console.log(m);
    // console.log(genesObj[m].data);
    if (finalGeneList.length > 0) {
      finalGeneList = finalGeneList.concat(genesObj[m].data);
    } else {
      finalGeneList = genesObj[m].data;
    }
  });
  viewerObj.offset = getOffset(finalGeneList);
  const finalObj = {
    viewerObj,
    features: genesObj,
  };
  return finalObj;
};

module.exports = { getSeroData };
