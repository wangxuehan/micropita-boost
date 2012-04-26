#######################################################
# Author: Timothy Tickle
# Description: Class to test the RunMicroPITA class
#######################################################

__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2011"
__credits__ = ["Timothy Tickle"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@sph.harvard.edu"
__status__ = "Development"

#Import libraries
from AbundanceTable import AbundanceTable
from Constants import Constants
from FileIO import FileIO
import os
import re
import unittest
from Utility_File import Utility_File

##
#Tests the Blog object
class AbundanceTableTest(unittest.TestCase):

    def testCheckRawDataFileForGoodCase(self):
        
        #Inputs
        inputFile = "./Testing/Data/AbridgedDocuments/hq.otu_04-nul-nul-mtd-trn-flt-abridged.ForChecking.txt"
        outputFile = Utility_File.getFileNamePrefix(inputFile)+Constants.OUTPUT_SUFFIX
        delimiter = Constants.TAB

        #Remove output file before the test
        if(os.path.exists(outputFile)):
            os.remove(outputFile)

        #Correct Answer
        answer = "\"TID\"\t700098986\t700098984\t700098982\t700098980\t700098988\t700037470\t700037472\t700037474\t700037476\t700037478\n\"STSite\"\t\"L_Antecubital_fossa\"\t\"R_Retroauricular_crease\"\t\"L_Retroauricular_crease\"\t\"Subgingival_plaque\"\t\"R_Antecubital_fossa\"\t\"L_Retroauricular_crease\"\t\"R_Retroauricular_crease\"\t\"L_Antecubital_fossa\"\t\"R_Antecubital_fossa\"\t\"Anterior_nares\"\n\"Bacteria|Firmicutes|Clostridia|Clostridiales|Clostridiaceae|Clostridium|72\"\t1\t0\t0\t12\t0\t6\t0\t2\t1\t0\n\"Bacteria|unclassified|4904\"\t0\t10\t0\t43\t6\t0\t23\t0\t1\t0\n\"Bacteria|Firmicutes|Bacilli|Lactobacillales|Lactobacillaceae|Lactobacillus|1361\"\t3\t0\t0\t29\t0\t45\t0\t1\t1\t0\n\"Bacteria|3417\"\t0\t45\t0\t34\t3\t0\t0\t0\t1\t0\n\"Bacteria|Firmicutes|Bacilli|Bacillales|Bacillaceae|unclassified|1368\"\t5\t0\t0\t2\t0\t6\t0\t1\t1\t0\n"

        #Call method
        AbundanceTable.checkRawDataFile(tempReadDataFileName=inputFile, tempDelimiter=delimiter)

        #Get answer
        readFile = FileIO(outputFile,True,False,False)
        result = readFile.readFullFile()
        readFile.close()

        #Check result against answer
        self.assertEqual(str(result),str(answer),"".join([str(self),"::\nExpected=\n",str(answer),". \nReceived=\n",str(result),"."]))

    def testCheckRawDataFileForGoodCaseDelimterSpace(self):
        
        #Inputs
        inputFile = "./Testing/Data/AbridgedDocuments/hq.otu_04-nul-nul-mtd-trn-flt-abridged.ForChecking_Space.txt"
        outputFile = Utility_File.getFileNamePrefix(inputFile)+Constants.OUTPUT_SUFFIX
        delimiter = Constants.WHITE_SPACE

        #Correct Answer
        answer = "\"TID\" 700098986 700098984 700098982 700098980 700098988 700037470 700037472 700037474 700037476 700037478\n\"STSite\" \"L_Antecubital_fossa\" \"R_Retroauricular_crease\" \"L_Retroauricular_crease\" \"Subgingival_plaque\" \"R_Antecubital_fossa\" \"L_Retroauricular_crease\" \"R_Retroauricular_crease\" \"L_Antecubital_fossa\" \"R_Antecubital_fossa\" \"Anterior_nares\"\n\"Bacteria|Firmicutes|Clostridia|Clostridiales|Clostridiaceae|Clostridium|72\" 1 0 0 12 0 6 0 2 1 0\n\"Bacteria|unclassified|4904\" 0 10 0 43 6 0 23 0 1 0\n\"Bacteria|Firmicutes|Bacilli|Lactobacillales|Lactobacillaceae|Lactobacillus|1361\" 3 0 0 29 0 45 0 1 1 0\n\"Bacteria|3417\" 0 45 0 34 3 0 0 0 1 0\n\"Bacteria|Firmicutes|Bacilli|Bacillales|Bacillaceae|unclassified|1368\" 5 0 0 2 0 6 0 1 1 0\n"

        #Call method
        AbundanceTable.checkRawDataFile(tempReadDataFileName=inputFile, tempDelimiter=delimiter)

        #Get answer
        readFile = FileIO(outputFile,True,False,False)
        result = readFile.readFullFile()
        readFile.close()

        #Remove output file after the test
        if(os.path.exists(outputFile)):
            os.remove(outputFile)

        #Check result against answer
        self.assertEqual(str(result),str(answer),"".join([str(self),"::\nExpected=\n",str(answer),". \nReceived=\n",str(result),"."]))

    def testNormalizeColumnsForGoodCaseNoNormalize(self):
        
        #Inputs
        inputFile = "./Testing/Data/AbridgedDocuments/hq.otu_04-nul-nul-mtd-trn-flt-abridged.txt"
        delimiter = Constants.TAB
        nameRow = 0
        firstDataRow = 2
        normalize = False
        data = AbundanceTable()
        columnNames = []

        #Correct Answer
        answer = "[ ('Bacteria|Firmicutes|Clostridia|Clostridiales|Clostridiaceae|Clostridium|72', 1.0, 0.0, 0.0, 12.0, 0.0, 6.0, 0.0, 2.0, 1.0, 0.0)\n ('Bacteria|unclassified|4904', 0.0, 10.0, 0.0, 43.0, 6.0, 0.0, 23.0, 0.0, 1.0, 0.0)\n ('Bacteria|Firmicutes|Bacilli|Lactobacillales|Lactobacillaceae|Lactobacillus|1361', 3.0, 0.0, 0.0, 29.0, 0.0, 45.0, 0.0, 1.0, 1.0, 0.0)\n ('Bacteria|3417', 0.0, 45.0, 0.0, 34.0, 3.0, 0.0, 0.0, 0.0, 1.0, 0.0)\n ('Bacteria|Firmicutes|Bacilli|Bacillales|Bacillaceae|unclassified|1368', 5.0, 0.0, 0.0, 2.0, 0.0, 6.0, 0.0, 1.0, 1.0, 0.0)]"

        #Call method
        result = data.textToStructuredArray(tempInputFile=inputFile, tempDelimiter=delimiter, tempNameRow=nameRow, tempFirstDataRow=firstDataRow, tempNormalize=normalize)
        result = data.normalizeColumns(tempStructuredArray=result[0], tempColumns=columnNames)

        #Check result against answer
        self.assertEqual(str(result),str(answer),"".join([str(self),"::Expected=",str(answer),". Received=",str(result),"."]))

    def testNormalizeColumnsForGoodCaseNormalize1(self):
        
        #Inputs
        inputFile = "./Testing/Data/AbridgedDocuments/hq.otu_04-nul-nul-mtd-trn-flt-abridged.txt"
        delimiter = Constants.TAB
        nameRow = 0
        firstDataRow = 2
        normalize = False
        data = AbundanceTable()
        columnNames = ["700098986"]

        #Correct Answer
        answer = "[ ('Bacteria|Firmicutes|Clostridia|Clostridiales|Clostridiaceae|Clostridium|72', 0.1111111111111111, 0.0, 0.0, 12.0, 0.0, 6.0, 0.0, 2.0, 1.0, 0.0)\n ('Bacteria|unclassified|4904', 0.0, 10.0, 0.0, 43.0, 6.0, 0.0, 23.0, 0.0, 1.0, 0.0)\n ('Bacteria|Firmicutes|Bacilli|Lactobacillales|Lactobacillaceae|Lactobacillus|1361', 0.3333333333333333, 0.0, 0.0, 29.0, 0.0, 45.0, 0.0, 1.0, 1.0, 0.0)\n ('Bacteria|3417', 0.0, 45.0, 0.0, 34.0, 3.0, 0.0, 0.0, 0.0, 1.0, 0.0)\n ('Bacteria|Firmicutes|Bacilli|Bacillales|Bacillaceae|unclassified|1368', 0.5555555555555556, 0.0, 0.0, 2.0, 0.0, 6.0, 0.0, 1.0, 1.0, 0.0)]"

        #Call method
        result = data.textToStructuredArray(tempInputFile=inputFile, tempDelimiter=delimiter, tempNameRow=nameRow, tempFirstDataRow=firstDataRow, tempNormalize=normalize)
        result = data.normalizeColumns(tempStructuredArray=result[0], tempColumns=columnNames)

        #Check result against answer
        self.assertEqual(str(result),str(answer),"".join([str(self),"::Expected=",str(answer),". Received=",str(result),"."]))

    def testNormalizeColumnsForGoodCaseNormalize14(self):
        
        #Inputs
        inputFile = "./Testing/Data/AbridgedDocuments/hq.otu_04-nul-nul-mtd-trn-flt-abridged.txt"
        delimiter = Constants.TAB
        nameRow = 0
        firstDataRow = 2
        normalize = False
        data = AbundanceTable()
        columnNames = ["700098986","700098980"]

        #Correct Answer
        answer = "[ ('Bacteria|Firmicutes|Clostridia|Clostridiales|Clostridiaceae|Clostridium|72', 0.1111111111111111, 0.0, 0.0, 0.1, 0.0, 6.0, 0.0, 2.0, 1.0, 0.0)\n ('Bacteria|unclassified|4904', 0.0, 10.0, 0.0, 0.35833333333333334, 6.0, 0.0, 23.0, 0.0, 1.0, 0.0)\n ('Bacteria|Firmicutes|Bacilli|Lactobacillales|Lactobacillaceae|Lactobacillus|1361', 0.3333333333333333, 0.0, 0.0, 0.24166666666666667, 0.0, 45.0, 0.0, 1.0, 1.0, 0.0)\n ('Bacteria|3417', 0.0, 45.0, 0.0, 0.2833333333333333, 3.0, 0.0, 0.0, 0.0, 1.0, 0.0)\n ('Bacteria|Firmicutes|Bacilli|Bacillales|Bacillaceae|unclassified|1368', 0.5555555555555556, 0.0, 0.0, 0.016666666666666666, 0.0, 6.0, 0.0, 1.0, 1.0, 0.0)]"

        #Call method
        result = data.textToStructuredArray(tempInputFile=inputFile, tempDelimiter=delimiter, tempNameRow=nameRow, tempFirstDataRow=firstDataRow, tempNormalize=normalize)
        result = data.normalizeColumns(tempStructuredArray=result[0], tempColumns=columnNames)

        #Check result against answer
        self.assertEqual(str(result),str(answer),"".join([str(self),"::Expected=",str(answer),". Received=",str(result),"."]))

    def testNormalizeColumnsForGoodCaseNormalizeAll(self):
        
        #Inputs
        inputFile = "./Testing/Data/AbridgedDocuments/hq.otu_04-nul-nul-mtd-trn-flt-abridged.txt"
        delimiter = Constants.TAB
        nameRow = 0
        firstDataRow = 2
        normalize = False
        data = AbundanceTable()
        columnNames = ["700098986","700098984","700098982","700098980","700098988","700037470","700037472","700037474","700037476","700037478"]

        #Correct Answer
        answer = "[ ('Bacteria|Firmicutes|Clostridia|Clostridiales|Clostridiaceae|Clostridium|72', 0.1111111111111111, 0.0, 0.0, 0.1, 0.0, 0.10526315789473684, 0.0, 0.5, 0.2, 0.0)\n ('Bacteria|unclassified|4904', 0.0, 0.18181818181818182, 0.0, 0.35833333333333334, 0.6666666666666666, 0.0, 1.0, 0.0, 0.2, 0.0)\n ('Bacteria|Firmicutes|Bacilli|Lactobacillales|Lactobacillaceae|Lactobacillus|1361', 0.3333333333333333, 0.0, 0.0, 0.24166666666666667, 0.0, 0.7894736842105263, 0.0, 0.25, 0.2, 0.0)\n ('Bacteria|3417', 0.0, 0.8181818181818182, 0.0, 0.2833333333333333, 0.3333333333333333, 0.0, 0.0, 0.0, 0.2, 0.0)\n ('Bacteria|Firmicutes|Bacilli|Bacillales|Bacillaceae|unclassified|1368', 0.5555555555555556, 0.0, 0.0, 0.016666666666666666, 0.0, 0.10526315789473684, 0.0, 0.25, 0.2, 0.0)]"

        #Call method
        result = data.textToStructuredArray(tempInputFile=inputFile, tempDelimiter=delimiter, tempNameRow=nameRow, tempFirstDataRow=firstDataRow, tempNormalize=normalize)
        result = data.normalizeColumns(tempStructuredArray=result[0], tempColumns=columnNames)

        #Check result against answer
        self.assertEqual(str(result),str(answer),"".join([str(self),"::Expected=",str(answer),". Received=",str(result),"."]))

    def testTextToStructuredArrayForGoodCaseNoNormalize(self):
        
        #Inputs
        inputFile = "./Testing/Data/AbridgedDocuments/hq.otu_04-nul-nul-mtd-trn-flt-abridged.txt"
        delimiter = Constants.TAB
        nameRow = 0
        firstDataRow = 2
        normalize = False
        microPITA = AbundanceTable()

        #Correct Answer
        answer = "[array([ ('Bacteria|Firmicutes|Clostridia|Clostridiales|Clostridiaceae|Clostridium|72', 1.0, 0.0, 0.0, 12.0, 0.0, 6.0, 0.0, 2.0, 1.0, 0.0),\n       ('Bacteria|unclassified|4904', 0.0, 10.0, 0.0, 43.0, 6.0, 0.0, 23.0, 0.0, 1.0, 0.0),\n       ('Bacteria|Firmicutes|Bacilli|Lactobacillales|Lactobacillaceae|Lactobacillus|1361', 3.0, 0.0, 0.0, 29.0, 0.0, 45.0, 0.0, 1.0, 1.0, 0.0),\n       ('Bacteria|3417', 0.0, 45.0, 0.0, 34.0, 3.0, 0.0, 0.0, 0.0, 1.0, 0.0),\n       ('Bacteria|Firmicutes|Bacilli|Bacillales|Bacillaceae|unclassified|1368', 5.0, 0.0, 0.0, 2.0, 0.0, 6.0, 0.0, 1.0, 1.0, 0.0)], \n      dtype=[('TID', '|S158'), ('700098986', '<f8'), ('700098984', '<f8'), ('700098982', '<f8'), ('700098980', '<f8'), ('700098988', '<f8'), ('700037470', '<f8'), ('700037472', '<f8'), ('700037474', '<f8'), ('700037476', '<f8'), ('700037478', '<f8')]), {'STSite': ['L_Antecubital_fossa', 'R_Retroauricular_crease', 'L_Retroauricular_crease', 'Subgingival_plaque', 'R_Antecubital_fossa', 'L_Retroauricular_crease', 'R_Retroauricular_crease', 'L_Antecubital_fossa', 'R_Antecubital_fossa', 'Anterior_nares']}]"

        #Call method
        result = microPITA.textToStructuredArray(tempInputFile=inputFile, tempDelimiter=delimiter, tempNameRow=nameRow, tempFirstDataRow=firstDataRow, tempNormalize=normalize)

        #Check result against answer
        self.assertEqual(str(result),str(answer),"".join([str(self),"::Expected=",str(answer),". Received=",str(result),"."]))

    def testTextToStructuredArrayForGoodCaseNormalize(self):
        
        #Inputs
        inputFile = "./Testing/Data/AbridgedDocuments/hq.otu_04-nul-nul-mtd-trn-flt-abridged.txt"
        delimiter = Constants.TAB
        nameRow = 0
        firstDataRow = 2
        normalize = True
        microPITA = AbundanceTable()

        #Correct Answer
        answer = "[array([ ('Bacteria|Firmicutes|Clostridia|Clostridiales|Clostridiaceae|Clostridium|72', 0.1111111111111111, 0.0, 0.0, 0.1, 0.0, 0.10526315789473684, 0.0, 0.5, 0.2, 0.0),\n       ('Bacteria|unclassified|4904', 0.0, 0.18181818181818182, 0.0, 0.35833333333333334, 0.6666666666666666, 0.0, 1.0, 0.0, 0.2, 0.0),\n       ('Bacteria|Firmicutes|Bacilli|Lactobacillales|Lactobacillaceae|Lactobacillus|1361', 0.3333333333333333, 0.0, 0.0, 0.24166666666666667, 0.0, 0.7894736842105263, 0.0, 0.25, 0.2, 0.0),\n       ('Bacteria|3417', 0.0, 0.8181818181818182, 0.0, 0.2833333333333333, 0.3333333333333333, 0.0, 0.0, 0.0, 0.2, 0.0),\n       ('Bacteria|Firmicutes|Bacilli|Bacillales|Bacillaceae|unclassified|1368', 0.5555555555555556, 0.0, 0.0, 0.016666666666666666, 0.0, 0.10526315789473684, 0.0, 0.25, 0.2, 0.0)], \n      dtype=[('TID', '|S158'), ('700098986', '<f8'), ('700098984', '<f8'), ('700098982', '<f8'), ('700098980', '<f8'), ('700098988', '<f8'), ('700037470', '<f8'), ('700037472', '<f8'), ('700037474', '<f8'), ('700037476', '<f8'), ('700037478', '<f8')]), {'STSite': ['L_Antecubital_fossa', 'R_Retroauricular_crease', 'L_Retroauricular_crease', 'Subgingival_plaque', 'R_Antecubital_fossa', 'L_Retroauricular_crease', 'R_Retroauricular_crease', 'L_Antecubital_fossa', 'R_Antecubital_fossa', 'Anterior_nares']}]"

        #Call method
        result = microPITA.textToStructuredArray(tempInputFile=inputFile, tempDelimiter=delimiter, tempNameRow=nameRow, tempFirstDataRow=firstDataRow, tempNormalize=normalize)

        #Check result against answer
        self.assertEqual(str(result),str(answer),"".join([str(self),"::\nExpected=",str(answer),".\nReceived=",str(result),"."]))

    def testTextToStructuredArrayForGoodCaseSpaceDelimiter(self):
        
        #Inputs
        inputFile = "./Testing/Data/AbridgedDocuments/hq.otu_04-nul-nul-mtd-trn-flt-abridged_Space.txt"
        delimiter = Constants.WHITE_SPACE
        nameRow = 0
        firstDataRow = 2
        normalize = False
        microPITA = AbundanceTable()

        #Correct Answer
        answer = "[array([ ('Bacteria|Firmicutes|Clostridia|Clostridiales|Clostridiaceae|Clostridium|72', 1.0, 0.0, 0.0, 12.0, 0.0, 6.0, 0.0, 2.0, 1.0, 0.0),\n       ('Bacteria|unclassified|4904', 0.0, 10.0, 0.0, 43.0, 6.0, 0.0, 23.0, 0.0, 1.0, 0.0),\n       ('Bacteria|Firmicutes|Bacilli|Lactobacillales|Lactobacillaceae|Lactobacillus|1361', 3.0, 0.0, 0.0, 29.0, 0.0, 45.0, 0.0, 1.0, 1.0, 0.0),\n       ('Bacteria|3417', 0.0, 45.0, 0.0, 34.0, 3.0, 0.0, 0.0, 0.0, 1.0, 0.0),\n       ('Bacteria|Firmicutes|Bacilli|Bacillales|Bacillaceae|unclassified|1368', 5.0, 0.0, 0.0, 2.0, 0.0, 6.0, 0.0, 1.0, 1.0, 0.0)], \n      dtype=[('TID', '|S158'), ('700098986', '<f8'), ('700098984', '<f8'), ('700098982', '<f8'), ('700098980', '<f8'), ('700098988', '<f8'), ('700037470', '<f8'), ('700037472', '<f8'), ('700037474', '<f8'), ('700037476', '<f8'), ('700037478', '<f8')]), {'STSite': ['L_Antecubital_fossa', 'R_Retroauricular_crease', 'L_Retroauricular_crease', 'Subgingival_plaque', 'R_Antecubital_fossa', 'L_Retroauricular_crease', 'R_Retroauricular_crease', 'L_Antecubital_fossa', 'R_Antecubital_fossa', 'Anterior_nares']}]"

        #Call method
        result = microPITA.textToStructuredArray(tempInputFile=inputFile, tempDelimiter=delimiter, tempNameRow=nameRow, tempFirstDataRow=firstDataRow, tempNormalize=normalize)

        #Check result against answer
        self.assertEqual(str(result),str(answer),"".join([str(self),"::Expected=",str(answer),". Received=",str(result),"."]))

    def testStratifyAbundanceTableByMetadataForGoodCaseByIndex(self):
        
        #Inputs
        inputFile = "./Testing/Data/AbridgedDocuments/hq.otu_04-nul-nul-mtd-trn-flt-abridged.txt"
        delimiter = Constants.TAB
        stratifyRow = 1
        table = AbundanceTable()

        #Correct Answer is blank indicating no error
        answer = ""

        #Should generate the following files
        anteriorNaresFileName = "./Testing/Data/AbridgedDocuments/hq.otu_04-nul-nul-mtd-trn-flt-abridged-by-Anterior_nares.txt"
        anteriorNaresFileNameAnswer = "./Testing/Data/CorrectTestingResults/hq.otu_04-nul-nul-mtd-trn-flt-abridged-by-Anterior_nares.txt"
        lAntecubitalFossaFileName = "./Testing/Data/AbridgedDocuments/hq.otu_04-nul-nul-mtd-trn-flt-abridged-by-L_Antecubital_fossa.txt"
        lAntecubitalFossaFileNameAnswer = "./Testing/Data/CorrectTestingResults/hq.otu_04-nul-nul-mtd-trn-flt-abridged-by-L_Antecubital_fossa.txt"
        lRetroauricularCreaseFileName = "./Testing/Data/AbridgedDocuments/hq.otu_04-nul-nul-mtd-trn-flt-abridged-by-L_Retroauricular_crease.txt"
        lRetroauricularCreaseFileNameAnswer = "./Testing/Data/CorrectTestingResults/hq.otu_04-nul-nul-mtd-trn-flt-abridged-by-L_Retroauricular_crease.txt"
        rAntecubitalFossaFileName = "./Testing/Data/AbridgedDocuments/hq.otu_04-nul-nul-mtd-trn-flt-abridged-by-R_Antecubital_fossa.txt"
        rAntecubitalFossaFileNameAnswer = "./Testing/Data/CorrectTestingResults/hq.otu_04-nul-nul-mtd-trn-flt-abridged-by-R_Antecubital_fossa.txt"
        rRetroauricularCreaseFileName = "./Testing/Data/AbridgedDocuments/hq.otu_04-nul-nul-mtd-trn-flt-abridged-by-R_Retroauricular_crease.txt"
        rRetroauricularCreaseFileNameAnswer = "./Testing/Data/CorrectTestingResults/hq.otu_04-nul-nul-mtd-trn-flt-abridged-by-R_Retroauricular_crease.txt"
        subgingivalPlaqueFileName = "./Testing/Data/AbridgedDocuments/hq.otu_04-nul-nul-mtd-trn-flt-abridged-by-Subgingival_plaque.txt"
        subgingivalPlaqueFileNameAnswer = "./Testing/Data/CorrectTestingResults/hq.otu_04-nul-nul-mtd-trn-flt-abridged-by-Subgingival_plaque.txt"

        dictCreatedFiles = {anteriorNaresFileName:anteriorNaresFileNameAnswer,
                            lAntecubitalFossaFileName:lAntecubitalFossaFileNameAnswer,
                            lRetroauricularCreaseFileName:lRetroauricularCreaseFileNameAnswer,
                            rAntecubitalFossaFileName:rAntecubitalFossaFileNameAnswer,
                            rRetroauricularCreaseFileName:rRetroauricularCreaseFileNameAnswer,
                            subgingivalPlaqueFileName:subgingivalPlaqueFileNameAnswer}

        #Delete files if they exist
        for strFile in dictCreatedFiles:
            if os.path.exists(strFile):
                os.remove(strFile)

        #Call method
        table.stratifyAbundanceTableByMetadata(tempInputFile = inputFile, tempDelimiter = delimiter, tempStratifyByRow = stratifyRow)

        #Check file creation
        error = ""
        for strFile in dictCreatedFiles:
            if(os.path.exists(strFile)):

                contents = list()
                contentsAnswer = list()
                with open(strFile) as f:
                    contents = f.read()
                    contents = filter(None,re.split("\n",contents))
                    f.close()
                with open(dictCreatedFiles[strFile]) as f:
                    contentsAnswer = f.read()
                    contentsAnswer = filter(None,re.split("\n",contentsAnswer))
                    f.close()
                if(not contents == contentsAnswer):
                    error = error + "\nFile: "+strFile+"\nExpected:"+",".join(contentsAnswer)+".\nReceived:"+",".join(contents)+"."
            else:
                error = error + "\nFile count not be found. Path:"+strFile
        result = error

        #Check result against answer
        self.assertEqual(str(result),str(answer),"".join([str(self),"::Expected=",str(answer),". Received=",str(result),"."]))

    def testStratifyAbundanceTableByMetadataForGoodCaseByKeyWord(self):
        
        #Inputs
        inputFile = "./Testing/Data/AbridgedDocuments/hq.otu_04-nul-nul-mtd-trn-flt-abridged.txt"
        delimiter = Constants.TAB
        stratifyRow = "STSite"
        table = AbundanceTable()

        #Correct Answer is blank indicating no error
        answer = ""

        #Should generate the following files
        anteriorNaresFileName = "./Testing/Data/AbridgedDocuments/hq.otu_04-nul-nul-mtd-trn-flt-abridged-by-Anterior_nares.txt"
        anteriorNaresFileNameAnswer = "./Testing/Data/CorrectTestingResults/hq.otu_04-nul-nul-mtd-trn-flt-abridged-by-Anterior_nares.txt"
        lAntecubitalFossaFileName = "./Testing/Data/AbridgedDocuments/hq.otu_04-nul-nul-mtd-trn-flt-abridged-by-L_Antecubital_fossa.txt"
        lAntecubitalFossaFileNameAnswer = "./Testing/Data/CorrectTestingResults/hq.otu_04-nul-nul-mtd-trn-flt-abridged-by-L_Antecubital_fossa.txt"
        lRetroauricularCreaseFileName = "./Testing/Data/AbridgedDocuments/hq.otu_04-nul-nul-mtd-trn-flt-abridged-by-L_Retroauricular_crease.txt"
        lRetroauricularCreaseFileNameAnswer = "./Testing/Data/CorrectTestingResults/hq.otu_04-nul-nul-mtd-trn-flt-abridged-by-L_Retroauricular_crease.txt"
        rAntecubitalFossaFileName = "./Testing/Data/AbridgedDocuments/hq.otu_04-nul-nul-mtd-trn-flt-abridged-by-R_Antecubital_fossa.txt"
        rAntecubitalFossaFileNameAnswer = "./Testing/Data/CorrectTestingResults/hq.otu_04-nul-nul-mtd-trn-flt-abridged-by-R_Antecubital_fossa.txt"
        rRetroauricularCreaseFileName = "./Testing/Data/AbridgedDocuments/hq.otu_04-nul-nul-mtd-trn-flt-abridged-by-R_Retroauricular_crease.txt"
        rRetroauricularCreaseFileNameAnswer = "./Testing/Data/CorrectTestingResults/hq.otu_04-nul-nul-mtd-trn-flt-abridged-by-R_Retroauricular_crease.txt"
        subgingivalPlaqueFileName = "./Testing/Data/AbridgedDocuments/hq.otu_04-nul-nul-mtd-trn-flt-abridged-by-Subgingival_plaque.txt"
        subgingivalPlaqueFileNameAnswer = "./Testing/Data/CorrectTestingResults/hq.otu_04-nul-nul-mtd-trn-flt-abridged-by-Subgingival_plaque.txt"

        dictCreatedFiles = {anteriorNaresFileName:anteriorNaresFileNameAnswer,
                            lAntecubitalFossaFileName:lAntecubitalFossaFileNameAnswer,
                            lRetroauricularCreaseFileName:lRetroauricularCreaseFileNameAnswer,
                            rAntecubitalFossaFileName:rAntecubitalFossaFileNameAnswer,
                            rRetroauricularCreaseFileName:rRetroauricularCreaseFileNameAnswer,
                            subgingivalPlaqueFileName:subgingivalPlaqueFileNameAnswer}

        #Delete files if they exist
        for strFile in dictCreatedFiles:
            if os.path.exists(strFile):
                os.remove(strFile)

        #Call method
        table.stratifyAbundanceTableByMetadata(tempInputFile = inputFile, tempDelimiter = delimiter, tempStratifyByRow = stratifyRow)

        #Check file creation
        error = ""
        for strFile in dictCreatedFiles:
            if(os.path.exists(strFile)):

                contents = list()
                contentsAnswer = list()
                with open(strFile) as f:
                    contents = f.read()
                    contents = filter(None,re.split("\n",contents))
                    f.close()
                with open(dictCreatedFiles[strFile]) as f:
                    contentsAnswer = f.read()
                    contentsAnswer = filter(None,re.split("\n",contentsAnswer))
                    f.close()
                if(not contents == contentsAnswer):
                    error = error + "\nFile: "+strFile+"\nExpected:"+",".join(contentsAnswer)+".\nReceived:"+",".join(contents)+"."
            else:
                error = error + "\nFile count not be found. Path:"+strFile
        result = error

        #Check result against answer
        self.assertEqual(str(result),str(answer),"".join([str(self),"::Expected=",str(answer),". Received=",str(result),"."]))


    def testTransposeDataMatrixForGoodCase(self):
        
        #Inputs
        inputFile = "./Testing/Data/AbridgedDocuments/hq.otu_04-nul-nul-mtd-trn-flt-abridged.txt"
        delimiter = Constants.TAB
        nameRow = 0
        firstDataRow = 2
        normalize = False
        data = AbundanceTable()
        removeAdornment = False

        #Correct Answer
        answer = "[[ 'Bacteria|Firmicutes|Clostridia|Clostridiales|Clostridiaceae|Clostridium|72'\n  'Bacteria|unclassified|4904'\n  'Bacteria|Firmicutes|Bacilli|Lactobacillales|Lactobacillaceae|Lactobacillus|1361'\n  'Bacteria|3417'\n  'Bacteria|Firmicutes|Bacilli|Bacillales|Bacillaceae|unclassified|1368']\n ['1.0' '0.0' '3.0' '0.0' '5.0']\n ['0.0' '10.0' '0.0' '45.0' '0.0']\n ['0.0' '0.0' '0.0' '0.0' '0.0']\n ['12.0' '43.0' '29.0' '34.0' '2.0']\n ['0.0' '6.0' '0.0' '3.0' '0.0']\n ['6.0' '0.0' '45.0' '0.0' '6.0']\n ['0.0' '23.0' '0.0' '0.0' '0.0']\n ['2.0' '0.0' '1.0' '0.0' '1.0']\n ['1.0' '1.0' '1.0' '1.0' '1.0']\n ['0.0' '0.0' '0.0' '0.0' '0.0']]"

        #Call method
        result = data.textToStructuredArray(tempInputFile=inputFile, tempDelimiter=delimiter, tempNameRow=nameRow, tempFirstDataRow=firstDataRow, tempNormalize=normalize)
        result = data.transposeDataMatrix(tempMatrix=result[0], tempRemoveAdornments=removeAdornment)

        #Check result against answer
        self.assertEqual(str(result),str(answer),"".join([str(self),"::Expected=",str(answer),". Received=",str(result),"."]))

    def testTransposeDataMatrixForGoodCaseRemoveAdornments(self):
        
        #Inputs
        inputFile = "./Testing/Data/AbridgedDocuments/hq.otu_04-nul-nul-mtd-trn-flt-abridged.txt"
        delimiter = Constants.TAB
        nameRow = 0
        firstDataRow = 2
        normalize = False
        data = AbundanceTable()
        removeAdornment = True

        #Correct Answer
        answer = "[[  1.   0.   3.   0.   5.]\n [  0.  10.   0.  45.   0.]\n [  0.   0.   0.   0.   0.]\n [ 12.  43.  29.  34.   2.]\n [  0.   6.   0.   3.   0.]\n [  6.   0.  45.   0.   6.]\n [  0.  23.   0.   0.   0.]\n [  2.   0.   1.   0.   1.]\n [  1.   1.   1.   1.   1.]\n [  0.   0.   0.   0.   0.]]"

        #Call method
        result = data.textToStructuredArray(tempInputFile=inputFile, tempDelimiter=delimiter, tempNameRow=nameRow, tempFirstDataRow=firstDataRow, tempNormalize=normalize)
        result = data.transposeDataMatrix(tempMatrix=result[0], tempRemoveAdornments=removeAdornment)

        #Check result against answer
        self.assertEqual(str(result),str(answer),"".join([str(self),"::Expected=",str(answer),". Received=",str(result),"."]))

    def notFilterByAbundanceForGoodCase(self):
        
        #Inputs
        inputFile = "./Testing/Data/AbridgedDocuments/hq.otu_04-nul-nul-mtd-trn-flt-abridged.txt"
        delimiter = Constants.TAB
        nameRow = 0
        firstDataRow = 2
        normalize = False
        data = AbundanceTable()
        removeAdornment = False

        #Correct Answer
        answer = ""
        result = "1"

        #Call method
        abndData, metadata = data.textToStructuredArray(tempInputFile=inputFile, tempDelimiter=delimiter, tempNameRow=nameRow, tempFirstDataRow=firstDataRow, tempNormalize=normalize)
        data.filterByAbundance(npaAbundance=abndData, dPercentileCutOff = 0.99, dPercentageAbovePercentile=0.9)

        #Check result against answer
        self.assertEqual(str(result),str(answer),"".join([str(self),"::Expected=",str(answer),". Received=",str(result),"."]))

##
#Creates a suite of tests
def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(AbundanceTableTest)
    return suite
