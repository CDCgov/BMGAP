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
        print "$array[0]\tA\t@array[4..6]\tcsaA,$array[72]\tcsaB,$array[73]\tcsaC,$array[74]\tcsaD,$array[75]\t\t\t\tComplete_capsule\n";
    }
    elsif ($array[1] =~ m/^A/ ) {
        print "$array[0]\tNG\t@array[4..6]\tcsaA,$array[72]\tcsaB,$array[73]\tcsaC,$array[74]\tcsaD,$array[75]\t\t\t\tPartial_or_Missing_essential_gene\n";
    }
##########BBBBBBBBBB    
    elsif ($array[1] =~ m/^B/ && $array[72] > $pa && $array[73] > $pa && $array[74] > $pa && $array[75] > $pa && $array[76] > $pa && $array[80] > $pa && $array[81] > $pa && $array[82] > $pa && $array[83] > $pa && $array[84] > $pa && $array[85] > $pa ) {
        print "$array[0]\tB\t@array[4..6]\tcssA,$array[72]\tcssB,$array[73]\tcssC,$array[74]\tcsb,$array[75]\tctrG,$array[76]\t\t\tComplete_capsule\n";
    }
    elsif ($array[1] =~ m/^B/ ) {
        print "$array[0]\tNG\t@array[4..6]\tcssA,$array[72]\tcssB,$array[73]\tcssC,$array[74]\tcsb,$array[75]\tctrG,$array[76]\t\t\tPartial_or_Missing_essential_gene\n";
    }
##########CCCCCCCCCC    
    elsif ($array[1] =~ m/^C/ && $array[72] > $pa && $array[73] > $pa && $array[74] > $pa && $array[75] > $pa && $array[77] > $pa && $array[80] > $pa && $array[81] > $pa && $array[82] > $pa && $array[83] > $pa && $array[84] > $pa && $array[85] > $pa ) {
        print "$array[0]\tC\t@array[4..6]\tcssA,$array[72]\tcssB,$array[73]\tcssC,$array[74]\tcsc,$array[75]\tcssE,$array[76]\tctrG,$array[77]\t\tComplete_capsule\n";
    }
    elsif ($array[1] =~ m/^C/ ) {
        print "$array[0]\tNG\t@array[4..6]\tcssA,$array[72]\tcssB,$array[73]\tcssC,$array[74]\tcsc,$array[75]\tcssE,$array[76]\tctrG,$array[77]\t\tPartial_or_Missing_essential_gene\n";
    }
##########EEEEEEEEEE    
    elsif ($array[1] =~ m/^E/ && $array[72] > $pa && $array[73] > $pa && $array[74] > $pa && $array[75] > $pa && $array[76] > $pa && $array[77] > $pa && $array[78] > $pa && $array[79] > $pa && $array[80] > $pa && $array[81] > $pa && $array[82] > $pa && $array[83] > $pa && $array[84] > $pa && $array[85] > $pa ) {
        print "$array[0]\tE\t@array[4..6]\tcseA,$array[72]\tcseB,$array[73]\tcseC,$array[74]\tcseD,$array[75]\tcseE,$array[76]\tcseF,$array[77]\tcseG,$array[78]\tComplete_capsule\n";
    }
    elsif ($array[1] =~ m/^E/ ) {
        print "$array[0]\tNG\t@array[4..6]\tcseA,$array[72]\tcseB,$array[73]\tcseC,$array[74]\tcseD,$array[75]\tcseE,$array[76]\tcseF,$array[77]\tcseG,$array[78]\tPartial_or_Missing_essential_gene\n";
    }
##########WWWWWWWWWW    
    elsif ($array[1] =~ m/^W/ && $array[72] > $pa && $array[73] > $pa && $array[74] > $pa && $array[75] > $pa && $array[77] > $pa && $array[80] > $pa && $array[81] > $pa && $array[82] > $pa && $array[83] > $pa && $array[84] > $pa && $array[85] > $pa ) {
        print "$array[0]\tW\t@array[4..6]\tcssA,$array[72]\tcssB,$array[73]\tcssC,$array[74]\tcsw,$array[75]\tcssF,$array[76]\tctrG,$array[77]\t\tComplete_capsule\n";
    }
    elsif ($array[1] =~ m/^W/ ) {
        print "$array[0]\tNG\t@array[4..6]\tcssA,$array[72]\tcssB,$array[73]\tcssC,$array[74]\tcsw,$array[75]\tcssF,$array[76]\tctrG,$array[77]\t\tPartial_or_Missing_essential_gene\n";
    }
##########YYYYYYYYYY    
    elsif ($array[1] =~ m/^Y/ && $array[72] > $pa && $array[73] > $pa && $array[74] > $pa && $array[75] > $pa && $array[77] > $pa && $array[80] > $pa && $array[81] > $pa && $array[82] > $pa && $array[83] > $pa && $array[84] > $pa && $array[85] > $pa ) {
        print "$array[0]\tY\t@array[4..6]\tcssA,$array[72]\tcssB,$array[73]\tcssC,$array[74]\tcsy,$array[75]\tcssF,$array[76]\tctrG,$array[77]\t\tComplete_capsule\n";
    }
    elsif ($array[1] =~ m/^Y/ ) {
        print "$array[0]\tNG\t@array[4..6]\tcssA,$array[72]\tcssB,$array[73]\tcssC,$array[74]\tcsy,$array[75]\tcssF,$array[76]\tctrG,$array[77]\t\tPartial_or_Missing_essential_gene\n";
    }
##########XXXXXXXXXX
    if ($array[1] =~ m/^X/ && $array[72] > $pa && $array[73] > $pa && $array[74] > $pa && $array[80] > $pa && $array[81] > $pa && $array[82] > $pa && $array[83] > $pa && $array[84] > $pa && $array[85] > $pa ) {
        print "$array[0]\tX\t@array[4..6]\tcsxA,$array[72]\tcsxB,$array[73]\tcsxC,$array[74]\t\t\t\t\tComplete_capsule\n";
    }
    elsif ($array[1] =~ m/^X/ ) {
        print "$array[0]\tNG\t@array[4..6]\tcsxA,$array[72]\tcsxB,$array[73]\tcsxC,$array[74]\t\t\t\t\tPartial_or_Missing_essential_gene\n";
    }
##########ZZZZZZZZZZ
    if ($array[1] =~ m/^Z/ && $array[72] > $pa && $array[73] > $pa && $array[74] > $pa && $array[75] > $pa && $array[80] > $pa && $array[81] > $pa && $array[82] > $pa && $array[83] > $pa && $array[84] > $pa && $array[85] > $pa ) {
        print "$array[0]\tZ\t@array[4..6]\tcszA,$array[72]\tcszB,$array[73]\tcszC,$array[74]\tcszD,$array[75]\t\t\t\tComplete_capsule\n";
    }
    elsif ($array[1] =~ m/^Z/ ) {
        print "$array[0]\tNG\t@array[4..6]\tcszA,$array[72]\tcszB,$array[73]\tcszC,$array[74]\tcszD,$array[75]\t\t\t\tPartial_or_Missing_essential_gene\n";
    }
##########NANANANANA
    if ($array[1] =~ m/^NA/ && $array[91] > $pa && $array[92] > $pa ) {
        print "$array[0]\tNG\t@array[4..6]\t-\t-\t-\t-\t-\t-\t-\tNG_Nm\n";
    }
    elsif ($array[1] =~ m/^NA/ ) {
	print "$array[0]\tNA\t@array[4..6]\t-\t-\t-\t-\t-\t-\t-\tNot_Nm\n";
    }
####################
}

