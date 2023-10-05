This README describes the code used in the paper "Electric vehicle battery chemistry affects supply chain disruption vulnerabilities" by Anthony L. Cheng, Erica R. H. Fuchs, Valerie J. Karplus, and Jeremy J. Michalek.

There are two major scripts used for analysis, both written in Python, by Anthony L. Cheng. Any errors made in the code are his alone. 

'SankeyData.py' takes trade and production data from IntraCen and USGS, Sun et al. 2021, and IFAStat respectively, and generates a material flow analysis in the form of a Sankey diagram and associated material flows comma separated values file. This material flow data was then analyzed in VulnerabilityCalc.py to measure the vulnerability index described in the paper. Both files output numerical results as well as visuals that are presented in the article. Detailed descriptions of each script and associated methods are included in each file. We acknowledge the use of ChatGPT to generate some code snippets, debug errors, and generate some code documentation.
Source data are provided with this paper; the data underlying these analyses is fully included in this GitHub repository, either as trade data files in the "Raw Trade Map Data" folder, processed material flows in the "Processed Data" folder, or as direct numerical inputs (production data) in the SankeyData.py file. 

There is an additional small script ("deturkey.py") that takes any reference to the spelling of the country of Turkey as "Türkiye" in the downloaded trade datasets and converts it to the former, for consistency of analysis. 

The below information is required as part of Nature Research's Code and Software Submission Checklist (https://www.nature.com/documents/nr-software-policy.pdf)
System Requirements:
- Any installation of python 3.9 or above should be able to run the code in this analysis. This analysis was run on Python 3.9.7.

Installation guide
- In addition to the standard installation of the python programming language, the following python libraries are required to run these scripts:
	- numpy
	- pandas
	- matplotlib
	- seaborn
	- plotly
- Files can be directly downloaded from this github repository (https://github.com/acheng98/ev-battery-chemistry-supply-chain-vulnerabilities) or the entire repository can be cloned (https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository). This should require very little installation time given a standard internet connection (<1 minute). 

- Demo
Though the file path names may need to be changed, particularly in "SankeyData.py", running each python script (e.g. python SankeyData.py in Terminal or PowerShell) should automatically output the desired figures and files (depending on the flags chosen in each top level '__main__' environment.) For example, running VulnerabilityCalc.py as provided will bring up a bar chart diagram of the calculated vulnerability indices for China, Russia, DRC, and South Africa for the five cathode-mineral pairs (see Fig. 5 for this plot). The runtime of this demo on a 'normal' desktop computer should be less than 15 seconds if not much faster. 

All data and code in this repository are available under the MIT license, copied below for convenience.

Copyright (c) 2023 Anthony L. Cheng

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.