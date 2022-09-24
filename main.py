from scapy.all import *
import sys
import time 

args = sys.argv
dstIP = str(args[1])
count = 1400

def cping():
  ping0 = 0
  ping3 = 0
  ping8 = 0
  times = 1
  for i in range(count):
    try:
      # ping packet create 
      ping = IP(dst=dstIP)/ICMP(seq=i)

      # ping send
      ans = sr1(ping, timeout=1, verbose=0)

      # ICMP type is "Echo Reply"
      if ans[ICMP].type == 0:
        print("!", end="") 
        ping0 = ping0 + 1

        # timestamp
        times = ans.time - ping.sent_time
        if i == 0:
          timeSum = times
          timeMax = times
          timeMin = times
        else:
          timeSum = timeSum + times
          if timeMax < times:
            timeMax = times
          if times < timeMin:
            timeMin = times
            
      # ICMP type is "Destination Unreachable"
      elif ans[ICMP].type == 3:
        print("U", end="") 
        ping3 = ping0 + 1

      # ICMP type is "Time Exceeded"
      else:
        print(".", end="") 
        ping8 = ping0 + 1
    except  OSError:
      print("error")

    f = i+1
    if f % 70 == 0:
      print("")

  #  time.sleep(times)
  timeAve = timeSum / count
  pingNo = ping3 + ping8
  pingOk = pingNo / ping0
#  print ("Success rate is ", pingOk, "percent (", ping3, "/", pingNo "), round-trip min/avg/max = ", timeMin, "/", timeAve, "/", timeMax, " ms")



def main():
  cping()

if __name__ == "__main__":
  main()  
