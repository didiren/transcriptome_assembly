#Di Ren
#CSE 6613
#Nov-25-2016
#Final project
#Using pipeline to create a untreated file to run a series of codes.
import os
import sys
#First obtain all input files and the path to using the softwares in Input.txt file so it is easier than I aske you to input one by one.
untreated=[]
treated=[]

inf=open('parameters.txt','r')
for line in inf:
    line=line.strip()
    if 'untreated' in line:
        untreated.append(line[8:])
    if 'treated' in line:
        treated.append(line[10:])
    if 'genome' in line:
        genomepath=line[7:]
    if 'annotation' in line:
        annotationpath=line[11:]
    if 'fastqc' in line:
        fastqcpath=line[7:]
    if 'trimmomatic' in line:
        trimmomaticpath=line[12:]
    if 'tophat' in line:
        tophatpath=line[7:]
    if 'bowtie2' in line:
        bowtie2path=line[8:]
    if 'samtools' in line:
        samtoolspath=line[9:]
    if 'htseq' in line:
        htseqpath=line[6:]
inf.close()        
#Run fastqc to acess the quality of the untreated seq files
for i in range(0,len(untreated)):
    commandline=fastqcpath+'fastqc '+untreated[i]
    #print(commandline)
    os.system(commandline)
#Run fastqc to acess the quality of the treated seq files
for i in range(0,len(treated)):
    commandline=fastqcpath+'fastqc '+treated[i]
    #print(commandline)
    os.system(commandline)



#Delete From___________________________________________________________________________________________    
#You can delete from here if you don't want to use trimmmomatic    
#After that, it is optional to trim the adaptors with trimmomatic
a=0
for i in range(0,int(len(untreated)/2)):
    commandline='java -jar '+trimmomaticpath+'trimmomatic-0.36.jar PE '+untreated[a]+' '+untreated[a+1]+' '+untreated[a]+'_p.fq.gz '+untreated[a]+'_up.fq.gz '+untreated[a+1]+'_p.fq.gz '+untreated[a+1]+'_up.fq.gz ILLUMINACLIP:master.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:25 MINLEN:36'
    a+=2
    #print(commandline)
    os.system(commandline)
#After that, it is optional to trim the adaptors with trimmomatic
a=0
for i in range(0,int(len(treated)/2)):
    commandline='java -jar '+trimmomaticpath+'trimmomatic-0.36.jar PE '+treated[a]+' '+treated[a+1]+' '+treated[a]+'_p.fq.gz '+treated[a]+'_up.fq.gz '+treated[a+1]+'_p.fq.gz '+treated[a+1]+'_up.fq.gz ILLUMINACLIP:master.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:25 MINLEN:36'
    a+=2
    #print(commandline)
    os.system(commandline)    
#Run fastqc again to acess the quality of the trimmed seq files (optional)
for i in range(0,len(untreated)):
    commandline=fastqcpath+'fastqc '+untreated[i]+'_p.fq.gz'
    #print(commandline)
    os.system(commandline)
#Run fastqc again to acess the quality of the trimmed seq files (optional)
for i in range(0,len(treated)):
    commandline=fastqcpath+'fastqc '+treated[i]+'_p.fq.gz'
    #print(commandline)
    os.system(commandline)
#You can delete end here if you don't want to use trimmmomatic    
#Delete end______________________________________________________________________________________________





#Using bowtie2-build TO build a index for your reference genome to accelate the alignment process.
commandline=bowtie2path+'bowtie2-build '+genomepath+' ref_genome'
#print(commandline)
os.system(commandline)


#Run tophat with specific command format to align the untrimmed reads to reference genome (only do this if you have a good reference genome):
a=0
for index in range(0,int(len(untreated)/2)):
    commandline=tophatpath+'tophat2 -p 8 -o untreatedout_index'+str(index+1)+' ref_genome '+untreated[a]+' '+untreated[a+1]
    a=a+2
    #print(commandline)
    os.system(commandline)

a=0
for index in range(3,int(len(untreated)/2)):
    commandline=tophatpath+'tophat2 -p 8 -o treatedout_index'+str(index+1)+' ref_genome '+treated[a]+' '+treated[a+1]
    a=a+2
    #print(commandline)
    os.system(commandline)



#Delete From___________________________________________________________________________________________    
#If you don't use trimmomatic, delete from here 
#Run tophat with specific command format to align the trimmed reads to reference genome (only do this if you have a good reference genome):
a=0
for index in range(0,int(len(untreated)/2)):
    commandline=tophatpath+'tophat2 -p 8 -o untreatedout_trime_index'+str(index+1)+' ref_genome '+untreated[a]+'_p.fq.gz '+untreated[a+1]+'_p.fq.gz'
    a=a+2
    #print(commandline)
    os.system(commandline)

a=0
for index in range(3,int(len(untreated)/2)):
    commandline=tophatpath+'tophat2 -p 8 -o treatedout_trim_index'+str(index+1)+' ref_genome '+treated[a]+'_p.fq.gz '+treated[a+1]+'_p.fq.gz'
    a=a+2
    #print(commandline)
    os.system(commandline)
#If you don't use trimmomatic, delete end here 
#Delete end______________________________________________________________________________________________





#Run samtools to sort the output files from tophat and feed them to htseq-count
for index in range(0,int(len(untreated)/2)):
    commandline=samtoolspath+'samtools sort -n untreatedout_index'+str(index+1)+'/accepted_hits.bam '+'untreatedout_index'+str(index+1)+'/sorted_accepted_hits'
    #print(commandline)
    os.system(commandline)
for index in range(0,int(len(treated)/2)):
    commandline=samtoolspath+'samtools sort -n treatedout_index'+str(index+1)+'/accepted_hits.bam '+'treatedout_index'+str(index+1)+'/sorted_accepted_hits'
    #print(commandline)
    os.system(commandline)



#Delete From___________________________________________________________________________________________
#If you don't use trimmomatic, delete from here 
#Run samtools to sort the output files from tophat and feed them to htseq-count
for index in range(0,int(len(untreated)/2)):
    commandline=samtoolspath+'samtools sort -n untreatedout_trim_index'+str(index+1)+'/accepted_hits.bam '+'untreatedout_trim_index'+str(index+1)+'/sorted_accepted_hits'
    #print(commandline)
    os.system(commandline)
for index in range(0,int(len(treated)/2)):
    commandline=samtoolspath+'samtools sort -n treatedout_trim_index'+str(index+1)+'/accepted_hits.bam '+'treatedout_trim_index'+str(index+1)+'/sorted_accepted_hits'
    #print(commandline)
    os.system(commandline)
#If you don't use trimmomatic, delete end here 
#Delete end______________________________________________________________________________________________




 
#feed the output from last step: sorted_accepted_hits.bam to htseq_count using 2017version gff file
for index in range(0,int(len(untreated)/2)):
    commandline=htseqpath+'htseq-count --format=bam --stranded=no untreatedout_index'+str(index+1)+'/sorted_accepted_hits.bam '+annotationpath+' -i transcript_id > untreated_index'+str(index+1)+'.txt'
    #print(commandline)
    os.system(commandline)
for index in range(0,int(len(treated)/2)):
    commandline=htseqpath+'htseq-count --format=bam --stranded=no treatedout_index'+str(index+1)+'/sorted_accepted_hits.bam '+annotationpath+' -i transcript_id > treated_index'+str(index+1)+'.txt'
    #print(commandline)
    os.system(commandline)

#Delete From___________________________________________________________________________________________
#If you don't use trimmomatic, delete from here 
#feed the output from last step: sorted_accepted_hits.bam to htseq_count using 2017version gff file
for index in range(0,int(len(untreated)/2)):
    commandline=htseqpath+'htseq-count --format=bam --stranded=no untreatedout_tirm_index'+str(index+1)+'/sorted_accepted_hits.bam '+annotationpath+' -i transcript_id > untreated_index'+str(index+1)+'.txt'
    #print(commandline)
    os.system(commandline)
for index in range(0,int(len(treated)/2)):
    commandline=htseqpath+'htseq-count --format=bam --stranded=no treatedout_trim_index'+str(index+1)+'/sorted_accepted_hits.bam '+annotationpath+' -i transcript_id > treated_index'+str(index+1)+'.txt'
    #print(commandline)
    os.system(commandline)
#If you don't use trimmomatic, delete end here 
#Delete end______________________________________________________________________________________________




    
