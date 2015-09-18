VERSION="0.1.1"
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
      echo "  sdd apkinfo <apk-file-path>           Show app infos"
    ;;
    "--version")
      echo $VERSION
    ;;
    "apkinfo")
      echo `/Users/saxer/Develope/GitHub/saxer-android-tools/src/apkinfo.py $1`
    ;;
  esac
}
