#!/bin/bash

echo "0%..."
git clone ssh://$1@review.fuel-infra.org:29418/openstack/$2 # &> /dev/null
echo "15%..."
pushd $2 &> /dev/null
echo "30%..."
git remote add upstream https://github.com/$3/$2.git &> /dev/null
echo "45%..."
git remote update &> /dev/null
echo "60%..."
git diff --stat $4 origin/openstack-ci/fuel-6.1/2014.2 > ../tmpfile
echo "75%..."
popd &> /dev/null
echo "90%..."
rm -rf $2
echo "Done!"