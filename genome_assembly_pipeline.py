# -*- coding: utf-8 -*-
"""Genome Assembly Pipeline.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1J0rZkucGUMFNIw4ZmV8OLRdlo7PSR54O

#Pipeline para análise de sequenciamento, montagem de genomas e análise da montagem


---
**Pipeline desenvolvida por Saulo Britto da Silva**

*Última atualização no dia 23.11.2020*

>Pipeline teste desenvolvida para analisar os arquivos de sequenciamento, realizar as montagens e analisar a qualidade das montagens.

---
"""

from google.colab import files
files.upload()

"""#Installing dependencies"""

#Prokka
!sudo apt-get install libdatetime-perl libxml-simple-perl libdigest-md5-perl git default-jre bioperl
!sudo cpan Bio::Perl
!git clone https://github.com/tseemann/prokka.git $HOME/prokka

#Prokka Correction makeblastdb
!rm '/usr/bin/makeblastdb'

#Prokka DataBase
!/root/prokka/bin/prokka --setupdb

#FastQC
!sudo apt install fastqc

#SPAdes
!wget http://cab.spbu.ru/files/release3.14.1/SPAdes-3.14.1-Linux.tar.gz
!tar -xzf SPAdes-3.14.1-Linux.tar.gz

# Commented out IPython magic to ensure Python compatibility.
#Edena
!wget http://www.genomic.ch/edena/EdenaV3.131028.tar.gz
!tar -xzf EdenaV3.131028.tar.gz
# %cd '/content/EdenaV3.131028'
!make
# %cd ..

# Commented out IPython magic to ensure Python compatibility.
#Unicycler
!sudo apt-get update
!sudo apt-get install gcc
!sudo apt-get install make
!sudo apt-get install libbz2-dev
!sudo apt-get install zlib1g-dev
!sudo apt-get install libncurses5-dev 
!sudo apt-get install libncursesw5-dev
!sudo apt-get install liblzma-dev

# %cd /content/
!wget https://github.com/samtools/htslib/releases/download/1.9/htslib-1.9.tar.bz2
!tar -vxjf htslib-1.9.tar.bz2
# %cd htslib-1.9
!make
# %cd ..
!wget https://github.com/samtools/samtools/releases/download/1.9/samtools-1.9.tar.bz2
!tar -vxjf samtools-1.9.tar.bz2
# %cd samtools-1.9
!make
# %cd ..

!git clone https://github.com/rrwick/Unicycler.git
# %cd Unicycler
!python3 setup.py install
# %cd ..

# Commented out IPython magic to ensure Python compatibility.
#QUAST
!sudo apt-get update && sudo apt-get install -y pkg-config libfreetype6-dev libpng-dev python3-matplotlib
!git clone https://github.com/ablab/quast
# %cd /content/quast
!./setup.py install
# %cd ..

#CONTIGuator
!git clone https://github.com/combogenomics/CONTIGuator

#Conectando o Google Drive à Pipeline
from google.colab import drive
drive.mount('/content/drive')

"""#FastQC"""

!fastqc '/content/drive/My Drive/IC UFLA/Sequenciamento/B137_Bab30 - sequências e resultados para praticar/25292_2#137_1.fastq'

"""Um arquivo .html foi criado na mesma pasta do arquivo analisado. Basta ir até o local e baixá-lo para visualizar a análise.

# Genome Assembly using SPAdes
"""

#testando a instalação
!/content/SPAdes-3.14.1-Linux/bin/spades.py --test

#Retirar  a # da opção escolhida

#Com vários K-mer  
#!/content/SPAdes-3.14.1-Linux/bin/spades.py -k 111,121,127 --careful -1 B_longum_1.fastq -2 B_longum_2.fastq -o spades_output
#!/content/SPAdes-3.14.1-Linux/bin/spades.py -k 111,121,127 --careful -1 '/content/drive/My Drive/IC UFLA/Sequenciamento/B137_Bab30 - sequências e resultados para praticar/25292_2#137_1.fastq' -2 '/content/drive/My Drive/IC UFLA/Sequenciamento/B137_Bab30 - sequências e resultados para praticar/25292_2#137_2.fastq' -o spades_output 

#Com apenas 1 k-mer 
#!/content/SPAdes-3.14.1-Linux/bin/spades.py -k 121 --careful -1 B_longum_1.fastq -2 B_longum_2.fastq -o spades_output
!/content/SPAdes-3.14.1-Linux/bin/spades.py -k 121 --careful -1 '/content/drive/My Drive/IC UFLA/Sequenciamento/B137_Bab30 - sequências e resultados para praticar/25292_2#137_1.fastq' -2 '/content/drive/My Drive/IC UFLA/Sequenciamento/B137_Bab30 - sequências e resultados para praticar/25292_2#137_2.fastq' -o spades_output

"""#Edena"""

#/content/EdenaV3.131028/bin/edena -nThreads <número_de_threads> -paired <arquivo_1.fastq> <arquivo_2.fastq> -p <nome_desejado_para_saída>

!/content/EdenaV3.131028/bin/edena -nThreads 8 -paired '/content/drive/My Drive/IC UFLA/Sequenciamento/B137_Bab30 - sequências e resultados para praticar/25292_2#137_1.fastq' '/content/drive/My Drive/IC UFLA/Sequenciamento/B137_Bab30 - sequências e resultados para praticar/25292_2#137_2.fastq' -p edena_bab30_2

#/content/EdenaV3.131028/bin/edena -e <arquivo.ovl> -p <nome_desejado_para_saída> -nThreads <número_de_threads>
 
 !/content/EdenaV3.131028/bin/edena -e '/content/EdenaV3.131028/edena_bab30_2.ovl' -p edena_bab30_final -nThreads 8

"""#Unicycler"""

#/opt/Unicycler20180426/Unicycler/unicycler-runner.py --spades_path /opt/SPAdes-3.9.1-Linux/bin/spades.py --samtools_path /opt/samtools-1.8/samtools/samtools  --pilon_path /opt/pilon/pilon-1.22.jar -1 file_reads_foward -2 file_reads_reverse -o unicycler_results

"""#QUAST


"""

#!./quast.py -R [genoma_referencia.fasta] -m 0 [montagem do edena] [montagem do spades]  

!/content/quast/quast.py -R '/content/drive/My Drive/IC UFLA/Genomas/prokka_Bab30_cro1/Bab30_cro1.fsa' -m 0 '/content/EdenaV3.131028/edena_bab30_final_contigs.fasta'

import IPython

display(IPython.display.HTML('/content/EdenaV3.131028/quast/quast_results/results_2020_11_16_16_59_45/report.html'))

"""#CONTIGuator"""

!python /content/CONTIGuator.py -r references.fna -c contigs.fna

"""#Prokka"""

# Vanilla (but with free toppings)
!prokka contigs.fa