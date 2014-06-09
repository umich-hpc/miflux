import sys
import os

from twisted.internet import threads
from twisted.python import log

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QProgressDialog
from PyQt5.QtWidgets import QApplication

import esky


class Update( object ):

    def __init__( self, window ):
        self.window = window
        self.app = None
        self.version = "development"
        self.update_version = None
        if not getattr( sys, "frozen", False ):
            log.msg( "MiFlux version: development (not frozen, not updatable)" )
            return
        self.app = esky.Esky( sys.executable, "https://miflux.lsa.umich.edu/mac/updates/")
        self.version = self.app.active_version
        log.msg( "MiFlux version: %s" % self.version )

    def __del__( self ):
        if self.app:
            self.app.cleanup()

    def _update_completed( self, update_version ):
        log.msg( "Update._update_completed()" )
        self._updateProgressDialog.close()
        appexe = esky.util.appexe_from_executable( sys.executable )
        os.execv( appexe, [appexe] + sys.argv[1:] )

    def _update_completedErr( self, failure ):
        log.msg( "Update._update_completedErr(): auto_update() failed: %s", failure )

    def _do_update_status( self, status ):
        # called by esky's auto_update() as progress is made
        log.msg( "auto_update() status changed: %s" % str( status ) )
        newLabelText = status.get( 'status', 'Updating...' )
        if newLabelText != self._updateProgressLabelText:
            self._updateProgressDialog.setLabelText( newLabelText )
            self._updateProgressLabelText = newLabelText
            if newLabelText == 'downloading':
                size = status.get( 'size', 100 )
                # +1 because there are steps after the downloading has finished
                self._updateProgressDialog.setMaximum( size + 1 )
        if newLabelText == 'downloading':
            received = status.get( 'received', 0 )
            self._updateProgressDialog.setValue( received )

    def _do_update( self ):
        # runs in a separate thread
        return self.app.auto_update( self._do_update_status )

    def _updateNowDialog_completed( self, result ):
        if result == QMessageBox.No:
            log.msg( "Update._updateNowDialog_completed: user chose not to update now" )
            return
        # We are not currently providing an option to cancel the update
        # because the current version of esky does not provide a way to
        # abort the download.  And attempts to quit the application cause
        # it to hang, presumably because the download thread is still running.
        # TODO: Look into having Esky abort the update if the callback
        # function signals it do so.
        self._updateProgressDialog = QProgressDialog(
            "Updating...", None, 0, 100, parent=self.window
            )
        self._updateProgressDialog.setWindowModality( Qt.WindowModal )
        self._updateProgressDialog.setWindowTitle( "Updating" )
        self._updateProgressDialog.setAutoClose( False )
        self._updateProgressDialog.setAutoReset( False )
        self._updateProgressDialog.setMinimumDuration( 0 )
        self._updateProgressDialog.setValue( 0 )
        self._updateProgressDialog.show()
        self._updateProgressLabelText = "Updating..."
        self._updateDeferred = threads.deferToThread( self._do_update )
        self._updateDeferred.addCallbacks( self._update_completed, self._update_completedErr )

    def _check_completed( self, update_version ):
        self.update_version = update_version
        if update_version == None:
            log.msg( "Update._check_completed(): no update available" )
            return
        log.msg( "Update is available: %s" % self.update_version )
        updateNowDialog = QMessageBox( QMessageBox.Question,
            "Update now?",
            "A new version of MiFlux is available, do you want to install it now?\n\nCurrently installed: %s\n\nNew version: %s" % ( self.version, self.update_version ),
            buttons=QMessageBox.Yes | QMessageBox.No,
            parent=self.window )
        updateNowDialog.setDefaultButton( QMessageBox.Yes )
        updateNowDialog.finished.connect( self._updateNowDialog_completed )
        updateNowDialog.open()
        return update_version

    def _check_completedErr( self, failure ):
        log.msg( "Update._check_completedErr: checking for updates failed: %s", failure )

    def _do_check( self ):
        # runs in a separate thread
        return self.app.find_update()

    def check( self ):
        log.msg( "Checking for updates" )
        if not self.app:
            log.msg( "Update.check(): error: app not set" )
            return
        self._checkDeferred = threads.deferToThread( self._do_check )
        self._checkDeferred.addCallbacks( self._check_completed, self._check_completedErr )

