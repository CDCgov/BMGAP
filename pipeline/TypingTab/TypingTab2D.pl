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
my $cov = 0; 
my $CovMin = 1;
my $pid = 95;
my $paln = 95;
my $varISO = 0;
my $head = "Sequence_File\tInferred_SG\tBased_SG\tGrouping_Gene\tcsaA\tcsaB\tcsaC\tcsaD\tcsb\tcsc\tcseA\tcseB\tcseC\tcseD\tcseE\tcseF\tcseG\tcshC\tcshD\tcsiA\tcsiB\tcsiC\tcsiD\tcsiE\tcskC\tcslA\tcslB\tcslC\tcssA\tcssB\tcssC\tcssE\tcssF\tcsw\tcsxA\tcsxB\tcsxC\tcsy\tcszA\tcszB\tcszC\tcszD\tctrG\tgalE\ttex\tctrA\tctrB\tctrC\tctrD\tctrE\tctrF\trfbA\trfbB\trfbC\tsodC\t16S\tISO\n";
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
#CovSCovSCovS
my $ACov = 0;
my $BCov = 0;
my $CCov = 0;
my $ECov = 0;
my $varH = "no";
my $HCov = 0;
my $ICov = 0;
my $KCov = 0;
my $LCov = 0;
my $WCov = 0;
my $XCov = 0;
my $YCov = 0;
my $ZCov = 0;
my $var16SCov = 0;


open $input, $ARGV[0];

foreach $line (<$input>){
    chomp $line;
    @array = split (" ", $line);   
    if ($array[1] =~ m/^A_csaB/ && $array[16] > $CovMin) {
        $varA = "A";
	$cov = sprintf("%.2f", $array[16]);
	#$csaB = join ( ',', 'csaB', $array[17]);
	$csaB = join ( '_', $cov, $array[17]);
	$ACov = $array[16];
    }
        elsif ($array[1] =~ m/^B_csb/ && $array[16] > $CovMin) {
        $varB = "B";
	$cov = sprintf("%.2f", $array[16]);
	#$csb  = join ( ',', 'csb', $array[17]);
	$csb  = join ( '_', $cov, $array[17]);
	$BCov = $array[16];
    }
        elsif ($array[1] =~ m/^C_csc/ && $array[16] > $CovMin) {
        $varC = "C";
	$cov = sprintf("%.2f", $array[16]);
	#$csc = join ( ',', 'csc', $array[17]);
	$csc = join ( '_', $cov, $array[17]);
	$CCov = $array[16];
    }
        elsif ($array[1] =~ m/^E_cseC/ && $array[16] > $CovMin) {
        $varE = "E";
	$cov = sprintf("%.2f", $array[16]);
	#$cseC = join ( ',', 'cseC', $array[17]);
	$cseC = join ( '_', $cov, $array[17]);
	$ECov = $array[16];
    }
        elsif ($array[1] =~ m/^H_cshC/ && $array[16] > $CovMin) {
        $varH = "H";
	$cov = sprintf("%.2f", $array[16]);
	#$cshC = join ( ',', 'cshC', $array[17]);
	$cshC = join ( '_', $cov, $array[17]);
	$HCov = $array[16];
    }
         elsif ($array[1] =~ m/^I_csiC/ && $array[16] > $CovMin) {
        $varI = "I";
	$cov = sprintf("%.2f", $array[16]);
	#$csiC = join ( ',', 'csiC', $array[17]);
	$csiC = join ( '_', $cov, $array[17]);
	$ICov = $array[16];
    }
        elsif ($array[1] =~ m/^K_cskC/ && $array[16] > $CovMin) {
        $varK = "K";
	$cov = sprintf("%.2f", $array[16]);
	#$cskC = join ( ',', 'cskC', $array[17]);
	$cskC = join ( '_', $cov, $array[17]);
	$KCov = $array[16];
    }
        elsif ($array[1] =~ m/^L_cslC/ && $array[16] > $CovMin) {
        $varL = "L";
	$cov = sprintf("%.2f", $array[16]);
	#$cslC = join ( ',', 'cslC', $array[17]);
	$cslC = join ( '_', $cov, $array[17]);
	$LCov = $array[16];
    }
       elsif ($array[1] =~ m/^W_csw/ && $array[16] > $CovMin) {
        $varW = "W";
	$cov = sprintf("%.2f", $array[16]);
	#$csw = join ( ',', 'csw', $array[17]);
	$csw = join ( '_', $cov, $array[17]);
	$WCov = $array[16];
    }
        elsif ($array[1] =~ m/^X_csxB/ && $array[16] > $CovMin) {
        $varX = "X";
	$cov = sprintf("%.2f", $array[16]);
	#$csxB = join ( ',', 'csxB', $array[17]);
	$csxB = join ( '_', $cov, $array[17]);
	$XCov = $array[16];
    }
        elsif ($array[1] =~ m/^Y_csy/ && $array[16] > $CovMin) {
        $varY = "Y";
	$cov = sprintf("%.2f", $array[16]);
	#$csy = join ( ',', 'csy', $array[17]);
	$csy = join ( '_', $cov, $array[17]);
	$YCov = $array[16];
    }
        elsif ($array[1] =~ m/^Z_cszD/ && $array[16] > $CovMin) {
        $varZ = "Z";
	$cov = sprintf("%.2f", $array[16]);
	#$cszD = join ( ',', 'cszD', $array[17]);
	$cszD = join ( '_', $cov, $array[17]);
	$ZCov = $array[16];
    }
}

open $input2, $ARGV[0];

foreach $line2 (<$input2>){
    chomp $line2;
    @array2 = split (" ", $line2);
    if ($array2[1] =~ m/^ctrA_/ && $array2[16] > $CovMin ) {
	$cov = sprintf("%.2f", $array[16]);
	$ctrA = join ( '_', $cov, $array2[17]);
	#$ctrA = join ( ',', 'ctrA', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $ctrA_id = "+";
	}
#	    else {
#	    $ctrA_id = "-";
#	}
   }   
        elsif ($array2[1] =~ m/^ctrB_/ && $array2[16] > $CovMin) {
        $cov = sprintf("%.2f", $array[16]);
	$ctrB = join ( '_', $cov, $array2[17]);
        #$ctrB = join ( ',', 'ctrB', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $ctrB_id = "+";
	}
#	    else {
#	    $ctrB_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^ctrC_/ && $array2[16] > $CovMin) {
        $cov = sprintf("%.2f", $array[16]);
	$ctrC = join ( '_', $cov, $array2[17]);
        #$ctrC = join ( ',', 'ctrC', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $ctrC_id = "+";
	}
#	    else {
#	    $ctrC_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^ctrD_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $ctrD = join ( '_', $cov, $array2[17]);
        #$ctrD = join ( ',', 'ctrD', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $ctrD_id = "+";
	}
#	    else {
#	    $ctrD_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^ctrE_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $ctrE = join ( '_', $cov, $array2[17]);
        #$ctrE = join ( ',', 'ctrE', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $ctrE_id = "+";
	}
#	    else {
#	    $ctrE_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^ctrF_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $ctrF = join ( '_', $cov, $array2[17]);
        #$ctrF = join ( ',', 'ctrF', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $ctrF_id = "+";
	}
#	    else {
#	    $ctrF_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^galE/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $galE = join ( '_', $cov, $array2[17]);
        #$galE = join ( ',', 'galE', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $galE_id = "+";
	}
#	    else {
#	    $galE_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^tex_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $tex = join ( '_', $cov, $array2[17]);
        #$tex = join ( ',', 'tex', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $tex_id = "+";
	}
#	    else {
#	    $tex_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^rfbC/ && $array2[16] > $CovMin) {        
	$cov = sprintf("%.2f", $array[16]);
	$rfbC = join ( '_', $cov, $array2[17]);
        #$rfbC = join ( ',', 'rfbC', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $rfbC_id = "+";
	}
#	    else {
#	    $rfbC_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^rfbA_/ && $array2[16] > $CovMin) {
        $cov = sprintf("%.2f", $array[16]);
	$rfbA = join ( '_', $cov, $array2[17]);
        #$rfbA = join ( ',', 'rfbA', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $rfbA_id = "+";
	}
#	    else {
#	    $rfbA_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^rfbB_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $rfbB = join ( '_', $cov, $array2[17]);
        #$rfbB = join ( ',', 'rfbB', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $rfbB_id = "+";
	}
#	    else {
#	    $rfbB_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^sodC_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $sodC = join ( '_', $cov, $array2[17]);
        #$sodC = join ( ',', 'sodC', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $sodC_id = "+";
	}
#	    else {
#	    $sodC_id = "-";
#	}
   }
######AAAAAA
	elsif ($array2[1] =~ m/^A_csaA_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $csaA = join ( '_', $cov, $array2[17]);
        #$csaA = join ( ',', 'csaA', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $csaA_id = "+";
	}
#	    else {
#	    $csaA_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^A_csaC_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $csaC = join ( '_', $cov, $array2[17]);
        #$csaC = join ( ',', 'csaC', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $csaC_id = "+";
	}
#	    else {
#	    $csaC_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^A_csaD_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $csaD = join ( '_', $cov, $array2[17]);
        #$csaD = join ( ',', 'csaD', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $csaD_id = "+";
	}
#	    else {
#	    $csaD_id = "-";
#	}
   }
######BBBBBB
	elsif ($array2[1] =~ m/^BCWY_cssA_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $cssA = join ( '_', $cov, $array2[17]);
        #$cssA = join ( ',', 'cssA', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cssA_id = "+";
	}
#	    else {
#	    $cssA_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^BCWY_cssB_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $cssB = join ( '_', $cov, $array2[17]);
        #$cssB = join ( ',', 'cssB', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cssB_id = "+";
	}
#	    else {
#	    $cssB_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^BCWY_cssC_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $cssC = join ( '_', $cov, $array2[17]);
        #$cssC = join ( ',', 'cssC', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cssC_id = "+";
	}
#	    else {
#	    $cssC_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^BCWY_ctrG_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $ctrG = join ( '_', $cov, $array2[17]);
        #$ctrG = join ( ',', 'ctrG', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $ctrG_id = "+";
	}
#	    else {
#	    $ctrG_id = "-";
#	}
   }
######CCCCCC
	elsif ($array2[1] =~ m/^C_cssE_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $cssE = join ( '_', $cov, $array2[17]);
        #$cssE = join ( ',', 'cssE', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cssE_id = "+";
	}
#	    else {
#	    $cssE_id = "-";
#	}
   }
######EEEEEE
	elsif ($array2[1] =~ m/^E_cseA_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $cseA = join ( '_', $cov, $array2[17]);
        #$cseA = join ( ',', 'cseA', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cseA_id = "+";
	}
#	    else {
#	    $cseA_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^E_cseB_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $cseB = join ( '_', $cov, $array2[17]);
        #$cseB = join ( ',', 'cseB', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cseB_id = "+";
	}
#	    else {
#	    $cseB_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^E_cseD_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $cseD = join ( '_', $cov, $array2[17]);
        #$cseD = join ( ',', 'cseD', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cseD_id = "+";
	}
#	    else {
#	    $cseD_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^E_cseE_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $cseE = join ( '_', $cov, $array2[17]);
        #$cseE = join ( ',', 'cseE', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cseE_id = "+";
	}
#	    else {
#	    $cseE_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^E_cseF_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $cseF = join ( '_', $cov, $array2[17]);
        #$cseF = join ( ',', 'cseF', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cseF_id = "+";
	}
#	    else {
#	    $cseF_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^E_cseG_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $cseG = join ( '_', $cov, $array2[17]);
        #$cseG = join ( ',', 'cseG', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cseG_id = "+";
	}
#	    else {
#	    $cseG_id = "-";
#	}
   }
#####HHHHHH
	elsif ($array2[1] =~ m/^H_cshD_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $cshD = join ( '_', $cov, $array2[17]);
        #$cshD = join ( ',', 'cshD', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cshD_id = "+";
	}
#	    else {
#	    $cshD_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^HZ_cszA_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $cszA = join ( '_', $cov, $array2[17]);
        #$cszA = join ( ',', 'cszA', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cszA_id = "+";
	}
#	    else {
#	    $cszA_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^HZ_cszB_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $cszB = join ( '_', $cov, $array2[17]);
        #$cszB = join ( ',', 'cszB', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cszB_id = "+";
	}
#	    else {
#	    $cszB_id = "-";
#	}
   }
#####IIIIII&KKKKKK
	elsif ($array2[1] =~ m/^IK_csiA_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $csiA = join ( '_', $cov, $array2[17]);
        #$csiA = join ( ',', 'csiA', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $csiA_id = "+";
	}
#	    else {
#	    $csiA_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^IK_csiB_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $csiB = join ( '_', $cov, $array2[17]);
        #$csiB = join ( ',', 'csiB', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $csiB_id = "+";
	}
#	    else {
#	    $csiB_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^IK_csiD_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $csiD = join ( '_', $cov, $array2[17]);
        #$csiD = join ( ',', 'csiD', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $csiD_id = "+";
	}
#	    else {
#	    $csiD_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^IK_csiE_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $csiE = join ( '_', $cov, $array2[17]);
        #$csiE = join ( ',', 'csiE', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $csiE_id = "+";
	}
#	    else {
#	    $csiE_id = "-";
#	}
   }
#####LLLLLL
	elsif ($array2[1] =~ m/^L_cslA_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $cslA = join ( '_', $cov, $array2[17]);
        #$cslA = join ( ',', 'cslA', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cslA_id = "+";
	}
#	    else {
#	    $cslA_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^L_cslB_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $cslB = join ( '_', $cov, $array2[17]);
        #$cslB = join ( ',', 'cslB', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cslB_id = "+";
	}
#	    else {
#	    $cslB_id = "-";
#	}
   }
#####WWWWWW
	elsif ($array2[1] =~ m/^WY_cssF_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $cssF = join ( '_', $cov, $array2[17]);
        #$cssF = join ( ',', 'cssF', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $cssF_id = "+";
	}
#	    else {
#	    $cssF_id = "-";
#	}
   }
#####XXXXXX
	elsif ($array2[1] =~ m/^X_csxA_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $csxA = join ( '_', $cov, $array2[17]);
        #$csxA = join ( ',', 'csxA', $array2[17]);
	    if ($array2[2] > $pid && $array[17] > $paln) {
	    $csxA_id = "+";
	}
#	    else {
#	    $csxA_id = "-";
#	}
   }
	elsif ($array2[1] =~ m/^X_csxC_/ && $array2[16] > $CovMin) {
	$cov = sprintf("%.2f", $array[16]);
        $csxC = join ( '_', $cov, $array2[17]);
        #$csxC = join ( ',', 'csxC', $array2[17]);
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
	$cov = sprintf("%.2f", $array[16]);
        $cszC = join ( '_', $cov, $array2[17]);
        #$cszC = join ( ',', 'cszC', $array2[17]);
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
	$cov = sprintf("%.2f", $array[16]);
	$s16S = join ( '_', $cov, $array2[17]);
	#$s16S = join ( ',', 's16S', $array2[17]);
	    $var16SCov = $array2[13];
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
    print "$var1\tNG\tNA\tNA\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";
    #print "Can't infer serotype!"; 
    #print "$var1\t$varNt\t-\t-\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\n";

#####################################################AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
#} elsif ($varA eq "A" && $ACov > $BCov && $ACov > $CCov && $ACov > $ECov && $ACov > $HCov && $ACov > $ICov && $ACov > $KCov && $ACov > $LCov && $ACov > $WCov && $ACov > $XCov && $ACov > $YCov && $ACov > $ZCov & $csaA_id eq "+" & $csaC_id eq "+" & $csaD_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
} elsif ($varA eq "A" && $ACov > $BCov && $ACov > $CCov && $ACov > $ECov && $ACov > $HCov && $ACov > $ICov && $ACov > $KCov && $ACov > $LCov && $ACov > $WCov && $ACov > $XCov && $ACov > $YCov && $ACov > $ZCov ) {
    print $head;
    print "$var1\t$varA\t$varA\tcsaB\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varA eq "A" && $ACov > $BCov && $ACov > $CCov && $ACov > $ECov && $ACov > $HCov && $ACov > $ICov && $ACov > $KCov && $ACov > $LCov && $ACov > $WCov && $ACov > $XCov && $ACov > $YCov && $ACov > $ZCov && ($csaA_id eq "-" || $csaC_id eq "-" || $csaD_id eq "-" || $ctrA_id eq "-" || $ctrB_id eq "-" || $ctrC_id eq "-" || $ctrD_id eq "-" || $ctrE_id eq "-" || $ctrF_id eq "-" )) {
#} elsif ($varA eq "A" && $ACov > $BCov && $ACov > $CCov && $ACov > $ECov && $ACov > $HCov && $ACov > $ICov && $ACov > $KCov && $ACov > $LCov && $ACov > $WCov && $ACov > $XCov && $ACov > $YCov && $ACov > $ZCov ) {
#    print $head;
#    print "$var1\tNG\t$varA\tcsaB\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
} elsif ($varB eq "B" && $BCov > $ACov && $BCov > $CCov && $BCov > $ECov && $BCov > $HCov && $BCov > $ICov && $BCov > $KCov && $BCov > $LCov && $BCov > $WCov && $BCov > $XCov && $BCov > $YCov && $BCov > $ZCov & $cssA_id eq "+" & $cssB_id eq "+" & $cssC_id eq "+" & $ctrG_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
    print $head;
    print "$var1\t$varB\t$varB\tcsb\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varB eq "B" && $BCov > $ACov && $BCov > $CCov && $BCov > $ECov && $BCov > $HCov && $BCov > $ICov && $BCov > $KCov && $BCov > $LCov && $BCov > $WCov && $BCov > $XCov && $BCov > $YCov && $BCov > $ZCov && ($cssA eq "-" || $cssB eq "-" || $cssC eq "-" || $ctrG eq "-" || $ctrA eq "-" || $ctrB eq "-" || $ctrC eq "-" || $ctrD eq "-" || $ctrE eq "-" || $ctrF eq "-" )) {
} elsif ($varB eq "B" && $BCov > $ACov && $BCov > $CCov && $BCov > $ECov && $BCov > $HCov && $BCov > $ICov && $BCov > $KCov && $BCov > $LCov && $BCov > $WCov && $BCov > $XCov && $BCov > $YCov && $BCov > $ZCov ) {
    print $head;
    print "$var1\tNG\t$varB\tcsb\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
} elsif ($varC eq "C" && $CCov > $ACov && $CCov > $BCov && $CCov > $ECov && $CCov > $HCov && $CCov > $ICov && $CCov > $KCov && $CCov > $LCov && $CCov > $WCov && $CCov > $XCov && $CCov > $YCov && $CCov > $ZCov & $cssA_id eq "+" & $cssB_id eq "+" & $cssC_id eq "+" & $cssE_id eq "+" & $ctrG_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
    print $head;
    print "$var1\t$varC\t$varC\tcsc\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varC eq "C" && $CCov > $ACov && $CCov > $BCov && $CCov > $ECov && $CCov > $HCov && $CCov > $ICov && $CCov > $KCov && $CCov > $LCov && $CCov > $WCov && $CCov > $XCov && $CCov > $YCov && $CCov > $ZCov && ($cssA eq "-" || $cssB eq "-" || $cssC eq "-" || $cssE eq "-" || $ctrG eq "-" || $ctrA eq "-" || $ctrB eq "-" || $ctrC eq "-" || $ctrD eq "-" || $ctrE eq "-" || $ctrF eq "-" )) {
} elsif ($varC eq "C" && $CCov > $ACov && $CCov > $BCov && $CCov > $ECov && $CCov > $HCov && $CCov > $ICov && $CCov > $KCov && $CCov > $LCov && $CCov > $WCov && $CCov > $XCov && $CCov > $YCov && $CCov > $ZCov ) {
    print $head;
    print "$var1\tNG\t$varC\tcsc\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
} elsif ($varE eq "E" && $ECov > $ACov && $ECov > $BCov && $ECov > $CCov && $ECov > $HCov && $ECov > $ICov && $ECov > $KCov && $ECov > $LCov && $ECov > $WCov && $ECov > $XCov && $ECov > $YCov && $ECov > $ZCov & $cseA_id eq "+" & $cseB_id eq "+" & $cseD_id eq "+" & $cseE_id eq "+" & $cseF_id eq "+" & $cseG_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
    print $head;
    print "$var1\t$varE\t$varE\tcseC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varE eq "E" && $ECov > $ACov && $ECov > $BCov && $ECov > $CCov && $ECov > $HCov && $ECov > $ICov && $ECov > $KCov && $ECov > $LCov && $ECov > $WCov && $ECov > $XCov && $ECov > $YCov && $ECov > $ZCov && ($cseA eq "-" || $cseB eq "-" || $cseD eq "-" || $cseE eq "-" || $cseF eq "-" || $cseG eq "-" || $ctrA eq "-" || $ctrB eq "-" || $ctrC eq "-" || $ctrD eq "-" || $ctrE eq "-" || $ctrF eq "-" )) {
} elsif ($varE eq "E" && $ECov > $ACov && $ECov > $BCov && $ECov > $CCov && $ECov > $HCov && $ECov > $ICov && $ECov > $KCov && $ECov > $LCov && $ECov > $WCov && $ECov > $XCov && $ECov > $YCov && $ECov > $ZCov ) {
    print $head;
    print "$var1\tNG\t$varE\tcseC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
} elsif ($varH eq "H" && $HCov > $ACov && $HCov > $BCov && $HCov > $CCov && $HCov > $ECov && $HCov > $ICov && $HCov > $KCov && $HCov > $LCov && $HCov > $WCov && $HCov > $XCov && $HCov > $YCov && $HCov > $ZCov & $cszA_id eq "+" & $cszB_id eq "+" & $cshD_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
    print $head;
    print "$var1\t$varH\t$varH\tcshC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varH eq "H" && $HCov > $ACov && $HCov > $BCov && $HCov > $CCov && $HCov > $ECov && $HCov > $ICov && $HCov > $KCov && $HCov > $LCov && $HCov > $WCov && $HCov > $XCov && $HCov > $YCov && $HCov > $ZCov && ($cszA eq "-" || $cszB eq "-" || $cshD eq "-" || $ctrA eq "-" || $ctrB eq "-" || $ctrC eq "-" || $ctrD eq "-" || $ctrE eq "-" || $ctrF eq "-" )) {
} elsif ($varH eq "H" && $HCov > $ACov && $HCov > $BCov && $HCov > $CCov && $HCov > $ECov && $HCov > $ICov && $HCov > $KCov && $HCov > $LCov && $HCov > $WCov && $HCov > $XCov && $HCov > $YCov && $HCov > $ZCov ) {
    print $head;
    print "$var1\tNG\t$varH\tcshC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
} elsif ($varI eq "I" && $ICov > $ACov && $ICov > $BCov && $ICov > $CCov && $ICov > $ECov && $ICov > $HCov && $ICov > $KCov && $ICov > $LCov && $ICov > $WCov && $ICov > $XCov && $ICov > $YCov && $ICov > $ZCov & $csiA_id eq "+" & $csiB_id eq "+" & $csiD_id eq "+" & $csiE_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
    print $head;
    print "$var1\t$varI\t$varI\tcsiC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varI eq "I" && $ICov > $ACov && $ICov > $BCov && $ICov > $CCov && $ICov > $ECov && $ICov > $HCov && $ICov > $KCov && $ICov > $LCov && $ICov > $WCov && $ICov > $XCov && $ICov > $YCov && $ICov > $ZCov && ($csiA eq "-" || $csiB eq "-" || $csiD eq "-" || $csiE eq "-" || $ctrA eq "-" || $ctrB eq "-" || $ctrC eq "-" || $ctrD eq "-" || $ctrE eq "-" || $ctrF eq "-" )) {
} elsif ($varI eq "I" && $ICov > $ACov && $ICov > $BCov && $ICov > $CCov && $ICov > $ECov && $ICov > $HCov && $ICov > $KCov && $ICov > $LCov && $ICov > $WCov && $ICov > $XCov && $ICov > $YCov && $ICov > $ZCov ) {
    print $head;
    print "$var1\tNG\t$varI\tcsiC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK
} elsif ($varK eq "K" && $KCov > $ACov && $KCov > $BCov && $KCov > $CCov && $KCov > $ECov && $KCov > $HCov && $KCov > $ICov && $KCov > $LCov && $KCov > $WCov && $KCov > $XCov && $KCov > $YCov && $KCov > $ZCov & $csiA_id eq "+" & $csiB_id eq "+" & $csiD_id eq "+" & $csiE_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
    print $head;
    print "$var1\t$varK\t$varK\tcskC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varK eq "K" && $KCov > $ACov && $KCov > $BCov && $KCov > $CCov && $KCov > $ECov && $KCov > $HCov && $KCov > $ICov && $KCov > $LCov && $KCov > $WCov && $KCov > $XCov && $KCov > $YCov && $KCov > $ZCov && ($csiA eq "-" || $csiB eq "-" || $csiD eq "-" || $csiE eq "-" )) {
} elsif ($varK eq "K" && $KCov > $ACov && $KCov > $BCov && $KCov > $CCov && $KCov > $ECov && $KCov > $HCov && $KCov > $ICov && $KCov > $LCov && $KCov > $WCov && $KCov > $XCov && $KCov > $YCov && $KCov > $ZCov ) {
    print $head;
    print "$var1\tNG\t$varK\tcskC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL
} elsif ($varL eq "L" && $LCov > $ACov && $LCov > $BCov && $LCov > $CCov && $LCov > $ECov && $LCov > $HCov && $LCov > $ICov && $LCov > $KCov && $LCov > $WCov && $LCov > $XCov && $LCov > $YCov && $LCov > $ZCov & $cslA_id eq "+" & $cslB_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
    print $head;
    print "$var1\t$varL\t$varL\tcslC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varL eq "L" && $LCov > $ACov && $LCov > $BCov && $LCov > $CCov && $LCov > $ECov && $LCov > $HCov && $LCov > $ICov && $LCov > $KCov && $LCov > $WCov && $LCov > $XCov && $LCov > $YCov && $LCov > $ZCov && ($cslA eq "-" || $cslB eq "-" )) {
} elsif ($varL eq "L" && $LCov > $ACov && $LCov > $BCov && $LCov > $CCov && $LCov > $ECov && $LCov > $HCov && $LCov > $ICov && $LCov > $KCov && $LCov > $WCov && $LCov > $XCov && $LCov > $YCov && $LCov > $ZCov ) {
    print $head;
    print "$var1\tNG\t$varL\tcslC\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
} elsif ($varW eq "W" && $WCov > $ACov && $WCov > $BCov && $WCov > $CCov && $WCov > $ECov && $WCov > $HCov && $WCov > $ICov && $WCov > $KCov && $WCov > $LCov && $WCov > $XCov && $WCov > $YCov && $WCov > $ZCov & $cssA_id eq "+" & $cssB_id eq "+" & $cssC_id eq "+" & $cssF_id eq "+" & $ctrG_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
    print $head;
    print "$var1\t$varW\t$varW\tcsw\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varW eq "W" && $WCov > $ACov && $WCov > $BCov && $WCov > $CCov && $WCov > $ECov && $WCov > $HCov && $WCov > $ICov && $WCov > $KCov && $WCov > $LCov && $WCov > $XCov && $WCov > $YCov && $WCov > $ZCov && ($cssA_id eq "-" || $cssB_id eq "-" || $cssC_id eq "-" || $cssF_id eq "-" || $ctrG_id eq "-" )) {
} elsif ($varW eq "W" && $WCov > $ACov && $WCov > $BCov && $WCov > $CCov && $WCov > $ECov && $WCov > $HCov && $WCov > $ICov && $WCov > $KCov && $WCov > $LCov && $WCov > $XCov && $WCov > $YCov && $WCov > $ZCov ) {
    print $head;
    print "$var1\tNG\t$varW\tcsw\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
} elsif ($varX eq "X" && $XCov > $ACov && $XCov > $BCov && $XCov > $CCov && $XCov > $ECov && $XCov > $HCov && $XCov > $ICov && $XCov > $KCov && $XCov > $LCov && $XCov > $WCov && $XCov > $YCov && $XCov > $ZCov & $csxA_id eq "+" & $csxC_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
    print $head;
    print "$var1\t$varX\t$varX\tcsxB\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varX eq "X" && $XCov > $ACov && $XCov > $BCov && $XCov > $CCov && $XCov > $ECov && $XCov > $HCov && $XCov > $ICov && $XCov > $KCov && $XCov > $LCov && $XCov > $WCov && $XCov > $YCov && $XCov > $ZCov && ($csxA eq "-" || $csxC eq "-" )) {
} elsif ($varX eq "X" && $XCov > $ACov && $XCov > $BCov && $XCov > $CCov && $XCov > $ECov && $XCov > $HCov && $XCov > $ICov && $XCov > $KCov && $XCov > $LCov && $XCov > $WCov && $XCov > $YCov && $XCov > $ZCov ) {
    print $head;
    print "$var1\tNG\t$varX\tcsxB\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
} elsif ($varY eq "Y" && $YCov > $ACov && $YCov > $BCov && $YCov > $CCov && $YCov > $ECov && $YCov > $HCov && $YCov > $ICov && $YCov > $KCov && $YCov > $LCov && $YCov > $WCov && $YCov > $XCov && $YCov > $ZCov & $cssA_id eq "+" & $cssB_id eq "+" & $cssC_id eq "+" & $cssF_id eq "+" & $ctrG_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
    print $head;
    print "$var1\t$varY\t$varY\tcsy\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varY eq "Y" && $YCov > $ACov && $YCov > $BCov && $YCov > $CCov && $YCov > $ECov && $YCov > $HCov && $YCov > $ICov && $YCov > $KCov && $YCov > $LCov && $YCov > $WCov && $YCov > $XCov && $YCov > $ZCov && ($cssA_id eq "-" || $cssB_id eq "-" || $cssC_id eq "-" || $cssF_id eq "-" || $ctrG_id eq "-" )) {
} elsif ($varY eq "Y" && $YCov > $ACov && $YCov > $BCov && $YCov > $CCov && $YCov > $ECov && $YCov > $HCov && $YCov > $ICov && $YCov > $KCov && $YCov > $LCov && $YCov > $WCov && $YCov > $XCov && $YCov > $ZCov ) {
    print $head;
    print "$var1\tNG\t$varY\tcsy\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ
} elsif ($varZ eq "Z" && $ZCov > $ACov && $ZCov > $BCov && $ZCov > $CCov && $ZCov > $ECov && $ZCov > $HCov && $ZCov > $ICov && $ZCov > $KCov && $ZCov > $LCov && $ZCov > $WCov && $ZCov > $XCov && $ZCov > $YCov & $cszA_id eq "+" & $cszB_id eq "+" & $cszC_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
    print $head;
    print "$var1\t$varZ\t$varZ\tcszD\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#} elsif ($varZ eq "Z" && $ZCov > $ACov && $ZCov > $BCov && $ZCov > $CCov && $ZCov > $ECov && $ZCov > $HCov && $ZCov > $ICov && $ZCov > $KCov && $ZCov > $LCov && $ZCov > $WCov && $ZCov > $XCov && $ZCov > $YCov && ($cszA eq "-" || $cszB eq "-" || $cszC eq "-" )) {
} elsif ($varZ eq "Z" && $ZCov > $ACov && $ZCov > $BCov && $ZCov > $CCov && $ZCov > $ECov && $ZCov > $HCov && $ZCov > $ICov && $ZCov > $KCov && $ZCov > $LCov && $ZCov > $WCov && $ZCov > $XCov && $ZCov > $YCov ) {
    print $head;
    print "$var1\tNG\t$varZ\tcszD\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

#####################################################????????????????????????????????????????????????????????????
} else {
    print $head;
    #print "Low Coverage! Can't infer serotype!";
    print "$var1\t$varNt\tTESTNm?\tNm?\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

}
