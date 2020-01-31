# BWR 6x6 Benchmark Environment

This environment is a benchmark of 6x6 BWR assembly with 1/2 symmetry (21 possible positions), two discrete enrichments are possible per location (1.87, 2.53), the positions are assigned as:
```
1
2 3
4 5 6
7 8 9 10
11 12 13 14 15
16 17 18 19 20 21 
```
`data.tar.gz` contains the dataset which is two csv files for the inputs (enrichments in all 21 positions) and outputs (keff, ppf, enrichment)

The input file (`input.csv` inside of `data.tar.gz`) looks like:

```
case,pos1,pos2,pos3,pos4,pos5,pos6,pos7,pos8,pos9,pos10,pos11,pos12,pos13,pos14,pos15,pos16,pos17,pos18,pos19,pos20,pos21,
1,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,
2,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,2.53,
3,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,1.87,2.53,1.87,
...
```

The output file (`output.csv` inside of `data.tar.gz`) looks like:

```
case, kinf, ppf, avg_enrich, 
1, 1.1981, 1.368, 1.87, 
2, 1.20088, 1.363, 1.888, 
3, 1.20291, 1.359, 1.907, 
...
```

The objective function is:

![Objective function](bwr6x6_objective_function.png)

If we set `w_p=0` when `PFF<1.35` then, of the 2M solutions, you should find 59 top solutions all with same objective function value of 0.016.

### Running the random agent:


### Running the examples:


### Visualization:
