import reporter
from multiprocessing import Pool
from random import randint


def run_process(empd):
    try:
        ep = empd.split(",")
        email = ep[0].strip()
        passwd = ep[1].strip()
        proxy = ''
        lengh = len(proxies)
        if lengh > 1:
            indx = randint(0, lengh-1)
            pro = proxies[indx]
            if not pro.isspace():
                proxy = pro.strip()
        if proxy != '':
            print("Using  proxy = ", proxy)
        reporter.Reporter(email, passwd, proxy)
    except Exception as c:
        print("Exception (start_reporting) ", str(c))


proxies = []
all_processes = []
processes = []
f = open("data.txt", "r")
for proces in f:
    all_processes.append(proces)
f.close()
p = open("../proxy.txt", "r")
proxies.append(" ")
for prox in p:
    proxies.append(prox)
p.close()
counter = 0
for x in all_processes:
    if not x.isspace() and x is not None and x != "":
        counter += 1
        processes.append(x)
    if __name__ == '__main__':
        try:
            if counter == 3:
                print("processes (" + str(counter) + ") = ", str(processes))
                counter = 0
                pool = Pool(processes=3)
                pool.map(run_process, processes)
                processes = []
        except Exception as vv:
            print("Exception (processes) = ", str(vv))
if 0 < counter < 3:
    if __name__ == '__main__':
        print("processes (" + str(counter) + ") = ", str(processes))
        pool = Pool(processes=counter)
        pool.map(run_process, processes)
