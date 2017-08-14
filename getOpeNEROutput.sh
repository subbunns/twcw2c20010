#! /bin/bash
echo $1 |curl -F 'input=<-' "http://opener.olery.com/language-identifier" | \
curl -F 'input=<-' "http://opener.olery.com/tokenizer" | \
curl -F 'input=<-' "http://opener.olery.com/pos-tagger" | \
curl -F 'input=<-' "http://opener.olery.com/constituent-parser" | \
curl -F 'input=<-' "http://opener.olery.com/ner"| \
curl -F 'input=<-' "http://opener.olery.com/kaf2json"
#end of file

