#!/usr/bin/perl
#seq_consensus.pl
#version1.0
#free perl script by Oliver Voigt 2007
#written for UNIX, linux and Mac OS X

my $description ="This script creates consensus from nucleotide sequences in an alignment\n(a) and appends the consensus sequence to the existing file.
Inout and output- formats are *.mase and *.fasta.";
my $usage= "perl seq_consensus.pl <input-file (.fasta or .mase)> <percent consensus>\n";
print "******************************************************************************\n"; 
print "                    seq_consensus.pl (version 1.0)\n";                           
print "******************************************************************************\n";
use strict;
use warnings;
my $file1;
my @ordertax;
#my %seqHashFile1;
my @helixnames;
my @helixstart;
my @baselist;
my $perCons="";

#Input files*************************************************************
unless ($file1=shift){     
    print "USAGE: $usage Input file name? :";
    $file1=<STDIN>;
    chomp ($file1);
   }
   
unless ($perCons=shift){
   print "No consesus level provided\n.";
}

#End of input files.***********************************************************

#convert linebreaks to unix;

&convertLinebreaks($file1);
my $fileformat=&fileFormat($file1);

if ($fileformat eq "mase"){
   print "File-format: mase\n";
   @ordertax=&maseIDsintoFile($file1);

}
elsif ($fileformat eq "fasta"){
     print "File-format: fasta\n";
    @ordertax=&fastaIDsintoFile($file1);
}

else {
   die "Input is not mase or fasta format!\n";
}
# sequences read to SeqHash;

#my $length=length ($seqHashFile1{$ordertax[0]});
print scalar(@ordertax) ," sequences in file:\n",join("\n", @ordertax);
if ($perCons eq ""){
    print "\nChoose % consensus? (90)";
    $perCons=<STDIN>;
    chomp ($perCons);
}
    if ($perCons eq ""){
        $perCons=0.1
    }
    else {
        $perCons=1-$perCons/100;
    }
   
my @list=&consSeq($file1, $perCons);

my $seqnumber=scalar(@ordertax);#move into hash!
#print"\"$file1\" has $seqnumber Sequences and ",length($list[1]), " characters.\n";
open (OUT, ">>$file1");
if ($fileformat eq "mase"){
    print OUT ";created with the script conseq.pl\nConsensus_",shift @list, "\n";
    print "Consensus-sequence:\n@list\n";
    print OUT shift @list,"\n";
}
else {
    print OUT ">Consensus_",shift @list, "\n";
    print "Consensus-sequence:\n@list\n";
    print OUT shift @list,"\n";

}close OUT;


#system ("open -a seaview $file1");



 #*****************************************************************************
sub convertLinebreaks{
    my $inputfile=$_[0];
    open (IN, "<$inputfile") or die "File $inputfile not found.\n";
    open (OUT, ">break.tmp");
    my$macbreak=my $dosbreak=0;

    while (<IN>){
        if ($_ =~ /\r\n/){
            print "*DOS-formated line breaks converted to Unix-formated line breaks in $inputfile.\n";
            $dosbreak=1;
            $_ =~ s/\r\n/\n/g;
            print OUT $_;
            }
        elsif ($_ =~ /\r/){
            print "*MAC-formated line breaks converted to Unix-formated line breaks in $inputfile.\n";
            $macbreak=1;
            $_ =~ s/\r/\n/g;
            print OUT $_;
            }
        }
    close IN;
    close OUT;
    if ($macbreak or $dosbreak){
        system ("mv break.tmp $inputfile");
     }
    else {
        print "The file \"$inputfile\" had unix line breaks.\n";
        system ("rm break.tmp");
    }
 }#end sub convertLinebreaks;


#*******************************************************************************

sub maseIDsintoFile {
    my @IDlist;
    my $lastseq="";
    my %seq;
    my $i=1;
    my $oldline="";
    if (open (FILE, $_[0])){
        until (eof(FILE)){
             my $line =<FILE>;
             chomp ($line);
             if (substr($line,0,2) eq";;"){
                  next;
              }
              if (substr($line,0,1) eq";"){
                  $oldline=$line;
                  next;
              }
             
          if (substr($oldline,0,1) eq ";"){
                 push (@IDlist, $line);
                 $oldline="";
            $i=$i+1;
            }

        }
        close(FILE);
    }
    else {
    print "\n File $_[0] not found.";
       }
    
    return @IDlist;
 }

#*******************************************************************************
 sub fastaIDsintoFile {
     my @IDlist;
     if (open (FILE, $_[0])){
         until (eof(FILE)){  
             my $line =<FILE>;
#             print "LINE: $line \n";
             chomp ($line);
             if (substr($line,0,1) eq ">"){
                 push (@IDlist, substr($line,1,length($line)-1));   
              }                            
            }#end until eof FILE
        }#end if open;
   else {
    print "\n File $_[0] not found.";
       }
    
    return @IDlist;
 }
#******************************************************************************* 

#******************************************************************************* 

sub fileFormat{
    my $fileformat;
    my $file1=$_[0];
    open (INFILE, "<$file1");
        my $firstline=<INFILE>;
        if (substr($firstline, 0,1) eq ">"){
            $fileformat="fasta";
        }
        elsif (substr($firstline, 0,1) eq ";"){
            $fileformat="mase";
        }
        else {
            die "Format of input file is not mase or fasta!\n";
        }
    close (INFILE);
return $fileformat;

}#end sub;

 
#******************************************************************************* 
sub MaseSeqsIntoHash {
    my %seqHash;
    my $lastseq="";
    my %seq;
    my $i=1;
    my $oldline="";
  ##  my @ordertax;
    if (open (FILE, $_[0])){
        until (eof(FILE)){
             my $line =<FILE>;
             chomp ($line);
             if (substr($line,0,2) eq";;"){
                  if (exists($seqHash{"HEADER"})){##
                      $seqHash{"HEADER"}=$seqHash{"HEADER"}.$line."\n";##
                  }##
                  else {##
                      $seqHash{HEADER}=$line."\n";##
                  }###
                      
                  next;
              }
              if (substr($line,0,1) eq";"){
                  $oldline=$line;
                  next;
              }             
           if (substr($oldline,0,1) eq ";"){
                 if (exists $seqHash{substr($line,0,length($line))}) {
                     die "There are two sequences in the file using the same ID:$line\n";
                 }
                 else {
                     $seqHash{substr($line,0,length($line))}="";
                     $lastseq=substr($line,0,length($line));
 ##                    push (@ordertax, substr($line,0,length($line)));#neu
                 }                        
            $i=$i+1;
            }
             else {
                 if (exists($seqHash{$lastseq})){
                     my $seqinHash=$seqHash{$lastseq};             #old value as read in
                     $seqHash{$lastseq}=$seqinHash.$line;          #new sequenceline is attached to value
                 }
            }
            $oldline=$line;
        }
        close(FILE);
    }
    else {
    die "\n File $_[0] not found.\n";
       }
    return %seqHash;
 }

#***********************************************************************************
#**
sub FastaSeqsIntoHash {
# print "\nFILE: $_[0]";
     my %seqHash;
     my $i=1;
     my $lastseq="";
     if (open (FILE, $_[0])){
         until (eof(FILE)){
             my $line =<FILE>;
             chomp ($line);
           if (substr($line,0,1) eq ">"){
                 if (exists $seqHash{substr($line,1,length($line)-1)}) {
                      die "There are two sequences in the file using the same ID:$line\n";
                 }
                 else {
                     $seqHash{substr($line,1,length($line)-1)}="";
                    $lastseq=substr($line,1,length($line)-1);
                 }
#            print "\n($i) ", substr($line,1,length($line)-1);
            
            $i=$i+1;
            }
            else {
                 if (exists($seqHash{$lastseq})){
                     my $seqinHash=$seqHash{$lastseq};             #old value as read in
                     $seqHash{$lastseq}=$seqinHash.$line;          #new sequenceline is attached to value
                 }
              #only if no seq-ID has been found before , the hash key $lastseq has no entry ;
                else {          
                  die "The file does not start with a sequence identifier.\n"
                 }
            }                    
        }
        close (FILE);
    }
          
    else {
        print "\n File $_[0] not found.";
    }
return %seqHash;
}

#**************************
#***********************************************************
 #SUB CONSENSUS
#Input: $file
sub consSeq{
    my $file1=$_[0];
    my $perCons=$_[1];
    my $fileformat=&fileFormat($file1);
    my %seqHashFile1;
    my @ordertax;
   if ($fileformat eq "mase"){
       @ordertax=maseIDsintoFile($file1);
       %seqHashFile1=&MaseSeqsIntoHash($file1);
     }
     elsif ($fileformat eq "fasta"){
         @ordertax=&fastaIDsintoFile($file1);
         %seqHashFile1=&FastaSeqsIntoHash($file1);
     }
# sequences read to SeqHash;

 #   my @IDsInFile1=keys (%seqHash);
    my $seqnumber=scalar (@ordertax);
    my$length=length ($seqHashFile1{$ordertax[0]});
    my $consSequence;
    my @baselist;
   
    print "Creating ", (1-$perCons)*100,"\% consensus sequence.\n";
    print "Nucleotide states present in less than ", $perCons * $seqnumber, " sequences will be discarded\n";
    for (my $position=0; $position<$length; $position++){#start for #1
         #print "POSITION:$position ";
         my $a=0;
         my $u=0;
         my $c=0;
         my $g=0;
         my $gap=0;
         my $seqzaehler=0;
          @baselist="";
         foreach my $seqname (@ordertax){
         my $base=substr($seqHashFile1{$seqname},$position,1);
         $base=uc $base;#new
         $base=~ tr/O/-/; #############
         
         if ($base eq "A"){
             $a++;
         }
         elsif ($base eq "U"){
             $u++;
         }
         elsif ($base eq "T"){
             $u++;
         }
         elsif ($base eq "C"){
             $c++;
         }
         elsif ($base eq "G"){
             $g++;
         }
         elsif ($base eq "R"){
             $a=$a+0.5;
             $g=$g+0.5;
         }
         elsif ($base eq "Y"){
             $c=$c+0.5;
             $u=$u+0.5;
         }
         elsif ($base eq "M"){
             $a=$a+0.5;
             $c=$c+0.5;
         }
         elsif ($base eq "S"){
             $c=$c+0.5;
             $g=$g+0.5;
         }
         elsif ($base eq "K"){
             $u=$u+0.5;
             $g=$g+0.5;
         }
         elsif ($base eq "W"){
             $a=$a+0.5;
             $u=$u+0.5;
         }
         elsif ($base eq "B"){
             $c=$c+1/3;
             $u=$u+1/3;
             $g=$g+1/3;
         }
         elsif ($base eq "B"){
             $c=$c+1/3;
             $u=$u+1/3;
             $g=$g+1/3;
         }
         elsif ($base eq "D"){
             $a=$a+1/3;
             $u=$u+1/3;
             $g=$g+1/3;
         }
         elsif ($base eq "H"){
             $c=$c+1/3;
             $u=$u+1/3;
             $a=$a+1/3;
         }
          elsif ($base eq "V"){
             $c=$c+1/3;
             $a=$a+1/3;
             $g=$g+1/3;
         }
          elsif ($base eq "N"){
             $c=$c+1/4;
             $u=$u+1/4;
             $g=$g+1/4;
             $a=$a+1/4;
         }
           
          elsif ($base eq "-"){
             $gap++;
         }
         
         else{
             die "Unknown charachter in $seqname position ",$position+1, ": \"$base\".\n";
         }
         
         $seqzaehler++;
               
         
        }#end foreach;
        push (@baselist, $a);
        push (@baselist, $u);
        push (@baselist, $g);
        push (@baselist, $c);
        push (@baselist, $gap);
        my $countingbase="";
        for (my $i=1; $i<=5; $i++){            
            my $element=$baselist[$i];
            
            if ($i==1 and $element>= $perCons * $seqnumber){
                $countingbase="A";
            }            
            if ($i==2 and $element>= $perCons * $seqnumber){
                $countingbase=$countingbase."U";
            }
            if ($i==3 and $element>= $perCons * $seqnumber){
                $countingbase=$countingbase."G";
            }
            if ($i==4 and $element>= $perCons * $seqnumber){
                $countingbase=$countingbase."C";
            }
            if ($i==5 and $element>= $perCons * $seqnumber){
                $countingbase=$countingbase."-";
            }                       
        }#end for;        
        if ($countingbase eq "AUGC"){
           $consSequence=$consSequence."N";
           }
        elsif ($countingbase eq "AGC"){
           $consSequence=$consSequence."V";
        }
       elsif ($countingbase eq "AUC"){
           $consSequence=$consSequence."H";
           }
       elsif ($countingbase eq "AUG"){
           $consSequence=$consSequence."D";
           }
       elsif ($countingbase eq "UGC"){
           $consSequence=$consSequence."B";
           }
       elsif ($countingbase eq "AU"){
           $consSequence=$consSequence."W";
           }
       elsif ($countingbase eq "UG"){
           $consSequence=$consSequence."K";
           }
       elsif ($countingbase eq "GC"){
           $consSequence=$consSequence."S";
           }
       elsif ($countingbase eq "AC"){
           $consSequence=$consSequence."M";
           }
       elsif ($countingbase eq "AG"){
           $consSequence=$consSequence."R";
           }
       elsif ($countingbase eq "UC"){
           $consSequence=$consSequence."Y";
           }
       elsif ($countingbase eq "AUGC"){
           $consSequence=$consSequence."N";
           }
       elsif (length($countingbase)==1){         #conserved position;
           $consSequence=$consSequence.$countingbase;
           #print"$countingbase: ",length($consSequence),"# ",substr($consSequence,length($consSequence)-1,1),"\n";#test:klappt;
           }
        elsif ($countingbase eq "AUGC-"){
           $consSequence=$consSequence."n";
           }
        elsif ($countingbase eq "AGC-"){
           $consSequence=$consSequence."v";
         }
        elsif ($countingbase eq "AUC-"){
           $consSequence=$consSequence."h";
        }
        elsif ($countingbase eq "AUG-"){
           $consSequence=$consSequence."d";
        }
        elsif ($countingbase eq "UGC-"){
           $consSequence=$consSequence."b";
        }
        elsif ($countingbase eq "AU-"){
            $consSequence=$consSequence."w";
        }
        elsif ($countingbase eq "UG-"){
            $consSequence=$consSequence."k";
        }
        elsif ($countingbase eq "GC-"){
            $consSequence=$consSequence."s";
        }
        elsif ($countingbase eq "AC-"){
            $consSequence=$consSequence."m";
        }
        elsif ($countingbase eq "AG-"){
            $consSequence=$consSequence."r";
        }
        elsif ($countingbase eq "UC-"){
            $consSequence=$consSequence."y";
        }
        elsif ($countingbase eq "A-"){
            $consSequence=$consSequence."a";
        }
       elsif ($countingbase eq "U-"){
           $consSequence=$consSequence."u";
           }
       elsif ($countingbase eq "G-"){
           $consSequence=$consSequence."g";
           }
       elsif ($countingbase eq "C-"){
           $consSequence=$consSequence."c";
           }
       else {$consSequence=$consSequence."?";}    
    } #end for #1;
 #print "Consensus sequence:\n", $consSequence, "\n";
 if ($length != length($consSequence)){
 print "Error: Consensus sequence has too much or too little characters\n";
 }
 my $cons=100-$perCons*100;
 push (my @return,$cons);
 push (@return, $consSequence);
 return @return;
}#end SUB conSeq;
