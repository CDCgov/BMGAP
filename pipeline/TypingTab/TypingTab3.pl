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
my $CovMin = 1;
my $pid = 95;
my $paln = 95;
my $varISO = 0;
#my $head = "Sequence_File\tInferred_SG\tBased_SG\tGrouping_Gene\tcsaA\tcsaB\tcsaC\tcsaD\tcsb\tcsc\tcseA\tcseB\tcseC\tcseD\tcseE\tcseF\tcseG\tcshC\tcshD\tcsiA\tcsiB\tcsiC\tcsiD\tcsiE\tcskC\tcslA\tcslB\tcslC\tcssA\tcssB\tcssC\tcssE\tcssF\tcsw\tcsxA\tcsxB\tcsxC\tcsy\tcszA\tcszB\tcszC\tcszD\tctrG\tgalE\ttex\tctrA\tctrB\tctrC\tctrD\tctrE\tctrF\trfbA\trfbB\trfbC\tsodC\t16S\tISO\n";
my $head = "Sequence_File\tBased_SG\tGrouping_Gene\tcsaA\tcsaB\tcsaC\tcsaD\tcsb\tcsc\tcseA\tcseB\tcseC\tcseD\tcseE\tcseF\tcseG\tcshC\tcshD\tcsiA\tcsiB\tcsiC\tcsiD\tcsiE\tcskC\tcslA\tcslB\tcslC\tcssA\tcssB\tcssC\tcssE\tcssF\tcsw\tcsxA\tcsxB\tcsxC\tcsy\tcszA\tcszB\tcszC\tcszD\tctrG\tgalE\ttex\tctrA\tctrB\tctrC\tctrD\tctrE\tctrF\trfbA\trfbB\trfbC\tsodC\t16S\tISO\n";

my $var1 = substr($ARGV[0], 0, -19);
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
    if ($array[1] =~ m/^A_csaB/ && $array[16] > $CovMin) {
        $varA = "A";
	#$csaB = join ( ',', $array[2], $array[17]);
	$csaB = join ( ',', 'csaB', $array[17]);
	$ABit = $array[13];
    }
        elsif ($array[1] =~ m/^B_csb/ && $array[16] > $CovMin) {
        $varB = "B";
	#$csb  = join ( ',', $array[2], $array[17]);
	$csb  = join ( ',', 'csb', $array[17]);
	$BBit = $array[13];
    }
        elsif ($array[1] =~ m/^C_csc/ && $array[16] > $CovMin) {
        $varC = "C";
	#$csc = join ( ',', $array[2], $array[17]);
	$csc = join ( ',', 'csc', $array[17]);
	$CBit = $array[13];
    }
        elsif ($array[1] =~ m/^E_cseC/ && $array[16] > $CovMin) {
        $varE = "E";
	#$cseC = join ( ',', $array[2], $array[17]);
	$cseC = join ( ',', 'cseC', $array[17]);
	$EBit = $array[13];
    }
        elsif ($array[1] =~ m/^H_cshC/ && $array[16] > $CovMin) {
        $varH = "H";
	#$cshC = join ( ',', $array[2], $array[17]);
	$cshC = join ( ',', 'cshC', $array[17]);
	$HBit = $array[13];
    }
         elsif ($array[1] =~ m/^I_csiC/ && $array[16] > $CovMin) {
        $varI = "I";
	#$csiC = join ( ',', $array[2], $array[17]);
	$csiC = join ( ',', 'csiC', $array[17]);
	$IBit = $array[13];
    }
        elsif ($array[1] =~ m/^K_cskC/ && $array[16] > $CovMin) {
        $varK = "K";
	#$cskC = join ( ',', $array[2], $array[17]);
	$cskC = join ( ',', 'cskC', $array[17]);
	$KBit = $array[13];
    }
        elsif ($array[1] =~ m/^L_cslC/ && $array[16] > $CovMin) {
        $varL = "L";
	#$cslC = join ( ',', $array[2], $array[17]);
	$cslC = join ( ',', 'cslC', $array[17]);
	$LBit = $array[13];
    }
       elsif ($array[1] =~ m/^W_csw/ && $array[16] > $CovMin) {
        $varW = "W";
	#$csw = join ( ',', $array[2], $array[17]);
	$csw = join ( ',', 'csw', $array[17]);
	$WBit = $array[13];
    }
        elsif ($array[1] =~ m/^X_csxB/ && $array[16] > $CovMin) {
        $varX = "X";
	#$csxB = join ( ',', $array[2], $array[17]);
	$csxB = join ( ',', 'csxB', $array[17]);
	$XBit = $array[13];
    }
        elsif ($array[1] =~ m/^Y_csy/ && $array[16] > $CovMin) {
        $varY = "Y";
	#$csy = join ( ',', $array[2], $array[17]);
	$csy = join ( ',', 'csy', $array[17]);
	$YBit = $array[13];
    }
        elsif ($array[1] =~ m/^Z_cszD/ && $array[16] > $CovMin) {
        $varZ = "Z";
	#$cszD = join ( ',', $array[2], $array[17]);
	$cszD = join ( ',', 'cszD', $array[17]);
	$ZBit = $array[13];
    }
}

open $input2, $ARGV[0];

foreach $line2 (<$input2>){
    chomp $line2;
    @array2 = split (" ", $line2);
    if ($array2[1] =~ m/^ctrA_/ && $array2[16] > $CovMin ) {
	#$ctrA = join ( ',', $array2[2], $array2[17]);
	$ctrA = join ( ',', 'ctrA', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $ctrA_id = "+";
	}
#	    else {
#	    $ctrA_id = "-";
#	}
   }   
        elsif ($array2[1] =~ m/^ctrB_/ && $array2[16] > $CovMin) {
        #$ctrB = join ( ',', $array2[2], $array2[17]);
        $ctrB = join ( ',', 'ctrB', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $ctrB_id = "+";
	}
#	    else {
#	    $ctrB_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^ctrC_/ && $array2[16] > $CovMin) {
        #$ctrC = join ( ',', $array2[2], $array2[17]);
        $ctrC = join ( ',', 'ctrC', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $ctrC_id = "+";
	}
#	    else {
#	    $ctrC_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^ctrD_/ && $array2[16] > $CovMin) {
        #$ctrD = join ( ',', $array2[2], $array2[17]);
        $ctrD = join ( ',', 'ctrD', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $ctrD_id = "+";
	}
#	    else {
#	    $ctrD_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^ctrE_/ && $array2[16] > $CovMin) {
        #$ctrE = join ( ',', $array2[2], $array2[17]);
        $ctrE = join ( ',', 'ctrE', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $ctrE_id = "+";
	}
#	    else {
#	    $ctrE_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^ctrF_/ && $array2[16] > $CovMin) {
        #$ctrF = join ( ',', $array2[2], $array2[17]);
        $ctrF = join ( ',', 'ctrF', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $ctrF_id = "+";
	}
#	    else {
#	    $ctrF_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^galE/ && $array2[16] > $CovMin) {
        #$galE = join ( ',', $array2[2], $array2[17]);
        $galE = join ( ',', 'galE', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $galE_id = "+";
	}
#	    else {
#	    $galE_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^tex_/ && $array2[16] > $CovMin) {
        #$tex = join ( ',', $array2[2], $array2[17]);
        $tex = join ( ',', 'tex', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $tex_id = "+";
	}
#	    else {
#	    $tex_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^rfbC/ && $array2[16] > $CovMin) {
        #$rfbC = join ( ',', $array2[2], $array2[17]);
        $rfbC = join ( ',', 'rfbC', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $rfbC_id = "+";
	}
#	    else {
#	    $rfbC_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^rfbA_/ && $array2[16] > $CovMin) {
        #$rfbA = join ( ',', $array2[2], $array2[17]);
        $rfbA = join ( ',', 'rfbA', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $rfbA_id = "+";
	}
#	    else {
#	    $rfbA_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^rfbB_/ && $array2[16] > $CovMin) {
        #$rfbB = join ( ',', $array2[2], $array2[17]);
        $rfbB = join ( ',', 'rfbB', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $rfbB_id = "+";
	}
#	    else {
#	    $rfbB_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^sodC_/ && $array2[16] > $CovMin) {
        #$sodC = join ( ',', $array2[2], $array2[17]);
        $sodC = join ( ',', 'sodC', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $sodC_id = "+";
	}
#	    else {
#	    $sodC_id = "-";
#	}
   }
######AAAAAA
	elsif ($array2[1] =~ m/^A_csaA_/ && $array2[16] > $CovMin) {
        #$csaA = join ( ',', $array2[2], $array2[17]);
        $csaA = join ( ',', 'csaA', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $csaA_id = "+";
	}
#	    else {
#	    $csaA_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^A_csaC_/ && $array2[16] > $CovMin) {
        #$csaC = join ( ',', $array2[2], $array2[17]);
        $csaC = join ( ',', 'csaC', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $csaC_id = "+";
	}
#	    else {
#	    $csaC_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^A_csaD_/ && $array2[16] > $CovMin) {
        #$csaD = join ( ',', $array2[2], $array2[17]);
        $csaD = join ( ',', 'csaD', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $csaD_id = "+";
	}
#	    else {
#	    $csaD_id = "-";
#	}
   }
######BBBBBB
	elsif ($array2[1] =~ m/^BCWY_cssA_/ && $array2[16] > $CovMin) {
        #$cssA = join ( ',', $array2[2], $array2[17]);
        $cssA = join ( ',', 'cssA', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cssA_id = "+";
	}
#	    else {
#	    $cssA_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^BCWY_cssB_/ && $array2[16] > $CovMin) {
        #$cssB = join ( ',', $array2[2], $array2[17]);
        $cssB = join ( ',', 'cssB', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cssB_id = "+";
	}
#	    else {
#	    $cssB_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^BCWY_cssC_/ && $array2[16] > $CovMin) {
        #$cssC = join ( ',', $array2[2], $array2[17]);
        $cssC = join ( ',', 'cssC', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cssC_id = "+";
	}
#	    else {
#	    $cssC_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^BCWY_ctrG_/ && $array2[16] > $CovMin) {
        #$ctrG = join ( ',', $array2[2], $array2[17]);
        $ctrG = join ( ',', 'ctrG', $array2[17]);
	#$ctrG_id = "+";
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $ctrG_id = "+";
	}
#	    else {
#	    $ctrG_id = "-";
#	}
   }
######CCCCCC
	elsif ($array2[1] =~ m/^C_cssE_/ && $array2[16] > $CovMin) {
        #$cssE = join ( ',', $array2[2], $array2[17]);
        $cssE = join ( ',', 'cssE', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cssE_id = "+";
	}
#	    else {
#	    $cssE_id = "-";
#	}
   }
######EEEEEE
	elsif ($array2[1] =~ m/^E_cseA_/ && $array2[16] > $CovMin) {
        #$cseA = join ( ',', $array2[2], $array2[17]);
        $cseA = join ( ',', 'cseA', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cseA_id = "+";
	}
#	    else {
#	    $cseA_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^E_cseB_/ && $array2[16] > $CovMin) {
        #$cseB = join ( ',', $array2[2], $array2[17]);
        $cseB = join ( ',', 'cseB', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cseB_id = "+";
	}
#	    else {
#	    $cseB_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^E_cseD_/ && $array2[16] > $CovMin) {
        #$cseD = join ( ',', $array2[2], $array2[17]);
        $cseD = join ( ',', 'cseD', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cseD_id = "+";
	}
#	    else {
#	    $cseD_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^E_cseE_/ && $array2[16] > $CovMin) {
        #$cseE = join ( ',', $array2[2], $array2[17]);
        $cseE = join ( ',', 'cseE', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cseE_id = "+";
	}
#	    else {
#	    $cseE_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^E_cseF_/ && $array2[16] > $CovMin) {
        #$cseF = join ( ',', $array2[2], $array2[17]);
        $cseF = join ( ',', 'cseF', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cseF_id = "+";
	}
#	    else {
#	    $cseF_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^E_cseG_/ && $array2[16] > $CovMin) {
        #$cseG = join ( ',', $array2[2], $array2[17]);
        $cseG = join ( ',', 'cseG', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cseG_id = "+";
	}
#	    else {
#	    $cseG_id = "-";
#	}
   }
#####HHHHHH
	elsif ($array2[1] =~ m/^H_cshD_/ && $array2[16] > $CovMin) {
        #$cshD = join ( ',', $array2[2], $array2[17]);
        $cshD = join ( ',', 'cshD', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cshD_id = "+";
	}
#	    else {
#	    $cshD_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^HZ_cszA_/ && $array2[16] > $CovMin) {
        #$cszA = join ( ',', $array2[2], $array2[17]);
        $cszA = join ( ',', 'cszA', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cszA_id = "+";
	}
#	    else {
#	    $cszA_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^HZ_cszB_/ && $array2[16] > $CovMin) {
        #$cszB = join ( ',', $array2[2], $array2[17]);
        $cszB = join ( ',', 'cszB', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cszB_id = "+";
	}
#	    else {
#	    $cszB_id = "-";
#	}
   }
#####IIIIII&KKKKKK
	elsif ($array2[1] =~ m/^IK_csiA_/ && $array2[16] > $CovMin) {
        #$csiA = join ( ',', $array2[2], $array2[17]);
        $csiA = join ( ',', 'csiA', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $csiA_id = "+";
	}
#	    else {
#	    $csiA_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^IK_csiB_/ && $array2[16] > $CovMin) {
        #$csiB = join ( ',', $array2[2], $array2[17]);
        $csiB = join ( ',', 'csiB', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $csiB_id = "+";
	}
#	    else {
#	    $csiB_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^IK_csiD_/ && $array2[16] > $CovMin) {
        #$csiD = join ( ',', $array2[2], $array2[17]);
        $csiD = join ( ',', 'csiD', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $csiD_id = "+";
	}
#	    else {
#	    $csiD_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^IK_csiE_/ && $array2[16] > $CovMin) {
        #$csiE = join ( ',', $array2[2], $array2[17]);
        $csiE = join ( ',', 'csiE', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $csiE_id = "+";
	}
#	    else {
#	    $csiE_id = "-";
#	}
   }
#####LLLLLL
	elsif ($array2[1] =~ m/^L_cslA_/ && $array2[16] > $CovMin) {
        #$cslA = join ( ',', $array2[2], $array2[17]);
        $cslA = join ( ',', 'cslA', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cslA_id = "+";
	}
#	    else {
#	    $cslA_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^L_cslB_/ && $array2[16] > $CovMin) {
        #$cslB = join ( ',', $array2[2], $array2[17]);
        $cslB = join ( ',', 'cslB', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cslB_id = "+";
	}
#	    else {
#	    $cslB_id = "-";
#	}
   }
#####WWWWWW
	elsif ($array2[1] =~ m/^WY_cssF_/ && $array2[16] > $CovMin) {
        #$cssF = join ( ',', $array2[2], $array2[17]);
        $cssF = join ( ',', 'cssF', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cssF_id = "+";
	}
#	    else {
#	    $cssF_id = "-";
#	}
   }
#####XXXXXX
	elsif ($array2[1] =~ m/^X_csxA_/ && $array2[16] > $CovMin) {
        #$csxA = join ( ',', $array2[2], $array2[17]);
        $csxA = join ( ',', 'csxA', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $csxA_id = "+";
	}
#	    else {
#	    $csxA_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^X_csxC_/ && $array2[16] > $CovMin) {
        #$csxC = join ( ',', $array2[2], $array2[17]);
        $csxC = join ( ',', 'csxC', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $csxC_id = "+";
	}
#	    else {
#	    $csxC_id = "-";
#	}
   }
#####YYYYYY
#####ZZZZZZ
	elsif ($array2[1] =~ m/^Z_cszC_/ && $array2[16] > $CovMin) {
        #$cszC = join ( ',', $array2[2], $array2[17]);
        $cszC = join ( ',', 'cszC', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cszC_id = "+";
	}
#	    else {
#	    $cszC_id = "-";
#	}
   }
#####16S16S
        elsif ($array2[1] =~ m/^16S_rDNA_/ && $array2[16] > $CovMin) {
        $var16S = "16S";
	#$s16S = join ( ',', $array2[2], $array2[17]);
	$s16S = join ( ',', 's16S', $array2[17]);
	    $var16SBit = $array2[13];
	    if ($array2[2] > $pid && $array[17] > $paln) {
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
    print $head;
    #print "$var1 has low coverage or no Nm typable genes exist in sample.\n";
    print "$var1\tNA\tNA\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";
    #print "Can't infer serotype!"; 
    #print "$var1\t$varNt\t-\t-\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\n";

#####################################################AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
} elsif ($varA eq "A" && $ABit > $BBit && $ABit > $CBit && $ABit > $EBit && $ABit > $HBit && $ABit > $IBit && $ABit > $KBit && $ABit > $LBit && $ABit > $WBit && $ABit > $XBit && $ABit > $YBit && $ABit > $ZBit & $csaA_id eq "+" & $csaB_id eq "+" & $csaD_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
    print $head;
    print "$var1\t$varA\tcsaB\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varA eq "A" && $ABit > $BBit && $ABit > $CBit && $ABit > $EBit && $ABit > $HBit && $ABit > $IBit && $ABit > $KBit && $ABit > $LBit && $ABit > $WBit && $ABit > $XBit && $ABit > $YBit && $ABit > $ZBit && ($csaA_id eq "-" || $csaB_id eq "-" || $csaD_id eq "-" || $ctrA_id eq "-" || $ctrB_id eq "-" || $ctrC_id eq "-" || $ctrD_id eq "-" || $ctrE_id eq "-" || $ctrF_id eq "-" )) {
} elsif ($varA eq "A" && $ABit > $BBit && $ABit > $CBit && $ABit > $EBit && $ABit > $HBit && $ABit > $IBit && $ABit > $KBit && $ABit > $LBit && $ABit > $WBit && $ABit > $XBit && $ABit > $YBit && $ABit > $ZBit ) {
    print $head;
    print "$var1\t$varA\tcsaB\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
} elsif ($varB eq "B" && $BBit > $ABit && $BBit > $CBit && $BBit > $EBit && $BBit > $HBit && $BBit > $IBit && $BBit > $KBit && $BBit > $LBit && $BBit > $WBit && $BBit > $XBit && $BBit > $YBit && $BBit > $ZBit & $cssA_id eq "+" & $cssB_id eq "+" & $cssC_id eq "+" & $ctrG_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
    print $head;
    print "$var1\t$varB\tcsb\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varB eq "B" && $BBit > $ABit && $BBit > $CBit && $BBit > $EBit && $BBit > $HBit && $BBit > $IBit && $BBit > $KBit && $BBit > $LBit && $BBit > $WBit && $BBit > $XBit && $BBit > $YBit && $BBit > $ZBit && ($cssA eq "-" || $cssB eq "-" || $cssC eq "-" || $ctrG eq "-" || $ctrA eq "-" || $ctrB eq "-" || $ctrC eq "-" || $ctrD eq "-" || $ctrE eq "-" || $ctrF eq "-" )) {
} elsif ($varB eq "B" && $BBit > $ABit && $BBit > $CBit && $BBit > $EBit && $BBit > $HBit && $BBit > $IBit && $BBit > $KBit && $BBit > $LBit && $BBit > $WBit && $BBit > $XBit && $BBit > $YBit && $BBit > $ZBit ) {
    print $head;
    print "$var1\t$varB\tcsb\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
} elsif ($varC eq "C" && $CBit > $ABit && $CBit > $BBit && $CBit > $EBit && $CBit > $HBit && $CBit > $IBit && $CBit > $KBit && $CBit > $LBit && $CBit > $WBit && $CBit > $XBit && $CBit > $YBit && $CBit > $ZBit & $cssA_id eq "+" & $cssB_id eq "+" & $cssC_id eq "+" & $cssE_id eq "+" & $ctrG_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
    print $head;
    print "$var1\t$varC\tcsc\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varC eq "C" && $CBit > $ABit && $CBit > $BBit && $CBit > $EBit && $CBit > $HBit && $CBit > $IBit && $CBit > $KBit && $CBit > $LBit && $CBit > $WBit && $CBit > $XBit && $CBit > $YBit && $CBit > $ZBit && ($cssA eq "-" || $cssB eq "-" || $cssC eq "-" || $cssE eq "-" || $ctrG eq "-" || $ctrA eq "-" || $ctrB eq "-" || $ctrC eq "-" || $ctrD eq "-" || $ctrE eq "-" || $ctrF eq "-" )) {
} elsif ($varC eq "C" && $CBit > $ABit && $CBit > $BBit && $CBit > $EBit && $CBit > $HBit && $CBit > $IBit && $CBit > $KBit && $CBit > $LBit && $CBit > $WBit && $CBit > $XBit && $CBit > $YBit && $CBit > $ZBit ) {
    print $head;
    print "$var1\t$varC\tcsc\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
} elsif ($varE eq "E" && $EBit > $ABit && $EBit > $BBit && $EBit > $CBit && $EBit > $HBit && $EBit > $IBit && $EBit > $KBit && $EBit > $LBit && $EBit > $WBit && $EBit > $XBit && $EBit > $YBit && $EBit > $ZBit & $cseA_id eq "+" & $cseB_id eq "+" & $cseD_id eq "+" & $cseE_id eq "+" & $cseF_id eq "+" & $cseG_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
    print $head;
    print "$var1\t$varE\tcseC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varE eq "E" && $EBit > $ABit && $EBit > $BBit && $EBit > $CBit && $EBit > $HBit && $EBit > $IBit && $EBit > $KBit && $EBit > $LBit && $EBit > $WBit && $EBit > $XBit && $EBit > $YBit && $EBit > $ZBit && ($cseA eq "-" || $cseB eq "-" || $cseD eq "-" || $cseE eq "-" || $cseF eq "-" || $cseG eq "-" || $ctrA eq "-" || $ctrB eq "-" || $ctrC eq "-" || $ctrD eq "-" || $ctrE eq "-" || $ctrF eq "-" )) {
} elsif ($varE eq "E" && $EBit > $ABit && $EBit > $BBit && $EBit > $CBit && $EBit > $HBit && $EBit > $IBit && $EBit > $KBit && $EBit > $LBit && $EBit > $WBit && $EBit > $XBit && $EBit > $YBit && $EBit > $ZBit ) {
    print $head;
    print "$var1\t$varE\tcseC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
} elsif ($varH eq "H" && $HBit > $ABit && $HBit > $BBit && $HBit > $CBit && $HBit > $EBit && $HBit > $IBit && $HBit > $KBit && $HBit > $LBit && $HBit > $WBit && $HBit > $XBit && $HBit > $YBit && $HBit > $ZBit & $cszA_id eq "+" & $cszB_id eq "+" & $cshD_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
    print $head;
    print "$var1\t$varH\tcshC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varH eq "H" && $HBit > $ABit && $HBit > $BBit && $HBit > $CBit && $HBit > $EBit && $HBit > $IBit && $HBit > $KBit && $HBit > $LBit && $HBit > $WBit && $HBit > $XBit && $HBit > $YBit && $HBit > $ZBit && ($cszA eq "-" || $cszB eq "-" || $cshD eq "-" || $ctrA eq "-" || $ctrB eq "-" || $ctrC eq "-" || $ctrD eq "-" || $ctrE eq "-" || $ctrF eq "-" )) {
} elsif ($varH eq "H" && $HBit > $ABit && $HBit > $BBit && $HBit > $CBit && $HBit > $EBit && $HBit > $IBit && $HBit > $KBit && $HBit > $LBit && $HBit > $WBit && $HBit > $XBit && $HBit > $YBit && $HBit > $ZBit ) {
    print $head;
    print "$var1\t$varH\tcshC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
} elsif ($varI eq "I" && $IBit > $ABit && $IBit > $BBit && $IBit > $CBit && $IBit > $EBit && $IBit > $HBit && $IBit > $KBit && $IBit > $LBit && $IBit > $WBit && $IBit > $XBit && $IBit > $YBit && $IBit > $ZBit & $csiA_id eq "+" & $csiB_id eq "+" & $csiD_id eq "+" & $csiE_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
    print $head;
    print "$var1\t$varI\tcsiC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varI eq "I" && $IBit > $ABit && $IBit > $BBit && $IBit > $CBit && $IBit > $EBit && $IBit > $HBit && $IBit > $KBit && $IBit > $LBit && $IBit > $WBit && $IBit > $XBit && $IBit > $YBit && $IBit > $ZBit && ($csiA eq "-" || $csiB eq "-" || $csiD eq "-" || $csiE eq "-" || $ctrA eq "-" || $ctrB eq "-" || $ctrC eq "-" || $ctrD eq "-" || $ctrE eq "-" || $ctrF eq "-" )) {
} elsif ($varI eq "I" && $IBit > $ABit && $IBit > $BBit && $IBit > $CBit && $IBit > $EBit && $IBit > $HBit && $IBit > $KBit && $IBit > $LBit && $IBit > $WBit && $IBit > $XBit && $IBit > $YBit && $IBit > $ZBit ) {
    print $head;
    print "$var1\t$varI\tcsiC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK
} elsif ($varK eq "K" && $KBit > $ABit && $KBit > $BBit && $KBit > $CBit && $KBit > $EBit && $KBit > $HBit && $KBit > $IBit && $KBit > $LBit && $KBit > $WBit && $KBit > $XBit && $KBit > $YBit && $KBit > $ZBit & $csiA_id eq "+" & $csiB_id eq "+" & $csiD_id eq "+" & $csiE_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
    print $head;
    print "$var1\t$varK\tcskC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varK eq "K" && $KBit > $ABit && $KBit > $BBit && $KBit > $CBit && $KBit > $EBit && $KBit > $HBit && $KBit > $IBit && $KBit > $LBit && $KBit > $WBit && $KBit > $XBit && $KBit > $YBit && $KBit > $ZBit && ($csiA eq "-" || $csiB eq "-" || $csiD eq "-" || $csiE eq "-" )) {
} elsif ($varK eq "K" && $KBit > $ABit && $KBit > $BBit && $KBit > $CBit && $KBit > $EBit && $KBit > $HBit && $KBit > $IBit && $KBit > $LBit && $KBit > $WBit && $KBit > $XBit && $KBit > $YBit && $KBit > $ZBit ) {
    print $head;
    print "$var1\t$varK\tcskC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL
} elsif ($varL eq "L" && $LBit > $ABit && $LBit > $BBit && $LBit > $CBit && $LBit > $EBit && $LBit > $HBit && $LBit > $IBit && $LBit > $KBit && $LBit > $WBit && $LBit > $XBit && $LBit > $YBit && $LBit > $ZBit & $cslA_id eq "+" & $cslB_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
    print $head;
    print "$var1\t$varL\tcslC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varL eq "L" && $LBit > $ABit && $LBit > $BBit && $LBit > $CBit && $LBit > $EBit && $LBit > $HBit && $LBit > $IBit && $LBit > $KBit && $LBit > $WBit && $LBit > $XBit && $LBit > $YBit && $LBit > $ZBit && ($cslA eq "-" || $cslB eq "-" )) {
} elsif ($varL eq "L" && $LBit > $ABit && $LBit > $BBit && $LBit > $CBit && $LBit > $EBit && $LBit > $HBit && $LBit > $IBit && $LBit > $KBit && $LBit > $WBit && $LBit > $XBit && $LBit > $YBit && $LBit > $ZBit ) {
    print $head;
    print "$var1\t$varL\tcslC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
} elsif ($varW eq "W" && $WBit > $ABit && $WBit > $BBit && $WBit > $CBit && $WBit > $EBit && $WBit > $HBit && $WBit > $IBit && $WBit > $KBit && $WBit > $LBit && $WBit > $XBit && $WBit > $YBit && $WBit > $ZBit & $cssA_id eq "+" & $cssB_id eq "+" & $cssC_id eq "+" & $cssF_id eq "+" & $ctrG_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
    print $head;
    print "$var1\t$varW\tcsw\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varW eq "W" && $WBit > $ABit && $WBit > $BBit && $WBit > $CBit && $WBit > $EBit && $WBit > $HBit && $WBit > $IBit && $WBit > $KBit && $WBit > $LBit && $WBit > $XBit && $WBit > $YBit && $WBit > $ZBit && ($cssA_id eq "-" || $cssB_id eq "-" || $cssC_id eq "-" || $cssF_id eq "-" || $ctrG_id eq "-" )) {
} elsif ($varW eq "W" && $WBit > $ABit && $WBit > $BBit && $WBit > $CBit && $WBit > $EBit && $WBit > $HBit && $WBit > $IBit && $WBit > $KBit && $WBit > $LBit && $WBit > $XBit && $WBit > $YBit && $WBit > $ZBit ) {
    print $head;
    print "$var1\t$varW\tcsw\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
} elsif ($varX eq "X" && $XBit > $ABit && $XBit > $BBit && $XBit > $CBit && $XBit > $EBit && $XBit > $HBit && $XBit > $IBit && $XBit > $KBit && $XBit > $LBit && $XBit > $WBit && $XBit > $YBit && $XBit > $ZBit & $csxA_id eq "+" & $csxC_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
    print $head;
    print "$var1\t$varX\tcsxB\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varX eq "X" && $XBit > $ABit && $XBit > $BBit && $XBit > $CBit && $XBit > $EBit && $XBit > $HBit && $XBit > $IBit && $XBit > $KBit && $XBit > $LBit && $XBit > $WBit && $XBit > $YBit && $XBit > $ZBit && ($csxA eq "-" || $csxC eq "-" )) {
} elsif ($varX eq "X" && $XBit > $ABit && $XBit > $BBit && $XBit > $CBit && $XBit > $EBit && $XBit > $HBit && $XBit > $IBit && $XBit > $KBit && $XBit > $LBit && $XBit > $WBit && $XBit > $YBit && $XBit > $ZBit ) {
    print $head;
    print "$var1\t$varX\tcsxB\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
} elsif ($varY eq "Y" && $YBit > $ABit && $YBit > $BBit && $YBit > $CBit && $YBit > $EBit && $YBit > $HBit && $YBit > $IBit && $YBit > $KBit && $YBit > $LBit && $YBit > $WBit && $YBit > $XBit && $YBit > $ZBit & $cssA_id eq "+" & $cssB_id eq "+" & $cssC_id eq "+" & $cssF_id eq "+" & $ctrG_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
    print $head;
    print "$var1\t$varY\tcsy\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varY eq "Y" && $YBit > $ABit && $YBit > $BBit && $YBit > $CBit && $YBit > $EBit && $YBit > $HBit && $YBit > $IBit && $YBit > $KBit && $YBit > $LBit && $YBit > $WBit && $YBit > $XBit && $YBit > $ZBit && ($cssA_id eq "-" || $cssB_id eq "-" || $cssC_id eq "-" || $cssF_id eq "-" || $ctrG_id eq "-" )) {
} elsif ($varY eq "Y" && $YBit > $ABit && $YBit > $BBit && $YBit > $CBit && $YBit > $EBit && $YBit > $HBit && $YBit > $IBit && $YBit > $KBit && $YBit > $LBit && $YBit > $WBit && $YBit > $XBit && $YBit > $ZBit ) {
    print $head;
    print "$var1\t$varY\tcsy\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ
} elsif ($varZ eq "Z" && $ZBit > $ABit && $ZBit > $BBit && $ZBit > $CBit && $ZBit > $EBit && $ZBit > $HBit && $ZBit > $IBit && $ZBit > $KBit && $ZBit > $LBit && $ZBit > $WBit && $ZBit > $XBit && $ZBit > $YBit & $cszA_id eq "+" & $cszB_id eq "+" & $cszC_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
    print $head;
    print "$var1\t$varZ\tcszD\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varZ eq "Z" && $ZBit > $ABit && $ZBit > $BBit && $ZBit > $CBit && $ZBit > $EBit && $ZBit > $HBit && $ZBit > $IBit && $ZBit > $KBit && $ZBit > $LBit && $ZBit > $WBit && $ZBit > $XBit && $ZBit > $YBit && ($cszA eq "-" || $cszB eq "-" || $cszC eq "-" )) {
} elsif ($varZ eq "Z" && $ZBit > $ABit && $ZBit > $BBit && $ZBit > $CBit && $ZBit > $EBit && $ZBit > $HBit && $ZBit > $IBit && $ZBit > $KBit && $ZBit > $LBit && $ZBit > $WBit && $ZBit > $XBit && $ZBit > $YBit ) {
    print $head;
    print "$var1\t$varZ\tcszD\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################????????????????????????????????????????????????????????????
} else {
    print $head;
    #print "Low Coverage! Can't infer serotype!";
    print "$var1\t$varNt\tTESTNm?\tNm?\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

}
