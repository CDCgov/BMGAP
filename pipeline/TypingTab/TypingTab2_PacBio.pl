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
my $CovMin = 0;
my $pid = 95;
my $paln = 95;
my $varISO = 0;
my $head = "Sequence_File\tInferred_SG\tBased_SG\tGrouping_Gene\tcsaA\tcsaB\tcsaC\tcsaD\tcsb\tcsc\tcseA\tcseB\tcseC\tcseD\tcseE\tcseF\tcseG\tcshC\tcshD\tcsiA\tcsiB\tcsiC\tcsiD\tcsiE\tcskC\tcslA\tcslB\tcslC\tcssA\tcssB\tcssC\tcssE\tcssF\tcsw\tcsxA\tcsxB\tcsxC\tcsy\tcszA\tcszB\tcszC\tcszD\tctrG\tgalE\ttex\tctrA\tctrB\tctrC\tctrD\tctrE\tctrF\trfbA\trfbB\trfbC\tsodC\t16S\tISO\n";
my $var1 = substr($ARGV[0], 0, -16);
my $varA = "no";
my $varB = "no";
my $varC = "no";
my $varE = "no";
my $varH = "no";
my $varI = "no";
my $varK = "no";
my $varL = "no";
my $varW = "no";
my $varX = "no";
my $varY = "no";
my $varZ = "no";
#################
my $var16S = "no";
#################
my $varNt = "ng";
my $sodC = "-";
my $sodC_id = "-";
my $rfbC = "-";
my $rfbC_id = "-";
my $rfbA = "-";
my $rfbA_id = "-";
my $rfbB = "-";
my $rfbB_id = "-";
my $galE = "-";
my $galE_id = "-";
my $ctrA = "-";
my $ctrA_id = "-";
my $ctrB = "-";
my $ctrB_id = "-";
my $ctrC = "-";
my $ctrC_id = "-";
my $ctrD = "-";
my $ctrD_id = "-";
my $tex = "-";
my $tex_id = "-";
my $galE2 = "-";
my $galE2_id = "-";
my $rfbB2 = "-";
my $rfbB2_id = "-";
my $rfbA2 = "-";
my $rfbA2_id = "-";
my $rfbC2 = "-";
my $rfbC2_id = "-";
my $ctrE = "-";
my $ctrE_id = "-";
my $ctrF = "-";
my $ctrF_id = "-";
my $s16S = "-";
my $s16S_id = "-";
#AAAAAAAAAAAAAA
my $csaD = "-";
my $csaC = "-";
my $csaB = "-";
my $csaA = "-";
my $csaD_id = "-";
my $csaC_id = "-";
my $csaB_id = "-";
my $csaA_id = "-";
#BBBBBBBBBBBBBB
my $ctrG = "-";
my $csb = "-";
my $cssC = "-";
my $cssB = "-";
my $cssA = "-";
my $ctrG_id = "-";
my $csb_id = "-";
my $cssC_id = "-";
my $cssB_id = "-";
my $cssA_id = "-";
#CCCCCCCCCCCCCC
my $cssE = "-";
my $csc = "-";
my $cssE_id = "-";
my $csc_id = "-";
#EEEEEEEEEEEEEE
my $cseG = "-";
my $cseF = "-";
my $cseE = "-";
my $cseD = "-";
my $cseC = "-";
my $cseB = "-";
my $cseA = "-";
my $cseG_id = "-";
my $cseF_id = "-";
my $cseE_id = "-";
my $cseD_id = "-";
my $cseC_id = "-";
my $cseB_id = "-";
my $cseA_id = "-";
#HHHHHHHHHHHHHH
my $cshD = "-";
my $cshC = "-";
my $cszB = "-";
my $cszA = "-";
my $cshD_id = "-";
my $cshC_id = "-";
my $cszB_id = "-";
my $cszA_id = "-";
#IIIIIIIIIIIIII
my $csiA = "-"; 
my $csiB = "-"; 
my $csiC = "-"; 
my $csiD = "-"; 
my $csiE = "-"; 
my $csiA_id = "-"; 
my $csiB_id = "-"; 
my $csiC_id = "-"; 
my $csiD_id = "-"; 
my $csiE_id = "-";
#KKKKKKKKKKKKKK
my $cskC = "-"; 
my $cskC_id = "-"; 
#LLLLLLLLLLLLLL
my $cslC = "-";
my $cslB = "-";
my $cslA = "-";
my $cslC_id = "-";
my $cslB_id = "-";
my $cslA_id = "-";
#WWWWWWWWWWWWWW
my $cssF = "-";
my $csw = "-";
my $cssF_id = "-";
my $csw_id = "-";
#XXXXXXXXXXXXXX
my $csxC = "-";
my $csxB = "-";
my $csxA = "-";
my $csxC_id = "-";
my $csxB_id = "-";
my $csxA_id = "-";
#YYYYYYYYYYYYYY
my $csy = "-";
my $csy_id = "-";
#ZZZZZZZZZZZZZZ
my $cszD = "-";
my $cszC = "-";
my $cszD_id = "-";
my $cszC_id = "-";
#BITSBITSBITS
my $ABit = 0;
my $BBit = 0;
my $CBit = 0;
my $EBit = 0;
my $varH = "no";
my $HBit = 0;
my $IBit = 0;
my $KBit = 0;
my $LBit = 0;
my $WBit = 0;
my $XBit = 0;
my $YBit = 0;
my $ZBit = 0;
my $var16SBit = 0;

#my @filename; 


open $input, $ARGV[0];

#@filename = split (/-/, $var1);
#$var1 = $filename[0];

foreach $line (<$input>){
    chomp $line;
    @array = split (" ", $line);   
    if ($array[1] =~ m/^A_csaB/ ) {
        $varA = "A";
	#$csaB = join ( ',', $array[2], $array[14]);
	$csaB = join ( ',', 'csaB', $array[14]);
	$ABit = $array[13];
    }
        elsif ($array[1] =~ m/^B_csb/ ) {
        $varB = "B";
	#$csb  = join ( ',', $array[2], $array[14]);
	$csb  = join ( ',', 'csb', $array[14]);
	$BBit = $array[13];
    }
        elsif ($array[1] =~ m/^C_csc/ ) {
        $varC = "C";
	#$csc = join ( ',', $array[2], $array[14]);
	$csc = join ( ',', 'csc', $array[14]);
	$CBit = $array[13];
    }
        elsif ($array[1] =~ m/^E_cseC/ ) {
        $varE = "E";
	#$cseC = join ( ',', $array[2], $array[14]);
	$cseC = join ( ',', 'cseC', $array[14]);
	$EBit = $array[13];
    }
        elsif ($array[1] =~ m/^H_cshC/ ) {
        $varH = "H";
	#$cshC = join ( ',', $array[2], $array[14]);
	$cshC = join ( ',', 'cshC', $array[14]);
	$HBit = $array[13];
    }
         elsif ($array[1] =~ m/^I_csiC/ ) {
        $varI = "I";
	#$csiC = join ( ',', $array[2], $array[14]);
	$csiC = join ( ',', 'csiC', $array[14]);
	$IBit = $array[13];
    }
        elsif ($array[1] =~ m/^K_cskC/ ) {
        $varK = "K";
	#$cskC = join ( ',', $array[2], $array[14]);
	$cskC = join ( ',', 'cskC', $array[14]);
	$KBit = $array[13];
    }
        elsif ($array[1] =~ m/^L_cslC/ ) {
        $varL = "L";
	#$cslC = join ( ',', $array[2], $array[14]);
	$cslC = join ( ',', 'cslC', $array[14]);
	$LBit = $array[13];
    }
       elsif ($array[1] =~ m/^W_csw/ ) {
        $varW = "W";
	#$csw = join ( ',', $array[2], $array[14]);
	$csw = join ( ',', 'csw', $array[14]);
	$WBit = $array[13];
    }
        elsif ($array[1] =~ m/^X_csxB/ ) {
        $varX = "X";
	#$csxB = join ( ',', $array[2], $array[14]);
	$csxB = join ( ',', 'csxB', $array[14]);
	$XBit = $array[13];
    }
        elsif ($array[1] =~ m/^Y_csy/ ) {
        $varY = "Y";
	#$csy = join ( ',', $array[2], $array[14]);
	$csy = join ( ',', 'csy', $array[14]);
	$YBit = $array[13];
    }
        elsif ($array[1] =~ m/^Z_cszD/ ) {
        $varZ = "Z";
	#$cszD = join ( ',', $array[2], $array[14]);
	$cszD = join ( ',', 'cszD', $array[14]);
	$ZBit = $array[13];
    }
}

open $input2, $ARGV[0];

foreach $line2 (<$input2>){
    chomp $line2;
    @array2 = split (" ", $line2);
    if ($array2[1] =~ m/^ctrA_/  ) {
	#$ctrA = join ( ',', $array2[2], $array2[14]);
	$ctrA = join ( ',', 'ctrA', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $ctrA_id = "+";
	}
#	    else {
#	    $ctrA_id = "-";
#	}
   }   
        elsif ($array2[1] =~ m/^ctrB_/ ) {
        #$ctrB = join ( ',', $array2[2], $array2[14]);
        $ctrB = join ( ',', 'ctrB', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $ctrB_id = "+";
	}
#	    else {
#	    $ctrB_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^ctrC_/ ) {
        #$ctrC = join ( ',', $array2[2], $array2[14]);
        $ctrC = join ( ',', 'ctrC', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $ctrC_id = "+";
	}
#	    else {
#	    $ctrC_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^ctrD_/ ) {
        #$ctrD = join ( ',', $array2[2], $array2[14]);
        $ctrD = join ( ',', 'ctrD', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $ctrD_id = "+";
	}
#	    else {
#	    $ctrD_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^ctrE_/ ) {
        #$ctrE = join ( ',', $array2[2], $array2[14]);
        $ctrE = join ( ',', 'ctrE', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $ctrE_id = "+";
	}
#	    else {
#	    $ctrE_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^ctrF_/ ) {
        #$ctrF = join ( ',', $array2[2], $array2[14]);
        $ctrF = join ( ',', 'ctrF', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $ctrF_id = "+";
	}
#	    else {
#	    $ctrF_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^galE/ ) {
        #$galE = join ( ',', $array2[2], $array2[14]);
        $galE = join ( ',', 'galE', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $galE_id = "+";
	}
#	    else {
#	    $galE_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^tex_/ ) {
        #$tex = join ( ',', $array2[2], $array2[14]);
        $tex = join ( ',', 'tex', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $tex_id = "+";
	}
#	    else {
#	    $tex_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^rfbC/ ) {
        #$rfbC = join ( ',', $array2[2], $array2[14]);
        $rfbC = join ( ',', 'rfbC', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $rfbC_id = "+";
	}
#	    else {
#	    $rfbC_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^rfbA_/ ) {
        #$rfbA = join ( ',', $array2[2], $array2[14]);
        $rfbA = join ( ',', 'rfbA', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $rfbA_id = "+";
	}
#	    else {
#	    $rfbA_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^rfbB_/ ) {
        #$rfbB = join ( ',', $array2[2], $array2[14]);
        $rfbB = join ( ',', 'rfbB', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $rfbB_id = "+";
	}
#	    else {
#	    $rfbB_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^sodC_/ ) {
        #$sodC = join ( ',', $array2[2], $array2[14]);
        $sodC = join ( ',', 'sodC', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $sodC_id = "+";
	}
#	    else {
#	    $sodC_id = "-";
#	}
   }
######AAAAAA
	elsif ($array2[1] =~ m/^A_csaA_/ ) {
        #$csaA = join ( ',', $array2[2], $array2[14]);
        $csaA = join ( ',', 'csaA', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $csaA_id = "+";
	}
#	    else {
#	    $csaA_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^A_csaC_/ ) {
        #$csaC = join ( ',', $array2[2], $array2[14]);
        $csaC = join ( ',', 'csaC', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $csaC_id = "+";
	}
#	    else {
#	    $csaC_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^A_csaD_/ ) {
        #$csaD = join ( ',', $array2[2], $array2[14]);
        $csaD = join ( ',', 'csaD', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $csaD_id = "+";
	}
#	    else {
#	    $csaD_id = "-";
#	}
   }
######BBBBBB
	elsif ($array2[1] =~ m/^BCWY_cssA_/ ) {
        #$cssA = join ( ',', $array2[2], $array2[14]);
        $cssA = join ( ',', 'cssA', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $cssA_id = "+";
	}
#	    else {
#	    $cssA_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^BCWY_cssB_/) {
        #$cssB = join ( ',', $array2[2], $array2[14]);
        $cssB = join ( ',', 'cssB', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $cssB_id = "+";
	}
#	    else {
#	    $cssB_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^BCWY_cssC_/ ) {
        #$cssC = join ( ',', $array2[2], $array2[14]);
        $cssC = join ( ',', 'cssC', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $cssC_id = "+";
	}
#	    else {
#	    $cssC_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^BCWY_ctrG_/ ) {
        #$ctrG = join ( ',', $array2[2], $array2[14]);
        $ctrG = join ( ',', 'ctrG', $array2[14]);
	#$ctrG_id = "+";
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $ctrG_id = "+";
	}
#	    else {
#	    $ctrG_id = "-";
#	}
   }
######CCCCCC
	elsif ($array2[1] =~ m/^C_cssE_/ ) {
        #$cssE = join ( ',', $array2[2], $array2[14]);
        $cssE = join ( ',', 'cssE', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $cssE_id = "+";
	}
#	    else {
#	    $cssE_id = "-";
#	}
   }
######EEEEEE
	elsif ($array2[1] =~ m/^E_cseA_/ ) {
        #$cseA = join ( ',', $array2[2], $array2[14]);
        $cseA = join ( ',', 'cseA', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $cseA_id = "+";
	}
#	    else {
#	    $cseA_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^E_cseB_/ ) {
        #$cseB = join ( ',', $array2[2], $array2[14]);
        $cseB = join ( ',', 'cseB', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $cseB_id = "+";
	}
#	    else {
#	    $cseB_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^E_cseD_/ ) {
        #$cseD = join ( ',', $array2[2], $array2[14]);
        $cseD = join ( ',', 'cseD', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $cseD_id = "+";
	}
#	    else {
#	    $cseD_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^E_cseE_/ ) {
        #$cseE = join ( ',', $array2[2], $array2[14]);
        $cseE = join ( ',', 'cseE', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $cseE_id = "+";
	}
#	    else {
#	    $cseE_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^E_cseF_/ ) {
        #$cseF = join ( ',', $array2[2], $array2[14]);
        $cseF = join ( ',', 'cseF', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $cseF_id = "+";
	}
#	    else {
#	    $cseF_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^E_cseG_/ ) {
        #$cseG = join ( ',', $array2[2], $array2[14]);
        $cseG = join ( ',', 'cseG', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $cseG_id = "+";
	}
#	    else {
#	    $cseG_id = "-";
#	}
   }
#####HHHHHH
	elsif ($array2[1] =~ m/^H_cshD_/ ) {
        #$cshD = join ( ',', $array2[2], $array2[14]);
        $cshD = join ( ',', 'cshD', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $cshD_id = "+";
	}
#	    else {
#	    $cshD_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^HZ_cszA_/ ) {
        #$cszA = join ( ',', $array2[2], $array2[14]);
        $cszA = join ( ',', 'cszA', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $cszA_id = "+";
	}
#	    else {
#	    $cszA_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^HZ_cszB_/ ) {
        #$cszB = join ( ',', $array2[2], $array2[14]);
        $cszB = join ( ',', 'cszB', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $cszB_id = "+";
	}
#	    else {
#	    $cszB_id = "-";
#	}
   }
#####IIIIII&KKKKKK
	elsif ($array2[1] =~ m/^IK_csiA_/ ) {
        #$csiA = join ( ',', $array2[2], $array2[14]);
        $csiA = join ( ',', 'csiA', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $csiA_id = "+";
	}
#	    else {
#	    $csiA_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^IK_csiB_/ ) {
        #$csiB = join ( ',', $array2[2], $array2[14]);
        $csiB = join ( ',', 'csiB', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $csiB_id = "+";
	}
#	    else {
#	    $csiB_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^IK_csiD_/ ) {
        #$csiD = join ( ',', $array2[2], $array2[14]);
        $csiD = join ( ',', 'csiD', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $csiD_id = "+";
	}
#	    else {
#	    $csiD_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^IK_csiE_/ ) {
        #$csiE = join ( ',', $array2[2], $array2[14]);
        $csiE = join ( ',', 'csiE', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $csiE_id = "+";
	}
#	    else {
#	    $csiE_id = "-";
#	}
   }
#####LLLLLL
	elsif ($array2[1] =~ m/^L_cslA_/ ) {
        #$cslA = join ( ',', $array2[2], $array2[14]);
        $cslA = join ( ',', 'cslA', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $cslA_id = "+";
	}
#	    else {
#	    $cslA_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^L_cslB_/ ) {
        #$cslB = join ( ',', $array2[2], $array2[14]);
        $cslB = join ( ',', 'cslB', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $cslB_id = "+";
	}
#	    else {
#	    $cslB_id = "-";
#	}
   }
#####WWWWWW
	elsif ($array2[1] =~ m/^WY_cssF_/ ) {
        #$cssF = join ( ',', $array2[2], $array2[14]);
        $cssF = join ( ',', 'cssF', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $cssF_id = "+";
	}
#	    else {
#	    $cssF_id = "-";
#	}
   }
#####XXXXXX
	elsif ($array2[1] =~ m/^X_csxA_/ ) {
        #$csxA = join ( ',', $array2[2], $array2[14]);
        $csxA = join ( ',', 'csxA', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $csxA_id = "+";
	}
#	    else {
#	    $csxA_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^X_csxC_/ ) {
        #$csxC = join ( ',', $array2[2], $array2[14]);
        $csxC = join ( ',', 'csxC', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $csxC_id = "+";
	}
#	    else {
#	    $csxC_id = "-";
#	}
   }
#####YYYYYY
#####ZZZZZZ
	elsif ($array2[1] =~ m/^Z_cszC_/ ) {
        #$cszC = join ( ',', $array2[2], $array2[14]);
        $cszC = join ( ',', 'cszC', $array2[14]);
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $cszC_id = "+";
	}
#	    else {
#	    $cszC_id = "-";
#	}
   }
#####16S16S
        elsif ($array2[1] =~ m/^16S_rDNA_/ ) {
        $var16S = "16S";
	#$s16S = join ( ',', $array2[2], $array2[14]);
	$s16S = join ( ',', 's16S', $array2[14]);
	    $var16SBit = $array2[13];
	    if ($array2[2] > $pid && $array[14] > $paln) {
	    $s16S_id = "+";
	}
#	    else {
#	    $s16S_id = "-";
#	}
    }
#####IS1301
        elsif ($array2[1] =~ m/^IS1301/) {
        $varISO = $varISO + 1; 
    }
}

#####################################################ctrctrctrctrctrctrctrctrctrctrctrctrctrctrctrctrctrctrctr
#if ($ctrA eq "-" || $ctrB eq "-" || $ctrC eq "-" || $ctrD eq "-" || $ctrE eq "-" || $ctrF eq "-") {
#    print $head; 
#    print "$var1\t$varNt\tctr-\tNm?\t-\t-\t-\t-\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\n";

#####################################################
#} 
if ($varA eq "no" && $varB eq "no" && $varC eq "no" && $varE eq "no" && $varH eq "no" && $varI eq "no" && $varK eq "no" && $varL eq "no" && $varW eq "no" && $varX eq "no" && $varY eq "no" && $varZ eq "no") {
    #print $head;
    print "$var1 has low coverage or no Nm typable genes exist in sample.\n";
    print "Can't infer serotype!"; 
    #print "$var1\t$varNt\t-\t-\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\n";

#####################################################AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
} elsif ($varA eq "A" && $ABit > $BBit && $ABit > $CBit && $ABit > $EBit && $ABit > $HBit && $ABit > $IBit && $ABit > $KBit && $ABit > $LBit && $ABit > $WBit && $ABit > $XBit && $ABit > $YBit && $ABit > $ZBit & $csaA_id eq "+" & $csaB_id eq "+" & $csaD_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
    print $head;
    print "$var1\t$varA\t$varA\tcsaB\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varA eq "A" && $ABit > $BBit && $ABit > $CBit && $ABit > $EBit && $ABit > $HBit && $ABit > $IBit && $ABit > $KBit && $ABit > $LBit && $ABit > $WBit && $ABit > $XBit && $ABit > $YBit && $ABit > $ZBit && ($csaA_id eq "-" || $csaB_id eq "-" || $csaD_id eq "-" || $ctrA_id eq "-" || $ctrB_id eq "-" || $ctrC_id eq "-" || $ctrD_id eq "-" || $ctrE_id eq "-" || $ctrF_id eq "-" )) {
} elsif ($varA eq "A" && $ABit > $BBit && $ABit > $CBit && $ABit > $EBit && $ABit > $HBit && $ABit > $IBit && $ABit > $KBit && $ABit > $LBit && $ABit > $WBit && $ABit > $XBit && $ABit > $YBit && $ABit > $ZBit ) {
    print $head;
    print "$var1\tNT\t$varA\tcsaB\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
} elsif ($varB eq "B" && $BBit > $ABit && $BBit > $CBit && $BBit > $EBit && $BBit > $HBit && $BBit > $IBit && $BBit > $KBit && $BBit > $LBit && $BBit > $WBit && $BBit > $XBit && $BBit > $YBit && $BBit > $ZBit & $cssA eq "+" & $cssB eq "+" & $cssC eq "+" & $ctrG eq "+" & $ctrA eq "+" & $ctrB eq "+" & $ctrC eq "+" & $ctrD eq "+" & $ctrE eq "+" & $ctrF eq "+" ) {
    print $head;
    print "$var1\t$varB\t$varB\tcsb\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varB eq "B" && $BBit > $ABit && $BBit > $CBit && $BBit > $EBit && $BBit > $HBit && $BBit > $IBit && $BBit > $KBit && $BBit > $LBit && $BBit > $WBit && $BBit > $XBit && $BBit > $YBit && $BBit > $ZBit && ($cssA eq "-" || $cssB eq "-" || $cssC eq "-" || $ctrG eq "-" || $ctrA eq "-" || $ctrB eq "-" || $ctrC eq "-" || $ctrD eq "-" || $ctrE eq "-" || $ctrF eq "-" )) {
} elsif ($varB eq "B" && $BBit > $ABit && $BBit > $CBit && $BBit > $EBit && $BBit > $HBit && $BBit > $IBit && $BBit > $KBit && $BBit > $LBit && $BBit > $WBit && $BBit > $XBit && $BBit > $YBit && $BBit > $ZBit ) {
    print $head;
    print "$var1\tNT\t$varB\tcsb\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
} elsif ($varC eq "C" && $CBit > $ABit && $CBit > $BBit && $CBit > $EBit && $CBit > $HBit && $CBit > $IBit && $CBit > $KBit && $CBit > $LBit && $CBit > $WBit && $CBit > $XBit && $CBit > $YBit && $CBit > $ZBit & $cssA eq "+" & $cssB eq "+" & $cssC eq "+" & $cssE eq "+" & $ctrG eq "+" & $ctrA eq "+" & $ctrB eq "+" & $ctrC eq "+" & $ctrD eq "+" & $ctrE eq "+" & $ctrF eq "+" ) {
    print $head;
    print "$var1\t$varC\t$varC\tcsc\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varC eq "C" && $CBit > $ABit && $CBit > $BBit && $CBit > $EBit && $CBit > $HBit && $CBit > $IBit && $CBit > $KBit && $CBit > $LBit && $CBit > $WBit && $CBit > $XBit && $CBit > $YBit && $CBit > $ZBit && ($cssA eq "-" || $cssB eq "-" || $cssC eq "-" || $cssE eq "-" || $ctrG eq "-" || $ctrA eq "-" || $ctrB eq "-" || $ctrC eq "-" || $ctrD eq "-" || $ctrE eq "-" || $ctrF eq "-" )) {
} elsif ($varC eq "C" && $CBit > $ABit && $CBit > $BBit && $CBit > $EBit && $CBit > $HBit && $CBit > $IBit && $CBit > $KBit && $CBit > $LBit && $CBit > $WBit && $CBit > $XBit && $CBit > $YBit && $CBit > $ZBit ) {
    print $head;
    print "$var1\tNT\t$varC\tcsc\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
} elsif ($varE eq "E" && $EBit > $ABit && $EBit > $BBit && $EBit > $CBit && $EBit > $HBit && $EBit > $IBit && $EBit > $KBit && $EBit > $LBit && $EBit > $WBit && $EBit > $XBit && $EBit > $YBit && $EBit > $ZBit & $cseA eq "+" & $cseB eq "+" & $cseD eq "+" & $cseE eq "+" & $cseF eq "+" & $cseG eq "+" & $ctrA eq "+" & $ctrB eq "+" & $ctrC eq "+" & $ctrD eq "+" & $ctrE eq "+" & $ctrF eq "+" ) {
    print $head;
    print "$var1\t$varE\t$varE\tcseC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varE eq "E" && $EBit > $ABit && $EBit > $BBit && $EBit > $CBit && $EBit > $HBit && $EBit > $IBit && $EBit > $KBit && $EBit > $LBit && $EBit > $WBit && $EBit > $XBit && $EBit > $YBit && $EBit > $ZBit && ($cseA eq "-" || $cseB eq "-" || $cseD eq "-" || $cseE eq "-" || $cseF eq "-" || $cseG eq "-" || $ctrA eq "-" || $ctrB eq "-" || $ctrC eq "-" || $ctrD eq "-" || $ctrE eq "-" || $ctrF eq "-" )) {
} elsif ($varE eq "E" && $EBit > $ABit && $EBit > $BBit && $EBit > $CBit && $EBit > $HBit && $EBit > $IBit && $EBit > $KBit && $EBit > $LBit && $EBit > $WBit && $EBit > $XBit && $EBit > $YBit && $EBit > $ZBit ) {
    print $head;
    print "$var1\tNT\t$varE\tcseC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
} elsif ($varH eq "H" && $HBit > $ABit && $HBit > $BBit && $HBit > $CBit && $HBit > $EBit && $HBit > $IBit && $HBit > $KBit && $HBit > $LBit && $HBit > $WBit && $HBit > $XBit && $HBit > $YBit && $HBit > $ZBit & $cszA eq "+" & $cszB eq "+" & $cshD eq "+" & $ctrA eq "+" & $ctrB eq "+" & $ctrC eq "+" & $ctrD eq "+" & $ctrE eq "+" & $ctrF eq "+" ) {
    print $head;
    print "$var1\t$varH\t$varH\tcshC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varH eq "H" && $HBit > $ABit && $HBit > $BBit && $HBit > $CBit && $HBit > $EBit && $HBit > $IBit && $HBit > $KBit && $HBit > $LBit && $HBit > $WBit && $HBit > $XBit && $HBit > $YBit && $HBit > $ZBit && ($cszA eq "-" || $cszB eq "-" || $cshD eq "-" || $ctrA eq "-" || $ctrB eq "-" || $ctrC eq "-" || $ctrD eq "-" || $ctrE eq "-" || $ctrF eq "-" )) {
} elsif ($varH eq "H" && $HBit > $ABit && $HBit > $BBit && $HBit > $CBit && $HBit > $EBit && $HBit > $IBit && $HBit > $KBit && $HBit > $LBit && $HBit > $WBit && $HBit > $XBit && $HBit > $YBit && $HBit > $ZBit ) {
    print $head;
    print "$var1\tNT\t$varH\tcshC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
} elsif ($varI eq "I" && $IBit > $ABit && $IBit > $BBit && $IBit > $CBit && $IBit > $EBit && $IBit > $HBit && $IBit > $KBit && $IBit > $LBit && $IBit > $WBit && $IBit > $XBit && $IBit > $YBit && $IBit > $ZBit & $csiA eq "+" & $csiB eq "+" & $csiD eq "+" & $csiE eq "+" & $ctrA eq "+" & $ctrB eq "+" & $ctrC eq "+" & $ctrD eq "+" & $ctrE eq "+" & $ctrF eq "+" ) {
    print $head;
    print "$var1\t$varI\t$varI\tcsiC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varI eq "I" && $IBit > $ABit && $IBit > $BBit && $IBit > $CBit && $IBit > $EBit && $IBit > $HBit && $IBit > $KBit && $IBit > $LBit && $IBit > $WBit && $IBit > $XBit && $IBit > $YBit && $IBit > $ZBit && ($csiA eq "-" || $csiB eq "-" || $csiD eq "-" || $csiE eq "-" || $ctrA eq "-" || $ctrB eq "-" || $ctrC eq "-" || $ctrD eq "-" || $ctrE eq "-" || $ctrF eq "-" )) {
} elsif ($varI eq "I" && $IBit > $ABit && $IBit > $BBit && $IBit > $CBit && $IBit > $EBit && $IBit > $HBit && $IBit > $KBit && $IBit > $LBit && $IBit > $WBit && $IBit > $XBit && $IBit > $YBit && $IBit > $ZBit ) {
    print $head;
    print "$var1\tNT\t$varI\tcsiC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK
} elsif ($varK eq "K" && $KBit > $ABit && $KBit > $BBit && $KBit > $CBit && $KBit > $EBit && $KBit > $HBit && $KBit > $IBit && $KBit > $LBit && $KBit > $WBit && $KBit > $XBit && $KBit > $YBit && $KBit > $ZBit & $csiA eq "+" & $csiB eq "+" & $csiD eq "+" & $csiE eq "+" & $ctrA eq "+" & $ctrB eq "+" & $ctrC eq "+" & $ctrD eq "+" & $ctrE eq "+" & $ctrF eq "+" ) {
    print $head;
    print "$var1\t$varK\t$varK\tcskC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varK eq "K" && $KBit > $ABit && $KBit > $BBit && $KBit > $CBit && $KBit > $EBit && $KBit > $HBit && $KBit > $IBit && $KBit > $LBit && $KBit > $WBit && $KBit > $XBit && $KBit > $YBit && $KBit > $ZBit && ($csiA eq "-" || $csiB eq "-" || $csiD eq "-" || $csiE eq "-" )) {
} elsif ($varK eq "K" && $KBit > $ABit && $KBit > $BBit && $KBit > $CBit && $KBit > $EBit && $KBit > $HBit && $KBit > $IBit && $KBit > $LBit && $KBit > $WBit && $KBit > $XBit && $KBit > $YBit && $KBit > $ZBit ) {
    print $head;
    print "$var1\tNT\t$varK\tcskC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL
} elsif ($varL eq "L" && $LBit > $ABit && $LBit > $BBit && $LBit > $CBit && $LBit > $EBit && $LBit > $HBit && $LBit > $IBit && $LBit > $KBit && $LBit > $WBit && $LBit > $XBit && $LBit > $YBit && $LBit > $ZBit & $cslA eq "+" & $cslB eq "+" & $ctrA eq "+" & $ctrB eq "+" & $ctrC eq "+" & $ctrD eq "+" & $ctrE eq "+" & $ctrF eq "+" ) {
    print $head;
    print "$var1\t$varL\t$varL\tcslC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varL eq "L" && $LBit > $ABit && $LBit > $BBit && $LBit > $CBit && $LBit > $EBit && $LBit > $HBit && $LBit > $IBit && $LBit > $KBit && $LBit > $WBit && $LBit > $XBit && $LBit > $YBit && $LBit > $ZBit && ($cslA eq "-" || $cslB eq "-" )) {
} elsif ($varL eq "L" && $LBit > $ABit && $LBit > $BBit && $LBit > $CBit && $LBit > $EBit && $LBit > $HBit && $LBit > $IBit && $LBit > $KBit && $LBit > $WBit && $LBit > $XBit && $LBit > $YBit && $LBit > $ZBit ) {
    print $head;
    print "$var1\tNT\t$varL\tcslC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
} elsif ($varW eq "W" && $WBit > $ABit && $WBit > $BBit && $WBit > $CBit && $WBit > $EBit && $WBit > $HBit && $WBit > $IBit && $WBit > $KBit && $WBit > $LBit && $WBit > $XBit && $WBit > $YBit && $WBit > $ZBit & $cssA_id eq "+" & $cssB_id eq "+" & $cssC_id eq "+" & $cssF_id eq "+" & $ctrG_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
    print $head;
    print "$var1\t$varW\t$varW\tcsw\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varW eq "W" && $WBit > $ABit && $WBit > $BBit && $WBit > $CBit && $WBit > $EBit && $WBit > $HBit && $WBit > $IBit && $WBit > $KBit && $WBit > $LBit && $WBit > $XBit && $WBit > $YBit && $WBit > $ZBit && ($cssA_id eq "-" || $cssB_id eq "-" || $cssC_id eq "-" || $cssF_id eq "-" || $ctrG_id eq "-" )) {
} elsif ($varW eq "W" && $WBit > $ABit && $WBit > $BBit && $WBit > $CBit && $WBit > $EBit && $WBit > $HBit && $WBit > $IBit && $WBit > $KBit && $WBit > $LBit && $WBit > $XBit && $WBit > $YBit && $WBit > $ZBit ) {
    print $head;
    print "$var1\tNT\t$varW\tcsw\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
} elsif ($varX eq "X" && $XBit > $ABit && $XBit > $BBit && $XBit > $CBit && $XBit > $EBit && $XBit > $HBit && $XBit > $IBit && $XBit > $KBit && $XBit > $LBit && $XBit > $WBit && $XBit > $YBit && $XBit > $ZBit & $csxA eq "+" & $csxC eq "+" & $ctrA eq "+" & $ctrB eq "+" & $ctrC eq "+" & $ctrD eq "+" & $ctrE eq "+" & $ctrF eq "+" ) {
    print $head;
    print "$var1\t$varX\t$varX\tcsxB\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varX eq "X" && $XBit > $ABit && $XBit > $BBit && $XBit > $CBit && $XBit > $EBit && $XBit > $HBit && $XBit > $IBit && $XBit > $KBit && $XBit > $LBit && $XBit > $WBit && $XBit > $YBit && $XBit > $ZBit && ($csxA eq "-" || $csxC eq "-" )) {
} elsif ($varX eq "X" && $XBit > $ABit && $XBit > $BBit && $XBit > $CBit && $XBit > $EBit && $XBit > $HBit && $XBit > $IBit && $XBit > $KBit && $XBit > $LBit && $XBit > $WBit && $XBit > $YBit && $XBit > $ZBit ) {
    print $head;
    print "$var1\tNT\t$varX\tcsxB\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
} elsif ($varY eq "Y" && $YBit > $ABit && $YBit > $BBit && $YBit > $CBit && $YBit > $EBit && $YBit > $HBit && $YBit > $IBit && $YBit > $KBit && $YBit > $LBit && $YBit > $WBit && $YBit > $XBit && $YBit > $ZBit & $cssA_id eq "+" & $cssB_id eq "+" & $cssC_id eq "+" & $cssF_id eq "+" & $ctrG_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
    print $head;
    print "$var1\t$varY\t$varY\tcsy\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varY eq "Y" && $YBit > $ABit && $YBit > $BBit && $YBit > $CBit && $YBit > $EBit && $YBit > $HBit && $YBit > $IBit && $YBit > $KBit && $YBit > $LBit && $YBit > $WBit && $YBit > $XBit && $YBit > $ZBit && ($cssA_id eq "-" || $cssB_id eq "-" || $cssC_id eq "-" || $cssF_id eq "-" || $ctrG_id eq "-" )) {
} elsif ($varY eq "Y" && $YBit > $ABit && $YBit > $BBit && $YBit > $CBit && $YBit > $EBit && $YBit > $HBit && $YBit > $IBit && $YBit > $KBit && $YBit > $LBit && $YBit > $WBit && $YBit > $XBit && $YBit > $ZBit ) {
    print $head;
    print "$var1\tNT\t$varY\tcsy\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ
} elsif ($varZ eq "Z" && $ZBit > $ABit && $ZBit > $BBit && $ZBit > $CBit && $ZBit > $EBit && $ZBit > $HBit && $ZBit > $IBit && $ZBit > $KBit && $ZBit > $LBit && $ZBit > $WBit && $ZBit > $XBit && $ZBit > $YBit & $cszA eq "+" & $cszB eq "+" & $cszC eq "+" & $ctrA eq "+" & $ctrB eq "+" & $ctrC eq "+" & $ctrD eq "+" & $ctrE eq "+" & $ctrF eq "+" ) {
    print $head;
    print "$var1\t$varZ\t$varZ\tcszD\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varZ eq "Z" && $ZBit > $ABit && $ZBit > $BBit && $ZBit > $CBit && $ZBit > $EBit && $ZBit > $HBit && $ZBit > $IBit && $ZBit > $KBit && $ZBit > $LBit && $ZBit > $WBit && $ZBit > $XBit && $ZBit > $YBit && ($cszA eq "-" || $cszB eq "-" || $cszC eq "-" )) {
} elsif ($varZ eq "Z" && $ZBit > $ABit && $ZBit > $BBit && $ZBit > $CBit && $ZBit > $EBit && $ZBit > $HBit && $ZBit > $IBit && $ZBit > $KBit && $ZBit > $LBit && $ZBit > $WBit && $ZBit > $XBit && $ZBit > $YBit ) {
    print $head;
    print "$var1\tNT\t$varZ\tcszD\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################????????????????????????????????????????????????????????????
} else {
    print $head;
    #print "Low Coverage! Can't infer serotype!";
    print "$var1\t$varNt\tTESTNm?\tNm?\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

}
