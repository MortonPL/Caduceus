rm -rf env

mkdir env
mkdir env/X
echo -n "A" > env/X/a
echo -n "B" > env/X/b
echo -n "A" > env/X/z
mkdir env/Y1
echo -n "A" > env/Y1/a
echo -n "C" > env/Y1/c\;
echo -n ""  > env/Y1/.tmp
mkdir env/Y2
echo -n ""  > env/Y2/b
echo -n "D" > env/Y2/d
