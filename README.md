HOW TO BUILD MATE ON DEBIAN GNU\LINUX (Wheezy or later):
========================================================

Prepering for the build
-----------------------

 1. Get all the tools needed to build mate:
    `aptitue install build-essential cdbs`
 2. Make your own gpg key if you don't already have.
    `gpg --gen-key`
    All the defaults are good enough!
 3. Set the environment variables for debuild:

```
export DEBMAIL="yourmail@example.com"
export DEBFULLNAME="Jon Smith"
```

    These have to match what you entered when you created your gpg key !


Building the a Debian Package:
------------------------------  

 1. Run the script `install_mate_dependecies.sh`.  
 2. Create a directory mate-desktop: `mkdir mate-desktop`  
 3. Go inside that directory.   
 4. Download all the mate-desktop repositories from github.com  
   Clone each repositroy with:
   `git clone git://github.com/mate-desktop/mate-doc-utils.git`
    You should replace `mate-doc-utils` for each repo.  

 5. After you clone each repository, you should create a bzipped tarball  
for each repository:
    `cd mate-doc-utils && git archive master | bzip2 > ../mate-doc-utils.orig.tar.bz2`
 6. Now you need to copy the Debian rules inside that directory:  
    `rsync -av ../debian-packages/mate-doc-utils/debian .`

 7. Edit the changlog with `dch -i`.
 8. If needed edit the `debian/control`.
 9. Create the source package: `debuild -S -sa`
 10. Build the package with: `debuild`
 11. Install the packages built with: `sudo dpkg -i ../*deb`
 12. Clean everthing above the directory with running the following commands:

```
mkdir -v {deb,deb-src}
mv -v *deb deb/
mv -v *tar.gz deb-src/
mv -v *dsc deb-src/
mv -v *build deb-src/
mv -v *changes deb-src/
mv -v *tar.bz2 deb-src/
``` 

 13. Continue building the next packages ...

What Happens if A package fails to build?
----------------------------------------
If a packages fails to build you will not be able to build it again in 
the same source tree. To clean the source tree first move the debian directory
one level up:
	mv -v debian ..
Then, clean everything in the tree with:
```
git reset --hard
git clean -f -x -d # CAUTION: This removes everything untracked. If you created new files, make sure you commit them before !!!
```
remove the `debian` directory back to where it is expected: `mv ../debian .`
Rebuild the package with repeating steps 9 and 10 from above. 
      


Order in which to build Mate
----------------------------
```
mate-common
mate-doc-utils
mate-corba
mate-conf
libmatecomponent
mate-mime-data
mate-vfs
libmate
libmatecanvas
libmatecomponentui
libmatekeyring
mate-keyring
libmateui
libmatenotify
libmatekbd
libmateweather
mate-icon-theme
mate-dialogs
mate-desktop
mate-file-manager
mate-notification-daemon
mate-backgrounds
mate-menus
mate-window-manager
mate-polkit
mate-settings-daemon (had to use mate-doc-prepare --force --copy; autoreconf -i --force)
mate-control-center (needs mate-window-manager installed, else complains about libmarco)
mate-panel (needs gobject-introspection removed on the host, or --disable-introspection in DEB_CONFIGURE_EXTRA_FLAGS in debian/rules)
mate-session-manager
```
