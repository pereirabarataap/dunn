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
    among multiple pairwise comparisons after a rejected null hypothesis for 
    Kruskal-Wallis test for stochastic dominance among k groups.

    Parameters
    ----------
    sample1, sample2, ... : array_like
        The sample data, possibly with different lengths
    "none", "bf", "fdr": string_like
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
    
    Returns
    -------
    dunn: hash_like
        Dunn's multiple pairwaise test statistics, p-values, and corrected alphas

    References
    ----------
    .. [1]  https://stats.stackexchange.com/tags/dunn-test/info
    .. [2]  Dunn, O. J. (1961). Multiple comparisons among means.
            Journal of the American Statistical Association, 56(293):52–64.
    .. [3]  Dunn, O. J. (1964). Multiple comparisons using rank sums.
            Technometrics, 6(3):241–252.

    """  
    try:
        dunn = {}
        groups = copy.deepcopy(args[0]) #tuple of len k
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
                dunn[key]["ID"] = str(i)+"-"+str(j)
                dunn[key]["statistic"] = stat
                dunn[key]["p-value"] = p
                key = key + 1
    except:
        dunn = {}
        groups = copy.deepcopy(args) #tuple of len k
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
                dunn[key]["ID"] = str(i)+"-"+str(j)
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
                if q >= pTop:
                    q = pTop
                else:
                    pass
                dunn[key]["q-value"] = q
        else:
            raise ValueError("correction keyword must be 'none', 'bonferroni' or 'fdr'")
    if "labels" not in kwargs.keys():
        kwargs["labels"] = range(0, len(groups))
    else:
        if len(kwargs["labels"]) != len(groups):
            raise ValueError("length of groups and length of labels must be the same")
    if "display" not in kwargs.keys():
        kwargs["display"] = True
    if kwargs["display"] == True:
        print ""
        lenLabels = []
        for label in kwargs["labels"]:
            lenLabels.append(len(label))
        maxLen = max(lenLabels)
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
        lenLabels = []
        for label in kwargs["labels"]:
            lenLabels.append(len(label))
        maxLen = max(lenLabels)
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
    return dunn

#==============================================================================
# a = [0.28551035, 0.338524035, 0.08831321, 0.205930807, 0.363240102]
# b = [0.52173913, 0.763358779, 0.32546786, 0.425305688, 0.378071834]
# c = [0.98911968, 1.192718142, 0.788288288, 0.549176236, 0.544588155]
# d = [1.26705653, 1.625320787, 1.266108976, 1.154187629, 1.268498943, 1.069518717]
# e = [1.25697569, 1.26589756, 1.2378914561, 0.954612564, 2.365415457]
# 
# f = dunn(a,b,c,d,e, correction="fdr", labels=("a1", "b34d", "con", "das", "er56t"))
#==============================================================================
