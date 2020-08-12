#!/usr/bin/perl
use warnings;
use strict;

# program used to extract sequnce region from contigs
# use Contig-Seq-Extract.pl $line > $line.seq
# will open $line-AllCap.out and $line.fasta to find gene of interest from Blast and then
# its corresponding sequence from it fasta file. 
open my $AllCap, '<', "$ARGV[0]-AllCap.out";
    chomp $AllCap;

foreach my $line (<$AllCap>) {
    chomp $line; 
    my @array = split (" ", $line);   
    if ($array[0] =~ m/^NODE/) {
	my $NodeFa = $array[0];
	my $SeqID = $array[1];
	my $Alen = $array[3];
	my $Slen = $array[5];
        my $Gap = $array[7];
	my $QStart = $array[8]-$Gap;
	#my $QStart = $array[8];
	my $QEnd = $array[9];

        my $AbsAlen = abs($QEnd-$QStart);

	my $SStart = $array[10];
	my $SEnd = $array[11]; 
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
    if ($id eq $NodeFa) {
	#print join "\n", ">$id", @seq, "\n";
	my $sequence = join "\n", @seq, "\n";  
	$sequence =~ s/\n//g;
        #print "$SeqID\tStart:$QStart\tLength:$Alen\tSStart:$SStart\tSEnd:$SEnd\tRatio:$Ratio\n";
          if ($Ratio < 1){
             #print ">$SeqID","_B$Bit","_","$ARGV[0]\n", substr($sequence, $QStart-1+$LenDiff, $Alen), "\n";
             print ">$SeqID","_B$Bit","_","$ARGV[0]\n", substr($sequence, $QStart-1, $AbsAlen), "\n";
          } elsif ($Ratio > 1) {
#             my $Seq = substr($sequence, $QStart-1, $Alen); 
             #my $Seq = substr($sequence, $QStart-1+$LenDiff, $Alen); 
             my $Seq = substr($sequence, $QStart-1, $AbsAlen); 
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






