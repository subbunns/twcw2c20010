#! /bin/bash
echo $1|curl -F 'input=<-' "http://opener.olery.com/kaf2json"
#end of file
