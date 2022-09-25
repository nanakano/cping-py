from scapy.all import *
import sys
import time 

args = sys.argv
dstIP = str(args[1])
count = 1400
count = 1

def cping():
  ping0 = 0
  ping3 = 0
  ping8 = 0
  times = 1
  payload = ""
  for i in range(count):
    try:
      # ping packet create 
      icmp = ICMP(seq=i)
      for j in range(56):
        payload = payload + "a"

      ping = IP(dst=dstIP)/icmp/payload
      ping.show()

      # ping send
  
      ans = sr1(ping, timeout=2, verbose=0)
      ans.show()

      # ICMP type is "Echo Reply"
      try: 
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
          ping3 = ping3 + 1

        # ICMP type is "Time Exceeded"
        else:
          print(".", end="") 
          ping8 = ping8 + 1
      # ICMP type is "Time Exceeded"
      except NameError:
        print(".", end="") 
        ping8 = ping0 + 1
      except TypeError:
        print(".", end="") 
        ping8 = ping0 + 1
    except  OSError:
      print("error")

    f = i+1
    if f % 70 == 0:
      print("")

  #  time.sleep(times)
  timeMin = round(timeMin * 100)
  timeMax = round(timeMax * 100)
  timeAve = timeSum / count
  timeAve = round(timeAve * 100)
  pingNo = ping3 + ping8
  pingOk = ( count - pingNo ) / ping0
  pintOk = pingOk * 100
  print("")
  print ("Success rate is ", pingOk, " percent (", count - pingNo, "/", count, "), round-trip min/avg/max = ", timeMin, "/", timeAve, "/", timeMax, " ms", sep='')



def main():
  cping()

if __name__ == "__main__":
  main()  
