# Butterfly: A Plugin for CFD Analysis (GPL) started by Mostapha Sadeghipour Roudsari
# This file is part of Butterfly.
#
# You should have received a copy of the GNU General Public License
# along with Ladybug; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Load results for a field in probes.

-

    Args:
        _solution: Butterfly Solution, Case or fullpath to the case folder.
        _field: Probes' filed as a string (e.g. p, U).
        
    Returns:
        skippedPoints: List of points that are skipped during the solution.
        values: List of values for the last timestep.
"""

ghenv.Component.Name = "Butterfly_Load Probes Value"
ghenv.Component.NickName = "loadProbesValue"
ghenv.Component.Message = 'VER 0.0.03\nOCT_30_2016'
ghenv.Component.Category = "Butterfly"
ghenv.Component.SubCategory = "06::Solution"
ghenv.Component.AdditionalHelpFromDocStrings = "3"

try:
    from butterfly.utilities import loadProbeValuesFromFolder
except ImportError as e:
    msg = '\nFailed to import butterfly. Did you install butterfly on your machine?' + \
            '\nYou can download the installer file from github: ' + \
            'https://github.com/mostaphaRoudsari/Butterfly/tree/master/plugin/grasshopper/samplefiles' + \
            '\nOpen an issue on github if you think this is a bug:' + \
            ' https://github.com/mostaphaRoudsari/Butterfly/issues'
        
    raise ImportError('{}\n{}'.format(msg, e))

from Rhino.Geometry import Point3d, Vector3d
import os


if _solution and _field:
    if isinstance(_solution, str):
        projectDir = _solution.replace('\\\\','/').replace('\\','/')
        probesDir = os.path.join(projectDir, 'postProcessing\\probes') 
        rawValues = loadProbeValuesFromFolder(probesDir, _field)
    else:
        assert hasattr(_solution, 'loadProbeValues'), \
            'Invalid Input: <{}> is not a valid Butterfly Solution.'.format(_solution)
        try:
            rawValues = _solution.loadProbeValues(_field)
        except Exception as e:
            raise ValueError('Failed to load values:\n\t{}'.format(e))
            
    try:
        values = tuple(Vector3d(*v) for v in rawValues)
    except:
        values = rawValues