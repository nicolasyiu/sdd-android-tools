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
    ;;
    "--version")
      echo $VERSION
    ;;
    "i")
      $SRC_PATH/apkinfo.py $2
    ;;
  esac
}
