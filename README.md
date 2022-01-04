1/4/2022

# Data Wrangling and Integration with pandas and numpy, using genome annotations and gene ontology definitions

We often have to integrate and reformat data to integrate into a report
or chart. In my case, I had to provide gene annotation details that are
at deeper level (transcript level) into a plot that was at a higher
level (locus level). Additionally, a column in the annotation file that
had gene ontology terms, was comma separated with no definitions. Those
terms needed to be placed into their own columns with definitions
provided from another file.

Please note, I’ll be using an R markdown file so that its easier to view
as the readme in this github repository, however, python code will be
utilized in code blocks. Additionally, a python file will be provided
(and potentially a jupyter notebook).

Here is a sample of what each files looked like:

**Genome Annotation**:

|  X.pacId | locusName       | transcriptName    | peptideName         | Pfam                            | Panther                   | KOG     | KEGG.ec  | KO     | GO                                                       | Best.hit.arabi.name | arabi.symbol                                                 | arabi.defline                                                              | Best.hit.rice.name | rice.symbol | rice.defline                                                  |
|---------:|:----------------|:------------------|:--------------------|:--------------------------------|:--------------------------|:--------|:---------|:-------|:---------------------------------------------------------|:--------------------|:-------------------------------------------------------------|:---------------------------------------------------------------------------|:-------------------|:------------|:--------------------------------------------------------------|
| 32806936 | Bradi0135s00100 | Bradi0135s00100.1 | Bradi0135s00100.1.p | PF00295                         | PTHR31375,PTHR31375:SF37  |         | 3.2.1.15 | K01213 | <GO:0005975,GO:0004650>                                  | AT3G07820.1         |                                                              | Pectin lyase-like superfamily protein                                      | LOC\_Os02g10300.1  | NA          | polygalacturonase, putative, expressed                        |
| 32805405 | Bradi1g00215    | Bradi1g00215.1    | Bradi1g00215.1.p    | PF00076                         | PTHR10501,PTHR10501:SF24  |         |          |        | <GO:0003676,GO:0017069,GO:0000398>                       | AT1G21320.1         |                                                              | nucleotide binding;nucleic acid binding                                    | LOC\_Os08g43360.1  | NA          | RNA recognition motif containing protein, putative, expressed |
| 32805623 | Bradi1g00272    | Bradi1g00272.1    | Bradi1g00272.1.p    | PF01554                         | PTHR11206,PTHR11206:SF102 | KOG1347 |          |        | <GO:0055085,GO:0016020,GO:0015297,GO:0015238,GO:0006855> | AT1G33110.1         |                                                              | MATE efflux family protein                                                 | LOC\_Os12g03260.1  | NA          | MATE efflux family protein, putative, expressed               |
| 32799309 | Bradi1g00350    | Bradi1g00350.1    | Bradi1g00350.1.p    | PF05000,PF04998,PF04992         | PTHR19376,PTHR19376:SF37  |         | 2.7.7.6  |        | <GO:0006351,GO:0003899,GO:0003677>                       | AT4G35800.1         | NRPB1,RNA\_POL\_II\_LS,RNA\_POL\_II\_LSRNA\_POL\_II\_LS,RPB1 | RNA polymerase II large subunit                                            | LOC\_Os05g05860.1  | NA          | retrotransposon protein, putative, unclassified, expressed    |
| 32793603 | Bradi1g00400    | Bradi1g00400.2    | Bradi1g00400.2.p    | PF02485                         | PTHR31042,PTHR31042:SF25  |         |          |        | <GO:0016020,GO:0008375>                                  | AT1G10280.1         |                                                              | Core-2/I-branching beta-1,6-N-acetylglucosaminyltransferase family protein | LOC\_Os04g20420.1  | NA          | DNA binding protein, putative, expressed                      |
| 32804480 | Bradi1g00607    | Bradi1g00607.1    | Bradi1g00607.1.p    | PF02736,PF00612,PF01843,PF00063 | PTHR13140,PTHR13140:SF382 |         | 3.6.4.1  | K10357 | <GO:0016459,GO:0005524,GO:0003774,GO:0005515>            | AT1G04160.1         | ATXIB,XI-8,XI-B,XIB                                          | myosin XI B                                                                | LOC\_Os03g64290.1  | NA          | myosin, putative, expressed                                   |
| 32804481 | Bradi1g00607    | Bradi1g00607.2    | Bradi1g00607.2.p    | PF00612,PF01843,PF00063         | PTHR13140,PTHR13140:SF382 |         | 3.6.4.1  |        | <GO:0005515,GO:0016459,GO:0005524,GO:0003774>            | AT1G04160.1         | ATXIB,XI-8,XI-B,XIB                                          | myosin XI B                                                                | LOC\_Os03g64290.1  | NA          | myosin, putative, expressed                                   |

**Gene ontology**:

| ID           | Name                                                     | Namespace           | alt\_id                 | Def                                                                                                                                                                                                                                                                                                                                     |
|:-------------|:---------------------------------------------------------|:--------------------|:------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| <GO:0000001> | mitochondrion inheritance                                | biological\_process |                         | The distribution of mitochondria, including the mitochondrial genome, into daughter cells after mitosis or meiosis, mediated by interactions between mitochondria and the cytoskeleton. \[GOC:mcc, <PMID:10873824>, <PMID:11389764>\]                                                                                                   |
| <GO:0000002> | mitochondrial genome maintenance                         | biological\_process |                         | The maintenance of the structure and integrity of the mitochondrial genome; includes replication and segregation of the mitochondrial chromosome. \[GOC:ai, GOC:vw\]                                                                                                                                                                    |
| <GO:0000003> | reproduction                                             | biological\_process | <GO:0019952,GO:0050876> |                                                                                                                                                                                                                                                                                                                                         |
| <GO:0000005> | obsolete ribosomal chaperone activity                    | molecular\_function |                         | OBSOLETE. Assists in the correct assembly of ribosomes or ribosomal subunits in vivo, but is not a component of the assembled ribosome when performing its normal biological function. \[GOC:jl, <PMID:12150913>\]                                                                                                                      |
| <GO:0000006> | high-affinity zinc transmembrane transporter activity    | molecular\_function |                         | Enables the transfer of zinc ions (Zn2+) from one side of a membrane to the other, probably powered by proton motive force. In high-affinity transport the transporter is able to bind the solute even if it is only present at very low concentrations. \[TC:2.A.5.1.1\]                                                               |
| <GO:0000007> | low-affinity zinc ion transmembrane transporter activity | molecular\_function |                         | Enables the transfer of a solute or solutes from one side of a membrane to the other according to the reaction: Zn2+ = Zn2+, probably powered by proton motive force. In low-affinity transport the transporter is able to bind the solute only if it is present at very high concentrations. \[GOC:mtg\_transport, <ISBN:0815340729>\] |

Its important to note that the gene ontology file has already been
modified from its intial format in the [Converting non-tabular data into
tabular data using
Python](https://github.com/patmendoza330/geneontologyconversion)
repository. Feel free to look that over for ways in which I modified
that format into tabular format.

## Issues

So, there were several issues, I needed to:

1.  Collapse the data in the genome annotation file so that only one
    record appeared for each locus but also included a column with all
    unique gene ontology terms for all transcripts that were associated
    with the gene.
2.  Split the comma delimited gene ontology column into as many columns
    were necessary and include the definition for those terms from the
    gene ontology file.

## Solution

### Libraries needed

Lets first install all of the needed libraries:

``` python
import pandas as pd
import numpy as np
```

Briefly, pandas will be the library that allows us to use dataframes,
SQL joins, and other functions necessary to manipulate the data, numpy
will provide us with any mathematical aids that are necessary (creating
numbers, etc.). Conversely, in R, the tidyr and dplyr packages were
used.

### Gene annotation file

Lets take the genome annotation file first and go over the steps that we
need.

Firs things first, lets load in the table:

``` python
y1 = pd.read_csv(r'supporting.files\Bdistachyon_314_v3.1.annotation_info.txt', sep="\t", header=0)
pd.set_option('display.max_columns', None)
len(y1.index)
```

    ## 52972

``` r
knitr::kable(head(py$y1), "pipe")
```

|  \#pacId | locusName       | transcriptName    | peptideName         | Pfam                    | Panther                   | KOG | KEGG/ec | KO     | GO           | Best-hit-arabi-name | arabi-symbol | arabi-defline                                   | Best-hit-rice-name | rice-symbol | rice-defline                              |
|---------:|:----------------|:------------------|:--------------------|:------------------------|:--------------------------|:----|:--------|:-------|:-------------|:--------------------|:-------------|:------------------------------------------------|:-------------------|------------:|:------------------------------------------|
| 32823775 | Bradi0012s00100 | Bradi0012s00100.1 | Bradi0012s00100.1.p | PF03144,PF03143,PF00009 | PTHR23115,PTHR23115:SF157 | NaN | 3.6.5.3 | K03231 | <GO:0005525> | AT1G07920.1         | NaN          | GTP binding Elongation factor Tu family protein | LOC\_Os03g08010.1  |         NaN | elongation factor Tu, putative, expressed |
| 32823776 | Bradi0012s00201 | Bradi0012s00201.1 | Bradi0012s00201.1.p | NaN                     | NaN                       | NaN | NaN     | NaN    | NaN          | NaN                 | NaN          | NaN                                             | NaN                |         NaN | NaN                                       |
| 32823777 | Bradi0012s00201 | Bradi0012s00201.2 | Bradi0012s00201.2.p | NaN                     | NaN                       | NaN | NaN     | NaN    | NaN          | NaN                 | NaN          | NaN                                             | NaN                |         NaN | NaN                                       |
| 32823779 | Bradi0012s00201 | Bradi0012s00201.3 | Bradi0012s00201.3.p | NaN                     | NaN                       | NaN | NaN     | NaN    | NaN          | NaN                 | NaN          | NaN                                             | NaN                |         NaN | NaN                                       |
| 32823780 | Bradi0012s00201 | Bradi0012s00201.4 | Bradi0012s00201.4.p | NaN                     | NaN                       | NaN | NaN     | NaN    | NaN          | NaN                 | NaN          | NaN                                             | NaN                |         NaN | NaN                                       |
| 32823778 | Bradi0012s00201 | Bradi0012s00201.5 | Bradi0012s00201.5.p | NaN                     | NaN                       | NaN | NaN     | NaN    | NaN          | NaN                 | NaN          | NaN                                             | NaN                |         NaN | NaN                                       |

Next, lets select only the fields that we want:

``` python
y2 = y1[['locusName', 'GO']].copy()
len(y2.index)
```

    ## 52972

``` r
knitr::kable(head(py$y2), "pipe")
```

| locusName       | GO           |
|:----------------|:-------------|
| Bradi0012s00100 | <GO:0005525> |
| Bradi0012s00201 | NaN          |
| Bradi0012s00201 | NaN          |
| Bradi0012s00201 | NaN          |
| Bradi0012s00201 | NaN          |
| Bradi0012s00201 | NaN          |

Ok, so now we have a table that has 52,972 records. We need to collapse
the locusName column and ensure that we have only unique gene ontology
terms. We’ll complete this first by dropping records that don’t have
values, then using a lambda join function:

``` python
y2.dropna(inplace=True)
y2.reset_index(drop=True, inplace=True)
y2['GO'] = y2.groupby('locusName')['GO'].transform(lambda x : ','.join(x))
len(y2.index)
```

    ## 24281

``` python
len(pd.unique(y2['locusName']))
```

    ## 14791

``` r
knitr::kable(head(py$y2), "pipe")
```

| locusName       | GO                      |
|:----------------|:------------------------|
| Bradi0012s00100 | <GO:0005525>            |
| Bradi0014s00100 | <GO:0043531>            |
| Bradi0135s00100 | <GO:0005975,GO:0004650> |
| Bradi0180s00100 | <GO:0005975,GO:0004650> |
| Bradi1g00200    | <GO:0005515>            |
| Bradi1g00210    | <GO:0005515>            |

As you can see, we now have collapsed the table into 24,281 rows. But,
the number of unique locusName is 14,791. Lets take a look at an entry
to figure out what’s going on.

``` python
y2.loc[y2['locusName'] =='Bradi1g00517']
```

    ##        locusName                                                 GO
    ## 35  Bradi1g00517  GO:0003676,GO:0003676,GO:0003676,GO:0003676,GO...
    ## 36  Bradi1g00517  GO:0003676,GO:0003676,GO:0003676,GO:0003676,GO...
    ## 37  Bradi1g00517  GO:0003676,GO:0003676,GO:0003676,GO:0003676,GO...
    ## 38  Bradi1g00517  GO:0003676,GO:0003676,GO:0003676,GO:0003676,GO...
    ## 39  Bradi1g00517  GO:0003676,GO:0003676,GO:0003676,GO:0003676,GO...
    ## 40  Bradi1g00517  GO:0003676,GO:0003676,GO:0003676,GO:0003676,GO...
    ## 41  Bradi1g00517  GO:0003676,GO:0003676,GO:0003676,GO:0003676,GO...
    ## 42  Bradi1g00517  GO:0003676,GO:0003676,GO:0003676,GO:0003676,GO...
    ## 43  Bradi1g00517  GO:0003676,GO:0003676,GO:0003676,GO:0003676,GO...

Because the locusName’s could have had multiple rows, the output of the
join also has multiple rows. We can fix this by dropping any duplicate
rows

``` python
y2 = y2.drop_duplicates(inplace=False, ignore_index=True)
y2.loc[y2['locusName'] =='Bradi1g00517']
```

    ##        locusName                                                 GO
    ## 22  Bradi1g00517  GO:0003676,GO:0003676,GO:0003676,GO:0003676,GO...

``` python
len(y2.index)
```

    ## 14791

``` python
len(pd.unique(y2['locusName']))
```

    ## 14791

Ok, now we’re good! The number or records corresponds with the number of
unique locusName.

However, you may have noticed that the GO terms for the Bradi1g00517
locus included duplicate GO terms. Lets pick out only unique terms for
that column.

``` python
y2['GO'] = y2['GO'].str.split(',').apply(lambda x: pd.unique(x))
y2.loc[y2['locusName'] =='Bradi1g00517']
```

    ##        locusName            GO
    ## 22  Bradi1g00517  [GO:0003676]

This eliminates duplicates but places the final column in list format.
We can convert it back to comma separated strings below:

``` python
y2['GO'] = [','.join(map(str, x)) for x in y2['GO']]
y2.loc[y2['locusName'] =='Bradi1g00517']
```

    ##        locusName          GO
    ## 22  Bradi1g00517  GO:0003676

``` r
knitr::kable(head(py$y2), "pipe")
```

| locusName       | GO                      |
|:----------------|:------------------------|
| Bradi0012s00100 | <GO:0005525>            |
| Bradi0014s00100 | <GO:0043531>            |
| Bradi0135s00100 | <GO:0005975,GO:0004650> |
| Bradi0180s00100 | <GO:0005975,GO:0004650> |
| Bradi1g00200    | <GO:0005515>            |
| Bradi1g00210    | <GO:0005515>            |

## Gene Ontology File

Lets load in the file

``` python
z1 = pd.read_csv(r'supporting.files\go.obo.txt', sep="\t", header=0)
pd.set_option('display.max_columns', None)
```

``` r
knitr::kable(head(py$z1), "pipe")
```

| ID           | Name                                                     | Namespace           | alt\_id                 | Def                                                                                                                                                                                                                                                                                                                                     |
|:-------------|:---------------------------------------------------------|:--------------------|:------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| <GO:0000001> | mitochondrion inheritance                                | biological\_process | NaN                     | The distribution of mitochondria, including the mitochondrial genome, into daughter cells after mitosis or meiosis, mediated by interactions between mitochondria and the cytoskeleton. \[GOC:mcc, <PMID:10873824>, <PMID:11389764>\]                                                                                                   |
| <GO:0000002> | mitochondrial genome maintenance                         | biological\_process | NaN                     | The maintenance of the structure and integrity of the mitochondrial genome; includes replication and segregation of the mitochondrial chromosome. \[GOC:ai, GOC:vw\]                                                                                                                                                                    |
| <GO:0000003> | reproduction                                             | biological\_process | <GO:0019952,GO:0050876> | NaN                                                                                                                                                                                                                                                                                                                                     |
| <GO:0000005> | obsolete ribosomal chaperone activity                    | molecular\_function | NaN                     | OBSOLETE. Assists in the correct assembly of ribosomes or ribosomal subunits in vivo, but is not a component of the assembled ribosome when performing its normal biological function. \[GOC:jl, <PMID:12150913>\]                                                                                                                      |
| <GO:0000006> | high-affinity zinc transmembrane transporter activity    | molecular\_function | NaN                     | Enables the transfer of zinc ions (Zn2+) from one side of a membrane to the other, probably powered by proton motive force. In high-affinity transport the transporter is able to bind the solute even if it is only present at very low concentrations. \[TC:2.A.5.1.1\]                                                               |
| <GO:0000007> | low-affinity zinc ion transmembrane transporter activity | molecular\_function | NaN                     | Enables the transfer of a solute or solutes from one side of a membrane to the other according to the reaction: Zn2+ = Zn2+, probably powered by proton motive force. In low-affinity transport the transporter is able to bind the solute only if it is present at very high concentrations. \[GOC:mtg\_transport, <ISBN:0815340729>\] |

I also want to rename the first column so that it matches our annotation
file:

``` python
z1.rename(columns={'ID':'GO'}, inplace=True)
```

``` r
knitr::kable(head(py$z1), "pipe")
```

| GO           | Name                                                     | Namespace           | alt\_id                 | Def                                                                                                                                                                                                                                                                                                                                     |
|:-------------|:---------------------------------------------------------|:--------------------|:------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| <GO:0000001> | mitochondrion inheritance                                | biological\_process | NaN                     | The distribution of mitochondria, including the mitochondrial genome, into daughter cells after mitosis or meiosis, mediated by interactions between mitochondria and the cytoskeleton. \[GOC:mcc, <PMID:10873824>, <PMID:11389764>\]                                                                                                   |
| <GO:0000002> | mitochondrial genome maintenance                         | biological\_process | NaN                     | The maintenance of the structure and integrity of the mitochondrial genome; includes replication and segregation of the mitochondrial chromosome. \[GOC:ai, GOC:vw\]                                                                                                                                                                    |
| <GO:0000003> | reproduction                                             | biological\_process | <GO:0019952,GO:0050876> | NaN                                                                                                                                                                                                                                                                                                                                     |
| <GO:0000005> | obsolete ribosomal chaperone activity                    | molecular\_function | NaN                     | OBSOLETE. Assists in the correct assembly of ribosomes or ribosomal subunits in vivo, but is not a component of the assembled ribosome when performing its normal biological function. \[GOC:jl, <PMID:12150913>\]                                                                                                                      |
| <GO:0000006> | high-affinity zinc transmembrane transporter activity    | molecular\_function | NaN                     | Enables the transfer of zinc ions (Zn2+) from one side of a membrane to the other, probably powered by proton motive force. In high-affinity transport the transporter is able to bind the solute even if it is only present at very low concentrations. \[TC:2.A.5.1.1\]                                                               |
| <GO:0000007> | low-affinity zinc ion transmembrane transporter activity | molecular\_function | NaN                     | Enables the transfer of a solute or solutes from one side of a membrane to the other according to the reaction: Zn2+ = Zn2+, probably powered by proton motive force. In low-affinity transport the transporter is able to bind the solute only if it is present at very high concentrations. \[GOC:mtg\_transport, <ISBN:0815340729>\] |

## Bringing it all together

Ok, so now we’ve made some modifications to the annotation file and
we’ve loaded in the GO terms and their definitions. Now we need a way to
join them together and present a table that has each gene, and all of
their associated GO terms and definitions as respective columns.

First we need to flatten our annotation file so that we have multiple
rows for every GO term:

``` python
gene_go = y2.copy()
```

I know that I converted my gene file with GO terms back into strings,
but it turns out that if I want to flatten this file with multiple rows
for each GO term I need it in list format. I’ll do that prior to using
the explode function that will flatten it:

``` python
gene_go.GO = gene_go.GO.str.split(',')
```

``` r
knitr::kable(head(py$gene_go), "pipe")
```

| locusName       | GO                         |
|:----------------|:---------------------------|
| Bradi0012s00100 | <GO:0005525>               |
| Bradi0014s00100 | <GO:0043531>               |
| Bradi0135s00100 | <GO:0005975>, <GO:0004650> |
| Bradi0180s00100 | <GO:0005975>, <GO:0004650> |
| Bradi1g00200    | <GO:0005515>               |
| Bradi1g00210    | <GO:0005515>               |

``` python
gene_go = gene_go.explode('GO')
```

``` r
knitr::kable(head(py$gene_go), "pipe")
```

    ## Warning in py_to_r.pandas.core.frame.DataFrame(x): index contains duplicated
    ## values: row names not set

| locusName       | GO           |
|:----------------|:-------------|
| Bradi0012s00100 | <GO:0005525> |
| Bradi0014s00100 | <GO:0043531> |
| Bradi0135s00100 | <GO:0005975> |
| Bradi0135s00100 | <GO:0004650> |
| Bradi0180s00100 | <GO:0005975> |
| Bradi0180s00100 | <GO:0004650> |

As you can see, the explode function will create duplicate rows for
every GO term in the GO column that is separated by a comma. Now we can
do a join to the gene ontology file:

``` python
# Columns that I intend to use from the gene annotation file
cols_to_use = list(['GO', 'Namespace', 'Name', 'Def'])
# Make a join
gene_go = pd.merge(gene_go, z1[cols_to_use], on='GO', how='left')
```

``` r
knitr::kable(head(py$gene_go), "pipe")
```

|     | locusName       | GO           | Namespace           | Name                           | Def                                                                                                                                   |
|:----|:----------------|:-------------|:--------------------|:-------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------|
| 0   | Bradi0012s00100 | <GO:0005525> | molecular\_function | GTP binding                    | Interacting selectively and non-covalently with GTP, guanosine triphosphate. \[GOC:ai\]                                               |
| 1   | Bradi0014s00100 | <GO:0043531> | molecular\_function | ADP binding                    | Interacting selectively and non-covalently with ADP, adenosine 5’-diphosphate. \[GOC:jl\]                                             |
| 2   | Bradi0135s00100 | <GO:0005975> | biological\_process | carbohydrate metabolic process | NaN                                                                                                                                   |
| 3   | Bradi0135s00100 | <GO:0004650> | molecular\_function | polygalacturonase activity     | Catalysis of the random hydrolysis of (1-&gt;4)-alpha-D-galactosiduronic linkages in pectate and other galacturonans. \[EC:3.2.1.15\] |
| 4   | Bradi0180s00100 | <GO:0005975> | biological\_process | carbohydrate metabolic process | NaN                                                                                                                                   |
| 5   | Bradi0180s00100 | <GO:0004650> | molecular\_function | polygalacturonase activity     | Catalysis of the random hydrolysis of (1-&gt;4)-alpha-D-galactosiduronic linkages in pectate and other galacturonans. \[EC:3.2.1.15\] |

Now, this is great, and its getting closer to where we want to be, but
we need to have a table with a single row for each locusName and a
column that has the GO term, Namespace, Name, and Def all pasted into an
individual column for each GO term.

Lets start by collapsing the columns in this table by pasting all the
gene ontology related information into one column (separated by a
comma):

``` python
gene_go.GO = gene_go[cols_to_use].apply(lambda x: ','.join(x[x.notnull()]), axis=1)
# Removing now redundant columns
gene_go.drop(['Namespace', 'Name', 'Def'], axis=1, inplace=True)
gene_go = gene_go.sort_values('locusName', ascending=True)
```

``` r
knitr::kable(head(py$gene_go), "pipe")
```

|     | locusName       | GO                                                                                                                                                                                               |
|:----|:----------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0   | Bradi0012s00100 | <GO:0005525,molecular_function,GTP> binding,Interacting selectively and non-covalently with GTP, guanosine triphosphate. \[GOC:ai\]                                                              |
| 1   | Bradi0014s00100 | <GO:0043531,molecular_function,ADP> binding,Interacting selectively and non-covalently with ADP, adenosine 5’-diphosphate. \[GOC:jl\]                                                            |
| 2   | Bradi0135s00100 | <GO:0005975,biological_process,carbohydrate> metabolic process                                                                                                                                   |
| 3   | Bradi0135s00100 | <GO:0004650,molecular_function,polygalacturonase> activity,Catalysis of the random hydrolysis of (1-&gt;4)-alpha-D-galactosiduronic linkages in pectate and other galacturonans. \[EC:3.2.1.15\] |
| 4   | Bradi0180s00100 | <GO:0005975,biological_process,carbohydrate> metabolic process                                                                                                                                   |
| 5   | Bradi0180s00100 | <GO:0004650,molecular_function,polygalacturonase> activity,Catalysis of the random hydrolysis of (1-&gt;4)-alpha-D-galactosiduronic linkages in pectate and other galacturonans. \[EC:3.2.1.15\] |

Now we need to finish up the table by adding an intermediate column that
will label all GO terms incrementally, then using the pivot function to
put them into columns

``` python
gene_go['Var'] = gene_go.groupby('locusName').cumcount()+1
```

``` r
knitr::kable(head(py$gene_go), "pipe")
```

|     | locusName       | GO                                                                                                                                                                                               | Var |
|:----|:----------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----:|
| 0   | Bradi0012s00100 | <GO:0005525,molecular_function,GTP> binding,Interacting selectively and non-covalently with GTP, guanosine triphosphate. \[GOC:ai\]                                                              |   1 |
| 1   | Bradi0014s00100 | <GO:0043531,molecular_function,ADP> binding,Interacting selectively and non-covalently with ADP, adenosine 5’-diphosphate. \[GOC:jl\]                                                            |   1 |
| 2   | Bradi0135s00100 | <GO:0005975,biological_process,carbohydrate> metabolic process                                                                                                                                   |   1 |
| 3   | Bradi0135s00100 | <GO:0004650,molecular_function,polygalacturonase> activity,Catalysis of the random hydrolysis of (1-&gt;4)-alpha-D-galactosiduronic linkages in pectate and other galacturonans. \[EC:3.2.1.15\] |   2 |
| 4   | Bradi0180s00100 | <GO:0005975,biological_process,carbohydrate> metabolic process                                                                                                                                   |   1 |
| 5   | Bradi0180s00100 | <GO:0004650,molecular_function,polygalacturonase> activity,Catalysis of the random hydrolysis of (1-&gt;4)-alpha-D-galactosiduronic linkages in pectate and other galacturonans. \[EC:3.2.1.15\] |   2 |

The way that we’ve constructed the Var column creates a column that
stores the number of gene ontology terms for each locusName. When a new
GO term is introduced in the table, the Var column has an incremented
value.

The pivot\_wider function (below) will give us our final desired table.
If a locusName does not have a GO term for a specific column, NA is
entered.

``` python
gene_go_pivoted = gene_go.pivot(index='locusName', columns='Var', values='GO')
```

``` r
knitr::kable(head(py$gene_go_pivoted), "pipe")
```

|                 | 1                                                                                                                                     | 2                                                                                                                                                                                                | 3   | 4   | 5   | 6   | 7   | 8   | 9   |
|:----------------|:--------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----|:----|:----|:----|:----|:----|:----|
| Bradi0012s00100 | <GO:0005525,molecular_function,GTP> binding,Interacting selectively and non-covalently with GTP, guanosine triphosphate. \[GOC:ai\]   | NaN                                                                                                                                                                                              | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Bradi0014s00100 | <GO:0043531,molecular_function,ADP> binding,Interacting selectively and non-covalently with ADP, adenosine 5’-diphosphate. \[GOC:jl\] | NaN                                                                                                                                                                                              | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Bradi0135s00100 | <GO:0005975,biological_process,carbohydrate> metabolic process                                                                        | <GO:0004650,molecular_function,polygalacturonase> activity,Catalysis of the random hydrolysis of (1-&gt;4)-alpha-D-galactosiduronic linkages in pectate and other galacturonans. \[EC:3.2.1.15\] | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Bradi0180s00100 | <GO:0005975,biological_process,carbohydrate> metabolic process                                                                        | <GO:0004650,molecular_function,polygalacturonase> activity,Catalysis of the random hydrolysis of (1-&gt;4)-alpha-D-galactosiduronic linkages in pectate and other galacturonans. \[EC:3.2.1.15\] | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Bradi1g00200    | <GO:0005515,molecular_function,protein> binding                                                                                       | NaN                                                                                                                                                                                              | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Bradi1g00210    | <GO:0005515,molecular_function,protein> binding                                                                                       | NaN                                                                                                                                                                                              | NaN | NaN | NaN | NaN | NaN | NaN | NaN |

Now, if we wanted to add this back to our original annotation file, we’d
simply make a join between this new table and our original:

``` python
yFinal = pd.merge(y1, gene_go_pivoted, on='locusName', how='left')
```

``` r
knitr::kable(head(py$yFinal), "pipe")
```

|     |  \#pacId | locusName       | transcriptName    | peptideName         | Pfam                    | Panther                   | KOG | KEGG/ec | KO     | GO           | Best-hit-arabi-name | arabi-symbol | arabi-defline                                   | Best-hit-rice-name | rice-symbol | rice-defline                              | 1                                                                                                                                   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   |
|:----|---------:|:----------------|:------------------|:--------------------|:------------------------|:--------------------------|:----|:--------|:-------|:-------------|:--------------------|:-------------|:------------------------------------------------|:-------------------|------------:|:------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------|:----|:----|:----|:----|:----|:----|:----|:----|
| 0   | 32823775 | Bradi0012s00100 | Bradi0012s00100.1 | Bradi0012s00100.1.p | PF03144,PF03143,PF00009 | PTHR23115,PTHR23115:SF157 | NaN | 3.6.5.3 | K03231 | <GO:0005525> | AT1G07920.1         | NaN          | GTP binding Elongation factor Tu family protein | LOC\_Os03g08010.1  |         NaN | elongation factor Tu, putative, expressed | <GO:0005525,molecular_function,GTP> binding,Interacting selectively and non-covalently with GTP, guanosine triphosphate. \[GOC:ai\] | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 1   | 32823776 | Bradi0012s00201 | Bradi0012s00201.1 | Bradi0012s00201.1.p | NaN                     | NaN                       | NaN | NaN     | NaN    | NaN          | NaN                 | NaN          | NaN                                             | NaN                |         NaN | NaN                                       | NaN                                                                                                                                 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 2   | 32823777 | Bradi0012s00201 | Bradi0012s00201.2 | Bradi0012s00201.2.p | NaN                     | NaN                       | NaN | NaN     | NaN    | NaN          | NaN                 | NaN          | NaN                                             | NaN                |         NaN | NaN                                       | NaN                                                                                                                                 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 3   | 32823779 | Bradi0012s00201 | Bradi0012s00201.3 | Bradi0012s00201.3.p | NaN                     | NaN                       | NaN | NaN     | NaN    | NaN          | NaN                 | NaN          | NaN                                             | NaN                |         NaN | NaN                                       | NaN                                                                                                                                 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 4   | 32823780 | Bradi0012s00201 | Bradi0012s00201.4 | Bradi0012s00201.4.p | NaN                     | NaN                       | NaN | NaN     | NaN    | NaN          | NaN                 | NaN          | NaN                                             | NaN                |         NaN | NaN                                       | NaN                                                                                                                                 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 5   | 32823778 | Bradi0012s00201 | Bradi0012s00201.5 | Bradi0012s00201.5.p | NaN                     | NaN                       | NaN | NaN     | NaN    | NaN          | NaN                 | NaN          | NaN                                             | NaN                |         NaN | NaN                                       | NaN                                                                                                                                 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |

# Conclusion

We now have a an annotation table that includes not just the GO terms
without definitions, but all deifinitions for each GO term included in
their own column.

# Citations

Ashburner, et al. (2000, 2000/05/01). Gene Ontology: tool for the
unification of biology. Nature Genetics, 25(1), 25-29.
<https://doi.org/10.1038/75556>

Gene Ontology, C. (2021). The Gene Ontology resource: enriching a GOld
mine. Nucleic acids research, 49(D1), D325-D334.
<https://doi.org/10.1093/nar/gkaa1113>

The International Brachypodium, I. (2010, 02/11/online). Genome
sequencing and analysis of the model grass Brachypodium distachyon
\[Article\]. Nature, 463, 763. <https://doi.org/10.1038/nature08747>
