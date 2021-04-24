#!/bin/bash

# input
rm -f a.out *.JPG down_temp
src=$1;

echo $1
echo $2

if [[ "$src" =~ ".cpp" ]];
then
	g++ $src
	./a.out $2 > output.txt &
elif [[ $src =~ ".c" ]];
then
	gcc $src 
	./a.out $2 > output.txt &
elif [[ $src =~ ".py" ]];
then
	python3 $src $2 > output.txt &
else
	echo "not supported" $src
fi

sleep 1

wget -O down_temp_biga -t 2 -T 10 http://localhost:$2/biga.html
sleep 1
wget -O down_temp_a -t 2 -T 10 http://localhost:$2/a.html
sleep 1
wget -O down_temp_b -t 2 -T 10 http://localhost:$2/b.html

killall -q a.out python3

succcnt=0
diff biga.html down_temp_biga
if [[ $? == 0 ]];
then
	let 'succcnt=succcnt+1'
fi
diff a.html down_temp_a
if [[ $? == 0 ]];
then
	let 'succcnt=succcnt+2'
fi
diff b.html down_temp_b
if [[ $? == 0 ]];
then
	let 'succcnt=succcnt+4'
fi

# show the result
echo "Result: " $succcnt $src


