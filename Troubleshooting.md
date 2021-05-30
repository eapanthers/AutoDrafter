# Troubleshooting Installation

When installing, you may run into one of the following issues:

## Invalid Syntax when running python AutoDrafter.py

This error is caused by an outdated version of Python. First, check your version by running python --version in your terminal. If you see it's older than Python 3.5, you must install a newer version. After doing this, if python --version does not display the updated version, try python3 --version. You should see the newer version. Follow these instructions to upgrade: https://askubuntu.com/questions/320996/how-to-make-python-program-command-execute-python-3

## ModuleNotFoundError

This means you have to manually install a package (usually pandas and/or scipy). To do this run pip install <package-name> (without the <>). If you get a 'pip not recognized' error, follow these instructions on installing pip (I recommend the *Installing with get-pip.py* way): https://pip.pypa.io/en/stable/installing/
  
##  invalid literal for int() with base 10: ''
  
This is caused by your configuration file not being set correctly (or at all). Make sure it follows the format in the sample config.
  
##  [Errno 2] No such file or directory: 'None set'

This means you haven't set the CSV files yet are running an operation that requires them.
