#! /usr/bin/python

import ConfigParser
import argparse
import json
import os
import re
import requests
import socket
import sys
import traceback

os.chdir(os.path.dirname(sys.argv[0]))

argParser = argparse.ArgumentParser(description="Notify Slack channel or user with message built from (potentially filtered) text piped in")

argParser.add_argument(
	'-c', '--slack-channel',
	required=True,
	action="store",
	dest='channel',
	help='Slack channel or user to notify; ex) @bob for a DM or #public-channel for a channel post'
)

argParser.add_argument(
	'-m', '--max-lines',
	action="store",
	dest='maxLines',
	default=1,
	help='Maximum number of lines to add to Slack notification; when used with -r, only add the specified number of lines that match the regular expression provided'
)

argParser.add_argument(
	'--config-path',
	action="store",
	dest='configPath',
	default='~/.pipe2slack',
	help='Path to configuration file for this script; default is ~/.pipe2slack'
)

argParser.add_argument(
	'-r', '--regex',
	action="store",
	dest='regex',
	help='Regular expression to match against input'
)

args = argParser.parse_args(sys.argv[1:])
channel = args.channel
maxLines = args.maxLines
configPath = args.configPath
regexString = args.regex

config = ConfigParser.RawConfigParser()

expandedConfigPath = os.path.expanduser(configPath)

if not config.read(expandedConfigPath):
	sys.stderr.write('No configuration file present at {0}\n'.format(expandedConfigPath))
	sys.exit(1)

def getConfigSection(section):
	return config.items(section)

def getConfigOption(section, option):
	return config.get(section, option)

iconEmoji = getConfigOption('slack', 'emoji')
webhookURL = getConfigOption('slack', 'webhookURL')

matchedLineCount = 0
text = ""

if regexString:
	regex = re.compile(regexString)
	for line in sys.stdin:
		sys.stdout.write(line)
		if matchedLineCount < maxLines:
			if regex.search(line):
				text += line
				matchedLineCount += 1
else:
	for line in sys.stdin:
		sys.stdout.write(line)
		if matchedLineCount < maxLines:
			text += line
			matchedLineCount += 1

payload = {
	'channel':		channel,
	'username':		socket.gethostname(),
	'text':			text,
	'icon_emoji':	iconEmoji
}

requests.post(webhookURL, data=json.dumps(payload))
