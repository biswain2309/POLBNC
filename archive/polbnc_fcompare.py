fpbc = open("POLBNC_sample.txt",'r')
fbil = open("BIL_sample.txt",'r')
passFile = open("text\PassFile.txt", 'w')
failFile = open("text\FailFile.txt", 'w')
count = 0
for linepbc in fpbc:
    for linebil in fbil:
        line_pbc_split = linepbc.split("|")
        line_bil_split = linebil.split("|")
        if line_pbc_split[8] == line_bil_split[2]:
            if line_pbc_split[53] == line_bil_split[4]:
                passFile.write(linepbc)
            else:
                failFile.write(line)

f.close()
passFile.close()
failFile.close()