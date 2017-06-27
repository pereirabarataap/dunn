# dunn
Performs a two-tailed Dunn's test for stochastic dominance.

Dunn’s test (1964) tests for stochastic dominance and reports the results
among multiple pairwise comparisons after a rejected null hypothesis for a
Kruskal-Wallis test for stochastic dominance among k groups.

Examples
--------
In [1]: a = [0.28551035, 0.338524035, 0.088631321, 0.205930807, 0.363240102]\n
In [2]: b = [0.52173913, 0.763358779, 0.325436786, 0.425305688, 0.378071834]
In [3]: c = [0.98911968, 1.192718142, 0.788288288, 0.549176236, 0.544588155]
In [4]: d = [1.26705653, 1.625320787, 1.266108976, 1.154187629, 1.268489431]
In [5]: e = [1.25697569, 1.265897356, 1.237814561, 0.954612564, 2.365415457]
In [6]: f = dunn(a,b,c,d,e)

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

In [7]: groups = a,b,c,d,e
In [8]: g = dunn(groups,
                 correction="fdr",
                 labels=("a", "b", "c", "d", "e"),
                 display=True,
                 save=False)

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

In [9]: f
Out [9]:
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
