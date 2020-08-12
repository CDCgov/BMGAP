#!/usr/bin/perl
use strict;
#use warnings;

my $input;
my $input2;
my $output;
my @array;
my @array2;
my $line;
my $line2;
my $Alen;
my $Qlen;
my $ASlen;
my $APer; 
my $ARnd;
my $head = "qseqid\tsseqid\tpident\tlength\tqle\tslen\tmismatch\tgapopen\tqstart\tqend\tsstart\tsend\tevalue\tbitscore\tnode\tlength\tcov\tpaln\n";

open $input, $ARGV[0];
#print $ARGV[1];
#print $head;
#@filename = split (/-/, $var1);
#$var1 = $filename[0];

foreach $line (<$input>){
    chomp $line;
    @array = split (" ", $line);   
  #if ($array[0] =~ m/^NODE/) {
  if ($array[0] ne "qseqid"){
#  if ($array[0] =~ m/^M/) {
	$Alen = $array[3];
        $Qlen = $array[4];
	$ASlen = $array[5];
	$APer = ($Alen/$ASlen)*100;
	$ARnd = sprintf("%.2f", $APer);        
	@array2 = split ("_", $array[0]); 
#	print "$line\t$array2[1]\t$array2[3]\t$array2[5]\t$ARnd\n";
	print "$line\t$array2[1]\t$Qlen\t$array2[5]\t$ARnd\n";
        }  
 
  elsif ($array[0] =~ m/^contigs/){
        print "No NODES!!!\n";
    }
}
