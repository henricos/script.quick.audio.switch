import xbmc
import xbmcgui
import xbmcaddon

__addon__      = xbmcaddon.Addon()
__addonname__  = __addon__.getAddonInfo('name')
__addonid__    = __addon__.getAddonInfo('id')

# ############################################################

def notify(txt):
	dialog = xbmcgui.Dialog()
	dialog.notification(__addonname__, txt)

# ############################################################
	
def writeToLog(message, xbmcloglevel=xbmc.LOGNOTICE):
	msg = u'[%s] %s' % (__addonid__, message)
	xbmc.log(msg.encode("utf-8"), xbmcloglevel)

# ############################################################
	
def executeJSONRPC(query):
	empty = []
	true = True
	false = False
	null = None

	writeToLog(("JSON Query\n%s" % query), xbmc.LOGDEBUG)
	
	response = xbmc.executeJSONRPC(query)
	
	writeToLog("JSON Response\n%s" % response, xbmc.LOGDEBUG)
	
	if response.startswith( "{" ):
		response = eval(response)
		try:
			if response.has_key('result'):
				result = response['result']
				return result
			else:
				writeToLog("Invalid JSON response - No result element!", xbmc.LOGERROR)
				return None
		except:
			writeToLog("Invalid JSON response", xbmc.LOGERROR)
			return empty
	else:
		writeToLog("Invalid JSON response - Doesn't look like JSON", xbmc.LOGERROR)
		return empty

# ############################################################

def getAudioSettings():
	query = '{"jsonrpc":"2.0","method":"Settings.GetSettings", "params":{"filter":{"section":"system","category":"audiooutput"},"level":"advanced"},"id":1}'
	ret = {}
	
	response = executeJSONRPC(query)
	settings = response.get('settings')
	for cursetting in settings:
		id = cursetting.get('id')
		value = cursetting.get('value')
		ret[id] = value
	
	return ret

# ############################################################

def getSettingOptions(setting):
	query = '{"jsonrpc":"2.0","method":"Settings.GetSettings", "params":{"filter":{"section":"system","category":"audiooutput"},"level":"advanced"},"id":1}'
	ret = {}
	
	response = executeJSONRPC(query)
	settings = response.get('settings')
	for cursetting in settings:
		id = cursetting.get('id')
		if id == setting:
			options = cursetting.get('options')
			for opt in options:
				ret[opt.get('label')] = opt.get('value')
				
	return ret

# ############################################################

def openDialogSelect(setting, profileno, titlestringno):
	options = getSettingOptions(setting)
	
	sortedkeys = sorted(options.keys())		
	dialog = xbmcgui.Dialog()
	ret = dialog.select(__addon__.getLocalizedString(titlestringno).encode("utf-8"), sortedkeys)
	
	if ret != -1:
		keyselected = sortedkeys[ret]
		__addon__.setSetting(setting + '.' + profileno, keyselected.__str__())
		__addon__.setSetting(setting + '.value.' + profileno, options[keyselected].__str__())
		if setting == 'audiooutput.audiodevice':
			if 'HDMI' in keyselected:
				__addon__.setSetting('profile.audiodevicecategory.' + profileno, 'HDMISPDIF')
			else:
				__addon__.setSetting('profile.audiodevicecategory.' + profileno, 'ANALOG')
	