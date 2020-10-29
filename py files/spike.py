import os
import subprocess

pos_file="/home/localuser/Desktop/position.txt"
pin_file="/home/localuser/Desktop/pin_info.txt"

f=open(pos_file,"r")
line_pos=f.readlines()
position_lines=len(line_pos)
print position_lines
f.close()

g=open(pin_file,"r")
line_pin=g.readlines()
pin_lines=len(line_pin)
print len(line_pin)
g.close()

re_dir="/home/localuser/Desktop"
scope_mod="m5"
scope_cnt="GPIB"
scope_ip="192.168.0.100"
scope_port="gpib0,26"
scope_channel="1"

with open(pos_file) as a:
    pos=a.readlines()[0]
    position=pos.split()
    print position[0],position[1],position[2]
    a.close()

with open(pin_file) as b:
    pin=b.readlines()[0]
    pin_info=pin.split()
    print pin_info[0],pin_info[1],pin_info[2]
    b.close()

p=pin_info[0]
th=pin_info[2]
tl=pin_info[1]
rmax=float(th)*1.2
rmin=float(tl)*0.8

print "START \n"
print re_dir+" "+p+" "+th+" "+tl+" "+str(rmax)+" "+str(rmin)+" "+scope_mod+" "+scope_cnt+" "+scope_ip+" "+scope_port+" "+scope_channel
print "\n"

proc = subprocess.Popen('/opt/hp93000/SpikeCheck/lib/.service/AutoSpikeCheck.sh -n' +
                            ' -o ' + re_dir+
                            ' -p ' + p + ' -tH ' + th+ ' -tL ' + tl +
                            ' -rMax ' + str(rmax)+ ' -rMin ' + str(rmin) +
                            ' -scope_model ' + scope_mod + ' -scope_cnt ' + scope_cnt+
                            ' -scope_ip ' +scope_ip+ ' -scope_port ' + scope_port+ ' -scope_chn '+scope_channel,
                            shell=True,stdout=subprocess.PIPE)
tmp = proc.stdout.read()
print tmp


i=2
j=2

while i <= position_lines:

    while j <=pin_lines:
        with open(pos_file) as a:
            print i, "\n"
            pos=a.readlines()[i - 1]
            position=pos.split()
            print position[0],position[1],position[2]
            a.close()

        with open(pin_file) as b:
            pin=b.readlines()[j - 1]
            pin_info=pin.split()
            print pin_info[0],pin_info[1],pin_info[2]
            b.close()

        p=pin_info[0]
        th=pin_info[2]
        tl=pin_info[1]
        rmax=float(th)*1.2
        rmin=float(tl)*0.8

        print re_dir+" "+p+" "+th+" "+tl+" "+str(rmax)+" "+str(rmin)+" "+scope_mod+" "+scope_cnt+" "+scope_ip+" "+scope_port+" "+scope_channel
        print "\n"
	
        proc = subprocess.Popen('/opt/hp93000/SpikeCheck/lib/.service/AutoSpikeCheck.sh -c'+
                                ' -o ' + re_dir+
                                ' -p ' + p + ' -tH ' + th+ ' -tL ' + tl +
                                ' -rMax ' + str(rmax)+ ' -rMin ' + str(rmin) +
                                ' -scope_model ' + scope_mod + ' -scope_cnt ' + scope_cnt+
                                ' -scope_ip ' +scope_ip+ ' -scope_port ' + scope_port+ ' -scope_chn '+scope_channel,
                                shell=True,stdout=subprocess.PIPE)
        tmp = proc.stdout.read()
        print tmp
	
        j=j+1
        i=i+1

        if j==pin_lines+1:
            j=1

        print i, position_lines, "\n \n \n"
        if i==position_lines+1:
            j=pin_lines+1
            i=position_lines+2
            print i
            print j