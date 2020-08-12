#!/usr/bin/perl
use strict;
#use warnings;


my $input;
my $input2;
my @data;
my @search;
my $line;
my $line2;
my @fields;
my @fields2;
my $list;

local $" = "\t";

#my $head = "Sequence_File\tInferred_SG\tBased_SG\tGrouping_Gene\tcsaA\tcsaB\tcsaC\tcsaD\tcsb\tcsc\tcseA\tcseB\tcseC\tcseD\tcseE\tcseF\tcseG\tcshC\tcshD\tcsiA\tcsiB\tcsiC\tcsiD\tcsiE\tcskC\tcslA\tcslB\tcslC\tcssA\tcssB\tcssC\tcssE\tcssF\tcsw\tcsxA\tcsxB\tcsxC\tcsy\tcszA\tcszB\tcszC\tcszD\tctrG\tgalE\ttex\tctrA\tctrB\tctrC\tctrD\tctrE\tctrF\trfbA\trfbB\trfbC\tsodC\t16S\tISO\n";
my $head = "Sequence_File\tInferred\tBased_SG\tSA\tPCR\tGrouping_Gene\tcsaA\tcsaB\tcsaC\tcsaD\tcsb\tcsc\tcseA\tcseB\tcseC\tcseD\tcseE\tcseF\tcseG\tcshC\tcshD\tcsiA\tcsiB\tcsiC\tcsiD\tcsiE\tcskC\tcslA\tcslB\tcslC\tcssA\tcssB\tcssC\tcssE\tcssF\tcsw\tcsxA\tcsxB\tcsxC\tcsy\tcszA\tcszB\tcszC\tcszD\tctrG\tgalE\ttex\tctrA\tctrB\tctrC\tctrD\tctrE\tctrF\trfbA\trfbB\trfbC\tsodC\t16S\tISO\n";

my $var1 = substr($ARGV[0], 0, 6); # get 1st six characters of argument

#open grouping file
$input = $ARGV[0];
chomp($input);
open (TABLE, $input);
@data = <TABLE>; 
close TABLE;

#open meta file
#my $input2 = "/scicomp/groups/OID/NCIRD-OD/OI/ncbs/projects/Meningitis/Nm/Meta.txt";
my $input2 = "/scicomp/groups/OID/NCIRD-OD/OI/ncbs/projects/Meningitis/by-instrument/Util/TypingTab/Meta.txt";
chomp($input2);
open (ANNOT, $input2);
my @search = <ANNOT>; 
close ANNOT;


foreach $line (@data){
    chomp $line;
    my @fields = split ("\t", $line);
#    if ($fields[0] =~ /^M/){
    if ($fields[0] ne "Sequence_File"){
    $list = "@fields[0..2]\t-\t-\t-\t@fields[3..90]\n";
   
    foreach $line2 (@search){
        if ($line2  =~ m/$var1/){
	my @fields2 = split (" ", $line2);
	$list = "@fields[0..2]\t$fields2[5]\t$fields2[6]\t$fields2[7]\t@fields[3..90]\n";
        }
    }
  }      
#print $head; 
print $list; 
}


