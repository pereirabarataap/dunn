# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 17:09:21 2017

@author: apbar
"""

import copy
import numpy as np
import scipy.stats as stats

def makeRanks(*args):
    """
    Converts tuple of arrays of values into ranks.

    Parameters
    ----------
    sample1, sample2, ... : tuple_array_like
        The sample data, possibly with different lengths
        
    Returns
    -------
    sample1, sample2, ... : tuple_array_like
        The ranked sample data 

    """
    Ranks = []
    RanksF = []
    try:
        for data in args[0]:
            data.sort()
            ranks = {}
            rank = 0
            for pt in data:
                rank = rank + 1 
                if pt in ranks.keys():
                    ranks[pt] = ranks[pt] + [rank]
                else:
                    ranks[pt] = [rank]
            Ranks.append(ranks)
        for ranks in Ranks:
            keys = ranks.keys()
            keys.sort()
            protoRanks = []
            for key in keys:
                value = np.mean(ranks[key])
                for i in range(0, len(ranks[key])):
                    protoRanks.append(value)
            RanksF.append(protoRanks)
    except:
        for data in args:
            data.sort()
            ranks = {}
            rank = 0
            for pt in data:
                rank = rank + 1 
                if pt in ranks.keys():
                    ranks[pt] = ranks[pt] + [rank]
                else:
                    ranks[pt] = [rank]
            Ranks.append(ranks)
        for ranks in Ranks:
            keys = ranks.keys()
            keys.sort()
            protoRanks = []
            for key in keys:
                value = np.mean(ranks[key])
                for i in range(0, len(ranks[key])):
                    protoRanks.append(value)
            RanksF.append(protoRanks)
    return tuple(RanksF)
    
def dunn(*args, **kwargs):
    """
    Performs a two-tailed Dunn's test for stochastic dominance.

    Dunn’s test (1964) tests for stochastic dominance and reports the results
    among multiple pairwise comparisons after a rejected null hypothesis for a 
    Kruskal-Wallis test for stochastic dominance among k groups.

    Parameters
    ----------
    sample1, sample2, ... : array_like
        The sample data, possibly with different lengths
    "none", "fdr", ... : string_like
        Type of correction to use.
        Default is correction="none",
        "bonferroni" -> bonferroni correction,
        "fdr" -> (Benjaminyi-Hochberg false discovery rate method)
    label1, label2, ... : array_string_like
        Group labels to use when displaying or saving results
        Default is labels=(0, 1, ..., n)
        n = len(groups)
    True, False: bool_like
        Prints results on screen when True
        Default is display=True
    False, True, "fileName": bool_string_like
        Saves results onto csv file
        Default is save=False
        True -> labels will be used as filename
        "myFile" -> myFile.csv will be created
    
    Returns
    -------
    dunn: hash_like
        Dunn's multiple pairwaise test statistics, p-values, and q-values (corrections)

    References
    ----------
    .. [1]  https://stats.stackexchange.com/tags/dunn-test/info
    .. [2]  Dunn, O. J. (1961). Multiple comparisons among means.
            Journal of the American Statistical Association, 56(293):52–64.
    .. [3]  Dunn, O. J. (1964). Multiple comparisons using rank sums.
            Technometrics, 6(3):241–252.
    
    Examples
    --------
    >>> a = [0.28551035, 0.338524035, 0.088631321, 0.205930807, 0.363240102]
    >>> b = [0.52173913, 0.763358779, 0.325436786, 0.425305688, 0.378071834]
    >>> c = [0.98911968, 1.192718142, 0.788288288, 0.549176236, 0.544588155]
    >>> d = [1.26705653, 1.625320787, 1.266108976, 1.154187629, 1.268489431]
    >>> e = [1.25697569, 1.265897356, 1.237814561, 0.954612564, 2.365415457]
    >>> f = dunn(a,b,c,d,e)
    
          1       2       3       4       
       0  -0.9882 -2.1054 -3.8241 -3.3944 0
       1  -       -1.1171 -2.8358 -2.4061 1
       2  -       -       -1.7187 -1.2890 2
       3  -       -       -       0.42967 3
          1       2       3       4       
    
    Dunn test H0 z-statistic
    
    
          1       2       3       4       
       0  0.32304 0.03526 0.00013 0.00069 0
       1  -       0.26393 0.00457 0.01612 1
       2  -       -       0.08567 0.19740 2
       3  -       -       -       0.66744 3
          1       2       3       4       
    
    Adjustment method for p-value: none
    
    >>> groups = a,b,c,d,e
    >>> g = dunn(groups,correction="fdr",labels=("a","b","c","d","e"),display=True,save=False)
    
          b       c       d       e       
       a  -0.9882 -2.1054 -3.8241 -3.3944 a
       b  -       -1.1171 -2.8358 -2.4061 b
       c  -       -       -1.7187 -1.2890 c
       d  -       -       -       0.42967 d
          b       c       d       e       
    
    Dunn test H0 z-statistic
    
    
          b       c       d       e       
       a  0.35893 0.07052 0.00131 0.00344 a
       b  -       0.32992 0.01524 0.04030 b
       c  -       -       0.14279 0.28199 c
       d  -       -       -       0.66744 d
          b       c       d       e       
    
    Adjustment method for p-value: fdr
    
    >>> g
    {0: {'ID': 'a-b',
      'p-value': 0.32303584413413144,
      'q-value': 0.35892871570459051,
      'statistic': -0.98823852617441732},
     1: {'ID': 'a-c',
      'p-value': 0.035258440790219898,
      'q-value': 0.070516881580439797,
      'statistic': -2.1053777296759324},
     2: {'ID': 'a-d',
      'p-value': 0.00013127544861251964,
      'q-value': 0.0013127544861251965,
      'statistic': -3.8240534273705715},
     3: {'ID': 'a-e',
      'p-value': 0.0006878304609215692,
      'q-value': 0.0034391523046078459,
      'statistic': -3.3943845029469117},
     4: {'ID': 'b-c',
      'p-value': 0.26393481049044942,
      'q-value': 0.32991851311306175,
      'statistic': -1.1171392035015151},
     5: {'ID': 'b-d',
      'p-value': 0.0045708928878404912,
      'q-value': 0.015236309626134972,
      'statistic': -2.8358149011961538},
     6: {'ID': 'b-e',
      'p-value': 0.016121821274057219,
      'q-value': 0.040304553185143047,
      'statistic': -2.4061459767724944},
     7: {'ID': 'c-d',
      'p-value': 0.085673439552316863,
      'q-value': 0.14278906592052812,
      'statistic': -1.7186756976946389},
     8: {'ID': 'c-e',
      'p-value': 0.19739573184449921,
      'q-value': 0.28199390263499891,
      'statistic': -1.2890067732709791},
     9: {'ID': 'd-e',
      'p-value': 0.66743649170988251,
      'q-value': 0.66743649170988251,
      'statistic': 0.42966892442365973}}
     
     """  
    try:
        dunn = {}
        groups = copy.deepcopy(args[0]) #tuple of len k
        if "labels" not in kwargs.keys():
            kwargs["labels"] = []
            for i in range(0, len(groups)):
                protoL = str(i)
                kwargs["labels"].append(protoL)
        else:
            if len(kwargs["labels"]) != len(groups):
                raise ValueError("length of groups and length of labels must be the same")
            else:
                for label in kwargs["labels"]:
                    if str(type(label)) != "<type 'str'>":
                        raise ValueError("each label must be a string")
        for i in range(0, len(groups)):
            group = groups[i]
            while group.count(None) > 0 :
                group.remove(None)
            while group.count(np.nan) > 0 :
                group.remove(np.nan)
            if len(group) < 5:
                print Warning("WARNING: at least one group has fewer than 5 proper elements")
                print kwargs["labels"][i], group
            if len(group) == 0:
                raise ValueError("at least one group has no proper values")
        key = 0
        metaG = []
        for i in range(0, len(groups)):
            metaG = metaG + groups[i]
        metaGR = makeRanks(metaG)[0]
        n = len(metaGR)
        ties = 0.0
        uniqueR = list(set(metaGR))
        for elem in uniqueR:
            if metaGR.count(elem) > 1:
                ties = ties + (metaGR.count(elem)**3 - metaGR.count(elem))
            else:
                pass
        for i in range(0, len(groups)-1): #for every group in groups, excluding last
            grp1 = list(groups[i])
            grp1.sort()
            n1 = float(len(grp1))
            ranks1 = []
            for k1 in range(0, len(grp1)):
                point1 = grp1[k1]
                idx1 = metaG.index(point1)
                rank1 = metaGR[idx1]
                ranks1.append(rank1)   
            meanR1 = np.mean(ranks1)
            for j in range(i+1, len(groups)): #for every group following grp1
                grp2 = list(groups[j])
                grp2.sort()
                n2 = float(len(grp2))
                ranks2 = []
                for k2 in range(0, len(grp2)):
                    point2 = grp2[k2]
                    idx2 = metaG.index(point2)
                    rank2 = metaGR[idx2]
                    ranks2.append(rank2)
                meanR2 = np.mean(ranks2)
                y = meanR1 - meanR2
                g = ((((n*(n+1))/12.0) - (ties/(12.0*(n-1)))) * (1.0/n1 + 1.0/n2))**0.5
                stat = y/g
                if stats.norm.cdf(stat) > 0.5:
                    p = 2*(1 - stats.norm.cdf(stat))
                else:
                    p = 2*(stats.norm.cdf(stat))
                dunn[key] = {}
                dunn[key]["ID"] = kwargs["labels"][i]+"-"+kwargs["labels"][j]
                dunn[key]["statistic"] = stat
                dunn[key]["p-value"] = p
                key = key + 1
    except:
        dunn = {}
        groups = copy.deepcopy(args) #tuple of len k
        if "labels" not in kwargs.keys():
            kwargs["labels"] = []
            for i in range(0, len(groups)):
                protoL = str(i)
                kwargs["labels"].append(protoL)
        else:
            if len(kwargs["labels"]) != len(groups):
                raise ValueError("length of groups and length of labels must be the same")
            else:
                for label in kwargs["labels"]:
                    if str(type(label)) != "<type 'str'>":
                        raise ValueError("each label must be a string")
        for i in range(0, len(groups)):
            group = groups[i]
            while group.count(None) > 0 :
                group.remove(None)
            while group.count(np.nan) > 0 :
                group.remove(np.nan)
            if len(group) < 5:
                print Warning("WARNING: at least one group has fewer than 5 proper elements")
                print kwargs["labels"][i], group
            if len(group) == 0:
                raise ValueError("at least one group has no proper values")
        key = 0
        metaG = []
        for i in range(0, len(groups)):
            metaG = metaG + groups[i]
        metaGR = makeRanks(metaG)[0]
        n = len(metaGR)
        ties = 0.0
        uniqueR = list(set(metaGR))
        for elem in uniqueR:
            if metaGR.count(elem) > 1:
                ties = ties + (metaGR.count(elem)**3 - metaGR.count(elem))
            else:
                pass
        for i in range(0, len(groups)-1): #for every group in groups, excluding last
            grp1 = list(groups[i])
            grp1.sort()
            n1 = float(len(grp1))
            ranks1 = []
            for k1 in range(0, len(grp1)):
                point1 = grp1[k1]
                idx1 = metaG.index(point1)
                rank1 = metaGR[idx1]
                ranks1.append(rank1)   
            meanR1 = np.mean(ranks1)
            for j in range(i+1, len(groups)): #for every group following grp1
                grp2 = list(groups[j])
                grp2.sort()
                n2 = float(len(grp2))
                ranks2 = []
                for k2 in range(0, len(grp2)):
                    point2 = grp2[k2]
                    idx2 = metaG.index(point2)
                    rank2 = metaGR[idx2]
                    ranks2.append(rank2)
                meanR2 = np.mean(ranks2)
                y = meanR1 - meanR2
                g = ((((n*(n+1))/12.0) - (ties/(12.0*(n-1)))) * (1.0/n1 + 1.0/n2))**0.5
                stat = y/g
                if stats.norm.cdf(stat) > 0.5:
                    p = 2*(1 - stats.norm.cdf(stat)) #two-tailed
                else:
                    p = 2*(stats.norm.cdf(stat))
                dunn[key] = {}
                dunn[key]["ID"] = kwargs["labels"][i]+"-"+kwargs["labels"][j]
                dunn[key]["statistic"] = stat
                dunn[key]["p-value"] = p
                key = key + 1
    if "correction" not in kwargs.keys():
        kwargs["correction"] = "none"  
    if kwargs["correction"] != "none":
        m = float(len(dunn))
        if kwargs["correction"] == "bonferroni":
            keys = dunn.keys()
            keys.sort()
            for key in keys:
                dunn[key]["q-value"] = dunn[key]["p-value"] * m
                if dunn[key]["q-value"] > 1:
                    dunn[key]["q-value"] = 1.0
        elif kwargs["correction"] == "fdr":
            ps = []
            keys = dunn.keys()
            keys.sort()
            for key in keys:
                ps.append(dunn[key]["p-value"])
            ps.sort()
            ps.reverse()
            pTop = ps[0]
            for key in keys:
                i = ps.index(dunn[key]["p-value"]) + 1
                q = dunn[key]["p-value"] * (m/(m+1-i))
                if q > pTop:
                    q = pTop
                else:
                    pass
                dunn[key]["q-value"] = q
        else:
            raise ValueError("correction keyword must be 'bonferroni' or 'fdr'")
    if "display" not in kwargs.keys():
        kwargs["display"] = True
    if kwargs["display"] == True:
        print ""
        lenLabels = []
        for label in kwargs["labels"]:
            lenLabels.append(len(label))
        maxLen = max(lenLabels)
        if maxLen < 3:
            maxLen = 4
        line1 = "  "
        for i in range(0, maxLen):
            line1 = line1 + " "
        for i in range(1, len(groups)):
            variable = kwargs["labels"][i]
            while len(variable) < maxLen:
                variable = variable + " "
            variable = variable + "    "
            line1 = line1 + variable
        print line1
        k = 0
        for i in range(0, len(groups)-1):
            line = kwargs["labels"][i]
            while len(line) < maxLen:
                line = " " + line
            line = line + "  "
            if i != 0:
                for some in range(0, i):
                    blank = "-"
                    while len(blank) < maxLen+4:
                        blank = blank + " "
                    line = line + blank
            for j in range(i+1, len(groups)):
                if maxLen < 4 :
                    decimalNeg = "{0:.4f}"
                    decimalPos = "{0:.5f}"
                else:    
                    decimalNeg = "{0:." + str(maxLen) + "f}"
                    decimalPos = "{0:." + str((maxLen+1)) + "f}"
                if dunn[k]["statistic"] < 0:
                    line = line + decimalNeg.format(dunn[k]["statistic"]) + " "
                else:
                    line = line + decimalPos.format(dunn[k]["statistic"]) + " "
                k = k + 1
            line = line + kwargs["labels"][i]
            print line
        line1 = "  "
        for i in range(0, maxLen):
            line1 = line1 + " "
        for i in range(1, len(groups)):
            variable = kwargs["labels"][i]
            while len(variable) < maxLen:
                variable = variable + " "
            variable = variable + "    "
            line1 = line1 + variable
        print line1
        print "\nDunn test H0 z-statistic\n"
        print ""
        line1 = "  "
        for i in range(0, maxLen):
            line1 = line1 + " "
        for i in range(1, len(groups)):
            variable = kwargs["labels"][i]
            while len(variable) < maxLen:
                variable = variable + " "
            variable = variable + "    "
            line1 = line1 + variable
        print line1
        k = 0
        for i in range(0, len(groups)-1):
            line = kwargs["labels"][i]
            while len(line) < maxLen:
                line = " " + line
            line = line + "  "
            if i != 0:
                for some in range(0, i):
                    blank = "-"
                    while len(blank) < maxLen+4:
                        blank = blank + " "
                    line = line + blank
            for j in range(i+1, len(groups)):
                if maxLen < 4 :
                    decimalNeg = "{0:.4f}"
                    decimalPos = "{0:.5f}"
                else:    
                    decimalNeg = "{0:." + str(maxLen) + "f}"
                    decimalPos = "{0:." + str((maxLen+1)) + "f}"
                if kwargs["correction"] == "none":
                    if dunn[k]["p-value"] < 0:
                        line = line + decimalNeg.format(dunn[k]["p-value"]) + " "
                    else:
                        line = line + decimalPos.format(dunn[k]["p-value"]) + " "
                else:
                    if dunn[k]["q-value"] < 0:
                        line = line + decimalNeg.format(dunn[k]["q-value"]) + " "
                    else:
                        line = line + decimalPos.format(dunn[k]["q-value"]) + " "
                k = k + 1
            line = line + kwargs["labels"][i]
            print line
        line1 = "  "
        for i in range(0, maxLen):
            line1 = line1 + " "
        for i in range(1, len(groups)):
            variable = kwargs["labels"][i]
            while len(variable) < maxLen:
                variable = variable + " "
            variable = variable + "    "
            line1 = line1 + variable
        print line1
        print "\nAdjustment method for p-value:", kwargs["correction"], "\n"
    if "save" in kwargs.keys():
        if kwargs["save"] != False:    
            if kwargs["save"] == True:
                fileName = ""
                for label in kwargs["labels"]:
                    fileName = fileName + str(label) + "_vs_"
                fileName = fileName[:-4] + ".csv"
            elif str(type(kwargs["save"])) == "<type 'str'>":
                fileName = kwargs["save"]
                if fileName[-4:] != ".csv":
                    fileName = fileName + ".csv"
            else:
                raise ValueError("save arg must be either True, or string")
            op = open(fileName, 'w')
            labels = kwargs["labels"]
            line1 = "statistic,"
            for label in labels[1:]:
                line1 = line1 + label + ","
            line1 = line1[:-1] + "\n"
            op.write(line1)
            k = 0
            for i in range(0, len(groups)-1):
                line = labels[i] + ","
                if i != 0:
                    for blank in range(0, i):
                        line = line + ","
                for j in range(i+1, len(groups)):
                    line = line + str(dunn[k]["statistic"]) + ","
                    k = k + 1
                line = line[:-1] + "\n"
                op.write(line)    
            op.write("\n")
            line1 = "p-value,"
            for label in labels[1:]:
                line1 = line1 + label + ","
            line1 = line1[:-1] + "\n"
            op.write(line1)
            k = 0
            for i in range(0, len(groups)-1):
                line = labels[i] + ","
                if i != 0:
                    for blank in range(0, i):
                        line = line + ","
                for j in range(i+1, len(groups)):
                    if kwargs["correction"] == "none":
                        line = line + str(dunn[k]["p-value"]) + ","
                    else:
                        line = line + str(dunn[k]["q-value"]) + ","
                    k = k + 1
                line = line[:-1] + "\n"
                op.write(line)    
            op.close()               
    return dunn
