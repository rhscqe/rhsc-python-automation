#!/usr/bin -e

function rpm_to_virtualenv() {
  project="$PWD/"
  RPM_URL=$1
  TMP=/tmp/extract
  rm -rf $TMP 
  mkdir -p $TMP 
  cd $TMP

  wget $RPM_URL >/dev/null
  rpm2cpio *.rpm | cpio -idmv 2> /dev/null >/dev/null

  PROJECT_SITE_PACKAGES=`find $project -name site-packages | head -n 1`
  RPM_SITE_PACKAGES=`find $TMP -name site-packages`
  if [ -z "$PROJECT_SITE_PACKAGES" ] 
  then
    echo project has not site-packages
    break
  fi

  if [ -z "$RPM_SITE_PACKAGES" ] 
  then
    echo rpm has no site-packages
    break
  fi

  echo "--------------Copying------------------"
  echo "cp -v -r $RPM_SITE_PACKAGES/* $PROJECT_SITE_PACKAGES"
  cp -v -r $RPM_SITE_PACKAGES/* $PROJECT_SITE_PACKAGES 
}


rpms=("http://bob.eng.lab.tlv.redhat.com/builds/sf9/rhevm-sdk-3.2.0.2-1.el6ev.noarch.rpm")
for i in "${rpms[@]}"
do
  rpm_to_virtualenv $i  
done


