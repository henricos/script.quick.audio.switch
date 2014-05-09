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

def setSettingValue(setting, value):
	query = '{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"' + setting + '","value":' + value + '},"id":1}'
	ret = False
	
	response = executeJSONRPC(query)
	
	if response == True:
		ret = True
		
	return ret

# ############################################################

def nextAudioProfile():
		nextprofile = __addon__.getSetting('profile.nextprofile')
		if nextprofile == '1':
			nextprofile = '2'
		else:
			nextprofile = '1'
			
		print nextprofile
		
		audiodevicecategory = __addon__.getSetting('profile.audiodevicecategory.' + nextprofile)
		
		if audiodevicecategory == 'HDMI':
			settingslist = ['audiooutput.audiodevice', 
							'audiooutput.channels', 
							'audiooutput.config', 
							#'audiooutput.samplerate', 
							'audiooutput.stereoupmix', 
							'audiooutput.normalizelevels', 
							'audiooutput.processquality', 
							'audiooutput.streamsilence', 
							'audiooutput.guisoundmode', 
							'audiooutput.passthrough',							
							'audiooutput.passthroughdevice', 
							'audiooutput.ac3passthrough', 
							'audiooutput.ac3transcode', 
							'audiooutput.eac3passthrough', 
							'audiooutput.dtspassthrough', 
							'audiooutput.truehdpassthrough', 
							'audiooutput.dtshdpassthrough']
		elif audiodevicecategory == 'SPDIF':
			settingslist = ['audiooutput.audiodevice', 
							#'audiooutput.channels', 
							'audiooutput.config', 
							'audiooutput.samplerate', 
							'audiooutput.stereoupmix', 
							'audiooutput.normalizelevels', 
							'audiooutput.processquality', 
							'audiooutput.streamsilence', 
							'audiooutput.guisoundmode', 
							'audiooutput.passthrough',
							'audiooutput.passthroughdevice', 
							'audiooutput.ac3passthrough', 
							'audiooutput.ac3transcode', 
							'audiooutput.eac3passthrough', 
							'audiooutput.dtspassthrough', 
							'audiooutput.truehdpassthrough', 
							'audiooutput.dtshdpassthrough']
		else:
			settingslist = ['audiooutput.audiodevice', 
							'audiooutput.channels', 
							'audiooutput.config', 
							#'audiooutput.samplerate', 
							'audiooutput.stereoupmix', 
							'audiooutput.normalizelevels', 
							'audiooutput.processquality', 
							'audiooutput.streamsilence', 
							'audiooutput.guisoundmode', 
							#'audiooutput.passthrough',
							#'audiooutput.passthroughdevice', 
							#'audiooutput.ac3passthrough', 
							#'audiooutput.ac3transcode', 
							#'audiooutput.eac3passthrough', 
							#'audiooutput.dtspassthrough', 
							#'audiooutput.truehdpassthrough', 
							#'audiooutput.dtshdpassthrough'
							]

		allok = True
		for setting in settingslist:
			value = __addon__.getSetting(setting + '.value.' + nextprofile)
			
			if setting in ['audiooutput.audiodevice','audiooutput.passthroughdevice']:
				value = '"' + value + '"'			
			writeToLog('Setting: %s ==> Value: %s' % (setting, value), xbmc.LOGDEBUG)
			result = setSettingValue(setting, value)
			if result == False:
				allopk = False

		if allok == True:
			notify('OK')
			__addon__.setSetting('profile.nextprofile', nextprofile)
		else:
			notify('Error')

	
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
				audiodevicecategory = 'HDMI'
			elif 'SPDIF' in keyselected:
				audiodevicecategory = 'SPDIF'
			else:
				audiodevicecategory = 'Analog'
			__addon__.setSetting('profile.audiodevicecategory.' + profileno, audiodevicecategory)
	