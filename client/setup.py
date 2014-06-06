
from esky import bdist_esky
from distutils.core import setup


DATA_FILES = []

PY2APP_OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'assets/miflux-icon/miflux-icon-1024.icns',
    'includes': [ 'esky', 'sip', 'PyQt5', 'twisted' ],
    'qt_plugins': [ 'platforms/*', 'imageformats/*' ],
    'excludes': [ 'PyQt5.QtWebKit', 'PyQt5.QtWebKitWidgets',
        'PyQt5.QtDesigner', 'PyQt5.QtXmlPatterns', 'PyQt5.QtQml',
        'PyQt5.QtQuick', 'PyQt5.QtDeclarative' ],
    'dylib_excludes': [ 'QtWebKit.framework', 'QtWebKitWidgets.framework',
        'QtDesigner.framework', 'QtXmlPatterns.framework', 'QtQml.framework',
        'QtQuick.framework', 'QtDeclarative' ]
    }

ESKY_OPTIONS = {
    "freezer_module": "py2app",
    "freezer_options": PY2APP_OPTIONS,
    }

MiFlux = bdist_esky.Executable( "MiFlux.py", gui_only=True )

setup(
    name='MiFlux',
    version = "2014060605",
    data_files=DATA_FILES,
    options = { "bdist_esky": ESKY_OPTIONS },
    packages=[ 'miflux', 'miflux.util' ],
    scripts=[ MiFlux ],
)

