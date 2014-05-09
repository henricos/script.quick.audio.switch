# -*- coding: utf-8 -*-
#

# Import system libraries
import sys
import os
import xbmc
import xbmcgui
import xbmcaddon

# Constants
__addon__      = xbmcaddon.Addon()
#__addonname__  = __addon__.getAddonInfo('name')
#__addonid__    = __addon__.getAddonInfo('id')
__cwd__        = __addon__.getAddonInfo('path').decode("utf-8")
#__version__    = __addon__.getAddonInfo('version')
#__language__   = __addon__.getLocalizedString
__resource__   = xbmc.translatePath(os.path.join( __cwd__, 'resources', 'lib' ))

# Append resource lib to path
sys.path.append(__resource__)

# Import extra functions (utils)
import utils

# ###################################################################################
# ###################################################################################
# ###################################################################################

# If the script has 3 arguments (2 parameters), its a call from the settings page
# to create dialog windows with system options
if len(sys.argv) == 3:

	parameter1 = sys.argv[1]
	parameter2 = sys.argv[2]
	
	# Audio Device dialog
	if parameter1 == 'audiooutput.audiodevice':
		utils.openDialogSelect(parameter1, parameter2, 32120)
		
	# Number of Channels dialog
	elif parameter1 == 'audiooutput.channels':
		utils.openDialogSelect(parameter1, parameter2, 32121)
		
	# Audio Output Config dialog
	elif parameter1 == 'audiooutput.config':
		utils.openDialogSelect(parameter1, parameter2, 32122)
		
	# Sample Rate dialog
	elif parameter1 == 'audiooutput.samplerate':
		utils.openDialogSelect(parameter1, parameter2, 32123)		
		
	# Process Quality dialog
	elif parameter1 == 'audiooutput.processquality':
		utils.openDialogSelect(parameter1, parameter2, 32126)		
		
	# Stream Silence dialog
	elif parameter1 == 'audiooutput.streamsilence':
		utils.openDialogSelect(parameter1, parameter2, 32127)		
	
	# GUI Sound Mode dialog
	elif parameter1 == 'audiooutput.guisoundmode':
		utils.openDialogSelect(parameter1, parameter2, 32128)		
	
	# Passthrough Device dialog
	elif parameter1 == 'audiooutput.passthroughdevice':
		utils.openDialogSelect(parameter1, parameter2, 32130)	

	# Unknown dialog
	else:
		utils.writeToLog('Unknown arguments' + parameter1, xbmc.LOGERROR)

# Any other case, runs the script (try to switch audio device)		
else:
	utils.writeToLog("------ Script Started ------")
	utils.notify('Script Started')

	audiosettings = utils.getAudioSettings()
	print 'Audio Settings'
	print audiosettings
		
	
	utils.writeToLog("------ Script Ended ------")
