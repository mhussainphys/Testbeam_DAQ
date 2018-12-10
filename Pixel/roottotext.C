#include <iostream>
#include "TFile.h"
#include "TTree.h"
#include <fstream>
using namespace std;

void roottotext(int run_number){
  TString roottotext_filename = Form("/home/otsdaq/CMSTiming_Pixel/roottotext/roottotext%i.txt", run_number);
  TString root_filename = Form("/data/TestBeam/2018_11_November_CMSTiming/RECO/v5_pixel_and_labview/DataVMETiming_Run%i.root", run_number);

  TFile *f=new TFile(root_filename); // opens the root file
  TTree *pulse=(TTree*)f->Get("pulse"); // creates the TTree object
  pulse->Scan(); // prints the content on the screen

  Float_t c,d;
  //float b,c; // create variables of the same type as the branches you want to access
  UInt_t a;
  Int_t b;
  //std::vector<float> x_pixel(64);
  //std::vector<float> y_pixel(64);
  pulse->SetBranchAddress("x_dut",&c); // for all the TTree branches you need this
  pulse->SetBranchAddress("y_dut",&d);
  //pulse->SetBranchAddress("i_evt",&a);
  //pulse->SetBranchAddress("ntracks",&b);

  ofstream myfile;
  myfile.open (roottotext_filename);

  for (int i=0;i<pulse->GetEntries();i++){
    //loop over the tree
    pulse->GetEntry(i);
    
    cout <<c[2]<< " " <<d[2]<<endl; //print to the screen
    //myfile << a <<" "<< c << " "<< d<<" "<<b<<"\n"; //write to file
  }
  myfile.close();
}
