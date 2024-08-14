# microPITA加速版本 by 王雪涵

<table>
  <tr>
    <th></th>
    <th></th>
    <th colspan="4" style="text-align: center; vertical-align: middle;border-left: 1px solid;">distinct</th>
    <th colspan="4" style="text-align: center; vertical-align: middle;border-left: 1px solid;">discriminant</th>
  </tr>
  <tr>
    <th>ASV数</th>
    <th>样本数</th>
    <th style="border-left: 1px solid;">新脚本运行时间</th>
    <th>旧脚本运行时间</th>
    <th>新脚本最大消耗内存</th>
    <th>旧脚本最大消耗内存</th>
    <th style="border-left: 1px solid;">新脚本运行时间</th>
    <th>旧脚本运行时间</th>
    <th>新脚本最大消耗内存</th>
    <th>旧脚本最大消耗内存</th>
  </tr>
  <tr>
    <td>70072</td>
    <td>99</td>
    <td>1m26.003s</td>
    <td>98m57.422s</td>
    <td>409.215M</td>
    <td>410.715M</td>
    <td>1m26.784s</td>
    <td>101m9.540s</td>
    <td>409.742M</td>
    <td>410.730M</td>
  </tr>
  <tr>
    <td>27245</td>
    <td>128</td>
    <td>2m17.255s</td>
    <td>725m7.820s</td>
    <td>231.918M</td>
    <td>232.133M</td>
    <td>2m10.973s</td>
    <td>713m29.524s</td>
    <td>231.922M</td>
    <td>232.129M</td>
  </tr>
  <tr>
    <td>165064</td>
    <td>522</td>
    <td>58m58.144s</td>
    <td>15448m25.926s</td>
    <td>3.842G</td>
    <td>3.845G</td>
    <td>78m30.488s</td>
    <td>>9d</td>
    <td>3.842G</td>
    <td>3.845G</td>
  </tr>
  <tr>
    <td>21955</td>
    <td>240</td>
    <td>0m12.054s</td>
    <td>5m14.873s</td>
    <td>311.430M</td>
    <td>311.402M</td>
    <td>0m34.942s</td>
    <td>5m15.221s</td>
    <td>45.637M</td>
    <td>311.402M</td>
  </tr>
  <tr>
    <td>18383</td>
    <td>513</td>
    <td>14m30.452s</td>
    <td>>9d</td>
    <td>475.305M</td>
    <td>471.816M</td>
    <td>15m16.039s</td>
    <td>2345m7.338s</td>
    <td>475.398M</td>
    <td>471.812M</td>
  </tr>
  <tr>
    <td>42170</td>
    <td>276</td>
    <td>0m55.925s</td>
    <td>56m18.635s</td>
    <td>618.613M</td>
    <td>617.145M</td>
    <td>0m57.075s</td>
    <td>60m36.021s</td>
    <td>629.680M</td>
    <td>617.117M</td>
  </tr>
  <tr>
    <td>4674</td>
    <td>40</td>
    <td>0m6.492s</td>
    <td>0m35.133s</td>
    <td>12.125M</td>
    <td>8.570M</td>
    <td>0m3.244s</td>
    <td>0m30.951s</td>
    <td>69.773M</td>
    <td>8.570M</td>
  </tr>
  <tr>
    <td>3144</td>
    <td>24</td>
    <td>0m4.388s</td>
    <td>0m5.368s</td>
    <td>16.277M</td>
    <td>12.547M</td>
    <td>0m8.133s</td>
    <td>0m6.556s</td>
    <td>12.547M</td>
    <td>12.547M</td>
  </tr>
</table>
  



# Using microPITA commandline #

These common commands can be used on the default data set obtained when downloading microPITA, simply cut and paste them into a commandline in the downloaded microPITA directory.


## Expected input file. ##

I. PCL file or BIOM file

BIOM file definition:
For BIOM file definition please see http://biom-format.org/

PCL file definition:
Although some defaults can be changed, microPITA expects a PCL file as an input file. Several PCL files are supplied by default in the input directory. A PCL file is a TEXT delimited file similar to an excel spread sheet with the following characteristics.

1. Rows represent metadata and features (bugs), columns represent samples.
2. The first row by default should be the sample ids.
3. Metadata rows should be next.
4. Lastly, rows containing features (bugs) measurements (like abundance) should be after metadata rows.
5. The first column should contain the ID describing the column. For metadata this may be, for example, "Age" for a row containing the age of the patients donating the samples. For measurements, this should be the feature name (bug name).
5. By default the file is expected to be TAB delimited.
6. If a consensus lineage or hierarchy of taxonomy is contained in the feature name, the default delimiter between clades is the pipe ("|").

II. Targeted feature file
If using the targeted feature methodology, you will need to provide a txt file listing the feature(s) of interest. Each feature should be on it's own line and should be written as found in the input PCL file.


## Basic unsupervised methods ##
Please note, all calls to microPITA should work interchangeably with PCL or BIOM files. BIOM files do not require the --lastmeta or --id arguments.

There are four unsupervised methods which can be performed:
diverse (maximum diversity), extreme (most dissimilar), representative (representative dissimilarity) and features (targeted feature).

The first three methods are performed as follows (selecting a default 10 samples):

> python MicroPITA.py --lastmeta Label -m representative input/Test.pcl output.txt
> python MicroPITA.py -m representative input/Test.biom output.txt

> python MicroPITA.py --lastmeta Label -m diverse input/Test.pcl output.txt
> python MicroPITA.py -m diverse input/Test.biom output.txt

> python MicroPITA.py --lastmeta Label -m extreme input/Test.pcl output.txt
> python MicroPITA.py -m extreme input/Test.biom output.txt

Each of the previous methods are made up of the following pieces:
1. python MicroPITA.py to call the microPITA script.
2. --lastmeta which indicates the keyword (first column value) of the last row that contains metadata (PCL input only).
3. -m which indicates the method to use in selection.
4. input/Test.pcl or input/Test.biom which is the first positional argument indicating an input file
5. output.txt which is the second positional argument indicating the location to write to the output file.

Selecting specific features has additional arguments to consider --targets (required) and --feature_method (optional).

> python MicroPITA.py --lastmeta Label -m features --targets input/TestFeatures.taxa input/Test.pcl output.txt
> python MicroPITA.py -m features --targets input/TestFeatures.taxa input/Test.biom output.txt

> python MicroPITA.py --lastmeta Label -m features --feature_method abundance --targets input/TestFeatures.taxa input/Test.pcl output.txt
> python MicroPITA.py -m features --feature_method abundance --targets input/TestFeatures.taxa input/Test.biom output.txt

These additional arguments are described as:
1. --targets The path to the file that has the features (bugs or clades) of interest. Make sure they are written as they appear in your input file!
2. --feature_method is the method of selection used and can be based on ranked abundance ("rank") or abundance ("abundance"). The default value is rank.
To differentiate the methods, rank tends to select samples in which the feature dominates the samples regardless of it's abundance.
Abundance tends to select samples in which the feature is most abundant without a guarantee that the feature is the most abundant feature in the sample. 


## Basic supervised methods ##

Two supervised methods are also available:
distinct and discriminant

These methods require an additional argument --label which is the first column keyword of the row used to classify samples for the supervised methods.
These methods can be performed as follows:

> python MicroPITA.py --lastmeta Label --label Label -m distinct input/Test.pcl output.txt
> python MicroPITA.py --label Label -m distinct input/Test.biom output.txt

> python MicroPITA.py --lastmeta Label --label Label -m discriminant input/Test.pcl output.txt
> python MicroPITA.py --label Label -m discriminant input/Test.biom output.txt


## Custom alpha- and beta-diversities ##

The default alpha diversity for the maximum diversity sampling method is inverse simpson; the default beta-diversity for representative and most dissimilar
selection is bray-curtis dissimilarity. There are several mechanisms that allow one to change this. You may: 

1. Choose from a selection of alpha-diveristy metrics.
Note when supplying an alpha diversity. This will affect the maximum diveristy sampling method only. Please make sure to use a diversity metric where the larger number indicates a higher diversity. If this is not the case make sure to use the -f or --invertDiversity flag to invert the metric. The inversion is multiplicative (1/alpha-metric).

> python MicroPITA.py --lastmeta Label -m diverse -a simpson input/Test.pcl output.txt
> python MicroPITA.py -m diverse -a simpson input/Test.biom output.txt

A case where inverting the metric is needed.

> python MicroPITA.py --lastmeta Label -m diverse -a dominance -f input/Test.pcl output.txt
> python MicroPITA.py -m diverse -a dominance -f input/Test.biom output.txt

2. Choose from a selection of beta-diversity metrics.
Note when supplying a beta-diversity. This will effect both the representative and most dissimilar sampling methods. The metric as given will be used for the representative method while 1-beta-metric is used for the most dissimilar.

> python MicroPITA.py --lastmeta Label -m representative -b euclidean input/Test.pcl output.txt
> python MicroPITA.py -m representative -b euclidean input/Test.biom output.txt

> python MicroPITA.py --lastmeta Label -m extreme -b euclidean input/Test.pcl output.txt
> python MicroPITA.py -m extreme -b euclidean input/Test.biom output.txt

Note for using Unifrac. Both Weighted and Unweighted unifrac are available for use. Make sure to supply the associated tree (-o, --tree) and environment files 
(-i,--envr) as well as indicate using Unifrac with (-b,--beta)

> python MicroPITA.py --lastmeta Label -m extreme -b unifrac_weighted -o input/Test.tree -i input/Test-env.txt input/Test.pcl output.txt
> python MicroPITA.py -m extreme -b unifrac_weighted -o input/Test.tree -i input/Test-env.txt input/Test.biom output.txt
> python MicroPITA.py --lastmeta Label -m extreme -b unifrac_unweighted -o input/Test.tree -i input/Test-env.txt input/Test.pcl output.txt
> python MicroPITA.py -m extreme -b unifrac_unweighted -o input/Test.tree -i input/Test-env.txt input/Test.biom output.txt
> python MicroPITA.py --lastmeta Label -m representative -b unifrac_weighted -o input/Test.tree -i input/Test-env.txt input/Test.pcl output.txt
> python MicroPITA.py -m representative -b unifrac_weighted -o input/Test.tree -i input/Test-env.txt input/Test.biom output.txt
> python MicroPITA.py --lastmeta Label -m representative -b unifrac_unweighted -o input/Test.tree -i input/Test-env.txt input/Test.pcl output.txt
> python MicroPITA.py -m representative -b unifrac_unweighted -o input/Test.tree -i input/Test-env.txt input/Test.biom output.txt

3. Supply your own custom alpha-diversity per sample as a metadata (row) in your pcl file.

> python MicroPITA.py --lastmeta Label -m diverse -q alpha_custom input/Test.pcl output.txt
> python MicroPITA.py -m diverse -q alpha_custom input/Test2.biom output.txt

4. Supply your own custom beta diversity as a matrix (provided in a seperate file).

> python MicroPITA.py --lastmeta Label -m representative -x input/Test_Matrix.txt input/Test.pcl output.txt
> python MicroPITA.py -m representative -x input/Test_Matrix.txt input/Test.biom output.txt
> python MicroPITA.py --lastmeta Label -m extreme -x input/Test_Matrix.txt input/Test.pcl output.txt
> python MicroPITA.py -m extreme -x input/Test_Matrix.txt input/Test.biom output.txt


## Changing defaults ##

Sample Selection:
To change the number of selected samples for any method use the -n argument. This example selects 6 representative samples instead of the default 10.

> python MicroPITA.py --lastmeta Label -m representative -n 6 input/Test.pcl output.txt
> python MicroPITA.py -m representative -n 6 input/Test.biom output.txt

When using a supervised method this indicates how many samples will be selected per class of sample. For example if you are performing supervised selection of 6 samples (-n 6) on a dataset with 2 classes (values) in it's label row, you will get 6 x 2 = 12 samples. If a class does not have 6 samples in it, you will get the max possible for that class. In a scenario where you are selecting 6 samples (-n 6) and have two classes but one class has only 3 samples then you will get 6 + 3 = 9 selected samples.

Stratification:
To stratify any method use the --stratify argument which is the first column keyword of the metadata row used to stratify samples before selection occurs. (Selection will occur independently within each strata). This example stratifies diverse selection by the "Label".

> python MicroPITA.py --lastmeta Label --stratify Label -m representative input/Test.pcl output.txt
> python MicroPITA.py --stratify Label -m representative input/Test.biom output.txt

> python MicroPITA.py --lastmeta Label --label Label --stratify StratifyLabel -m distinct input/Test.pcl output.txt
> python MicroPITA.py --label Label --stratify StratifyLabel -m distinct input/Test2.biom output.txt 

Changing PCL file defaults:
Some PCL files have feature metadata. These are columns of data that comment on bug features (rows) in the file. An example of this could be a certain taxonomy clade for different bug features. If this type of data exists please use -w or --lastFeatureMetadata to indicate the last column of feature metadata before the first column which is a sample. For an example please look in docs for PCL-Description.txt. This only applys to PCL files.

> python MicroPITA.py --lastmeta Label -m representative -w taxonomy_5 input/FeatureMetadata.pcl output.txt

MicroPITA assumes the first row of the input file is the sample IDs, if it is not you may use --id to indicate the row.
--id expects the entry in the first column of your input file that matches the row used as Sample Ids. See the input file and the following command as an example.
This only applys to PCL files.

> python MicroPITA.py --id Sample --lastmeta Label -m representative input/Test.pcl output.txt

MicroPITA assumes the input file is TAB delimited, we strongly recommend you use this convention. If not, you can use --delim to change the delimiter used to read in the file.
Here is an example of reading the comma delimited file micropita/input/CommaDelim.pcl
This only applys to PCL files.

> python MicroPITA.py --delim , --lastmeta Label -m representative input/CommaDelim.pcl output.txt

MicroPITA assumes the input file has feature names in which, if the name contains the consensus lineage or full taxonomic hierarchy, it is delimited with a pipe "|". We strongly recommend you use this default. The delimiter of the feature name can be changed using --featdelim. Here is an example of reading in a file with periods as the delimiter.
This only applys to PCL files.

> python MicroPITA.py --featdelim . --lastmeta Label -m representative input/PeriodDelim.pcl output.txt


## Dependencies ##
Please note the following dependencies need to be installed for micropita to run.
1. Python 2.x		http://www.python.org/download/
2. blist		http://pypi.python.org/pypi/blist/
3. NumPy		http://numpy.scipy.org/
4. SciPy		http://www.scipy.org/
5. PyCogent		http://pycogent.sourceforge.net/install.html
6. mlpy			http://mlpy.sourceforge.net/
7. mpi4py		http://mpi4py.scipy.org/
8. biome support 	http://biom-format.org/

This covers how to use microPITA. Thank you for using this software and good luck with all your endeavors!

## Contributions ## 
Thanks go to these wonderful people:

