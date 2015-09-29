#!/usr/bin/env python
#/******************************************************************************
# * $Id$
# *
# * Project:  GDAL Make Histogram and Cumlative graph from Tab delimited tab as 
#                generated by gdal_hist.py
# * Purpose:  Take a gdal_hist.py output and create a histogram plot using matplotlib
# * Author:   Trent Hare, thare@usgs.gov
# *
# ******************************************************************************
# * Public domain licenes (unlicense)
# *
# * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# * OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# * DEALINGS IN THE SOFTWARE.
# ****************************************************************************/
import sys
import os
import math
import numpy as np
import pandas as pd
from pandas.tools.plotting import table
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def usage():
    print 'Usage: slope_histogram_cumlative_graph.py -name "InSight E1" slope_histogram_table.tab outfile.png'
    print "  This program is geared to run on a table as generated by gdal_hist.py"
    print 'slope_histogram_cumlative_graph.py -name "E_Marg_CE 01" DEM_1m_E_Marg_CE_adir_1m_hist.xls DEM_1m_E_Marg_CE_adir_1m_hist.png'
    sys.exit(0)

#set None for commandline options
name = ""
infile = None
outfile = None

# =============================================================================
# Parse command line arguments.
# =============================================================================
i = 1
while i < len(sys.argv):
    arg = sys.argv[i]

    if arg == '-name':
        i = i + 1
        name = sys.argv[i]
    elif infile is None:
        infile = arg
    elif outfile is None:
        outfile = arg
    else:
        Usage()
    i = i + 1

if infile is None:
    usage()

if not(os.path.isfile(infile)):
    input = sys.argv[1]
    print "filename %s does not exist." % (infile)
    sys.exit(1)

#load table
df = pd.DataFrame.from_csv(infile, sep='\t', header=1)

#initialize figure
fig, ax1 = plt.subplots()

#calculate unscaled values
#df.value = (df.value * 5) - 0.2
#df.ix[df.value < 0] = 0; df

#not to reverse histogram before calculating 'approx' stats
#min = round(df.value.min(),2)
#max = round(df.value.max(),2)
#mean = round(df.value.mean(),2)
#stddev = round(df.value.std(),2)
#rms = round(math.sqrt((mean * mean) + (stddev * stddev)),2)

#statsDict = {'Min':min,'Max':max,'Mean':mean \
             #,'StdDev':stddev,'RMS':rms}
#statsSeries = pd.Series(statsDict,name='stats')
#statsSeries.sort()

#t = table(ax1, statsSeries, \
      #loc='lower right', colWidths=[0.1] * 2)
#t.set_fontsize(18)
#props = t.properties()
#cells = props['child_artists']
#for c in cells:
    #c.set_height(0.05)

#Plot frequency histogram from input table
ax1.fill(df.value,df['count'],'gray')
#df.plot(ax1=ax1, kind='area', color='gray', legend=True)
ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
ax1.get_yaxis().set_tick_params(direction='out')

#get min and max as found by pandas for plotting 'arrow' at X=15
#minY = round(df['count'].min(),0)
#maxY = round(df['count'].max(),0)

#grab existing ax1 axes
#ax = plt.axes()
#ax.arrow(15, minY, 0, maxY, head_width=0, head_length=0, fc='k', ec='k')
ax1.axvline(x=15, color='black', alpha=0.5)

#add cumlative plot on 'Y2' axis using save X axes
ax2 = ax1.twinx()
ax2.plot(df.value,df['cumlative'],'blue')
#df.plot(ax2=ax2, df.value,df['cumlative'],'blue')
ax2.get_yaxis().set_tick_params(direction='out')

#define labels
ax1.set_xlabel('Slope (degrees)')
ax1.set_ylabel('Count')
ax2.set_ylabel('Cumlative')
plt.suptitle(name + ' Slope Histogram and Cumlative Plot')

#save out PNG
plt.savefig(outfile)
print "Graph exported to %s" % (outfile)
