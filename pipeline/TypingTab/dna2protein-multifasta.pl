#!/usr/bin/perl
use strict;
use warnings;
use Data::Dumper;

# This script will converts DNA fasta sequence to PROTEIN Sequence (only in first frame)
# Also makes a NT hash with {name => seq}; and protein hash with {name => amino acid}
# use: perl dna2protein.pl input.seq > output.pro

my %fasta_hash;
my %protein_hash;

$/ = '>';

while (<>) {
    chomp;
    /([\w\-]+)\n(.+)/s and $fasta_hash{$1} = $2 or next; 
    # key is sequence name and value is DNA sequence 
    }
#print Dumper(\%fasta_hash);

for my $seq (keys %fasta_hash){
    #print ">$seq\n";
    my $DNA = $fasta_hash{$seq};
    #print "Hash\n$DNA\n";
    $DNA =~ s/\s//g;
    #print "$DNA\n";
    my $protein = '';
    my $codon;
    for(my $i = 0;$i<(length($DNA)-2);$i+=3) {
        $codon = substr($DNA,$i,3);
        $protein .=& codon2aa($codon);
    }
    my @Stop = ($protein =~ /_/g);
    my $Count = @Stop;
    print ">$seq\tStops:$Count\n";
    print "$protein\n"; 
    $protein_hash{$seq} = $protein;
}
#print Dumper(\%protein_hash);


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


