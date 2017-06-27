# dunn
Performs a two-tailed Dunn's test for stochastic dominance.

Dunn’s test (1964) tests for stochastic dominance and reports the results
among multiple pairwise comparisons after a rejected null hypothesis for a
Kruskal-Wallis test for stochastic dominance among k groups.

Examples
--------
In [1]: a = [0.28551035, 0.338524035, 0.088631321, 0.205930807, 0.363240102]

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
