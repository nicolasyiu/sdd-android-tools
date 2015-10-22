# sdd-android-tools

## install
```shell
git clone https://github.com/mumaoxi/sdd-android-tools
source sdd-android-tools/bin/sdd.sh
```

## usage

查看apk基本信息
```shell
$ sdd i $apkfilepath
$ versionCode	24370000
  packageName	com.tencent.mm
  icLauncher	res/drawable-hdpi/app_icon.png
  versionName	2.437
  appName	微信
```

只查看包名
```shell
$ sdd i p $apkfilepath
$ com.tencent.mm,apkpath.apk
```

查看签名信息
```shell
$ sdd v sign $apkfilepath
Owner: CN=Tencent, OU=Tencent Guangzhou Research and Development Center, O=Tencent Technology(Shenzhen) Company Limited, L=Shenzhen, ST=Guangdong, C=86
Issuer: CN=Tencent, OU=Tencent Guangzhou Research and Development Center, O=Tencent Technology(Shenzhen) Company Limited, L=Shenzhen, ST=Guangdong, C=86
Serial number: 4d36f7a4
Valid from: Wed Jan 19 22:39:32 CST 2011 until: Fri Jan 11 22:39:32 CST 2041
Certificate fingerprints:
	 MD5:  18:C8:67:F0:71:7A:A6:7B:2A:B7:34:75:05:BA:07:ED
	 SHA1: CC:80:D7:6A:A9:FE:94:EC:20:5E:F0:C3:36:BF:C4:24:59:6D:A2:90
	 SHA256: 0F:E4:FF:85:C2:15:91:83:96:DA:DC:7C:D8:CE:69:63:33:9A:F3:3D:37:75:1A:56:E5:4C:72:06:B6:3A:3C:7C
	 Signature algorithm name: SHA1withRSA
	 Version: 3
```
