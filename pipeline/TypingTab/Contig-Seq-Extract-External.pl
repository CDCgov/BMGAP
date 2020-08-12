#!/usr/bin/perl
use warnings;
#use strict;

# program used to generate percent alignment
# extract gene sequnce from contig
# find the number of stop within a gene and 
# outputs the information in a blast outfmt 6 manner. 
# use Contig-Seq-Extract.pl $line - #when piping after blast.  
# example: blastn... | perl Contig-Seq-Extract-External.pl M42461_VF005B01 - > M43461_VF005B01-AllCap.out
# the blast output is piped into perl script. 
# can save output to file > $line.out
# will open input-contigs.fasta and input.fasta to find gene of interest from Blast and then
# its corresponding sequence from it fasta file. 

#my $head = "sseqid\tnode\tcov\tpident\tlength\tqlen\tslen\tmm\tgap\tqstart\tqend\tsstart\tsend\tevalue\tbit\tpaln\tstop\tseq\n";
my $head = "qseqid\tsseqid\tpident\talen\tqlen\tslen\tmm\tgap\tqstart\tqend\tsstart\tsend\tevalue\tbit\tnode\tcov\taper\tstops\tseq\t";

open my $input, $ARGV[1];
foreach my $line (<$input>){
    chomp $line;
    my @array = split (" ", $line); 
	my $NodeFa = $array[0];
	my $SeqID = $array[1];
	my $PerID = $array[2];
	my $Alen = $array[3];
        my $Qlen = $array[4];
	my $Slen = $array[5];
	my $APer = ($Alen/$Slen)*100;
	my $ARnd = sprintf("%.2f", $APer); 
	my @array2 = split ("_", $array[0]); 
	my $Node = $array2[1];
	my $Cov = $array2[5];
	my $MM = $array[6];        
	my $Gap = $array[7];
	my $Qbeg = $array[8];
	my $QStart = $array[8]-$Gap;
	my $QEnd = $array[9];

        my $AbsAlen = abs($QEnd-$Qbeg);

	my $SStart = $array[10];
	my $SEnd = $array[11];
	my $Eval = $array[12]; 
        my $Ratio = ($SStart/$SEnd);
	my $LenDiff = $Alen-$Slen;
        my $Bit = $array[13];
        chomp $Bit;
	
#open F, "$ARGV[0].fasta";
open my $fasta, '<', "$ARGV[0]-contigs.fasta";
$/ = "\n>";
while (<$fasta>) {
    s/>//g; 
    my @seq = split (/\n/, $_);
    my $id = shift @seq;
    my $DNA;
    if ($id eq $NodeFa) {
	my $sequence = join "\n", @seq, "\n";  
	$sequence =~ s/\n//g;
          if ($Ratio < 1){
             #my $Seq = substr($sequence, $QStart-1+$LenDiff, $Alen); 
             #my $Seq = substr($sequence, $QStart-1, $AbsAlen+1); 
             my $Seq = substr($sequence, $Qbeg-1, $Alen); 
             #print $array[1],",",$array2[1],",",$array2[5],",",$array[2],",",$array[3],",",$array[4],",",$array[5],",",$array[6],",",$array[7],",",$array[8],",",$array[9],",",$array[10],",",$array[11],",",$array[12],",",$array[13],",",$ARnd;
             print "$NodeFa\t$SeqID\t$PerID\t$Alen\t$Qlen\t$Slen\t$MM\t$Gap\t$Qbeg\t$QEnd\t$SStart\t$SEnd\t$Eval\t$Bit\t$Node\t$Cov\t$ARnd\t";
             $DNA = $Seq;
          } elsif ($Ratio > 1) {
             #my $Seq = substr($sequence, $QStart-1+$LenDiff, $Alen); 
             #my $Seq = substr($sequence, $QStart-1, $AbsAlen+1); 
             my $Seq = substr($sequence, $Qbeg-1, $Alen); 
             my $RevSeq = reverse $Seq; 
             $RevSeq =~ tr/ACGTacgt/TGCAtgca/;
             #print $array[1],",",$array2[1],",",$array2[5],",",$array[2],",",$array[3],",",$array[4],",",$array[5],",",$array[6],",",$array[7],",",$array[8],",",$array[9],",",$array[10],",",$array[11],",",$array[12],",",$array[13],",",$ARnd;
             print "$NodeFa\t$SeqID\t$PerID\t$Alen\t$Qlen\t$Slen\t$MM\t$Gap\t$Qbeg\t$QEnd\t$SStart\t$SEnd\t$Eval\t$Bit\t$Node\t$Cov\t$ARnd\t";
             $DNA = $RevSeq;
          } else {
            print "NOOOOOOOOOOOOOOOO\n";
          }  
        $DNA =~ s/\s//g;
        my $protein = '';
        my $codon;
        for(my $i = 0;$i<(length($DNA)-2);$i+=3) {
            $codon = substr($DNA,$i,3);
            $protein .=& codon2aa($codon);
        }
        my @Stop = ($protein =~ /_/g);
        my $Count = @Stop;
        print "\t","$Count","\t","$DNA\n";
        #print "\t","$Count","\t","$DNA","\t","$protein","\n";
        } 
    }
}

####################
sub codon2aa{
my($codon) = @_;
$codon = uc $codon;
my(%g) = ('TCA'=>'S','TCC'=>'S','TCG'=>'S','TCT'=>'S','TTC'=>'F','TTT'=>'F','TTA'=>'L','TTG'=>'L','TAC'=>'Y','TAT'=>'Y','TAA'=>'_','TAG'=>'_','TGC'=>'C','TGT'=>'C','TGA'=>'_','TGG'=>'W','CTA'=>'L','CTC'=>'L','CTG'=>'L','CTT'=>'L','CCA'=>'P','CCC'=>'P','CCG'=>'P','CCT'=>'P','CAC'=>'H','CAT'=>'H','CAA'=>'Q','CAG'=>'Q','CGA'=>'R','CGC'=>'R','CGG'=>'R','CGT'=>'R','ATA'=>'I','ATC'=>'I','ATT'=>'I','ATG'=>'M','ACA'=>'T','ACC'=>'T','ACG'=>'T','ACT'=>'T','AAC'=>'N','AAT'=>'N','AAA'=>'K','AAG'=>'K','AGC'=>'S','AGT'=>'S','AGA'=>'R','AGG'=>'R','GTA'=>'V','GTC'=>'V','GTG'=>'V','GTT'=>'V','GCA'=>'A','GCC'=>'A','GCG'=>'A','GCT'=>'A','GAC'=>'D','GAT'=>'D','GAA'=>'E','GAG'=>'E','GGA'=>'G','GGC'=>'G','GGG'=>'G','GGT'=>'G');
    if(exists $g{$codon}){
        return $g{$codon};
    }
    else {
        print STDERR "Bad codon \"$codon\"!!\n";
        exit;
    }
}

