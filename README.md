# AutoDrafter

A fantasy football drafter which plans an entire draft given certain parameters. See https://eaanalytics.blogspot.com/2021/01/building-better-auto-drafter-using-gene.html for more information.

## How to run:
 - Open your terminal of choice, clone this repository ($ git clone https://github.com/eapanthers/AutoDrafter.git), and install the appropriate python packages. 
 - Run python Drafter.py after navigating to AutoDrafter/src. It may take a minute to cache for first time use this session. 
 - Go to File -> Set Config... and choose the configuration file located in the same directory as AutoDrafter, or set your own configuration values. Picks can be either a full list, or if you made no trades just the index of your first pick.
 - Click Done and go to File -> Set CSVs (unless you set your CSV paths in the config json). Select the sample CSVs in the fantasyCSVs folder in the same directory as AutoDrafter. Once those are all set, you can view the board using the View Board option, or run the simulation.

For common issues, see [Troubleshooting.md](https://github.com/eapanthers/AutoDrafter/blob/main/Troubleshooting.md)
 
 Sample datasets containing ADP and player projections from ESPN are included.
 
 ## Known issues:
 On rare occasions player names will appear twice. Simply re-run and the problem should go away. If the issue persists, verify your player weights sum to the number of rounds.
 
 Running on some instances of macOS will cause some menus not to display. Buttons included in that case.
 
 When adding file paths to the config, replace all `\` with `\\` to avoid loading errors.
 
 As of July 2021, Travis Kelce will be the recommended first round pick for you if you're picking outside of the top 3. This isn't an error - the program is working as intended - its due to his projected points being way higher than any other TEs. If you don't want to have him projected top ~8, manually drop his point projections closer to the other TEs.
 
 ## Future improvements:
   - Update live during drafts
   - Fill correct values when re-initializing config menu
