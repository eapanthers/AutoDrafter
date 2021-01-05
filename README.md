# AutoDrafter

A fantasy football drafter which plans an entire draft given certain parameters.

Clone this repository, then install the appropriate python packages. Then run python Drafter.py with the following parameters in order:
  - The index of the first pick 
  - The number of rounds in the draft (two will be subtracted to account for kicker and defense picks)
  - The number of teams in the league
  - The weight given towards drafting QBs, on a scale of 1 to number of rounds -- this number will correspond approximately to the number that get picked
  - The weight given towards drafting RBs
  - The weight given towards drafting WRs
  - The weight given towards drafting TEs - the sum of these weights should equal the number of rounds - 2. So in a 14 round league, I'd recommend 1, 5, 5, 1 as the weights
  - (Optional) Whether the league scoring is standard or ppr - by default standard
  - (Optional) The amount of variance observed when simulating the draft on a scale of 1-10. Lower is more variance, higher will more strictly obey player ADP. Defaults to 10
  
  So a sample appropriate input to run would be $ python Drafter.py 4 14 12 1 5 5 1 ppr 6
 
 Sample datasets containing ADP and player projections from ESPN are included.
