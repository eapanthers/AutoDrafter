# AutoDrafter

A fantasy football drafter which plans an entire draft given certain parameters. See https://eaanalytics.blogspot.com/2021/01/building-better-auto-drafter-using-gene.html for more information.

Clone this repository ($ git clone https://github.com/eapanthers/AutoDrafter.git), then install the appropriate python packages. Then run python Drafter.py after navigating to the correct directory and answer the following prompts:
  - The index of the first pick 
  - The number of rounds in the draft (two will be subtracted to account for kicker and defense picks)
  - The number of teams in the league
  - The weight given towards drafting QBs, on a scale of 1 to number of rounds -- this number will correspond approximately to the number that get picked
  - The weight given towards drafting RBs
  - The weight given towards drafting WRs
  - The weight given towards drafting TEs - the sum of these weights should equal the number of rounds - 2. So in a 14 round league, I'd recommend 1, 5, 5, 1 as the weights
  - (Optional) The amount of variance observed when simulating the draft on a scale of 1-10.
 
 Sample datasets containing ADP and player projections from ESPN are included.
 
 Known issues:
 On rare occasions player names will appear twice. Simply re-run and the problem should go away.
 Running on some instances of macOS will cause some menus not to display. Buttons included in that case.
 
 Future improvements:
   - Implement a UI
   - Update live during drafts
