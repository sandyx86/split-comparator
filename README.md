# split-comparator
A comparison tool for .lss files from LiveSplit

Functions:
  - Count how many times each segment has been reset on.
  - Compare each segment from two runs in the same or different files.
  - Create a hybrid run from the better segments of two runs.
  - Create a list of all your runs in order from fastest to slowest, and show their IDs.

If you've skipped a segment in a run, the comparison tool will also skip the segment in its comparisons.
The filename of the splits file can't have any spaces in it for now.

Need Python 3.10, it's a CLI program and uses ANSI color codes so
you may want a terminal other than cmd or powershell, or just
make the green red and clear variables empty strings so that
it will look right in cmd.
