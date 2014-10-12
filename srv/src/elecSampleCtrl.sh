#! /usr/bin/env sh
MAIN_MODULE=eletrSampleServer
MODULE_PATH=/app/srv/src
LOG_PATH=/app/srv/log
PID_PATH=/app/srv/pid

case $1 in
    start)
        /usr/local/bin/twistd --python=${MODULE_PATH}/${MAIN_MODULE}.py --logfile=${LOG_PATH}/${MAIN_MODULE}.log --pidfile=${PID_PATH}/${MAIN_MODULE}.pid --rundir=${MODULE_PATH}
        ;;
    stop)
        kill `cat ${PID_PATH}/${MAIN_MODULE}.pid`
        ;;
    restart)
        kill `cat ${PID_PATH}/${MAIN_MODULE}.pid`
        sleep 1
        /usr/local/bin/twistd --python=${MODULE_PATH}/${MAIN_MODULE}.py --logfile=${LOG_PATH}/${MAIN_MODULE}.log --pidfile=${PID_PATH}/${MAIN_MODULE}.pid --rundir=${MODULE_PATH}
        ;;
    log)
        tail -f ${LOG_PATH}/${MAIN_MODULE}.log
        ;;
    *)
        echo "Usage: ./elecSampleCtrl.sh start | stop | restart | log"
        ;;
esac
