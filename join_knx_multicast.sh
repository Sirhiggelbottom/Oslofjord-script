#!/bin/bash
sudo socat UDP4-RECVFROM:3671,ip-add-membership=224.0.23.12:eth0,fork -
