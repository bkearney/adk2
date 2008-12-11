#!/bin/bash
rm -rf deps
mkdir deps
pushd .
cd deps
git clone git://git.et.redhat.com/act
hg clone http://hg.et.redhat.com/virt/applications/virtinst--devel
popd


