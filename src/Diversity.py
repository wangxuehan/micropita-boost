######################################
# Author: Timothy Tickle
# Description: Calculates diversity metrics
#####################################

__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2011"
__credits__ = ["Timothy Tickle"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@sph.harvard.edu"
__status__ = "Development"

#Update path
import sys
import Constants
import numpy as np
import ValidateData
if(not Constants.Constants.COGENT_SRC in sys.path):
    sys.path.append(Constants.Constants.COGENT_SRC)
if(not Constants.Constants.QIIME_SRC in sys.path):
    sys.path.append(Constants.Constants.QIIME_SRC)

#External libraries
from cogent.maths.stats.alpha_diversity import chao1_uncorrected, chao1_bias_corrected
from cogent.maths.unifrac.fast_unifrac import fast_unifrac
from cogent.maths.unifrac.fast_tree import UniFracTreeNode, count_envs
from cogent.parse.tree import DndParser
from qiime.format import format_unifrac_sample_mapping
from qiime.parse import parse_otu_table
from scipy.spatial.distance import pdist

class Diversity:

    #Diversity metrics Alpha
    c_SHANNON_A_DIVERSITY = "ShannonD"
    c_SIMPSON_A_DIVERSITY = "SimpsonD"
    c_INV_SIMPSON_A_DIVERSITY = "InSimpsonD"
    c_CHAO1_A_DIVERSITY = "Chao1"

    #Diversity metrics Beta
    c_UNIFRAC_B_DIVERSITY = "uUnifrac"
    c_WEIGHTED_UNIFRAC_B_DIVERSITY = "wUnifrac"
    c_BRAY_CURTIS_B_DIVERSITY = "B_Curtis"

    #Addative inverses of beta metrics
    c_INVERSE_BRAY_CURTIS_B_DIVERSITY = "InB_Curtis"
    c_INVERSE_UNIFRAC_B_DIVERSITY = "InuUnifrac"
    c_INVERSE_WEIGHTED_UNIFRAC_B_DIVERSITY = "InwUnifrac"

    #Alpha diversity
    #Testing: Happy Path
    #Calculates the Simpsons diversity index as defined as sum(Pi*Pi)
    #Note***: Assumes that the abundance measurements are already normalized by the total population N
    #@params tempSampleTaxaAbundancies Vector of organisms in a sample
    #@return 1 float is returned
    @staticmethod
    def getSimpsonsDiversityIndex(tempSampleTaxaAbundancies=None):
        #Validate data

        #Calculate metric
        return sum((tempSampleTaxaAbundancies)*(tempSampleTaxaAbundancies))

    #Alpha diversity
    #Testing: Happy Path
    #Calculates Inverse Simpsons diversity index 1/sum(Pi*Pi)
    #This is multiplicative inverse which reverses the order of the simpsons diversity index
    #Note***: Assumes that the abundance measurements are already normalized by the total population N
    @staticmethod
    def getInverseSimpsonsDiversityIndex(tempSampleTaxaAbundancies=None):
        #Validate data

        simpsons = Diversity.getSimpsonsDiversityIndex(tempSampleTaxaAbundancies)
        #Return False if the diversity is 0 before inverting it
        if(simpsons == 0):
            return False
        #If simpsons is false return false, else return inverse
        if(not ValidateData.ValidateData.isFalse(simpsons)):
            simpsons = 1/simpsons
        return simpsons

    #Alpha diversity
    #Testing: Happy Path
    #Calculates the Shannon diversity index
    #Note***: Assumes that the abundance measurements are already normalized by the total population N
    #If not normalized, include N in the parameter tempTotalN and it will be
    ## Calculates the Shannon index
    @staticmethod
    def getShannonDiversityIndex(tempSampleTaxaAbundancies=None):
        #Validate data

        #Calculate metric
        tempSampleTaxaAbundancies = tempSampleTaxaAbundancies[np.where(tempSampleTaxaAbundancies != 0)]
        tempIntermediateNumber = sum(tempSampleTaxaAbundancies*(np.log(tempSampleTaxaAbundancies)))
        if(tempIntermediateNumber == 0.0):
            return 0.0
        return -1 * tempIntermediateNumber

    #Alpha diversity
    #Testing: Happy Path Tested the no bias option
    #Testing: Need to test the biased option
    #Calculates the Chao1 diversity index
    #Note***: Not normalized by abundance
    #@params tempSampleTaxaAbundance =
    #@params tempCorrectForBias False indicates uncorrected for bias (uncorrected = Chao 1984, corrected = Chao 1987, Eq. 2)
    @staticmethod
    def getChao1DiversityIndex(tempSampleTaxaAbundancies=None, tempCorrectForBias=False):
        #Validate data

        #Observed = total number of species observed in all samples pooled
        totalObservedSpecies = len(tempSampleTaxaAbundancies)-len(tempSampleTaxaAbundancies[tempSampleTaxaAbundancies == 0])

        #Singles = number of species that occur in exactly 1 sample
        singlesObserved = len(tempSampleTaxaAbundancies[tempSampleTaxaAbundancies == 1.0])

        #Doubles = number of species that occue in exactly 2 samples
        doublesObserved = len(tempSampleTaxaAbundancies[tempSampleTaxaAbundancies == 2.0])

        #If singles or doubles = 0, return observations so that a divided by zero error does not occur
        if((singlesObserved == 0) or (doublesObserved == 0)):
            return totalObservedSpecies

        #Calculate metric
        if(tempCorrectForBias == True):
            return chao1_bias_corrected(observed = totalObservedSpecies, singles = singlesObserved, doubles = doublesObserved)
        else:
            return chao1_uncorrected(observed = totalObservedSpecies, singles = singlesObserved, doubles = doublesObserved)

    #Beta diversity
    #Testing: Happy Path
    #Calculates the BrayCurtis Beta diversity index
    #d(u,v)=sum(abs(row1-row2))/sum(row1+row2)
    #This is scale invariant
    #If you have 5 rows (labeled r1,r2,r3,r4,r5) the vector are the distances in this order
    #condensed form = [d(r1,r2), d(r1,r3), d(r1,r4), d(r1,r5), d(r2,r3), d(r2,r4), d(r2,r5), d(r3,r4), d(r3,r5), d(r4,r5)]
    #Note***: Assumes that the abundance measurements are already normalized by the total population N
    #@params tempSampleTaxaAbundancies an np.array of samples (rows) x measurements (columns) in which diversity is measured between rows
    #@return ndarray A condensed distance matrix
    @staticmethod
    def getBrayCurtisDissimilarity(tempSampleTaxaAbundancies=None):
        #Validate data

        #Calculate metric
        try:
            return pdist(X=tempSampleTaxaAbundancies, metric='braycurtis')
        except ValueError as error:
            print "".join(["Diversity.getBrayCurtisDissimilarity. Error=",str(error)])
            return False

    #Beta diversity
    #Testing: Happy Path
    #Calculates 1 - the BrayCurtis Beta diversity index
    #d(u,v)=1-(sum(abs(row1-row2))/sum(row1+row2))
    #This is scale invariant
    #If you have 5 rows (labeled r1,r2,r3,r4,r5) the vector are the distances in this order
    #condensed form = [d(r1,r2), d(r1,r3), d(r1,r4), d(r1,r5), d(r2,r3), d(r2,r4), d(r2,r5), d(r3,r4), d(r3,r5), d(r4,r5)]
    #Note***: Assumes that the abundance measurements are already normalized by the total population N
    #@params tempSampleTaxaAbundancies an np.array of samples (rows) x measurements (columns) in which diversity is measured between rows
    #@return ndarray A condensed distance matrix
    @staticmethod
    def getInverseBrayCurtisDissimilarity(tempSampleTaxaAbundancies = None):
        bcValue = Diversity.getBrayCurtisDissimilarity(tempSampleTaxaAbundancies = tempSampleTaxaAbundancies)
        if(not ValidateData.ValidateData.isFalse(bcValue)):
            #TODO Since brays curtis can get larger than 1, need to normalize this with a different value
            #TODO Need all inverses to be inverse in a specific way ... maybe multiplicative inverse is better
            return 1-bcValue
        return False

    #Beta diversity
    #Testing: Happy path tested the unweighted option
    #Testing: Need to test the weigthed option
    #Calculates the Unifrac Beta diversity index
    #Note: It seems unifrac takes abundancies not relative abundancies
    #@params tempTaxonomyTree String A rooted (outgroup) Newick format phylogenetics tree
    #@params tempSampleTaxaAbundancies String filename of the Qiime output formatted abundancy matrix
    ##TODO Abundancy matrix Rows = Samples, Columns = Sequences (Taxa,OTU) in a Qiime format
    #@return ndarray A condensed distance matrix
    @staticmethod
    def getUnifracDistance(tempSampleTaxaAbundancies=None, tempTaxonomyTree=None, tempWeighted=True):
        #Validate data
        #Translate abundances into dict for unifrac
        #The following if clause code is from the qiime script convert_otu_table_to_unifrac_sample_mapping.py
        #Used it in this manner to avoid commandline calls and to tie directly into Qiime
        if(ValidateData.ValidateData.isValidFileName(tempSampleTaxaAbundancies)):
            otuReader = open(tempSampleTaxaAbundancies, 'U')
            sample_ids, otu_ids, otu_table_array, lineages = parse_otu_table(otuReader, float)
            envs = format_unifrac_sample_mapping(sample_ids, otu_ids, otu_table_array)
            otuReader.close()

            #Convert to a dictionary for unifrac
            envs_Dict = dict()
            for mapping in envs:
                elements = mapping.split(Constants.Constants.TAB)
                if(len(elements) > 1):
                    if(not elements[0] in envs_Dict):
                        envs_Dict[elements[0]] = dict([[elements[1],int(float(elements[2]))]])
                    else:
                        envs_Dict[elements[0]][elements[1]]=int(float(elements[2]))

            #prefunction for the tree
            tr = DndParser(tempTaxonomyTree, UniFracTreeNode)
            #Calculate metric
            #Results of unifrac
            #The distance matrix is res['distance_matrix']
            #The PCoA data is res['pcoa']
            return fast_unifrac(tr,envs_Dict,weighted=tempWeighted)
        else:
            print "".join(["Diversity.getUnifracDistance. Invalid tempSampleTaxaAbundancies filename. Received=",str(tempSampleTaxaAbundancies)])
            return False
