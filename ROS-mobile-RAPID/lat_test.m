old_phone = [32
47
5
56
52
5
54
50
31
16
7
48
50
6
19
12
16
25
50
12
76
58
49
59
6
25
6
51
50
13
51
50
18
48
48
5
45
50
49
5
50
13
51
47
49
47
5
50
48
61];

old_phone_2_nodes = [13
24
48
50
5
49
15
6
51
50
7
5
49
29
50
50
6
10
50
52
49
53
42
39
8
28
7
45
49
9
97
32
48
51
50
37
6
53
7
9
15
29
8
48
37
64
46
13
41
52];

new_phone = [7
6
5
5
6
8
4
5
5
5
5
4
5
4
5
6
6
7
6
6
7
6
9
5
6
6
7
7
6
8
6
6
5
6
5
6
7
6
6
6
22
6
22
6
22
8
6
5
15
4];

x = 1:50;
sz = 15;
scatter(x,old_phone, sz, "filled")
hold on
scatter(x,new_phone, sz, "filled")
%scatter(x,old_phone_2_nodes, sz, "filled")
%legend({'old phone', 'new phone', 'old phone with 2 nodes'})
legend({'old phone', 'new phone'})
title('Plot of latency between the phone and Raspberry Pi')
xlabel('Iteration') 
ylabel('Latency [ms]') 
grid
yline(mean(new_phone))
yline(mean(old_phone))
hold off

mean(old_phone)
mean(old_phone_2_nodes)
mean(new_phone)