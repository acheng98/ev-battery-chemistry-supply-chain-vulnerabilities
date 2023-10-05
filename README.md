This README describes the code used in the paper "Electric vehicle battery chemistry affects supply chain disruption vulnerabilities" by Anthony L. Cheng, Erica R. H. Fuchs, Valerie J. Karplus, and Jeremy J. Michalek.

There are two major scripts used for analysis, both written in Python, by Anthony L. Cheng. Any errors made in the code are his alone. 

'SankeyData.py' takes trade and production data from IntraCen and USGS, Sun et al. 2021, and IFAStat respectively, and generates a material flow analysis in the form of a Sankey diagram and associated material flows comma separated values file. This material flow data was then analyzed in VulnerabilityCalc.py to measure the vulnerability index described in the paper. Both files output numerical results as well as visuals that are presented in the article. Detailed descriptions of each script and associated methods are included in each file. We acknowledge the use of ChatGPT to generate some code snippets, debug errors, and generate some code documentation.

There is an additional small script ("deturkey.py") that takes any reference to the spelling of the country of Turkey as "Türkiye" in the downloaded trade datasets and converts it to the former, for consistency of analysis. 

All data and code in this repository are available under the MIT license, copied below for convenience.

Copyright (c) 2023 Anthony L. Cheng

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.