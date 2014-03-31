#!/usr/bin/env python

import optparse
import os
import sys

parser = optparse.OptionParser()
parser.add_option("-a", "--all", action="store_true")
parser.add_option("--gtk2", action="store_true")
parser.add_option("--gtk3", action="store_true")
(options, args) = parser.parse_args()

if not options.gtk2 and not options.gtk3:
	print "E: Set GTK version!"
	sys.exit(1)
if options.gtk2 and options.gtk3:
	print "E: Set only one GTK version!"
	sys.exit(1)

if options.all:
	packages = os.listdir(".")
else:
	packages = args

replaces = []
replaces.append(["--with-gtk=2.0", "--with-gtk=3.0"])
replaces.append(["libgtk2.0-dev", "libgtk-3-dev"])
replaces.append(["libgtk2.0-doc", "libgtk-3-doc"])
replaces.append(["libunique-dev", "libunique-3.0-dev"])
replaces.append(["gir1.2-gtk-2.0", "gir1.2-gtk-3.0"])
replaces.append(["libcanberra-gtk-dev", "libcanberra-gtk3-dev"])
replaces.append(["libvte-dev", "libvte-2.90-dev"])
replaces.append(["libgail-dev", "libgail-3-dev"])
replaces.append(["libwnck-dev", "libwnck-3-dev"])
replaces.append(["libgtkmm-2.4-dev", "libgtkmm-3.0-dev"])
replaces.append(["libgtksourceview2.0-dev", "libgtksourceview-3.0-dev"])

for package in packages:
	if os.path.isdir(package):
		for dfile in ["control", "rules"]:
			pfile = package + "/debian/" + dfile
			if os.path.exists(pfile):
				if not options.all:
					print pfile
				for r in replaces:
					if options.gtk2:
						r1 = r[1]
						r2 = r[0]
					elif options.gtk3:
						r1 = r[0]
						r2 = r[1]
					os.system("sed -i 's/" + r1 + "/" + r2 + "/' " + pfile)
