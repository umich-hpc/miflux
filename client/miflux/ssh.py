
from __future__ import print_function
import sys
import struct

from twisted.conch.ssh import transport, connection, userauth, channel, common
from twisted.internet import defer, protocol
from twisted.python import log

from PyQt5.QtWidgets import QInputDialog, QLineEdit


class ClientCommandTransport( transport.SSHClientTransport ):
    _secured = False

    def __init__( self, factory ):
        log.msg( "ClientCommandTransport()" )
        self.factory = factory
        self.clientConnection = None

    def verifyHostKey( self, pubKey, fingerprint ):
        log.msg( "ClientCommandTransport.verifyHostKey()" )
        # in a real app, you should verify that the fingerprint matches
        # the one you expected to get from this server
        return defer.succeed( True )

    def connectionSecure( self ):
        log.msg( "ClientCommandTransport.connectionSecure()" )
        self._secured = True
        self.clientConnection = ClientConnection( self.factory )
        self.requestService(
            PasswordAuth( self.factory.username, self.clientConnection ) )

    def runCommand( self, command, outputCallback=None ):
        log.msg( "ClientCommandTransport.runCommand( \"%s\" )" % command,
            file=sys.stderr )
        if not self.clientConnection or not self.clientConnection.connected:
            log.msg( "ClientCommandTransport.runCommand(): not connected" )
            return
        self.clientConnection.openChannel(
            CommandChannel( command, outputCallback, conn=self.clientConnection ) )

    # I don't think we have self.factory in our code yet, see example at
    # https://stackoverflow.com/questions/4617507/best-way-to-run-remote-commands-thru-ssh-in-twisted
    #def connectionLost(self, reason):
    #    if not self._secured:
    #        self.factory.commandConnected.errback(reason)



class PasswordAuth( userauth.SSHUserAuthClient ):
    def __init__( self, user, connection ):
        log.msg( "PasswordAuth()" )
        self.connection = connection
        userauth.SSHUserAuthClient.__init__( self, user, connection )

    def getPassword( self, prompt=None ):
        log.msg( "PasswordAuth.getPassword()" )
        secret, ok = QInputDialog.getText( self.connection.factory.window,
            'Log In to Flux', 'Password:', echo=QLineEdit.Password )
        if ok:
            return defer.succeed( secret )
        else:
            return defer.fail()

    def getGenericAnswers( self, name, instruction, questions ):
        log.msg( "PasswordAuth.getGenericAnswers()" )
        log.msg( "  name = %s" % name )
        log.msg( "  instruction = %s" % instruction )
        answers = []
        for prompt, echo in questions:
            log.msg( "  prompt = %s, echo = %s" % (prompt, echo) )
            echoMode = QLineEdit.Normal if echo else QLineEdit.Password
            secret, ok = QInputDialog.getText( self.connection.factory.window,
                'Log In to Flux', prompt, echo=echoMode )
            if ok:
                answers.append( secret )
            else:
                return defer.fail()
        return defer.succeed( answers )


class ClientConnection( connection.SSHConnection ):
    def __init__( self, factory, *args, **kwargs ):
        log.msg( "ClientConnection()" )
        self.factory = factory
        self.connected = False
        connection.SSHConnection.__init__( self )

    def serviceStarted( self ):
        log.msg( "ClientConnection.serviceStarted()" )
        self.connected = True
        self.factory.window.ui.connectButton.setText( "Disconnect" )
        if self.factory.connectedCallback:
            self.factory.connectedCallback.callback( self.factory )

    def serviceStopped( self ):
        log.msg( "ClientConnection.serviceStopped()" )
        self.connected = False
        self.factory.window.ui.connectButton.setText( "Connect" )


class CommandChannel( channel.SSHChannel ):
    name = 'session' # needed for commands

    def __init__( self, command, outputCallback=None, *args, **kwargs ):
        log.msg( "CommandChannel()" )
        channel.SSHChannel.__init__( self, *args, **kwargs )
        self.command = command
        self.outputCallback = outputCallback
        self.output = ''

    def channelOpen( self, data ):
        log.msg( "CommandChannel.channelOpen()" )
        self.conn.sendRequest(
            self, 'exec', common.NS( self.command ),
            wantReply=True ).addCallback( self._gotResponse )

    def openFailed( self, reason ):
        log.msg( 'CommandChannel.openFailed: command = %s, reason = %s' %
            ( self.command, reason ) )

    def _gotResponse( self, _ ):
        log.msg( "CommandChannel._gotResponse()" )
        self.conn.sendEOF( self )

    def dataReceived( self, data ):
        log.msg( "CommandChannel.dataReceived(): %s" % data)
        self.output += data

    def extReceived( self, data ):
        log.msg( "CommandChannel.extReceived(): %s" % data )

    def closed( self ):
        log.msg( "CommandChannel.closed()" )
        self.loseConnection()
        if self.outputCallback:
            self.outputCallback.callback( self.output )
        #reactor.stop()

    def request_exit_status( self, data ):
        status = struct.unpack( '>L', data )[0]
        log.msg( 'CommandChannel.request_exit_status(): status=%s' % status,
            file=sys.stderr )
        self.loseConnection()


class ClientCommandFactory( protocol.ClientFactory ):
    def __init__( self, window, username, connectedCallback=None ):
        log.msg( "ClientCommandFactory()" )
        self.window = window
        self.username = username
        self.connectedCallback = connectedCallback
        self.protocol = None

    def buildProtocol( self, addr ):
        log.msg( "ClientCommandFactory.buildProtocol()" )
        self.protocol = ClientCommandTransport( self )
        return self.protocol

    def runCommand( self, command, outputCallback=None ):
        self.protocol.runCommand( command, outputCallback )

    def disconnect( self ):
        self.protocol.sendDisconnect( transport.DISCONNECT_BY_APPLICATION,
            'user requested disconnect' )


# TODO: implement KeepAlive: https://gist.github.com/grugq/1436495

