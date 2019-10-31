# Introduction

This is the semiformal program spec for Hari Amoor's CSV analyzer (technical challenge for Petal).

# Running the Code

Please run the code as follows:

```
./csv_analyzer file_1.csv.gz file_2.csv.gz
```

The file names can be arbitrary, as long as they're separated by spaces. Furthermore, as many files as needed can be included, and the program will run them all on multiple processes.

# Design Decisions

The code is written entirely in Python, using nothing but the standard library. It reflects the design philosophies of the author, Hari Amoor; a featureful and reliable standard library should provide developers with most of what they need in most situations, and third-party tools should be used only in the case that the standard library either does not have a module that satisfies the use case.

The CSV documents are parsed using the Python `csv` module; ideally, this will deal with most of the cases regarding the "desc" and "misc" columns, which are arbitrary and possibly hard-to-parse strings.

# Discussion on Parallelism

The spec for a parallelized CSV analyzer is as follows.

Python runs under a Global Interpreter Lock (GIL), which is essentially a _mutex_ on the interpreter; that is, Python program memory cannot be accessed by more than one context at one time. There is a `threading` module supplied in the standard library, but it is of no use in this case, since it would not enable CPU-level parallelism because of the GIL; its purpose is instead to facilitate I/O-heavy workloads in which multiple contexts are necessary, but not necessarily CPU-level parallelism.

Instead, to enable CPU-level parallelism, I use the `multiprocessing` module to enable process-level CPU parallelism. This will ultimately result in better CPU utilization, unlike in the case with threads via the `threading` module, because multiprocessing involves copying the full address-space of a program in memory; this would effectively circumvent the issue presented by the GIL.
