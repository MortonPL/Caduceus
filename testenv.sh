rm -rf env

mkdir env
mkdir env/X
mkdir env/Y1
mkdir env/Y2

echo -n "A" > env/X/a     && touch env/X/a      -m -t 199509260000.01
echo -n "B" > env/X/b     && touch env/X/b      -m -t 199509260000.02
echo -n "A" > env/X/z     && touch env/X/z      -m -t 199509260000.03

echo -n "A" > env/Y1/a    && touch env/Y1/a     -m -t 199509260000.04
echo -n "C" > env/Y1/c\;  && touch env/Y1/c\;   -m -t 199509260000.05
echo -n ""  > env/Y1/.tmp && touch env/Y1/.tmp  -m -t 199509260000.06

echo -n "aa" > env/Y2/a   && touch env/Y2/a     -m -t 199509260000.00
echo -n ""  > env/Y2/b    && touch env/Y2/b     -m -t 199509260000.07
echo -n "D" > env/Y2/d    && touch env/Y2/d     -m -t 199509260000.08
