import ROOT
import sys

run_number = sys.argv[1]
f = ROOT.TFile.Open("/data/TestBeam/2018_11_November_CMSTiming/RECO/v5/DataVMETiming_Run%s.root" % run_number)
roottotext = open("/home/otsdaq/CMSTiming_Pixel/roottotext/roottotext%s.txt" % run_number, "a+") 

for event in f.pulse:
      roottotext.write(str(event.i_evt) + "\t" + str(event.x_dut[2]) + "\t" + str(event.y_dut[2]) + "\t" + str(event.ntracks) + "\n")        
roottotext.close();



