root="/home/vagrant/proj/test"
box_root="/var/local/lib/isolate/0/box"

sudo cp test.cpp $box_root/code.cpp

# this line is generate by judge.py
isolate \
--box-id=0 \
--silent \
--time=60.00 \
--wall-time=60.00 \
--fsize=65536 \
--processes=64 \
--dir=$root \
-e \
--meta=$root/compile_meta \
--stdout=compile_out \
--stderr-to-stdout \
--run \
-- \
/usr/bin/env g++ code.cpp -Icompile -Wall -Wshadow -Wno-unused-result -static -O2 -std=c++11 -o submit

sudo cp $box_root/compile_out ./compile_out