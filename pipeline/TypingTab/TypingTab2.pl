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
my $CovMin = 0;
my $pid = 95;
my $paln = 95;
my $varISO = 0;
my $head = "Sequence_File\tBased_SG\tBased_SG\tGrouping_Gene\tA\tB\tC\tE\tH\tI\tK\tL\tW\tX\tY\tZ\tcsaA\tcsaB\tcsaC\tcsaD\tcsb\tcsc\tcseA\tcseB\tcseC\tcseD\tcseE\tcseF\tcseG\tcshC\tcshD\tcsiA\tcsiB\tcsiC\tcsiD\tcsiE\tcskC\tcslA\tcslB\tcslC\tcssA\tcssB\tcssC\tcssE\tcssF\tcsw\tcsxA\tcsxB\tcsxC\tcsy\tcszA\tcszB\tcszC\tcszD\tctrG\tgalE\ttex\tctrA\tctrB\tctrC\tctrD\tctrE\tctrF\trfbA\trfbB\trfbC\tsodC\t16S\tISO\tG1\tG2\tG3\tG4\tG5\tG6\tG7\tG8\tctrE\tctrF\tctrA\tctrB\tctrC\tctrD\trfbA\trfbB\trfbC\tgalE\ttex\tsodC\t16S\n";
my $var1 = substr($ARGV[0], 0, -11);
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


#PID
#AAAA
my $csaAPID = "-";   
my $csaBPID = "-";   
my $csaCPID = "-";   
my $csaDPID = "-";
#BBBB
my $cssAPID = "-";   
my $cssBPID = "-";   
my $cssCPID = "-"; 
my $csbPID = "-";   
my $ctrGPID = "-";   
#CCCC 
my $cscPID = "-";   
my $cssEPID = "-";   
#EEEE
my $cseAPID = "-";   
my $cseBPID = "-";  
my $cseCPID = "-";  
my $cseDPID = "-";   
my $cseEPID = "-";   
my $cseFPID = "-";   
my $cseGPID = "-";   
#WWWW
my $cswPID = "-";  
#XXXX
my $csxAPID = "-";   
my $csxBPID = "-"; 
my $csxCPID = "-";  
#YYYY
my $csyPID = "-";  
my $cssFPID = "-";   
#ZZZZ
my $cszAPID = "-";   
my $cszBPID = "-"; 
my $cszCPID = "-";
my $cszDPID = "-";  

#HIHI
my $csiAPID = "-";   
my $csiBPID = "-";   
my $csiCPID = "-";
my $cshCPID = "-";      
my $csiDPID = "-";   
my $cshDPID = "-";  
my $csiEPID = "-";   
#KLKL
my $cslAPID = "-";   
my $cslBPID = "-";   
my $cslCPID = "-"; 
my $cskCPID = "-";   
#ABCDEF
my $ctrAPID = "-";   
my $ctrBPID = "-";   
my $ctrCPID = "-";   
my $ctrDPID = "-";   
my $ctrEPID = "-";   
my $ctrFPID = "-";   
my $galEPID = "-";   
my $texPID = "-";   
my $rfbAPID = "-";   
my $rfbBPID = "-";  
my $rfbCPID = "-";   
my $sodCPID = "-";  
my $s16SPID = "-";



open $input, $ARGV[0];

foreach $line (<$input>){
    chomp $line;
    @array = split (" ", $line);   
    if ($array[1] =~ m/^A_csaB/ && $array[16] > $CovMin) {
        $varA = "A";
	$cov = sprintf("%.2f", $array[16]);
	#$csaB = join ( ',', 'csaB', $array[17]);
	$csaB = join ( '_', $varA, $cov, $array[17]);
	$csaBPID = $array[17];
	$ACov = $array[16];
    }
        elsif ($array[1] =~ m/^B_csb/ && $array[16] > $CovMin) {
        $varB = "B";
	$cov = sprintf("%.2f", $array[16]);
	#$csb  = join ( ',', 'csb', $array[17]);
	$csb  = join ( '_', $varB, $cov, $array[17]);
	$csbPID = $array[17];
	$BCov = $array[16];
    }
        elsif ($array[1] =~ m/^C_csc/ && $array[16] > $CovMin) {
        $varC = "C";
	$cov = sprintf("%.2f", $array[16]);
	#$csc = join ( ',', 'csc', $array[17]);
	$csc = join ( '_', $varC, $cov, $array[17]);
	$cscPID = $array[17];
	$CCov = $array[16];
    }
        elsif ($array[1] =~ m/^E_cseC/ && $array[16] > $CovMin) {
        $varE = "E";
	$cov = sprintf("%.2f", $array[16]);
	#$cseC = join ( ',', 'cseC', $array[17]);
	$cseC = join ( '_', $varE, $cov, $array[17]);
	$cseCPID = $array[17];
	$ECov = $array[16];
    }
        elsif ($array[1] =~ m/^H_cshC/ && $array[16] > $CovMin) {
        $varH = "H";
	$cov = sprintf("%.2f", $array[16]);
	#$cshC = join ( ',', 'cshC', $array[17]);
	$cshC = join ( '_', $varH, $cov, $array[17]);
	$cshCPID = $array[17];
	$HCov = $array[16];
    }
         elsif ($array[1] =~ m/^I_csiC/ && $array[16] > $CovMin) {
        $varI = "I";
	$cov = sprintf("%.2f", $array[16]);
	#$csiC = join ( ',', 'csiC', $array[17]);
	$csiC = join ( '_', $varI, $cov, $array[17]);
	$csiCPID = $array[17];
	$ICov = $array[16];
    }
        elsif ($array[1] =~ m/^K_cskC/ && $array[16] > $CovMin) {
        $varK = "K";
	$cov = sprintf("%.2f", $array[16]);
	#$cskC = join ( ',', 'cskC', $array[17]);
	$cskC = join ( '_', $varK, $cov, $array[17]);
	$cskCPID = $array[17];
	$KCov = $array[16];
    }
        elsif ($array[1] =~ m/^L_cslC/ && $array[16] > $CovMin) {
        $varL = "L";
	$cov = sprintf("%.2f", $array[16]);
	#$cslC = join ( ',', 'cslC', $array[17]);
	$cslC = join ( '_', $varL, $cov, $array[17]);
	$cslCPID = $array[17];
	$LCov = $array[16];
    }
       elsif ($array[1] =~ m/^W_csw/ && $array[16] > $CovMin) {
        $varW = "W";
	$cov = sprintf("%.2f", $array[16]);
	#$csw = join ( ',', 'csw', $array[17]);
	$csw = join ( '_', $varW, $cov, $array[17]);
	$cswPID = $array[17];
	$WCov = $array[16];
    }
        elsif ($array[1] =~ m/^X_csxB/ && $array[16] > $CovMin) {
        $varX = "X";
	$cov = sprintf("%.2f", $array[16]);
	#$csxB = join ( ',', 'csxB', $array[17]);
	$csxB = join ( '_', $varX, $cov, $array[17]);
	$csxBPID = $array[17];
	$XCov = $array[16];
    }
        elsif ($array[1] =~ m/^Y_csy/ && $array[16] > $CovMin) {
        $varY = "Y";
	$cov = sprintf("%.2f", $array[16]);
	#$csy = join ( ',', 'csy', $array[17]);
	$csy = join ( '_', $varY, $cov, $array[17]);
	$csyPID = $array[17];
	$YCov = $array[16];
    }
        elsif ($array[1] =~ m/^Z_cszD/ && $array[16] > $CovMin) {
        $varZ = "Z";
	$cov = sprintf("%.2f", $array[16]);
	#$cszD = join ( ',', 'cszD', $array[17]);
	$cszD = join ( '_', $varZ, $cov, $array[17]);
	$cszDPID = $array[17];
	$ZCov = $array[16];
    }
}

open $input2, $ARGV[0];

foreach $line2 (<$input2>){
    chomp $line2;
    @array2 = split (" ", $line2);
    if ($array2[1] =~ m/^ctrA_/ && $array2[16] > $CovMin ) {
	$cov = sprintf("%.2f", $array[16]);
	$ctrA = join ( '_', 'ctrA', $cov, $array2[17]);
	$ctrAPID = $array2[17];
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
	$ctrB = join ( '_', 'ctrB', $cov, $array2[17]);
	$ctrBPID = $array2[17];
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
	$ctrC = join ( '_', 'ctrC', $cov, $array2[17]);
	$ctrCPID = $array2[17];
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
        $ctrD = join ( '_', 'ctrD', $cov, $array2[17]);
	$ctrDPID = $array2[17];
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
        $ctrE = join ( '_', 'ctrE', $cov, $array2[17]);
	$ctrEPID = $array2[17];
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
        $ctrF = join ( '_', 'ctrF', $cov, $array2[17]);
	$ctrFPID = $array2[17];
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
        $galE = join ( '_', 'galE', $cov, $array2[17]);
	$galEPID = $array2[17];
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
        $tex = join ( '_', 'tex', $cov, $array2[17]);
	$texPID = $array2[17];
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
	$rfbC = join ( '_', 'rfbC', $cov, $array2[17]);
	$rfbCPID = $array2[17];
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
	$rfbA = join ( '_', 'rfbA', $cov, $array2[17]);
	$rfbAPID = $array2[17];
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
        $rfbB = join ( '_', 'rfbB', $cov, $array2[17]);
	$rfbBPID = $array2[17];
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
        $sodC = join ( '_', 'sodC', $cov, $array2[17]);
	$sodCPID = $array2[17];
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
        $csaA = join ( '_', 'csaA', $cov, $array2[17]);
	$csaAPID = $array2[17];
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
        $csaC = join ( '_', 'csaC', $cov, $array2[17]);
	$csaCPID = $array2[17];
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
        $csaD = join ( '_', 'csaD', $cov, $array2[17]);
	$csaDPID = $array2[17];
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
        $cssA = join ( '_', 'cssA', $cov, $array2[17]);
	$cssAPID = $array2[17];
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
        $cssB = join ( '_', 'cssB', $cov, $array2[17]);
	$cssBPID = $array2[17];
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
        $cssC = join ( '_', 'cssC', $cov, $array2[17]);
	$cssCPID = $array2[17];
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
        $ctrG = join ( '_', 'ctrG', $cov, $array2[17]);
	$ctrGPID = $array2[17];
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
        $cssE = join ( '_', 'cssE', $cov, $array2[17]);
	$cssEPID = $array2[17];
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
        $cseA = join ( '_', 'cseA', $cov, $array2[17]);
	$cseAPID = $array2[17];
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
        $cseB = join ( '_', 'cseB', $cov, $array2[17]);
	$cseBPID = $array2[17];
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
        $cseD = join ( '_', 'cseD', $cov, $array2[17]);
	$cseDPID = $array2[17];
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
        $cseE = join ( '_', 'cseE', $cov, $array2[17]);
	$cseEPID = $array2[17];
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
        $cseF = join ( '_', 'cseF', $cov, $array2[17]);
	$cseFPID = $array2[17];
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
        $cseG = join ( '_', 'cseG', $cov, $array2[17]);
	$cseGPID = $array2[17];
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
        $cshD = join ( '_', 'cshD', $cov, $array2[17]);
	$cshDPID = $array2[17];
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
        $cszA = join ( '_', 'cszA', $cov, $array2[17]);
	$cszAPID = $array2[17];
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
        $cszB = join ( '_', 'cszB', $cov, $array2[17]);
	$cszBPID = $array2[17];
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
        $csiA = join ( '_', 'csiA', $cov, $array2[17]);
	$csiAPID = $array2[17];
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
        $csiB = join ( '_', 'csiB', $cov, $array2[17]);
	$csiBPID = $array2[17];
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
        $csiD = join ( '_', 'csiD', $cov, $array2[17]);
	$csiDPID = $array2[17];
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
        $csiE = join ( '_', 'csiE', $cov, $array2[17]);
	$csiEPID = $array2[17];
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
        $cslA = join ( '_', 'cslA', $cov, $array2[17]);
	$cslAPID = $array2[17];
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
        $cslB = join ( '_', 'cslB', $cov, $array2[17]);
	$cslBPID = $array2[17];
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
        $cssF = join ( '_', 'cssF', $cov, $array2[17]);
	$cssFPID = $array2[17];
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
        $csxA = join ( '_', 'csxA', $cov, $array2[17]);
	$csxAPID = $array2[17];
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
        $csxC = join ( '_', 'csxC', $cov, $array2[17]);
	$csxCPID = $array2[17];
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
        $cszC = join ( '_', 'cszC', $cov, $array2[17]);
	$cszCPID = $array2[17]; 
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
	$s16S = join ( '_', 's16S', $cov, $array2[17]);
	$s16SPID = $array2[17];
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
    print "$var1\tNA\tNA\tNA\t";
    print "$csaB\t$csb\t$csc\t$cseC\t$cshC\t$csiC\t$cskC\t$cslC\t$csw\t$csxB\t$csy\t$cszD\t";
    print "$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\t";
    print "-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t$galEPID\t$texPID\t$sodCPID\t$s16SPID\n";    

    #print "Can't infer serotype!"; 
    #print "$var1\t$varNt\t-\t-\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\n";

#####################################################AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
#} elsif ($varA eq "A" && $ACov > $BCov && $ACov > $CCov && $ACov > $ECov && $ACov > $HCov && $ACov > $ICov && $ACov > $KCov && $ACov > $LCov && $ACov > $WCov && $ACov > $XCov && $ACov > $YCov && $ACov > $ZCov & $csaA_id eq "+" & $csaC_id eq "+" & $csaD_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
} elsif ($varA eq "A" && $ACov > $BCov && $ACov > $CCov && $ACov > $ECov && $ACov > $HCov && $ACov > $ICov && $ACov > $KCov && $ACov > $LCov && $ACov > $WCov && $ACov > $XCov && $ACov > $YCov && $ACov > $ZCov ) {
    print $head;
    print "$var1\t$varA\t$varA\tcsaB\t";
    print "$csaB\t$csb\t$csc\t$cseC\t$cshC\t$csiC\t$cskC\t$cslC\t$csw\t$csxB\t$csy\t$cszD\t";
    print "$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\t";
    print "$csaAPID\t$csaBPID\t$csaCPID\t$csaDPID\tNA\tNA\tNA\tNA\t";
    print "$ctrEPID\t$ctrFPID\t$ctrAPID\t$ctrBPID\t$ctrCPID\t$ctrDPID\t$rfbAPID\t$rfbBPID\t$rfbCPID\t$galEPID\t$texPID\t$sodCPID\t$s16SPID\n";

#####################################################BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
#} elsif ($varB eq "B" && $BCov > $ACov && $BCov > $CCov && $BCov > $ECov && $BCov > $HCov && $BCov > $ICov && $BCov > $KCov && $BCov > $LCov && $BCov > $WCov && $BCov > $XCov && $BCov > $YCov && $BCov > $ZCov & $cssA_id eq "+" & $cssB_id eq "+" & $cssC_id eq "+" & $ctrG_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
} elsif ($varB eq "B" && $BCov > $ACov && $BCov > $CCov && $BCov > $ECov && $BCov > $HCov && $BCov > $ICov && $BCov > $KCov && $BCov > $LCov && $BCov > $WCov && $BCov > $XCov && $BCov > $YCov && $BCov > $ZCov ) {
    print $head;
    print "$var1\t$varB\t$varB\tcsb\t";
    print "$csaB\t$csb\t$csc\t$cseC\t$cshC\t$csiC\t$cskC\t$cslC\t$csw\t$csxB\t$csy\t$cszD\t";
    print "$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\t";
    print "$cssAPID\t$cssBPID\t$cssCPID\t$csbPID\t$ctrGPID\tNA\tNA\tNA\t";
    print "$ctrEPID\t$ctrFPID\t$ctrAPID\t$ctrBPID\t$ctrCPID\t$ctrDPID\t$rfbAPID\t$rfbBPID\t$rfbCPID\t$galEPID\t$texPID\t$sodCPID\t$s16SPID\n";

#####################################################CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
#} elsif ($varC eq "C" && $CCov > $ACov && $CCov > $BCov && $CCov > $ECov && $CCov > $HCov && $CCov > $ICov && $CCov > $KCov && $CCov > $LCov && $CCov > $WCov && $CCov > $XCov && $CCov > $YCov && $CCov > $ZCov & $cssA_id eq "+" & $cssB_id eq "+" & $cssC_id eq "+" & $cssE_id eq "+" & $ctrG_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
} elsif ($varC eq "C" && $CCov > $ACov && $CCov > $BCov && $CCov > $ECov && $CCov > $HCov && $CCov > $ICov && $CCov > $KCov && $CCov > $LCov && $CCov > $WCov && $CCov > $XCov && $CCov > $YCov && $CCov > $ZCov ) {
    print $head;
    print "$var1\t$varC\t$varC\tcsc\t";
    print "$csaB\t$csb\t$csc\t$cseC\t$cshC\t$csiC\t$cskC\t$cslC\t$csw\t$csxB\t$csy\t$cszD\t";
    print "$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\t";
    print "$cssAPID\t$cssBPID\t$cssCPID\t$cscPID\t$cssEPID\t$ctrGPID\tNA\tNA\t";
    print "$ctrEPID\t$ctrFPID\t$ctrAPID\t$ctrBPID\t$ctrCPID\t$ctrDPID\t$rfbAPID\t$rfbBPID\t$rfbCPID\t$galEPID\t$texPID\t$sodCPID\t$s16SPID\n";

#####################################################EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
#} elsif ($varE eq "E" && $ECov > $ACov && $ECov > $BCov && $ECov > $CCov && $ECov > $HCov && $ECov > $ICov && $ECov > $KCov && $ECov > $LCov && $ECov > $WCov && $ECov > $XCov && $ECov > $YCov && $ECov > $ZCov & $cseA_id eq "+" & $cseB_id eq "+" & $cseD_id eq "+" & $cseE_id eq "+" & $cseF_id eq "+" & $cseG_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
} elsif ($varE eq "E" && $ECov > $ACov && $ECov > $BCov && $ECov > $CCov && $ECov > $HCov && $ECov > $ICov && $ECov > $KCov && $ECov > $LCov && $ECov > $WCov && $ECov > $XCov && $ECov > $YCov && $ECov > $ZCov ) {
    print $head;
    print "$var1\t$varE\t$varE\tcseC\t";
    print "$csaB\t$csb\t$csc\t$cseC\t$cshC\t$csiC\t$cskC\t$cslC\t$csw\t$csxB\t$csy\t$cszD\t";
    print "$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\t";
    print "$cseAPID\t$cseBPID\t$cseCPID\t$cseDPID\t$cseEPID\t$cseFPID\t$cseGPID\t$galEPID\t";
    print "$ctrEPID\t$ctrFPID\t$ctrAPID\t$ctrBPID\t$ctrCPID\t$ctrDPID\t$rfbAPID\t$rfbBPID\t$rfbCPID\t$galEPID\t$texPID\t$sodCPID\t$s16SPID\n";
#####################################################HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
#} elsif ($varH eq "H" && $HCov > $ACov && $HCov > $BCov && $HCov > $CCov && $HCov > $ECov && $HCov > $ICov && $HCov > $KCov && $HCov > $LCov && $HCov > $WCov && $HCov > $XCov && $HCov > $YCov && $HCov > $ZCov & $cszA_id eq "+" & $cszB_id eq "+" & $cshD_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
} elsif ($varH eq "H" && $HCov > $ACov && $HCov > $BCov && $HCov > $CCov && $HCov > $ECov && $HCov > $ICov && $HCov > $KCov && $HCov > $LCov && $HCov > $WCov && $HCov > $XCov && $HCov > $YCov && $HCov > $ZCov ) {
    print $head;
    print "$var1\t$varH\t$varH\tcshC\t"; 
    print "$csaB\t$csb\t$csc\t$cseC\t$cshC\t$csiC\t$cskC\t$cslC\t$csw\t$csxB\t$csy\t$cszD\t";
    print "$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\t";
    print "$cszAPID\t$cszBPID\t$cshCPID\t$cshDPID\tNA\tNA\tNA\tNA\t";
    print "$ctrEPID\t$ctrFPID\t$ctrAPID\t$ctrBPID\t$ctrCPID\t$ctrDPID\t$rfbAPID\t$rfbBPID\t$rfbCPID\t$galEPID\t$texPID\t$sodCPID\t$s16SPID\n";

#####################################################IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
#} elsif ($varI eq "I" && $ICov > $ACov && $ICov > $BCov && $ICov > $CCov && $ICov > $ECov && $ICov > $HCov && $ICov > $KCov && $ICov > $LCov && $ICov > $WCov && $ICov > $XCov && $ICov > $YCov && $ICov > $ZCov & $csiA_id eq "+" & $csiB_id eq "+" & $csiD_id eq "+" & $csiE_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
} elsif ($varI eq "I" && $ICov > $ACov && $ICov > $BCov && $ICov > $CCov && $ICov > $ECov && $ICov > $HCov && $ICov > $KCov && $ICov > $LCov && $ICov > $WCov && $ICov > $XCov && $ICov > $YCov && $ICov > $ZCov ) {
    print $head;
    print "$var1\t$varI\t$varI\tcsiC\t";
    print "$csaB\t$csb\t$csc\t$cseC\t$cshC\t$csiC\t$cskC\t$cslC\t$csw\t$csxB\t$csy\t$cszD\t";
    print "$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\t";
    print "$csiAPID\t$csiBPID\t$csiCPID\t$csiDPID\t$csiEPID\tNA\tNA\tNA\t";
    print "$ctrEPID\t$ctrFPID\t$ctrAPID\t$ctrBPID\t$ctrCPID\t$ctrDPID\t$rfbAPID\t$rfbBPID\t$rfbCPID\t$galEPID\t$texPID\t$sodCPID\t$s16SPID\n";

#####################################################KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK
#} elsif ($varK eq "K" && $KCov > $ACov && $KCov > $BCov && $KCov > $CCov && $KCov > $ECov && $KCov > $HCov && $KCov > $ICov && $KCov > $LCov && $KCov > $WCov && $KCov > $XCov && $KCov > $YCov && $KCov > $ZCov & $csiA_id eq "+" & $csiB_id eq "+" & $csiD_id eq "+" & $csiE_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
} elsif ($varK eq "K" && $KCov > $ACov && $KCov > $BCov && $KCov > $CCov && $KCov > $ECov && $KCov > $HCov && $KCov > $ICov && $KCov > $LCov && $KCov > $WCov && $KCov > $XCov && $KCov > $YCov && $KCov > $ZCov ) {
    print $head;
    print "$var1\t$varK\t$varK\tcskC\t";
    print "$csaB\t$csb\t$csc\t$cseC\t$cshC\t$csiC\t$cskC\t$cslC\t$csw\t$csxB\t$csy\t$cszD\t";
    print "$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\t";
    print "$csiAPID\t$csiBPID\t$cskCPID\t$csiDPID\t$csiEPID\tNA\tNA\tNA\t";
    print "$ctrEPID\t$ctrFPID\t$ctrAPID\t$ctrBPID\t$ctrCPID\t$ctrDPID\t$rfbAPID\t$rfbBPID\t$rfbCPID\t$galEPID\t$texPID\t$sodCPID\t$s16SPID\n";

#####################################################LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL
#} elsif ($varL eq "L" && $LCov > $ACov && $LCov > $BCov && $LCov > $CCov && $LCov > $ECov && $LCov > $HCov && $LCov > $ICov && $LCov > $KCov && $LCov > $WCov && $LCov > $XCov && $LCov > $YCov && $LCov > $ZCov & $cslA_id eq "+" & $cslB_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
} elsif ($varL eq "L" && $LCov > $ACov && $LCov > $BCov && $LCov > $CCov && $LCov > $ECov && $LCov > $HCov && $LCov > $ICov && $LCov > $KCov && $LCov > $WCov && $LCov > $XCov && $LCov > $YCov && $LCov > $ZCov ) {
    print $head;
    print "$var1\t$varL\t$varL\tcslC\t";
    print "$csaB\t$csb\t$csc\t$cseC\t$cshC\t$csiC\t$cskC\t$cslC\t$csw\t$csxB\t$csy\t$cszD\t";
    print "$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\t";
    print "$cslAPID\t$cslBPID\t$cslCPID\tNA\tNA\tNA\tNA\tNA\t";
    print "$ctrEPID\t$ctrFPID\t$ctrAPID\t$ctrBPID\t$ctrCPID\t$ctrDPID\t$rfbAPID\t$rfbBPID\t$rfbCPID\t$galEPID\t$texPID\t$sodCPID\t$s16SPID\n";

#####################################################WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
#} elsif ($varW eq "W" && $WCov > $ACov && $WCov > $BCov && $WCov > $CCov && $WCov > $ECov && $WCov > $HCov && $WCov > $ICov && $WCov > $KCov && $WCov > $LCov && $WCov > $XCov && $WCov > $YCov && $WCov > $ZCov & $cssA_id eq "+" & $cssB_id eq "+" & $cssC_id eq "+" & $cssF_id eq "+" & $ctrG_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
} elsif ($varW eq "W" && $WCov > $ACov && $WCov > $BCov && $WCov > $CCov && $WCov > $ECov && $WCov > $HCov && $WCov > $ICov && $WCov > $KCov && $WCov > $LCov && $WCov > $XCov && $WCov > $YCov && $WCov > $ZCov ) {
    print $head;
    print "$var1\t$varW\t$varW\tcsw\t";
    print "$csaB\t$csb\t$csc\t$cseC\t$cshC\t$csiC\t$cskC\t$cslC\t$csw\t$csxB\t$csy\t$cszD\t";
    print "$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\t";
    print "$cssAPID\t$cssBPID\t$cssCPID\t$cswPID\t$cssFPID\t$ctrGPID\tNA\tNA\t";
    print "$ctrEPID\t$ctrFPID\t$ctrAPID\t$ctrBPID\t$ctrCPID\t$ctrDPID\t$rfbAPID\t$rfbBPID\t$rfbCPID\t$galEPID\t$texPID\t$sodCPID\t$s16SPID\n";

#####################################################XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#} elsif ($varX eq "X" && $XCov > $ACov && $XCov > $BCov && $XCov > $CCov && $XCov > $ECov && $XCov > $HCov && $XCov > $ICov && $XCov > $KCov && $XCov > $LCov && $XCov > $WCov && $XCov > $YCov && $XCov > $ZCov & $csxA_id eq "+" & $csxC_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
} elsif ($varX eq "X" && $XCov > $ACov && $XCov > $BCov && $XCov > $CCov && $XCov > $ECov && $XCov > $HCov && $XCov > $ICov && $XCov > $KCov && $XCov > $LCov && $XCov > $WCov && $XCov > $YCov && $XCov > $ZCov ) {
    print $head;
    print "$var1\t$varX\t$varX\tcsxB\t"; 
    print "$csaB\t$csb\t$csc\t$cseC\t$cshC\t$csiC\t$cskC\t$cslC\t$csw\t$csxB\t$csy\t$cszD\t";
    print "$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\t";
    print "$csxAPID\t$csxBPID\t$csxCPID\tNA\tNA\tNA\tNA\tNA\t";
    print "$ctrEPID\t$ctrFPID\t$ctrAPID\t$ctrBPID\t$ctrCPID\t$ctrDPID\t$rfbAPID\t$rfbBPID\t$rfbCPID\t$galEPID\t$texPID\t$sodCPID\t$s16SPID\n";

#####################################################YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
#} elsif ($varY eq "Y" && $YCov > $ACov && $YCov > $BCov && $YCov > $CCov && $YCov > $ECov && $YCov > $HCov && $YCov > $ICov && $YCov > $KCov && $YCov > $LCov && $YCov > $WCov && $YCov > $XCov && $YCov > $ZCov & $cssA_id eq "+" & $cssB_id eq "+" & $cssC_id eq "+" & $cssF_id eq "+" & $ctrG_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
} elsif ($varY eq "Y" && $YCov > $ACov && $YCov > $BCov && $YCov > $CCov && $YCov > $ECov && $YCov > $HCov && $YCov > $ICov && $YCov > $KCov && $YCov > $LCov && $YCov > $WCov && $YCov > $XCov && $YCov > $ZCov ) {
    print $head;
    print "$var1\t$varY\t$varY\tcsy\t";
    print "$csaB\t$csb\t$csc\t$cseC\t$cshC\t$csiC\t$cskC\t$cslC\t$csw\t$csxB\t$csy\t$cszD\t";
    print "$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\t";
    print "$cssAPID\t$cssBPID\t$cssCPID\t$csyPID\t$cssFPID\t$ctrGPID\tNA\tNA\t";
    print "$ctrEPID\t$ctrFPID\t$ctrAPID\t$ctrBPID\t$ctrCPID\t$ctrDPID\t$rfbAPID\t$rfbBPID\t$rfbCPID\t$galEPID\t$texPID\t$sodCPID\t$s16SPID\n";

#####################################################ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ
#} elsif ($varZ eq "Z" && $ZCov > $ACov && $ZCov > $BCov && $ZCov > $CCov && $ZCov > $ECov && $ZCov > $HCov && $ZCov > $ICov && $ZCov > $KCov && $ZCov > $LCov && $ZCov > $WCov && $ZCov > $XCov && $ZCov > $YCov & $cszA_id eq "+" & $cszB_id eq "+" & $cszC_id eq "+" & $ctrA_id eq "+" & $ctrB_id eq "+" & $ctrC_id eq "+" & $ctrD_id eq "+" & $ctrE_id eq "+" & $ctrF_id eq "+" ) {
} elsif ($varZ eq "Z" && $ZCov > $ACov && $ZCov > $BCov && $ZCov > $CCov && $ZCov > $ECov && $ZCov > $HCov && $ZCov > $ICov && $ZCov > $KCov && $ZCov > $LCov && $ZCov > $WCov && $ZCov > $XCov && $ZCov > $YCov ) {
    print $head;
    print "$var1\t$varZ\t$varZ\tcszD\t";
    print "$csaB\t$csb\t$csc\t$cseC\t$cshC\t$csiC\t$cskC\t$cslC\t$csw\t$csxB\t$csy\t$cszD\t";
    print "$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\t";
    print "$cszAPID\t$cszBPID\t$cszCPID\t$cszDPID\tNA\tNA\tNA\tNA\t";
    print "$ctrEPID\t$ctrFPID\t$ctrAPID\t$ctrBPID\t$ctrCPID\t$ctrDPID\t$rfbAPID\t$rfbBPID\t$rfbCPID\t$galEPID\t$texPID\t$sodCPID\t$s16SPID\n";

#####################################################????????????????????????????????????????????????????????????
} else {
    print $head;
    #print "Low Coverage! Can't infer serotype!";
    print "$var1\t$varNt\tTESTNm?\tNm?\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$s16S\t$varISO\n";

}
