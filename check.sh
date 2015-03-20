#!/bin/bash

git clone ssh://$1@review.fuel-infra.org:29418/openstack/$2
cd $2
git remote add upstream https://github.com/openstack/$2.git
git remote update
git diff --stat upstream/stable/juno origin/openstack-ci/fuel-6.1/2014.2
cd ..
rm -rf $2