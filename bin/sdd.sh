VERSION="0.1.1"
SRC_PATH=$(cd `dirname $0`;cd ../src;pwd) #current shell path
TMP_PATH=$(cd `dirname $0`;cd ../tmp;pwd) #current shell path
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
      echo "  sdd i myapp <packaname>               Show app info in myapp"
      echo "  sdd i myapp d <packaname>             Show app download url in myapp"
      echo "  sdd v sign <apk-file-path>            Show  app signature"
      echo "  sdd b install <apk-file-parent-path>  Batch install apk"
      echo "  sdd b uninstall <packges-file-path>   Batch uninstall apk"
      echo "  sdd sync-myapp b <packges-file-path> <output-dir> Download apks from myapp"
    ;;
    "--version")
      echo $VERSION
    ;;
    "i")
      if [ "p" = $2 ]
      then
        $SRC_PATH/i_p.py $3
      elif [ "myapp" = $2 ]
      then
        if [ "d" = $3 ]
        then
          $SRC_PATH/myapp.py download $4
        else
          $SRC_PATH/myapp.py $3
        fi
      else
        $SRC_PATH/i.py $2
      fi
    ;;
    "v")
      if [ "sign" = $2 ]
      then
        sudo rm -r $TMP_PATH/apk_files/* >> /dev/null 2>&1 #delete unused files
        unzip $3 -d $TMP_PATH/apk_files/ >> /dev/null 2>&1 #unzip apk files to specified directory
        for rsa in $TMP_PATH/apk_files/META-INF/*.RSA
        do
          keytool -printcert -file $rsa
        done
        sudo rm -r $TMP_PATH/apk_files/* >> /dev/null 2>&1 #delete unused files
      else
        echo 'none'
      fi
    ;;
    "b")
      if [ "install" = $2 ]
      then
        for apk in $3/*.apk
        do
          adb install $apk
        done
      else
        for package in `cat $3`
        do
          adb uninstall $package
        done
      fi
    ;;
    "sync-myapp")
      if [ "b" == $2 ]
      then
        for package in `cat $3`
        do
          wget `$SRC_PATH/myapp.py download $package` -O $4/$package.apk
        done
      else
      fi
    ;;
  esac
}
