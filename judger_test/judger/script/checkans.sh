root="/home/vagrant/proj/test"
box_root="/var/local/lib/isolate/0/box"

sudo cp compile/checkans $box_root/checkans
sudo cp ans $box_root/ans

# this line is generate by judge.py
isolate \
--box-id=0 \
--silent \
--time=60.00 \
--wall-time=60.00 \
--processes=64 \
-e \
--meta=$root/checkans_meta \
--stdin=/dev/null \
--stdout=/dev/null \
--stderr=/dev/null \
--run \
-- \
./checkans in out ans

isolate --box-id=0 -e --run /usr/bin/env ls