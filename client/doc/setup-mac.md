
# MacOS X toolchain setup instructions

The following are instructions for setting up the MiFlux development environment and toolchain under MacOS X.

This has only been tested under MacOS 10.9 (Mavericks) so far.

## XCode

Install XCode from the Apple App Store, then install the command line tools:

```bash
xcode-select --install
```

## Environment

Set up the environment to be make sure that no Homebrew or XQuartz stuff gets built in to what we're doing, as these things won't be on the systems the app gets installed on.

You can set `${TOOLCHAIN}` below to be whatever directory you want.  This is where all of the tools needed to develop MiFlux will be installed.

```bash
unset DYLD_LIBRARY_PATH
unset LD_LIBRARY_PATH
export TOOLCHAIN=${HOME}/miflux/client/toolchain
export PATH=${TOOLCHAIN}/Frameworks/Python.framework/Versions/2.7/bin:${TOOLCHAIN}/bin:/usr/bin:/bin:/usr/sbin:/sbin
```


## Install Python

Most (but not all) articles on using py2app say that building our own version of Python is necessary, and that using the Apple-supplied Python won't work.  To be safe, and also to have full control over the toolchain used by MiFlux, we will build and install our own version of Python.

We'd like to use the latest version of Python 3, just to have the latest features and be up to date, but Twisted 14.0 has not been fully ported to Python 3, so we need to install Python 2.7.  Pretty much everything else that MiFlux depends upon seems to work fine with Python 3, however.

See:

* http://binarybuilder.wordpress.com/2012/10/09/building-python-2-7-on-mac-os-x-mountain-lion/
* step 5 at http://www.trondkristiansen.com/?page_id=79

We're currently using the 10.8 SDK because this is the oldest that XCode 5.1.1 supports.  If we need the 10.7 SDK later, try https://github.com/devernay/xcodelegacy

```bash
mkdir -p ${TOOLCHAIN}/src
cd ${TOOLCHAIN}/src

curl -O -L https://www.python.org/ftp/python/2.7.6/Python-2.7.6.tgz
tar zxf Python-2.7.6.tgz
cd Python-2.7.6
# Make sure homebrew stuff is not used:
export PATH=${TOOLCHAIN}/bin:/usr/bin:/bin:/usr/sbin:/sbin

# TODO: Mac: install our own Tcl/Tk to avoid dependence on Apple ones which may differ between versions of MacOS X?

./configure MACOSX_DEPLOYMENT_TARGET=10.8 \
  --prefix=${TOOLCHAIN} \
  --enable-framework=${TOOLCHAIN}/Frameworks \
  --enable-toolbox-glue \
  --enable-universalsdk="/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.8.sdk" \
  --with-universal-archs=intel \
  2>&1 | tee log.configure

make 2>&1 | tee log.make
make test 2>&1 | tee log.test
  # with framework:    364 OK, 33 skipped, 3 unexpected skip on Darwin
  # without framework: 363 OK, 34 skipped, 4 unexpected skip on Darwin
make install 2>&1 | tee log.install
```


## Install pip

* https://pip.pypa.io/en/latest/installing.html

```bash
cd ${TOOLCHAIN}/src
curl -O -L https://bootstrap.pypa.io/get-pip.py
python ./get-pip.py 2>&1 | tee log.pip
```


## Install Qt5

* http://qt-project.org/
* http://qt-project.org/resources/getting_started

```bash
cd ${TOOLCHAIN}/src

curl -O -L http://download.qt-project.org/official_releases/qt/5.3/5.3.0/single/qt-everywhere-opensource-src-5.3.0.tar.gz
tar zxf qt-everywhere-opensource-src-5.3.0.tar.gz
cd qt-everywhere-opensource-src-5.3.0
# Make sure homebrew stuff is not used:
export PATH=${TOOLCHAIN}/bin:/usr/bin:/bin:/usr/sbin:/sbin

./configure -prefix ${TOOLCHAIN} \
  -opensource -confirm-license \
  -framework -sdk macosx10.8 -release 2>&1 | tee log.configure

make 2>&1 | tee log.make
make install 2>&1 | tee log.install
make docs html_docs 2>&1 | tee log.docs
make install_docs install_html_docs 2>&1 | tee log.docs-install

# Test:
open ${TOOLCHAIN}/bin/Designer.app
```


## Install SIP

* http://www.riverbankcomputing.com/software/sip/download
* http://pyqt.sourceforge.net/Docs/sip4/

```bash
cd ${TOOLCHAIN}/src

curl -O -L \
  http://sourceforge.net/projects/pyqt/files/sip/sip-4.16/sip-4.16.tar.gz
tar zxf sip-4.16.tar.gz
cd sip-4.16
python configure.py 2>&1 | tee log.configure
make 2>&1 | tee log.make
make install 2>&1 | tee log.install
```


## Install PyQt5

* http://pyqt.sourceforge.net/Docs/PyQt5/installation.html

```bash
cd ${TOOLCHAIN}/src

curl -O -L http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.3/PyQt-gpl-5.3.tar.gz
tar zxf PyQt-gpl-5.3.tar.gz
cd PyQt-gpl-5.3
python configure.py --confirm-license \
  --pyuic5-interpreter=${TOOLCHAIN}/bin/python2.7 \
  --sip=${TOOLCHAIN}/Frameworks/Python.framework/Versions/2.7/bin/sip \
  2>&1 | tee log.configure
make 2>&1 | tee log.make
make install 2>&1 | tee log.install

# Test it:
python ./examples/qtdemo/qtdemo.py
```


## Install dependencies for Twisted and Conch

```bash
cd ${TOOLCHAIN}/src
pip install zope.interface 2>&1 | tee log.zope.interface
pip install PyCrypto 2>&1 | tee log.PyCrypto
pip install PyASN1 2>&1 | tee log.ASN1
pip install pyOpenSSL 2>&1 | tee log.pyOpenSSL
```

Note for the future: when we do this on Windows, also install pywin 32 (included with ActivePython).



## Install Twisted

* https://twistedmatrix.com/trac/wiki/Downloads

```bash
cd ${TOOLCHAIN}/src
curl -O -L http://twistedmatrix.com/Releases/Twisted/14.0/Twisted-14.0.0.tar.bz2
tar zxf Twisted-14.0.0.tar.bz2
cd Twisted-14.0.0
python setup.py build 2>&1 | tee log.build
python setup.py install 2>&1 | tee log.install
```


## Install py2app

* http://pythonhosted.org//py2app/

We are installing this from source rather than via pip because we need to patch it to work with PyQt5.

```bash
cd ${TOOLCHAIN}/src
# Take care of py2app dependencies separately to simplify the py2app install:
pip install macholib 2>&1 | tee log.macholib
pip install modulegraph 2>&1 | tee log.modulegraph
pip install altgraph 2>&1 | tee log.altgraph

curl -O -L https://pypi.python.org/packages/source/p/py2app/py2app-0.8.1.tar.gz
tar zxf py2app-0.8.1.tar.gz
cd py2app-0.8.1
sed "s%@@TOOLCHAIN@@%${TOOLCHAIN}%g" <../../../py2app.patch.in >py2app.patch
patch -p 1 < py2app.patch
python setup.py build 2>&1 | tee log.build
python setup.py install 2>&1 | tee log.install
```


# Building the MiFlux application

This is currently a very rough, manual process.  It will be improved and automated in the near future.

## One-time-only setup

This has already been done, and you should not need to re-do it (re-doing it will lose the modifications that were subsequently made to setup.py):

```bash
cd ~/miflux/client
py2applet --make-setup src/MiFlux.py  # only needs to be run once, ever
```

## Building MiFlux for development

When building MiFlux in alias mode (`py2app -A`) you can make changes to the MiFlux code in the `src` directory without needing to rebuild MiFlux after each change.

```bash
cd ~/miflux/client/src
pyuic5 -o ui_MainWindow.py MainWindow.ui

cd ..
python setup.py py2app -A   # alias mode, for testing and development
```

If you run MiFlux normally (that is, without a tty), debugging messages will be written to `~/.miflux/miflux.log`:

```bash
open dist/MiFlux.app
```

Alternatively, you can run MiFlux with a tty and debugging messages will be displayed on stderr:

```bash
./dist/MiFlux.app/Contents/MacOS/MiFlux
```

## Building MiFlux for distribution

Do the following, but do not try to run MiFlux yet -- we will need to do some manual steps after this.

```bash
cd ~/miflux/client/src
pyuic5 -o ui_MainWindow.py MainWindow.ui
rm *.pyc

cd ..
rm -rf build dist
python setup.py py2app 2>&1 | tee log.bundle

```

The application bundle that py2app produces crashes because it can't find the plugin libqcocoa.dylib (see the debugging section below for information on how to determine this).  For a discussion of this problem, see http://qt-project.org/forums/viewthread/26446

Here is our temporary solution until we can modify the py2app sip recipe to take care of this for us automatically:

```
cd ~/miflux/client/dist/MiFlux.app/Contents/Resources
rm -rf qt_plugins
mkdir qt_plugins
cp -r ~/miflux/client/toolchain/plugins/* qt_plugins/

# You can run this to see what needs to be fixed up:
#otool -L qt_plugins/platforms/libqcocoa.dylib

for f in `find qt_plugins -type f -name "*.dylib"` ; do
  echo $f
  install_name_tool -id @executable_path/../Resources/$f $f
  refs=`otool -L $f | perl -a -n -e 'print "$F[0]\n" if $F[0] =~ /\/client\/toolchain\//;'`
  for r in $refs ; do
    r2=`echo "$r" | perl -p -e 's/^.*\/client\/toolchain\/lib/\@executable_path\/..\/Frameworks/;'`
    install_name_tool -change "$r" "$r2" $f
  done
done
```

You should now be able to double-click the app in Finder, or launch it from the command line:

```bash
open dist/MiFlux.app
```

We will soon be enhancing `setup.py` to create a .dmg containing the app bundle, an applications alias, and a pretty background, for easy installation by the end user.  Until then, you can create a `.zip` archive in order to distribute the app.

If you get the error "The application cannot be opened because its executable is missing", you can either `rm -rf build dist` then rebuild the app (using the procedure above) or you can rebuild the Launch Services database:

```bash
/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -f dist/MiFlux.app
```

## Debugging crashes

If the application dies and the crash reporter runs, there will be a text file containing the details and a stack trace in the directory `Library/Logs/DiagnosticReports` -- you will want the file whose name begins with `MiFlux_` *not* the crash report whose filename begins with `python.exe_`.

When `qFatal()` gets called in the Qt libraries, this will result in the following:

```text
Crashed Thread:  0  Dispatch queue: com.apple.main-thread

Exception Type:  EXC_CRASH (SIGABRT)
Exception Codes: 0x0000000000000000, 0x0000000000000000

Application Specific Information:
abort() called

Thread 0 Crashed:: Dispatch queue: com.apple.main-thread
0   libsystem_kernel.dylib              0x00007fff85259866 __pthread_kill + 10
1   libsystem_pthread.dylib             0x00007fff88dfc35c pthread_kill + 92
2   libsystem_c.dylib                   0x00007fff8548eb1a abort + 125
3   QtCore                              0x0000000108462eb9 0x108442000 + 134841
4   QtCore                              0x0000000108464361 QMessageLogger::fatal(char const*, ...) const + 161
```

Unfortunately, we do not currently have debugging information for the Qt libraries, even if py2app is run with `--no-strip`.  Someone should look into this and see what needs to be done to have/keep debugging information or to use the debugging versions of the Qt libraries.  But this blog post is helpful in determining which registers contain which function arguments in the absence of debugging information:

http://www.clarkcox.com/blog/2009/02/04/inspecting-obj-c-parameters-in-gdb/

```
lldb ./dist/MiFlux.app/Contents/MacOS/MiFlux
breakpoint set --name QMessageLogger::fatal
run
bt
frame info
register read
p (char *)$rsi    # arg 0, usually "%s"
p (char *)$rdx    # arg 1, the first format string parameter / error message
```

