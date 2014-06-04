#!/usr/bin/env python

from __future__ import print_function
import sys
import os
import re
import getpass
import json

from os.path import expanduser
userHomeDir = expanduser( "~" )

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

from miflux.ui_MainWindow import Ui_MainWindow

if __name__ == '__main__':
    app = QApplication( sys.argv )
    import miflux.qt5reactor
    miflux.qt5reactor.install()

from twisted.internet import reactor
from twisted.internet.defer import Deferred, setDebugging
from twisted.python import log

from miflux.ssh import *

fluxSession = None
fluxAccounts = None


def connectToFlux_useroutput( data ):
    global fluxSession
    log.msg( "connectToFlux_useroutput() called" )
    log.msg( "data=>>>%s<<<" %data )
    if not data:
        log.msg( "connectToFlux_useroutput(): no data " )
        return
    # TODO: write to PyQt5.QtCore.QStandardPaths CacheLocation
    data = data.strip()
    user, accounts = data.split(':')
    if not accounts:
        log.msg( "connectToFlux_useroutput(): no accounts " )
        return
    account_list = accounts.split(',')
    if not account_list:
        log.msg( "connectToFlux_useroutput(): could not split account list" )
        return
    log.msg( "connectToFlux_useroutput(): %s " % ', '.join( account_list ) )
    for account in account_list:
        fluxSession.window.ui.accountDropdown.addItem( account )
    

def connectToFlux_accountoutput( data ):
    global fluxSession, fluxAccounts
    log.msg( "connectToFlux_accountoutput() called" )
    #log.msg( "data=>>>%s<<<" %data )
    if not data:
        log.msg( "connectToFlux_accountoutput(): no data " )
        return
    # TODO: write to PyQt5.QtCore.QStandardPaths CacheLocation
    fluxAccounts = json.loads( data )

def connectToFlux_done( fluxSession ):
    global miFluxServerPath
    log.msg( "connectToFlux_done() called" )
    ####
    d = Deferred()
    d.addCallback( connectToFlux_useroutput )
    # TODO: put full path to grep (/bin/grep on Flux, /usr/bin/grep for MacOS X)
    command = "grep '^" + fluxSession.username + ":' " + miFluxServerPath + "/data/user_accounts"
    fluxSession.runCommand( command, d )
    ####
    d = Deferred()
    d.addCallback( connectToFlux_accountoutput )
    # TODO: put full path to grep (/bin/grep on Flux, /usr/bin/grep for MacOS X)
    command = "cat " + miFluxServerPath + "/data/flux_accounts"
    fluxSession.runCommand( command, d )


def connectToFlux( window, username ):
    global miFluxServerHost
    log.msg( "connectToFlux() called, username = %s" % username )
    if ( not username or not re.search( r'^[a-z]{3,8}$', username ) ):
        log.msg( "connectToFlux(): bad username" )
        return
    d = Deferred()
    d.addCallback( connectToFlux_done )
    fluxSession = ClientCommandFactory( window, username, d )
    window.reactor.connectTCP( miFluxServerHost, 22, fluxSession )
    return fluxSession


class MainWindow( QMainWindow ):
    def __init__( self, reactor, parent = None ):
        super( MainWindow, self ).__init__( parent )
        self.reactor = reactor
        self.ui = Ui_MainWindow()
        self.ui.setupUi( self )
        self.ui.connectButton.setText( "Connect" )
        username = getpass.getuser()
        if ( username and re.search( r'^[a-z]{3,8}$', username ) ):
            self.ui.uniqname.insert( str(username) )
            self.ui.uniqname.setSelection( 0, len(username) )

    @pyqtSlot()
    def on_uniqname_textChanged( uniqname ):
        log.msg( "uniqname set: %s" % uniqname )
        # TODO: enable or disable the Connect button based on username validity
        if ( uniqname and re.search( r'^[a-z]{3,8}$', str( uniqname ) ) ):
            log.msg( "uniqname is OK" )
        else:
            log.msg( "uniqname is not a uniqname" )

    @pyqtSlot()
    def on_connectButton_clicked( self ):
        global fluxSession
        if not fluxSession:
            uniqname = str( self.ui.uniqname.text() )
            fluxSession = connectToFlux( self, uniqname )
        else:
            fluxSession.disconnect()
            fluxSession = None

    @pyqtSlot( 'QString' )
    def on_accountDropdown_currentIndexChanged( self, account ):
        global fluxSession, fluxAccounts
        log.msg( "account set: %s" % account )
        if account not in fluxAccounts:
            log.msg( "account information not found for %s" % account )
            return
        maxproc = fluxAccounts[account]['maxproc']
        maxmem = fluxAccounts[account]['maxmem'] / 1024 / 1024
        log.msg( "resources: %d cores, %d GB" % (maxproc, maxmem) )
        self.ui.resourcesValueLabel.setText( str( "%d cores, %d GB RAM" % ( maxproc, maxmem ) ) )

    @pyqtSlot()
    def on_aButton_clicked( self ):
        global fluxSession
        log.msg( "Button A clicked" )
        if not fluxSession:
            log.msg( "  not connected" )
            return
        fluxSession.runCommand( "/bin/ls -la" )

    @pyqtSlot()
    def on_bButton_clicked( self ):
        global fluxSession
        log.msg( "Button B clicked" )
        if not fluxSession:
            log.msg( "  not connected" )
            return
        fluxSession.runCommand( "/sbin/ifconfig en0" )

    def closeEvent(self, e):
        if self.reactor.getThreadPool():
            self.reactor.threadpool.stop()  # TODO: add this to qt5reactor code
        self.reactor.stop()


if __name__ == '__main__':

    if True:
      # The Real Deal:
      miFluxServerHost = "flux-login.engin.umich.edu"
      miFluxServerPath = "/home/software/rhel6/lsa/miflux"
    else:
      # Local testing environment -- saves us from having to use two-factor auth:
      miFluxServerHost = "localhost"
      miFluxServerPath = userHomeDir + "/miflux-localserver"

    if sys.stdout.isatty():
        log.startLogging( sys.stderr, setStdout=False )
    else:
        try: 
            # TODO: use PyQt5.QtCore.QStandardPaths with DataLocation
            os.mkdir( userHomeDir + "/.miflux", 0700 )
        except OSError:
            if not os.path.isdir( userHomeDir + "/.miflux" ):
                raise
        log.startLogging( open( userHomeDir + "/.miflux/miflux.log", 'w' ), setStdout=False )
    setDebugging( True )

    fluxui = MainWindow( reactor )
    fluxui.show()
    reactor.run()
    sys.exit( 0 )
  
