#!/usr/bin/perl
use strict;
#use warnings;


my $input;
my $output;
my @array;
my $line;
my $pa = 95;
#my $head = "Sequence_File\tInferred_SG\tBased_SG\tGrouping_Gene\tcsaA\tcsaB\tcsaC\tcsaD\tcsb\tcsc\tcseA\tcseB\tcseC\tcseD\tcseE\tcseF\tcseG\tcshC\tcshD\tcsiA\tcsiB\tcsiC\tcsiD\tcsiE\tcskC\tcslA\tcslB\tcslC\tcssA\tcssB\tcssC\tcssE\tcssF\tcsw\tcsxA\tcsxB\tcsxC\tcsy\tcszA\tcszB\tcszC\tcszD\tctrG\tgalE\ttex\tctrA\tctrB\tctrC\tctrD\tctrE\tctrF\trfbA\trfbB\trfbC\tsodC\t16S\tISO\n";
my $head = "Sequence_File\tBased_SG\tGrouping_Gene\tcsaA\tcsaB\tcsaC\tcsaD\tcsb\tcsc\tcseA\tcseB\tcseC\tcseD\tcseE\tcseF\tcseG\tcshC\tcshD\tcsiA\tcsiB\tcsiC\tcsiD\tcsiE\tcskC\tcslA\tcslB\tcslC\tcssA\tcssB\tcssC\tcssE\tcssF\tcsw\tcsxA\tcsxB\tcsxC\tcsy\tcszA\tcszB\tcszC\tcszD\tctrG\tgalE\ttex\tctrA\tctrB\tctrC\tctrD\tctrE\tctrF\trfbA\trfbB\trfbC\tsodC\t16S\tISO\n";
my $var1 = substr($ARGV[0], 0, -19);
local $" = "\t";

open $input, $ARGV[0];

#@filename = split (/-/, $var1);
#$var1 = $filename[0];

foreach $line (<$input>){
    chomp $line;
    @array = split ("\t", $line);   
##########AAAAAAAAAA
    if ($array[1] =~ m/^A/ && $array[72] > $pa && $array[73] > $pa && $array[74] > $pa && $array[75] > $pa && $array[80] > $pa && $array[81] > $pa && $array[82] > $pa && $array[83] > $pa && $array[84] > $pa && $array[85] > $pa ) {
	print "$array[0]\tA\tctrE,$array[80]\tctrF,$array[81]\tctrA,$array[82]\tctrB,$array[83]\tctrC,$array[84]\tctrD,$array[85]\trfbA,$array[86]\trfbB,$array[87]\trfbC,$array[88]\tgalE,$array[89]\ttex,$array[90]\tsodC,$array[91]\tNm16S,$array[92]\n";
    }
    elsif ($array[1] =~ m/^A/ ) {
	print "$array[0]\tNG\tctrE,$array[80]\tctrF,$array[81]\tctrA,$array[82]\tctrB,$array[83]\tctrC,$array[84]\tctrD,$array[85]\trfbA,$array[86]\trfbB,$array[87]\trfbC,$array[88]\tgalE,$array[89]\ttex,$array[90]\tsodC,$array[91]\tNm16S,$array[92]\n";
    }
##########BBBBBBBBBB    
    elsif ($array[1] =~ m/^B/ && $array[72] > $pa && $array[73] > $pa && $array[74] > $pa && $array[75] > $pa && $array[76] > $pa && $array[80] > $pa && $array[81] > $pa && $array[82] > $pa && $array[83] > $pa && $array[84] > $pa && $array[85] > $pa ) {
	print "$array[0]\tB\tctrE,$array[80]\tctrF,$array[81]\tctrA,$array[82]\tctrB,$array[83]\tctrC,$array[84]\tctrD,$array[85]\trfbA,$array[86]\trfbB,$array[87]\trfbC,$array[88]\tgalE,$array[89]\ttex,$array[90]\tsodC,$array[91]\tNm16S,$array[92]\n";
    }
    elsif ($array[1] =~ m/^B/ ) {
	print "$array[0]\tNG\tctrE,$array[80]\tctrF,$array[81]\tctrA,$array[82]\tctrB,$array[83]\tctrC,$array[84]\tctrD,$array[85]\trfbA,$array[86]\trfbB,$array[87]\trfbC,$array[88]\tgalE,$array[89]\ttex,$array[90]\tsodC,$array[91]\tNm16S,$array[92]\n";
    }
##########CCCCCCCCCC    
    elsif ($array[1] =~ m/^C/ && $array[72] > $pa && $array[73] > $pa && $array[74] > $pa && $array[75] > $pa && $array[77] > $pa && $array[80] > $pa && $array[81] > $pa && $array[82] > $pa && $array[83] > $pa && $array[84] > $pa && $array[85] > $pa ) {
	print "$array[0]\tC\tctrE,$array[80]\tctrF,$array[81]\tctrA,$array[82]\tctrB,$array[83]\tctrC,$array[84]\tctrD,$array[85]\trfbA,$array[86]\trfbB,$array[87]\trfbC,$array[88]\tgalE,$array[89]\ttex,$array[90]\tsodC,$array[91]\tNm16S,$array[92]\n";
    }
    elsif ($array[1] =~ m/^C/ ) {
	print "$array[0]\tNG\tctrE,$array[80]\tctrF,$array[81]\tctrA,$array[82]\tctrB,$array[83]\tctrC,$array[84]\tctrD,$array[85]\trfbA,$array[86]\trfbB,$array[87]\trfbC,$array[88]\tgalE,$array[89]\ttex,$array[90]\tsodC,$array[91]\tNm16S,$array[92]\n";
    }
##########EEEEEEEEEE    
    elsif ($array[1] =~ m/^E/ && $array[72] > $pa && $array[73] > $pa && $array[74] > $pa && $array[75] > $pa && $array[76] > $pa && $array[77] > $pa && $array[78] > $pa && $array[79] > $pa && $array[80] > $pa && $array[81] > $pa && $array[82] > $pa && $array[83] > $pa && $array[84] > $pa && $array[85] > $pa ) {
	print "$array[0]\tE\tctrE,$array[80]\tctrF,$array[81]\tctrA,$array[82]\tctrB,$array[83]\tctrC,$array[84]\tctrD,$array[85]\trfbA,$array[86]\trfbB,$array[87]\trfbC,$array[88]\tgalE,$array[89]\ttex,$array[90]\tsodC,$array[91]\tNm16S,$array[92]\n";
    }
    elsif ($array[1] =~ m/^E/ ) {
	print "$array[0]\tNG\tctrE,$array[80]\tctrF,$array[81]\tctrA,$array[82]\tctrB,$array[83]\tctrC,$array[84]\tctrD,$array[85]\trfbA,$array[86]\trfbB,$array[87]\trfbC,$array[88]\tgalE,$array[89]\ttex,$array[90]\tsodC,$array[91]\tNm16S,$array[92]\n";
    }
##########WWWWWWWWWW    
    elsif ($array[1] =~ m/^W/ && $array[72] > $pa && $array[73] > $pa && $array[74] > $pa && $array[75] > $pa && $array[77] > $pa && $array[80] > $pa && $array[81] > $pa && $array[82] > $pa && $array[83] > $pa && $array[84] > $pa && $array[85] > $pa ) {
	print "$array[0]\tW\tctrE,$array[80]\tctrF,$array[81]\tctrA,$array[82]\tctrB,$array[83]\tctrC,$array[84]\tctrD,$array[85]\trfbA,$array[86]\trfbB,$array[87]\trfbC,$array[88]\tgalE,$array[89]\ttex,$array[90]\tsodC,$array[91]\tNm16S,$array[92]\n";
    }
    elsif ($array[1] =~ m/^W/ ) {
	print "$array[0]\tNG\tctrE,$array[80]\tctrF,$array[81]\tctrA,$array[82]\tctrB,$array[83]\tctrC,$array[84]\tctrD,$array[85]\trfbA,$array[86]\trfbB,$array[87]\trfbC,$array[88]\tgalE,$array[89]\ttex,$array[90]\tsodC,$array[91]\tNm16S,$array[92]\n";
    }
##########YYYYYYYYYY    
    elsif ($array[1] =~ m/^Y/ && $array[72] > $pa && $array[73] > $pa && $array[74] > $pa && $array[75] > $pa && $array[77] > $pa && $array[80] > $pa && $array[81] > $pa && $array[82] > $pa && $array[83] > $pa && $array[84] > $pa && $array[85] > $pa ) {
	print "$array[0]\tY\tctrE,$array[80]\tctrF,$array[81]\tctrA,$array[82]\tctrB,$array[83]\tctrC,$array[84]\tctrD,$array[85]\trfbA,$array[86]\trfbB,$array[87]\trfbC,$array[88]\tgalE,$array[89]\ttex,$array[90]\tsodC,$array[91]\tNm16S,$array[92]\n";
    }
    elsif ($array[1] =~ m/^Y/ ) {
	print "$array[0]\tNG\tctrE,$array[80]\tctrF,$array[81]\tctrA,$array[82]\tctrB,$array[83]\tctrC,$array[84]\tctrD,$array[85]\trfbA,$array[86]\trfbB,$array[87]\trfbC,$array[88]\tgalE,$array[89]\ttex,$array[90]\tsodC,$array[91]\tNm16S,$array[92]\n";
    }
##########XXXXXXXXXX
    if ($array[1] =~ m/^X/ && $array[72] > $pa && $array[73] > $pa && $array[74] > $pa && $array[80] > $pa && $array[81] > $pa && $array[82] > $pa && $array[83] > $pa && $array[84] > $pa && $array[85] > $pa ) {
	print "$array[0]\tX\tctrE,$array[80]\tctrF,$array[81]\tctrA,$array[82]\tctrB,$array[83]\tctrC,$array[84]\tctrD,$array[85]\trfbA,$array[86]\trfbB,$array[87]\trfbC,$array[88]\tgalE,$array[89]\ttex,$array[90]\tsodC,$array[91]\tNm16S,$array[92]\n";
    }
    elsif ($array[1] =~ m/^X/ ) {
	print "$array[0]\tNG\tctrE,$array[80]\tctrF,$array[81]\tctrA,$array[82]\tctrB,$array[83]\tctrC,$array[84]\tctrD,$array[85]\trfbA,$array[86]\trfbB,$array[87]\trfbC,$array[88]\tgalE,$array[89]\ttex,$array[90]\tsodC,$array[91]\tNm16S,$array[92]\n";
    }
##########ZZZZZZZZZZ
    if ($array[1] =~ m/^Z/ && $array[72] > $pa && $array[73] > $pa && $array[74] > $pa && $array[75] > $pa && $array[80] > $pa && $array[81] > $pa && $array[82] > $pa && $array[83] > $pa && $array[84] > $pa && $array[85] > $pa ) {
	print "$array[0]\tZ\tctrE,$array[80]\tctrF,$array[81]\tctrA,$array[82]\tctrB,$array[83]\tctrC,$array[84]\tctrD,$array[85]\trfbA,$array[86]\trfbB,$array[87]\trfbC,$array[88]\tgalE,$array[89]\ttex,$array[90]\tsodC,$array[91]\tNm16S,$array[92]\n";
    }
    elsif ($array[1] =~ m/^Z/ ) {
	print "$array[0]\tNG\tctrE,$array[80]\tctrF,$array[81]\tctrA,$array[82]\tctrB,$array[83]\tctrC,$array[84]\tctrD,$array[85]\trfbA,$array[86]\trfbB,$array[87]\trfbC,$array[88]\tgalE,$array[89]\ttex,$array[90]\tsodC,$array[91]\tNm16S,$array[92]\n";
    }
##########NANANANANA
    if ($array[1] =~ m/^NA/ && $array[91] > $pa && $array[92] > $pa ) {
	print "$array[0]\tNG\t-\t-\t-\t-\t-\t-\t-\t-\t-\tgalE,$array[89]\ttex,$array[90]\tsodC,$array[91]\tNm16S,$array[92]\n";
    }
    elsif ($array[1] =~ m/^NA/ ) {
	print "$array[0]\tNA\t-\t-\t-\t-\t-\t-\t-\t-\t-\tgalE,$array[89]\ttex,$array[90]\tsodC,$array[91]\tNm16S,$array[92]\n";
    }
####################
}
