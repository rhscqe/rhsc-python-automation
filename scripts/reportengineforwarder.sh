    MBE_USER='root'

# Directory holding the mythbackend binary (empty means autodetect)
    MBE_DIR=''

# Name of mythbackend binary
    MBE_PROG='mythbackend'

# Startup options for mythbackend
    MBE_OPTIONS=''

# Directory holding the mythbackend log file
    LOG_DIR='/var/log/mythtv'

# Name of mythbackend log file
    LOG_FILE='mythbackend.log'

# Logging options for mythbackend (empty means '-v important,general')
    LOG_OPTS=''

PID_FILE="lock.pid"
NAME="engine"


# Start the process
#
    start() {
    # Already running?
        if [ -f "$PID_FILE" ]; then
            echo "is already running."
            return 0
        fi
 
   # Start
        echo -n "Starting $NAME: "
        java -jar reportengine_plugin/reportengineforwarder.jar&
        echo "$!" > $PID_FILE
        return 0 
    }

#
# Stop the process
#
    stop() {
        echo -n "Stopping $MBE_PROG: "
        killproc "$MBE_PROG"
        RETVAL=$?
        [ $RETVAL -eq 0 ] &&  rm -f $PID_FILE 
        echo
        return $RETVAL
    }


#
# Restart
#
    restart() {
        stop
        start
    }

###############################################################################

case "$1" in
start)
  start
  ;;
stop)
  stop
  ;;
restart)
  restart
  ;;
condrestart)
  if [ -f "/var/lock/subsys/$MBE_PROG" ]; then
      restart
  fi
  ;;
status)
  status "$MBE_BIN"
        RETVAL=$?
  ;;
*)
  echo "Usage: $0 {start|stop|restart|condrestart|status}"
  exit 1
esac

exit $RETVAL
