VERSION="0.1.1"
SRC_PATH=$(cd `dirname $0`;cd ../src;pwd) #current shell path
sdd(){
  if [ $# -lt 1 ];then
    sdd help
    return
  fi
  case $1 in
    "help")
      echo
      echo "Android Tools Manager"
      echo
      echo "Usage:"
      echo "  sdd help                              Show this message"
      echo "  sdd --version                         Print out the latest released version of sdd"
      echo "  sdd i <apk-file-path>                 Show app infos"
      echo "  sdd i p <apk-file-path>               Show  app packageName"
    ;;
    "--version")
      echo $VERSION
    ;;
    "i")
      if [ "p" = $2 ]
      then
        $SRC_PATH/i_p.py $3
      else
        $SRC_PATH/i.py $2
      fi
    ;;
  esac
}
