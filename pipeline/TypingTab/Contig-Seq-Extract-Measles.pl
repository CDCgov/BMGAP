#!/usr/bin/perl
use warnings;
use strict;

# program used to extract sequnce region from contigs
# use Contig-Seq-Extract-Measles.pl stdin.fasta stdin.blast
# will open blast.out and input.fasta to find gene of interest from Blast and then
# its corresponding sequence from it fasta file. 
open my $BLAST, '<', $ARGV[1];
    chomp $BLAST;

foreach my $line (<$BLAST>) {
    chomp $line; 
    my @array = split (" ", $line);   
    #if ($array[0] =~ m/^NODE/) {
    if ($array[0] ne "qseqid") {
	my $NodeFa = $array[0];
	my $SeqID = $array[4];
	my $Alen = $array[5];
        my $Gap = $array[6];
	my $QStart = $array[7]-$Gap;
	my $QEnd = $array[8];
	my $SStart = $array[9];
	my $SEnd = $array[10]; 
        my $Ratio = ($SStart/$SEnd);
        my $Bit = $array[11];
        chomp $Bit;

	
#open F, "$ARGV[0].fasta";
open my $FASTA, '<', $ARGV[0];
$/ = "\n>";
while (<$FASTA>) {
    s/>//g; 
    my @seq = split (/\n/, $_);
    my $id = shift @seq;
    if ($id eq $NodeFa) {
	#print join "\n", ">$id", @seq, "\n";
	my $sequence = join "\n", @seq, "\n";  
	$sequence =~ s/\n//g;
        #print "$SeqID\tStart:$QStart\tLength:$Alen\tSStart:$SStart\tSEnd:$SEnd\tRatio:$Ratio\n";
          if ($Ratio < 1){
             print ">$SeqID","_B$Bit","_","$ARGV[0]\n", substr($sequence, $QStart-1, $Alen), "\n";
          } elsif ($Ratio > 1) {
             my $Seq = substr($sequence, $QStart-1, $Alen); 
             my $RevSeq = reverse $Seq; 
             $RevSeq =~ tr/ACGTacgt/TGCAtgca/;
             print ">$SeqID","_B$Bit","_","$ARGV[0]\n", $RevSeq,"\n";
          } else {
            print "NOOOOOOOOOOOOOOOO\n";
          }  
    } 
   } 
  }
 }






