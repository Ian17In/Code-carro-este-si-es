def PID(IR:list,kp:int,ki:int,kd:int,avgSpeed:int):
    i= 0
    while True:
        e = IR[2] -IR[0]

        i += e 
        if e*i < 0:
            i=0
    
        etemp = e
        d = e - etemp
        u = kp*e + ki*i + kd*d

        driveFunc(avgSpeed+u,avgSpeed-u)

