#!/bin/bash
rm -rf deps
mkdir deps
pushd .
cd deps
hg clone http://hg.et.redhat.com/virt/applications/virtinst--devel
popd


