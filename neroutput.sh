#! /bin/bash
echo $1 | 
curl -F 'input=<-' "http://opener.olery.com/language-identifier" | \
#curl -F 'input=<-' "http://opener.olery.com/ner"| \
curl -F 'input=<-' "http://opener.olery.com/kaf2json"
#end of file


