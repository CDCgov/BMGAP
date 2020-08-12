var mongoose = require('mongoose')
var paginator = require('mongoose-paginate')

// model ===========================
var Sample = mongoose.Schema({
  mash: {
    Top_Species: String
  },
  Run_ID: String,
  Lab_ID: String,
  MLST: {
    Filename: String,
    Hi_MLST_ST: String,
    Nm_MLST_ST: String,
    Nm_MLST_cc: String
  },
  serogrouping: {
    Infer: String,
    baseSG: String
  },
  meta: {
    Organism: String,
    Submitter_Country: String,
    Submitter_State: String,
    Submitter_Type: String,
    Year_Collected: Number
  },
  serotyping: {
    ST: String
  },	
  PMGA:{
		filejson : String,
		filegff  : String,
	},
  Serogroup :{
		Query : String,
		SG : String,
		Genes_Present : String,
		Notes : String,
	},
  Serotype :{
		Query : String,
		ST : String,
		Genes_Present : String,
		Notes : String,
	},
	cleanData : {
		Bases_In_Contigs :String,
		Contig_Count :String,
		N50 : String,
		N90 : String,
		Mean_Coverage : String,
		Ambiguous_nucleotides : String,
		Mean_Coverage_raw : String,
		HalfCov_Contig_Bases: String,
		Bases_In_Contigs_raw: String,
		HalfCov_Contig_Count: String,
		Status: String,
	},
	PMGATyping :{
		Serogroup : [{
			baseSG: String,
			predicted_sg : String,
			
			}],
		Serotype :[{
			baseST: String,
			predicted_st : String,
			}],
		
	},
	
}, {collection: 'internal'})

Sample.index({'mash.Top_Species': 1})
Sample.index({'serogrouping.Infer': 1})
Sample.index({'serotyping.ST': 1})
Sample.index({'meta.Year_Collected': 1})
Sample.index({'MLST.Nm_MLST_ST': 1})
Sample.index({'MLST.Hi_MLST_ST': 1})
Sample.plugin(paginator)

module.exports = mongoose.model('Sample', Sample)
