old_phone = [90
166
80
155
73
182
233
216
224
252
242
117
228
264
229
149
183
159
211
140
137
152
183
133
105
180
181
251
254
79
152
81
225
134
131
91
132
148
224
198
374
317
297
110
263
225
735
76
91
73];

old_phone_5g = [16
6
14
20
6
7
11
10
19
16
4
13
32
14
10
10
12
7
8
9
13
15
11
14
17
12
14
10
5
9
15
22
11
16
17
14
5
12
9
5
5
8
11
5
17
10
11
14
13
6];

new_phone_5g = [9
5
4
7
11
8
9
6
5
9
4
9
6
13
6
16
4
6
10
3
10
5
5
6
4
42
13
74
22
10
7
8
7
5
14
8
8 
8
11
13
4 
8
8
14
15
3
2
5
5
13];

new_phone = [60
32
103
128
136
44
63
182
144
63
102
141
40
36
41
45
24
39
71
36
70
19
27
9
48
39
39
132
54
52
16
24
16
40
37
54
55
33
62
132
21
50
49
118
164
120
536
278
240
240];

x = 1:50;
sz = 15;
scatter(x,old_phone, sz, "filled", "blue")
hold on
scatter(x,old_phone_5g, sz, "filled", "green")
scatter(x,new_phone, sz, "filled", "red")
scatter(x,new_phone_5g, sz, "filled", "magenta")
plot(x,old_phone, "blue")
plot(x,old_phone_5g, "green")
plot(x,new_phone, "red")
plot(x,new_phone_5g, "magenta")
legend({'old phone', 'old phone 5g', 'new phone', 'new phone 5g'})
title('Plot of latency between the phone and Raspberry Pi')

xlabel('Iteration') 
ylabel('Latency [ms]') 
grid
hold off

old_phone_mean = mean(old_phone)
old_phone_5g_mean = mean(old_phone_5g)
new_phone_mean = mean(new_phone)
new_phone_5g_mean = mean(new_phone_5g)