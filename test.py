import time
file = 'hdt_log1.txt'
file1 = 'hdt_log.txt'
ffile = 'power1.log'
ffile1 = 'power.log'
f= open(file,encoding="utf8")
f1= open(file1,"w",encoding="utf8")
ff= open(ffile,encoding="utf8")
ff1= open(ffile1,"w",encoding="utf8")
done = False
time0 = None
t2 = 0
s = ""
ss = ""
while True:
    ss1 = ff.readline()
    if ss1 == "":  #end
        print("end")
        print(ss)
        ff1.write(ss)
        break
    if not time0:
        time0 = ss1[2:10]
        print(time0)
        # print(time.strptime(time0,"%H:%M:%S"))
        # t0=time.mktime(time.strptime(time0,"%H:%M:%S"))
        t0 = int(time0.split(":")[0])*3600+int(time0.split(":")[1])*60+int(time0.split(":")[2])
        print(t0)
    time1 = ss1[2:10]
    if time1 == time0:
        ss += ss1
    else:
        # print(ss)
        ff1.write(ss)
        ss = ss1
        time0 = ss1[2:10]
        print(time0)
        # t0=time.mktime(time.strptime(time0,"%H:%M:%S"))
        t0 = int(time0.split(":")[0])*3600+int(time0.split(":")[1])*60+int(time0.split(":")[2])
        print(t0)
        time.sleep(1)
        
        
    if t2 > t0:
        # print(s)
        if s != "":
            f1.write(s)
            s = ""
        continue
        
    s1 = f.readline()
    if s1 == "":  #end
        print("end")
        print(s)
        f1.write(s)
        break
    # if not time0:
        # time0 = s1[:7]
    time3 = s1[:8]
    print(time3)
    # t3=time.mktime(time.strptime(time3,"%H:%M:%S"))
    if time3.find(":") > -1:
        t3 = int(time3.split(":")[0])*3600+int(time3.split(":")[1])*60+int(time3.split(":")[2])
    else:
        t3 = t2
    print(t3)
    if t3 <= t2:
        s += s1
    else:
        f1.write(s)
        s = s1
        t2 = t3
    '''
    if time2 == time0:
        s += s1
    else:
        # print(s)
        f1.write(s)
        s = s1
        # time0 = s1[:7]
        # time.sleep(0.5)
    '''

        
'''    
    for i in range(200):
        s1 = f.readline()
        if s1 == "":
            done = True
            break
        s += s1
        
    f1.write(s)
    if done:
        break
        
    ss = ""
    for i in range(200):
        ss1 = ff.readline()
        if ss1 == "":
            done = True
            break
        ss += ss1
        
    ff1.write(ss)
    if done:
        break
'''

    
f.close()
f1.close()
ff.close()
ff1.close()