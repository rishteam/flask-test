root="/home/vagrant/proj/test"
box_root="/var/local/lib/isolate/0/box"

# Compiling
./compile.sh

sudo cp in $box_root

isolate \
--box-id=0 \
--silent \
--time=3.00 \
--wall-time=5.00 \
--fsize=65536 \
--processes=64 \
--dir=$root \
-e \
--meta=$root/run_meta \
--stdin=in \
--stderr-to-stdout \
--stdout=out \
--run \
-- \
submit

sudo cp $box_root/out ./run_out

# check ans
./checkans.sh

# --cg \