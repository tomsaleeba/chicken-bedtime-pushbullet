#!/bin/bash
# BROKEN! This almost works. It gets something you can upload but the
# ephem._libastro module doesn't load in Lambda
set euo -pipefail
cd `dirname "$0"`

tmpdir=`mktemp -d`
target=$tmpdir/project
mkdir $target
cp \
  lambda_function.py \
  requirements.txt \
  $target

pushd $target
pip install -r requirements.txt -t ./
chmod -R 755 .
output=../chicken-dist.zip
zip -r $output .

echo "[INFO] done. Output is:"
echo "[INFO]   $target/$output"
