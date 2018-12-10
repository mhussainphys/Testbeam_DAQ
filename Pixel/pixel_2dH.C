using namespace::std;
void pixel_2dH(int run_number)
{
	TString root_filename = Form("/data/TestBeam/2018_11_November_CMSTiming/RECO/v5_pixel_and_labview/DataVMETiming_Run%i.root", run_number);
	TCanvas *c1 = new TCanvas("c1", "c1",900,900);                                                 
	c1->Divide(2,3);
	gStyle->SetOptStat(0);                                                              

	TFile *f1 = new TFile(root_filename);
	TTree *pulse = (TTree*)f1->Get("pulse"); 

	c1->cd(1);
	pulse->Draw("y_dut[2]:x_dut[2]>>tele(300,10,30,300,10,30)","x_dut[2]!=-999&&y_dut[2]!=-999&&x_dut<20&&x_dut>14&&y_dut>20&y_dut<26");
	TH2F *tele = (TH2F*)gDirectory->Get("tele");
	tele->SetMinimum(1);
	tele->Draw("COLZ");

	c1->cd(2);
	pulse->Draw("0.001*x_pixel+20:0.001*y_pixel+12>>pixel(267,10,30,267,10,30)","x_dut[2]!=-999&&y_dut[2]!=-999&&x_pixel<6000&&x_pixel>0&&y_pixel>2000&y_pixel<8000");
	TH2F *pixel = (TH2F*)gDirectory->Get("pixel");
	pixel->SetMinimum(1);
	pixel->Draw("COLZ");

	c1->cd(3);
	pulse->Draw("0.001*x_pixel-x_dut[2]","x_dut[2]!=-999&&ntracks!=0&&no_of_hits_pixel!=0");
	//pulse->Draw("0.001*x_pixel-x_dut[2]","x_dut[2]!=-999&&x_dut<20&&x_dut>14&&y_dut<26&&y_dut>20&&x_pixel<6000&&x_pixel>0&&y_pixel>2000&y_pixel<8000&&ntracks==1");
	//pulse->Draw("0.001*x_pixel-x_dut[2]","x_dut[2]!=-999&&x_dut<20&&x_dut>14&&y_dut<26&&y_dut>20&&x_pixel<6000&&x_pixel>0&&y_pixel>2000&y_pixel<8000&&ntracks==1");
	/*TH2F *xdiff = (TH2F*)gDirectory->Get("xdiff");
	xdiff->SetMinimum(1);
	xdiff->Draw("COLZ");
	*/
	c1->cd(4);
	pulse->Draw("0.001*y_pixel-y_dut[2]","y_dut[2]!=-999&&ntracks!=0&&no_of_hits_pixel!=0");
	c1->cd(5);
	pulse->Draw("x_dut[2]:0.001*x_pixel>>tele5(300,-30,30,300,-30,30)");
	TH2F *tele5 = (TH2F*)gDirectory->Get("tele5");
	tele5->SetMinimum(1);
	tele5->Draw("COLZ");
	c1->cd(6);
	pulse->Draw("y_dut[2]:0.001*y_pixel>>tele6(300,-30,30,300,-30,30)");
	TH2F *tele6 = (TH2F*)gDirectory->Get("tele6");
	tele6->SetMinimum(1);
	tele6->Draw("COLZ");



	//c1->cd(5);
	//c1->cd(6);
	//pulse->Draw("0.001*y_pixel-y_dut[2]","y_dut[2]!=-999&&ntracks!=0");
	/*TH2F *ydiff = (TH2F*)gDirectory->Get("ydiff");
	ydiff->SetMinimum(1);
	ydiff->Draw("COLZ");*/

}




	

        /*TH2F *h2 = new TH2F("h2","",300,10,25,300,15,30);                                                     
	for(int i=0;i<(int)pixel_table.size();i++ ){
	  if(!(pixel_table[i][1]==16&&pixel_table[i][2]==0&&pixel_table[i][3]==0)){
	    for(int j=0;j<(int)pixel_table[i][3];j++ ){
	    h2->Fill(pixel_table[i][1]*0.001 + 14,pixel_table[i][2]*0.001 + 17.5);
	    }}}	
	h2->SetMinimum(1);
	gStyle->SetPalette(1);	
	c1->cd(1);
	h2->Draw("COLZ");*/

