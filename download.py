#!/usr/bin/python

import os
import commands

for path in commands.getoutput("find . -name changelog").split("\n"):
	(current, project, debian, changelog) = path.split("/")
	header = commands.getoutput("cat %s/debian/changelog | grep urgency | head -1" % project)
	version = header.split("(")[1]	
	version = version.split(")")[0]	
	if ("-" in version):
		version = version.split("-")[0]	
	version_components = version.split(".")
	major = "%s.%s" % (version_components[0], version_components[1])
	if project == "caja-dropbox":
		url = "http://pub.mate-desktop.org/releases/1.4/%s-%s.tar.xz" % (project, version)
	else:
		url = "http://pub.mate-desktop.org/releases/%s/%s-%s.tar.xz" % (major, project, version)
	dest = "%s_%s.orig.tar.xz" % (project, version)
	command = "wget -c %s -O %s" % (url, dest)
	print "Running %s" % command
	os.system(command)
