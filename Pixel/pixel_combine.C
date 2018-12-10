#include <iostream>
#include <fstream>
using namespace std;

void pixel_combine(TString pixel_filename, TString root_filename)
{

	//Opening file
	TFile f1(root_filename, "UPDATE");
	TTree *pulse = (TTree*)f1.Get("pulse");
	int tree_entries = pulse->GetEntries();

	//Defining Branches    
	vector<float> * x_pixel = new vector<float>(); 
	vector<float> * y_pixel = new vector<float>();
	vector<int> * no_of_hits_pixel = new vector<int>();

	TBranch * b_x_pixel = pulse->Branch("x_pixel",&x_pixel);
	pulse->SetBranchAddress("x_pixel",&x_pixel,&b_x_pixel);	

	TBranch * b_y_pixel = pulse->Branch("y_pixel",&y_pixel);
	pulse->SetBranchAddress("y_pixel",&y_pixel,&b_y_pixel);

	TBranch * b_no_of_hits_pixel = pulse->Branch("no_of_hits_pixel",&no_of_hits_pixel);
	pulse->SetBranchAddress("no_of_hits_pixel",&no_of_hits_pixel,&b_no_of_hits_pixel);

	//Read text file
	ifstream infile;
	infile.open(pixel_filename); 

	vector< vector<float> > pixel_table; 
	float x_pix, y_pix, no_of_hits;
	int total_pixel_rows = 0;
	int trigger_no;

	while(infile >> trigger_no >> x_pix >> y_pix >> no_of_hits) {
	  vector<float> one_row;
	  one_row.push_back(trigger_no);
	  one_row.push_back(x_pix);
	  one_row.push_back(y_pix);
	  one_row.push_back(no_of_hits);
	  pixel_table.push_back(one_row);
	  }

	bool finished_event=false;
	int pixel_events=0;
     
	for(int i=0;i<(int)pixel_table.size();i++ ){
	  if(!(pixel_table[i][1]==16&&pixel_table[i][2]==0&&pixel_table[i][3]==0)){
	    x_pixel->push_back(pixel_table[i][1]);
	    y_pixel->push_back(pixel_table[i][2]);
	    no_of_hits_pixel->push_back(pixel_table[i][3]);
	  }
	  if(i==pixel_table.size()-1 || pixel_table[i][0] != pixel_table[i+1][0]){	        
	    finished_event=true;
	    if(x_pixel->size()==0){
	      x_pixel->push_back(-1);
	      y_pixel->push_back(-1);
	      no_of_hits_pixel->push_back(0);
	    }
	  } //this is last row of this event
	
	  if(finished_event){
	    b_x_pixel->Fill();
	    b_y_pixel->Fill();
	    std::cout<< &b_x_pixel<<endl;
	    std::cout<< &b_y_pixel<<endl;
	    b_no_of_hits_pixel->Fill();
	    finished_event=false;
	    x_pixel->clear();
	    y_pixel->clear();
	    no_of_hits_pixel->clear();
	    pixel_events++;
	  }
	  
	}	
	
        std::cout << "Entries in the tree: " << tree_entries << endl; 
	std::cout << "Rows in the pixel file: " << pixel_events << endl; 
	pulse->Write();
	f1.Close();
}                                                                                                        
