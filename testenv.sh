rm -rf env

mkdir env
mkdir env/X
echo "A" > env/X/a
echo "B" > env/X/b
echo "A" > env/X/z
mkdir env/Y1
echo "A" > env/Y1/a
echo ""  > env/Y1/c\;.tmp
mkdir env/Y2
echo ""  > env/Y2/b
echo ""  > env/Y2/d
