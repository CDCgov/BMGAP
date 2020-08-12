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
my $thd = 85;
my $head = "Sequence_File\tInferred_SG\tBased_SG\tGrouping_Gene\t%ID\tlen\tslen\t%Aln\tcsaA\tcsaB\tcsaC\tcsaD\tcsb\tcsc\tcseA\tcseB\tcseC\tcseD\tcseE\tcseF\tcseG\tcshC\tcshD\tcsiA\tcsiB\tcsiC\tcsiD\tcsiE\tcskC\tcslA\tcslB\tcslC\tcssA\tcssB\tcssC\tcssE\tcssF\tcsw\tcsxA\tcsxB\tcsxC\tcsy\tcszA\tcszB\tcszC\tcszD\tctrG\tgalE\ttex\tctrA\tctrB\tctrC\tctrD\tctrE\tctrF\trfbA\trfbB\trfbC\tsodC\t16S\n";
my $var1 = substr($ARGV[0], 0, -11);
my $varA = "no";
my $Anum;
my $Alen;
my $ASlen;
my $APer;
my $ARnd;
my $ABit = 0;
my $varB = "no";
my $Bnum;
my $Blen;
my $BSlen;
my $BPer;
my $BRnd;
my $BBit = 0;
my $varC = "no";
my $Cnum;
my $Clen;
my $CSlen;
my $CPer;
my $CRnd;
my $CBit = 0;
my $varE = "no";
my $Enum;
my $Elen;
my $ESlen;
my $EPer;
my $ERnd;
my $EBit = 0;
my $varH = "no";
my $Hnum;
my $Hlen;
my $HSlen;
my $HPer;
my $HRnd;
my $HBit = 0;
my $varI = "no";
my $Inum;
my $Ilen;
my $ISlen;
my $IPer;
my $IRnd;
my $IBit = 0;
my $varK = "no";
my $Knum;
my $Klen;
my $KSlen;
my $KPer;
my $KRnd;
my $KBit = 0;
my $varL = "no";
my $Lnum;
my $Llen;
my $LSlen;
my $LPer;
my $LRnd;
my $LBit = 0;
my $varW = "no";
my $Wnum;
my $Wlen;
my $WSlen;
my $WPer;
my $WRnd;
my $WBit = 0;
my $varX = "no";
my $Xnum;
my $Xlen;
my $XSlen;
my $XPer;
my $XRnd;
my $XBit = 0;
my $varY = "no";
my $Ynum;
my $YSlen;
my $YPer;
my $YRnd;
my $Ylen;
my $YBit = 0;
my $varZ = "no";
my $Znum;
my $ZSlen;
my $ZPer;
my $ZRnd;
my $Zlen;
my $ZBit = 0;
#################
my $var16S = "no";
my $var16Snum;
my $var16SSlen;
my $var16SPer;
my $var16SRnd;
my $var16Slen;
my $var16SBit = 0;
#################
my $varNt = "ng";
my $Ntnum = "-";
my $Ntlen = "-";
my $NtSlen = "-";
my $NtPer = "-";
my $sodC = "-";
my $rfbC = "-";
my $rfbA = "-";
my $rfbB = "-";
my $galE = "-";
my $ctrA = "-";
my $ctrB = "-";
my $ctrC = "-";
my $ctrD = "-";
my $tex = "-";
my $galE2 = "-";
my $rfbB2 = "-";
my $rfbA2 = "-";
my $rfbC2 = "-";
my $ctrE = "-";
my $ctrF = "-";
my $s16S = "-";
#AAAAAAAAAAAAAA
my $csaD = "-";
my $csaC = "-";
my $csaB = "-";
my $csaA = "-";
#BBBBBBBBBBBBBB
my $ctrG = "-";
my $csb = "-";
my $cssC = "-";
my $cssB = "-";
my $cssA = "-";
#CCCCCCCCCCCCCC
my $cssE = "-";
my $csc = "-";
#EEEEEEEEEEEEEE
my $cseG = "-";
my $cseF = "-";
my $cseE = "-";
my $cseD = "-";
my $cseC = "-";
my $cseB = "-";
my $cseA = "-";
#HHHHHHHHHHHHHH
my $cshD = "-";
my $cshC = "-";
my $cszB = "-";
my $cszA = "-";
#IIIIIIIIIIIIII
my $csiA = "-"; 
my $csiB = "-"; 
my $csiC = "-"; 
my $csiD = "-"; 
my $csiE = "-"; 
#KKKKKKKKKKKKKK
my $cskC = "-"; 
#LLLLLLLLLLLLLL
my $cslC = "-";
my $cslB = "-";
my $cslA = "-";
#WWWWWWWWWWWWWW
my $cssF = "-";
my $csw = "-";
#XXXXXXXXXXXXXX
my $csxC = "-";
my $csxB = "-";
my $csxA = "-";
#YYYYYYYYYYYYYY
my $csy = "-";
#ZZZZZZZZZZZZZZ
my $cszD = "-";
my $cszC = "-";

#my @filename; 


open $input, $ARGV[0];

#@filename = split (/-/, $var1);
#$var1 = $filename[0];

foreach $line (<$input>){
    chomp $line;
    @array = split (" ", $line);   
    if ($array[1] =~ m/^A_csaB/) {
        $varA = "A";
	$csaB = "+";
	$Anum = $array[2];
	$Alen = $array[3];
	$ASlen = $array[5];
	$APer = ($Alen/$ASlen)*100;
	$ARnd = sprintf("%.2f", $APer);
	$ABit = $array[13];
    }
        elsif ($array[1] =~ m/^B_csb/) {
        $varB = "B";
	$csb  = "+";
	$Bnum = $array[2];
	$Blen = $array[3];
	$BSlen = $array[5];
	$BPer = ($Blen/$BSlen)*100;
	$BRnd = sprintf("%.2f", $BPer);	
	$BBit = $array[13];
    }
        elsif ($array[1] =~ m/^C_csc/) {
        $varC = "C";
	$csc = "+";
	$Cnum = $array[2];
	$Clen = $array[3];
	$CSlen = $array[5];	
	$CPer = ($Clen/$CSlen)*100;	
	$CRnd = sprintf("%.2f", $CPer);	
	$CBit = $array[13];
    }
        elsif ($array[1] =~ m/^E_cseC/) {
        $varE = "E";
	$cseC = "+";
	$Enum = $array[2];
	$Elen = $array[3];
	$ESlen = $array[5];
	$EPer = ($Elen/$ESlen)*100;
	$ERnd = sprintf("%.2f", $EPer);	
	$EBit = $array[13];
    }
        elsif ($array[1] =~ m/^H_cshC/) {
        $varH = "H";
	$cshC = "+";
	$Hnum = $array[2];
	$HSlen = $array[5];	
	$Hlen = $array[3];
	$HPer = ($Hlen/$HSlen)*100;
	$HRnd = sprintf("%.2f", $HPer);
	$HBit = $array[13];
    }
         elsif ($array[1] =~ m/^I_csiC/) {
        $varI = "I";
	$csiC = "+";
	$Inum = $array[2];
	$Ilen = $array[3];
	$ISlen = $array[5];	
	$IPer = ($Ilen/$ISlen)*100;	
	$IBit = $array[13];
    }
        elsif ($array[1] =~ m/^K_cskC/) {
        $varK = "K";
	$cskC = "+";
	$Knum = $array[2];
	$Klen = $array[3];
	$KSlen = $array[5];	
	$KPer = ($Klen/$KSlen)*100;	
	$KRnd = sprintf("%.2f", $KPer);	
	$KBit = $array[13];
    }
        elsif ($array[1] =~ m/^L_cslC/) {
        $varL = "L";
	$cslC = "+";
	$Lnum = $array[2];
	$Llen = $array[3];
	$LSlen = $array[5];	
	$LPer = ($Llen/$LSlen)*100;
	$LRnd = sprintf("%.2f", $LPer);	
	$LBit = $array[13];
    }
       elsif ($array[1] =~ m/^W_csw/) {
        $varW = "W";
	$csw = "+";
	$Wnum = $array[2];
	$Wlen = $array[3];
	$WSlen = $array[5];	
	$WPer = ($Wlen/$WSlen)*100;
	$WRnd = sprintf("%.2f", $WPer);		
	$WBit = $array[13];
    }
        elsif ($array[1] =~ m/^X_csxB/) {
        $varX = "X";
	$csxB = "+";
	$Xnum = $array[2];
	$Xlen = $array[3];
	$XSlen = $array[5];	
	$XPer = ($Xlen/$XSlen)*100;	
	$XRnd = sprintf("%.2f", $XPer);
	$XBit = $array[13];
    }
        elsif ($array[1] =~ m/^Y_csy/) {
        $varY = "Y";
	$csy = "+";
	$Ynum = $array[2];
	$Ylen = $array[3];
	$YSlen = $array[5];	
	$YPer = ($Ylen/$YSlen)*100;	
	$YRnd = sprintf("%.2f", $YPer);
	$YBit = $array[13];
    }
        elsif ($array[1] =~ m/^Z_cszD/) {
        $varZ = "Z";
	$cszD = "+";
	$Znum = $array[2];
	$Zlen = $array[3];
	$ZSlen = $array[5];	
	$ZPer = ($Zlen/$ZSlen)*100;	
	$ZRnd = sprintf("%.2f", $ZPer);
	$ZBit = $array[13];
    }
}

open $input2, $ARGV[0];

foreach $line2 (<$input2>){
    chomp $line2;
    @array2 = split (" ", $line2);
    if ($array2[1] =~ m/^ctrA_/) {
        $ctrA = "+";
    }   
        elsif ($array2[1] =~ m/^ctrB_/) {
        $ctrB = "+";
   }
	elsif ($array2[1] =~ m/^ctrC_/) {
        $ctrC = "+";
   }
	elsif ($array2[1] =~ m/^ctrD_/) {
        $ctrD = "+";
   }
	elsif ($array2[1] =~ m/^ctrE_/) {
        $ctrE = "+";
   }
	elsif ($array2[1] =~ m/^ctrF_/) {
        $ctrF = "+";
   }
	elsif ($array2[1] =~ m/^galE_/) {
        $galE = "+";
   }
	elsif ($array2[1] =~ m/^galE2_/) {
        $galE2 = "+";
   }
	elsif ($array2[1] =~ m/^tex_/) {
        $tex = "+";
   }
	elsif ($array2[1] =~ m/^rfbC_/) {
        $rfbC = "+";
   }
	elsif ($array2[1] =~ m/^rfbA_/) {
        $rfbA = "+";
   }
	elsif ($array2[1] =~ m/^rfbB_/) {
        $rfbB = "+";
   }
	elsif ($array2[1] =~ m/^rfbB2_/) {
        $rfbB2 = "+";
   }
	elsif ($array2[1] =~ m/^rfbA2_/) {
        $rfbA2 = "+";
   }
	elsif ($array2[1] =~ m/^rfbC2_/) {
        $rfbC2 = "+";
   }
	elsif ($array2[1] =~ m/^sodC_/) {
        $sodC = "+";
   }
######AAAAAA
	elsif ($array2[1] =~ m/^A_csaA_/) {
        $csaA = "+";
   }
	elsif ($array2[1] =~ m/^A_csaC_/) {
        $csaC = "+";
   }
	elsif ($array2[1] =~ m/^A_csaD_/) {
        $csaD = "+";
   }
######BBBBBB
	elsif ($array2[1] =~ m/^BCWY_cssA_/) {
        $cssA = "+";
   }
	elsif ($array2[1] =~ m/^BCWY_cssB_/) {
        $cssB = "+";
   }
	elsif ($array2[1] =~ m/^BCWY_cssC_/) {
        $cssC = "+";
   }
	elsif ($array2[1] =~ m/^BCWY_ctrG_/) {
        $ctrG = "+";
   }
######CCCCCC
	elsif ($array2[1] =~ m/^C_cssE_/) {
        $cssE = "+";
   }
######EEEEEE
	elsif ($array2[1] =~ m/^E_cseA_/) {
        $cseA = "+";
   }
	elsif ($array2[1] =~ m/^E_cseB_/) {
        $cseB = "+";
   }
	elsif ($array2[1] =~ m/^E_cseD_/) {
        $cseD = "+";
   }
	elsif ($array2[1] =~ m/^E_cseE_/) {
        $cseE = "+";
   }
	elsif ($array2[1] =~ m/^E_cseF_/) {
        $cseF = "+";
   }
	elsif ($array2[1] =~ m/^E_cseG_/) {
        $cseG = "+";
   }
#####HHHHHH
	elsif ($array2[1] =~ m/^H_cshD_/) {
        $cshD = "+";
   }
	elsif ($array2[1] =~ m/^HZ_cszA_/) {
        $cszA = "+";
   }
	elsif ($array2[1] =~ m/^HZ_cszB_/) {
        $cszB = "+";
   }
#####IIIIII&KKKKKK
	elsif ($array2[1] =~ m/^IK_csiA_/) {
        $csiA = "+";
   }
	elsif ($array2[1] =~ m/^IK_csiB_/) {
        $csiB = "+";
   }
	elsif ($array2[1] =~ m/^IK_csiD_/) {
        $csiD = "+";
   }
	elsif ($array2[1] =~ m/^IK_csiE_/) {
        $csiE = "+";
   }
#####LLLLLL
	elsif ($array2[1] =~ m/^L_cslA_/) {
        $cslA = "+";
   }
	elsif ($array2[1] =~ m/^L_cslB_/) {
        $cslB = "+";
   }
#####WWWWWW
	elsif ($array2[1] =~ m/^WY_cssF_/) {
        $cssF = "+";
   }
#####XXXXXX
	elsif ($array2[1] =~ m/^X_csxA_/) {
        $csxA = "+";
   }
	elsif ($array2[1] =~ m/^X_csxC_/) {
        $csxC = "+";
   }
#####YYYYYY
#####ZZZZZZ
	elsif ($array2[1] =~ m/^Z_cszC_/) {
        $cszC = "+";
   }
#####16S16S
        elsif ($array2[1] =~ m/^16S_rDNA_/) {
        $var16S = "16S";
	$s16S = "+";
	$var16Snum = $array2[2];
	$var16Slen = $array2[3];
	$var16SSlen = $array2[5];	
	$var16SPer = ($var16Slen/$var16SSlen)*100;	
	$var16SRnd = sprintf("%.2f", $var16SPer);
	$var16SBit = $array2[13];
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
    print "$var1\t$varNt\t-\t-\t-\t-\t-\t-\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$var16SRnd\n";

#####################################################AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
} elsif ($varA eq "A" && $ABit > $BBit && $ABit > $CBit && $ABit > $EBit && $ABit > $HBit && $ABit > $IBit && $ABit > $KBit && $ABit > $LBit && $ABit > $WBit && $ABit > $XBit && $ABit > $YBit && $ABit > $ZBit & $csaA eq "+" & $csaB eq "+" & $csaD eq "+" & $ctrA eq "+" & $ctrB eq "+" & $ctrC eq "+" & $ctrD eq "+" & $ctrE eq "+" & $ctrF eq "+" & $ARnd >= $thd) {
    print $head;
    print "$var1\t$varA\t$varA\tcsaB\t$Anum\t$Alen\t$ASlen\t$ARnd\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$var16SRnd\n";

} elsif ($varA eq "A" && $ABit > $BBit && $ABit > $CBit && $ABit > $EBit && $ABit > $HBit && $ABit > $IBit && $ABit > $KBit && $ABit > $LBit && $ABit > $WBit && $ABit > $XBit && $ABit > $YBit && $ABit > $ZBit && ($csaA eq "-" || $csaB eq "-" || $csaD eq "-" || $ctrA eq "-" || $ctrB eq "-" || $ctrC eq "-" || $ctrD eq "-" || $ctrE eq "-" || $ctrF eq "-" || $thd >= $ARnd)) {
    print $head;
    print "$var1\tng\t$varA\tcsaB\t$Anum\t$Alen\t$ASlen\t$ARnd\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$var16SRnd\n";

#####################################################BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
} elsif ($varB eq "B" && $BBit > $ABit && $BBit > $CBit && $BBit > $EBit && $BBit > $HBit && $BBit > $IBit && $BBit > $KBit && $BBit > $LBit && $BBit > $WBit && $BBit > $XBit && $BBit > $YBit && $BBit > $ZBit & $cssA eq "+" & $cssB eq "+" & $cssC eq "+" & $ctrG eq "+" & $ctrA eq "+" & $ctrB eq "+" & $ctrC eq "+" & $ctrD eq "+" & $ctrE eq "+" & $ctrF eq "+" & $BRnd >= $thd) {
    print $head;
    print "$var1\t$varB\t$varB\tcsb\t$Bnum\t$Blen\t$BSlen\t$BRnd\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$var16SRnd\n";

} elsif ($varB eq "B" && $BBit > $ABit && $BBit > $CBit && $BBit > $EBit && $BBit > $HBit && $BBit > $IBit && $BBit > $KBit && $BBit > $LBit && $BBit > $WBit && $BBit > $XBit && $BBit > $YBit && $BBit > $ZBit && ($cssA eq "-" || $cssB eq "-" || $cssC eq "-" || $ctrG eq "-" || $ctrA eq "-" || $ctrB eq "-" || $ctrC eq "-" || $ctrD eq "-" || $ctrE eq "-" || $ctrF eq "-" || $thd >= $BRnd)) {
    print $head;
    print "$var1\tng\t$varB\tcsb\t$Bnum\t$Blen\t$BSlen\t$BRnd\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$var16SRnd\n";

#####################################################CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
} elsif ($varC eq "C" && $CBit > $ABit && $CBit > $BBit && $CBit > $EBit && $CBit > $HBit && $CBit > $IBit && $CBit > $KBit && $CBit > $LBit && $CBit > $WBit && $CBit > $XBit && $CBit > $YBit && $CBit > $ZBit & $cssA eq "+" & $cssB eq "+" & $cssC eq "+" & $cssE eq "+" & $ctrG eq "+" & $ctrA eq "+" & $ctrB eq "+" & $ctrC eq "+" & $ctrD eq "+" & $ctrE eq "+" & $ctrF eq "+" &$CRnd >= $thd) {
    print $head;
    print "$var1\t$varC\t$varC\tcsc\t$Cnum\t$Clen\t$CSlen\t$CRnd\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$var16SRnd\n";

} elsif ($varC eq "C" && $CBit > $ABit && $CBit > $BBit && $CBit > $EBit && $CBit > $HBit && $CBit > $IBit && $CBit > $KBit && $CBit > $LBit && $CBit > $WBit && $CBit > $XBit && $CBit > $YBit && $CBit > $ZBit && ($cssA eq "-" || $cssB eq "-" || $cssC eq "-" || $cssE eq "-" || $ctrG eq "-" || $ctrA eq "-" || $ctrB eq "-" || $ctrC eq "-" || $ctrD eq "-" || $ctrE eq "-" || $ctrF eq "-" || $thd >= $CRnd)) {
    print $head;
    print "$var1\tng\t$varC\tcsc\t$Cnum\t$Clen\t$CSlen\t$CRnd\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$var16SRnd\n";

#####################################################EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
} elsif ($varE eq "E" && $EBit > $ABit && $EBit > $BBit && $EBit > $CBit && $EBit > $HBit && $EBit > $IBit && $EBit > $KBit && $EBit > $LBit && $EBit > $WBit && $EBit > $XBit && $EBit > $YBit && $EBit > $ZBit & $cseA eq "+" & $cseB eq "+" & $cseD eq "+" & $cseE eq "+" & $cseF eq "+" & $cseG eq "+" & $ctrA eq "+" & $ctrB eq "+" & $ctrC eq "+" & $ctrD eq "+" & $ctrE eq "+" & $ctrF eq "+" & $ERnd >= $thd) {
    print $head;
    print "$var1\t$varE\t$varE\tcseC\t$Enum\t$Elen\t$ESlen\t$ERnd\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$var16SRnd\n";

} elsif ($varE eq "E" && $EBit > $ABit && $EBit > $BBit && $EBit > $CBit && $EBit > $HBit && $EBit > $IBit && $EBit > $KBit && $EBit > $LBit && $EBit > $WBit && $EBit > $XBit && $EBit > $YBit && $EBit > $ZBit && ($cseA eq "-" || $cseB eq "-" || $cseD eq "-" || $cseE eq "-" || $cseF eq "-" || $cseG eq "-" || $ctrA eq "-" || $ctrB eq "-" || $ctrC eq "-" || $ctrD eq "-" || $ctrE eq "-" || $ctrF eq "-" || $thd >= $ERnd)) {
    print $head;
    print "$var1\tng\t$varE\tcseC\t$Enum\t$Elen\t$ESlen\t$ERnd\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$var16SRnd\n";

#####################################################HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
} elsif ($varH eq "H" && $HBit > $ABit && $HBit > $BBit && $HBit > $CBit && $HBit > $EBit && $HBit > $IBit && $HBit > $KBit && $HBit > $LBit && $HBit > $WBit && $HBit > $XBit && $HBit > $YBit && $HBit > $ZBit & $cszA eq "+" & $cszB eq "+" & $cshD eq "+" & $ctrA eq "+" & $ctrB eq "+" & $ctrC eq "+" & $ctrD eq "+" & $ctrE eq "+" & $ctrF eq "+" & $HRnd >= $thd) {
    print $head;
    print "$var1\t$varH\t$varH\tcshC\t$Hnum\t$Hlen\t$HSlen\t$HRnd\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$var16SRnd\n";

} elsif ($varH eq "H" && $HBit > $ABit && $HBit > $BBit && $HBit > $CBit && $HBit > $EBit && $HBit > $IBit && $HBit > $KBit && $HBit > $LBit && $HBit > $WBit && $HBit > $XBit && $HBit > $YBit && $HBit > $ZBit && ($cszA eq "-" || $cszB eq "-" || $cshD eq "-" || $ctrA eq "-" || $ctrB eq "-" || $ctrC eq "-" || $ctrD eq "-" || $ctrE eq "-" || $ctrF eq "-" || $thd >= $HRnd)) {
    print $head;
    print "$var1\tng\t$varH\tcshC\t$Hnum\t$Hlen\t$HSlen\t$HRnd\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$var16SRnd\n";

#####################################################IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
} elsif ($varI eq "I" && $IBit > $ABit && $IBit > $BBit && $IBit > $CBit && $IBit > $EBit && $IBit > $HBit && $IBit > $KBit && $IBit > $LBit && $IBit > $WBit && $IBit > $XBit && $IBit > $YBit && $IBit > $ZBit & $csiA eq "+" & $csiB eq "+" & $csiD eq "+" & $csiE eq "+" & $ctrA eq "+" & $ctrB eq "+" & $ctrC eq "+" & $ctrD eq "+" & $ctrE eq "+" & $ctrF eq "+" & $IRnd >= $thd) {
    print $head;
    print "$var1\t$varI\t$varI\tcsiC\t$Inum\t$Ilen\t$ISlen\t$IRnd\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$var16SRnd\n";

} elsif ($varI eq "I" && $IBit > $ABit && $IBit > $BBit && $IBit > $CBit && $IBit > $EBit && $IBit > $HBit && $IBit > $KBit && $IBit > $LBit && $IBit > $WBit && $IBit > $XBit && $IBit > $YBit && $IBit > $ZBit && ($csiA eq "-" || $csiB eq "-" || $csiD eq "-" || $csiE eq "-" || $ctrA eq "-" || $ctrB eq "-" || $ctrC eq "-" || $ctrD eq "-" || $ctrE eq "-" || $ctrF eq "-" || $thd >= $IRnd)) {
    print $head;
    print "$var1\tng\t$varI\tcsiC\t$Inum\t$Ilen\t$ISlen\t$IRnd\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$var16SRnd\n";

#####################################################KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK
} elsif ($varK eq "K" && $KBit > $ABit && $KBit > $BBit && $KBit > $CBit && $KBit > $EBit && $KBit > $HBit && $KBit > $IBit && $KBit > $LBit && $KBit > $WBit && $KBit > $XBit && $KBit > $YBit && $KBit > $ZBit & $csiA eq "+" & $csiB eq "+" & $csiD eq "+" & $csiE eq "+" & $ctrA eq "+" & $ctrB eq "+" & $ctrC eq "+" & $ctrD eq "+" & $ctrE eq "+" & $ctrF eq "+" & $KRnd >= $thd) {
    print $head;
    print "$var1\t$varK\t$varK\tcskC\t$Knum\t$Klen\t$KSlen\t$KRnd\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$var16SRnd\n";

} elsif ($varK eq "K" && $KBit > $ABit && $KBit > $BBit && $KBit > $CBit && $KBit > $EBit && $KBit > $HBit && $KBit > $IBit && $KBit > $LBit && $KBit > $WBit && $KBit > $XBit && $KBit > $YBit && $KBit > $ZBit && ($csiA eq "-" || $csiB eq "-" || $csiD eq "-" || $csiE eq "-" || $thd >= $KRnd)) {
    print $head;
    print "$var1\tng\t$varK\tcskC\t$Knum\t$Klen\t$KSlen\t$KRnd\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$var16SRnd\n";

#####################################################LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL
} elsif ($varL eq "L" && $LBit > $ABit && $LBit > $BBit && $LBit > $CBit && $LBit > $EBit && $LBit > $HBit && $LBit > $IBit && $LBit > $KBit && $LBit > $WBit && $LBit > $XBit && $LBit > $YBit && $LBit > $ZBit & $cslA eq "+" & $cslB eq "+" & $ctrA eq "+" & $ctrB eq "+" & $ctrC eq "+" & $ctrD eq "+" & $ctrE eq "+" & $ctrF eq "+" & $LRnd >= $thd) {
    print $head;
    print "$var1\t$varL\t$varL\tcslC\t$Lnum\t$Llen\t$LSlen\t$LRnd\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$var16SRnd\n";

} elsif ($varL eq "L" && $LBit > $ABit && $LBit > $BBit && $LBit > $CBit && $LBit > $EBit && $LBit > $HBit && $LBit > $IBit && $LBit > $KBit && $LBit > $WBit && $LBit > $XBit && $LBit > $YBit && $LBit > $ZBit && ($cslA eq "-" || $cslB eq "-" || $thd >= $LRnd)) {
    print $head;
    print "$var1\tng\t$varL\tcslC\t$Lnum\t$Llen\t$LSlen\t$LRnd\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$var16SRnd\n";

#####################################################WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
} elsif ($varW eq "W" && $WBit > $ABit && $WBit > $BBit && $WBit > $CBit && $WBit > $EBit && $WBit > $HBit && $WBit > $IBit && $WBit > $KBit && $WBit > $LBit && $WBit > $XBit && $WBit > $YBit && $WBit > $ZBit & $cssA eq "+" & $cssB eq "+" & $cssC eq "+" & $cssF eq "+" & $ctrG eq "+" & $ctrA eq "+" & $ctrB eq "+" & $ctrC eq "+" & $ctrD eq "+" & $ctrE eq "+" & $ctrF eq "+" & $WRnd >= $thd) {
    print $head;
    print "$var1\t$varW\t$varW\tcsw\t$Wnum\t$Wlen\t$WSlen\t$WRnd\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$var16SRnd\n";

} elsif ($varW eq "W" && $WBit > $ABit && $WBit > $BBit && $WBit > $CBit && $WBit > $EBit && $WBit > $HBit && $WBit > $IBit && $WBit > $KBit && $WBit > $LBit && $WBit > $XBit && $WBit > $YBit && $WBit > $ZBit && ($cssA eq "-" || $cssB eq "-" || $cssC eq "-" || $cssF eq "-" || $ctrG eq "-" || $thd >= $WRnd)) {
    print $head;
    print "$var1\tng\t$varW\tcsw\t$Wnum\t$Wlen\t$WSlen\t$WRnd\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$var16SRnd\n";

#####################################################XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
} elsif ($varX eq "X" && $XBit > $ABit && $XBit > $BBit && $XBit > $CBit && $XBit > $EBit && $XBit > $HBit && $XBit > $IBit && $XBit > $KBit && $XBit > $LBit && $XBit > $WBit && $XBit > $YBit && $XBit > $ZBit & $csxA eq "+" & $csxC eq "+" & $ctrA eq "+" & $ctrB eq "+" & $ctrC eq "+" & $ctrD eq "+" & $ctrE eq "+" & $ctrF eq "+" & $XRnd >= $thd) {
    print $head;
    print "$var1\t$varX\t$varX\tcsxB\t$Xnum\t$Xlen\t$XSlen\t$XRnd\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$var16SRnd\n";

} elsif ($varX eq "X" && $XBit > $ABit && $XBit > $BBit && $XBit > $CBit && $XBit > $EBit && $XBit > $HBit && $XBit > $IBit && $XBit > $KBit && $XBit > $LBit && $XBit > $WBit && $XBit > $YBit && $XBit > $ZBit && ($csxA eq "-" || $csxC eq "-" || $thd >= $XRnd)) {
    print $head;
    print "$var1\tng\t$varX\tcsxB\t$Xnum\t$Xlen\t$XSlen\t$XRnd\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$var16SRnd\n";

#####################################################YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
} elsif ($varY eq "Y" && $YBit > $ABit && $YBit > $BBit && $YBit > $CBit && $YBit > $EBit && $YBit > $HBit && $YBit > $IBit && $YBit > $KBit && $YBit > $LBit && $YBit > $WBit && $YBit > $XBit && $YBit > $ZBit & $cssA eq "+" & $cssB eq "+" & $cssC eq "+" & $cssF eq "+" & $ctrG eq "+" & $ctrA eq "+" & $ctrB eq "+" & $ctrC eq "+" & $ctrD eq "+" & $ctrE eq "+" & $ctrF eq "+" & $YRnd >= $thd) {
    print $head;
    print "$var1\t$varY\t$varY\tcsy\t$Ynum\t$Ylen\t$YSlen\t$YRnd\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$var16SRnd\n";

} elsif ($varY eq "Y" && $YBit > $ABit && $YBit > $BBit && $YBit > $CBit && $YBit > $EBit && $YBit > $HBit && $YBit > $IBit && $YBit > $KBit && $YBit > $LBit && $YBit > $WBit && $YBit > $XBit && $YBit > $ZBit && ($cssA eq "-" || $cssB eq "-" || $cssC eq "-" || $cssF eq "-" || $ctrG eq "-" || $thd >= $YRnd)) {
    print $head;
    print "$var1\tng\t$varY\tcsy\t$Ynum\t$Ylen\t$YSlen\t$YRnd\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$var16SRnd\n";

#####################################################ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ
} elsif ($varZ eq "Z" && $ZBit > $ABit && $ZBit > $BBit && $ZBit > $CBit && $ZBit > $EBit && $ZBit > $HBit && $ZBit > $IBit && $ZBit > $KBit && $ZBit > $LBit && $ZBit > $WBit && $ZBit > $XBit && $ZBit > $YBit & $cszA eq "+" & $cszB eq "+" & $cszC eq "+" & $ctrA eq "+" & $ctrB eq "+" & $ctrC eq "+" & $ctrD eq "+" & $ctrE eq "+" & $ctrF eq "+" & $ZRnd >= $thd) {
    print $head;
    print "$var1\t$varZ\t$varZ\tcszD\t$Znum\t$Zlen\t$ZSlen\t$ZRnd\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$var16SRnd\n";

} elsif ($varZ eq "Z" && $ZBit > $ABit && $ZBit > $BBit && $ZBit > $CBit && $ZBit > $EBit && $ZBit > $HBit && $ZBit > $IBit && $ZBit > $KBit && $ZBit > $LBit && $ZBit > $WBit && $ZBit > $XBit && $ZBit > $YBit && ($cszA eq "-" || $cszB eq "-" || $cszC eq "-" || $thd >= $ZRnd)) {
    print $head;
    print "$var1\tng\t$varZ\tcszD\t$Znum\t$Zlen\t$ZSlen\t$ZRnd\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$var16SRnd\n";

#####################################################????????????????????????????????????????????????????????????
} else {
    print $head;
    print "$var1\t$varNt\tNm?\tNm?\t-\t-\t-\t-\t$csaA\t$csaB\t$csaC\t$csaD\t$csb\t$csc\t$cseA\t$cseB\t$cseC\t$cseD\t$cseE\t$cseF\t$cseG\t$cshC\t$cshD\t$csiA\t$csiB\t$csiC\t$csiD\t$csiE\t$cskC\t$cslA\t$cslB\t$cslC\t$cssA\t$cssB\t$cssC\t$cssE\t$cssF\t$csw\t$csxA\t$csxB\t$csxC\t$csy\t$cszA\t$cszB\t$cszC\t$cszD\t$ctrG\t$galE\t$tex\t$ctrA\t$ctrB\t$ctrC\t$ctrD\t$ctrE\t$ctrF\t$rfbA\t$rfbB\t$rfbC\t$sodC\t$var16SRnd\n";

}
