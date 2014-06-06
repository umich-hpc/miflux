import sys
import os

from twisted.python import log

import esky


def do_update():
    log.msg( "do_update(): checking for updates" )
    if getattr( sys, "frozen", False ):
        app = esky.Esky( sys.executable, "https://miflux.lsa.umich.edu/mac/updates/")
        log.msg( "Running MiFlux version: %s" % app.active_version )
        try:
            update = app.find_update()
            if( update != None ):
                log.msg( "Update is available: %s" % update )
                app.auto_update()
                log.msg( "Update done" )
                appexe = esky.util.appexe_from_executable( sys.executable )
                os.execv( appexe,[appexe] + sys.argv[1:] )
            else:
                log.msg( "No update available" )
        except Exception, e:
            log.msg( "ERROR UPDATING APP:", e )
        app.cleanup()
    else:
        log.msg( "Not updatable: running version is not frozen" )

