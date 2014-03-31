#!/usr/bin/env python

import codecs
import datetime
import optparse
import os
import subprocess
import sys

parser = optparse.OptionParser()
parser.add_option("-s", "--source", dest="source", action="store_true", help="Build source package")
parser.add_option("-i", "--i386", dest="i386", action="store_true", help="Build i386 binary package")
(options, args) = parser.parse_args()

if len(args) == 0:
    print "E: No package given!"
    sys.exit(1)
elif len(args) > 1:
    print "E: Too many packages given!"
    sys.exit(1)

package = args[0]

if package == "":
    sys.exit(1)
if package[-1] == "/":
    package = package[:-1]

if not os.path.exists(package):
    print "E: package '%s' not found" % package
    sys.exit(1)

# create build script needed folders
os.system ("mkdir -p ~/mate/deb")
os.system ("mkdir -p ~/mate/logs")

os.system("rm -rf /tmp/%s/ " % package)
os.system("cp " + package + " /tmp/" + package + "/ -R") 

os.chdir("/tmp/%s" % package)
os.system("rm -rf debian/")
os.system("cp -R ~/mate/debian-packages/%s/debian/ ." % package)
os.system("echo '3.0 (native)' > debian/source/format")

# debian/changelog
date = datetime.date.today().strftime("%Y%m%d")
head = subprocess.check_output(["git", "rev-parse", "HEAD"])[:7]
suffix = "+git." + date + "." + head
orig_changelog_file = codecs.open("debian/changelog", encoding="utf-8", mode="r")
orig_changelog = orig_changelog_file.read().splitlines()
orig_changelog_file.close()
new_changelog = orig_changelog
new_changelog[0] = new_changelog[0].replace(")", suffix + ")")
if options.source:
    for i in range(10):
        new_changelog[0] = new_changelog[0].replace("-" + str(i), "")
new_changelog_file = codecs.open("debian/changelog", encoding="utf-8", mode="w")
new_changelog_file.write("\n".join(new_changelog))
new_changelog_file.close()

# debian/rules
orig_rules_file = codecs.open("debian/rules", encoding="utf-8", mode="r")
orig_rules = orig_rules_file.read()
orig_rules_file.close()
new_rules = orig_rules
new_rules = new_rules.replace("dh_auto_configure --", "NOCONFIGURE=1 ./autogen.sh\n\tdh_auto_configure --")
new_rules = new_rules.replace("#DEB_CONFIGURE_SCRIPT := ./autogen.sh", "DEB_CONFIGURE_SCRIPT := ./autogen.sh")
new_rules_file = codecs.open("debian/rules", encoding="utf-8", mode="w")
new_rules_file.write(new_rules)
new_rules_file.close()

if options.source:
    os.system("dpkg-buildpackage -S -Zxz -uc -us")
    os.system("mv -v ../*.dsc ~/mate/deb/")
    os.system("mv -v ../*.xz ~/mate/deb/")
    os.system("mv -v ../*.changes ~/mate/deb/")
else:
    if options.i386:
        os.system("dpkg-buildpackage -B -ai386 -Zxz -uc -tc 2>&1 | tee build.log")
    else:
        os.system("dpkg-buildpackage -b -Zxz -uc -tc 2>&1 | tee build.log")
    os.system("mv -v build.log ~/mate/logs/%s.log" % package)
    os.system("rm -v ../*.changes")
    os.system("mv -v ../*.deb ~/mate/deb/")
os.chdir(os.path.join(os.path.expanduser("~"), "mate"))
os.system("rm -rf /tmp/%s/ " % package)
print "---------------------------------------------------------------"
os.system("ls -1 deb/")
print "---------------------------------------------------------------"
