#!/bin/bash
rm -rf deps
mkdir deps
pushd .
cd deps
git clone git://git.et.redhat.com/ace
git clone git://git.et.redhat.com/act
git clone git://git.fedorahosted.org/hosted/livecd
hg clone http://hg.et.redhat.com/virt/applications/virtinst--devel
popd


