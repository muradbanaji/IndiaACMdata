//Compile on linux with
//g++ -lm -std=gnu++11 Excess12MC.cc -o Excess12MC
//run with ./Excess12MC
//output is a set of csv files. The national file is
//TT_sim.csv; remaining files are with each state omitted

//Order of states: Andhra Pradesh, Bihar, Haryana, Himachal Pradesh, Karnataka, Kerala, Madhya Pradesh, Maharashtra, Punjab, Rajasthan, Tamil Nadu, West Bengal



#include <string.h>
#include <iostream>
#include <random>

//Gamma distribution [not used here]

double gamma(double alpha, double disp, std::default_random_engine & generator)
{
  static std::gamma_distribution<double> dist;
  return dist(generator, std::gamma_distribution<double>::param_type(alpha, disp));
}

//Gaussian

double norml(double mean, double stdev, std::default_random_engine & generator)
{
  static std::normal_distribution<double> dist1;
  return dist1(generator, std::normal_distribution<double>::param_type(mean, stdev));
}

//
// Uniform distribution
//

double unif(double lend, double rend, std::default_random_engine & generator)
{
  static std::uniform_real_distribution<double> dist1;
  return dist1(generator, std::uniform_real_distribution<double>::param_type(lend, rend));
}

//Beta distribution based on gamma distribution, as described at
//https://stackoverflow.com/questions/10358064/random-numbers-from-beta-distribution-c
//[not used here]

double betad(double alpha, double beta, std::default_random_engine & generator)
{
  static std::gamma_distribution<double> dist;
  double d1, d2;
  d1=dist(generator, std::gamma_distribution<double>::param_type(alpha, 1));
  d2=dist(generator, std::gamma_distribution<double>::param_type(beta, 1));
  return d1/(d1+d2);
}

//suffix _pre is for the pre-pandemic reference period
//suffix _pand is for the pandemic period
//suffix _change for a relative change between pre-pandemic 
//   and pandemic period. E.g. -0.05 = a 5% drop.
//pop = total population (units of 10K)
//reg = registered deaths in whatever system is 
//   generating the data (e.g. online system) as a fraction of total
//regdth = registered deaths (units of 10K) in 
//    whatever system is generating the data (e.g. online system)
//dth = absolute number of deaths (units of 10K)
//   i.e., dth = regdth/reg
//mort = mortality = dth/pop

//Order of states: Andhra Pradesh, Bihar, Haryana, Himachal Pradesh, Karnataka, Kerala, Madhya Pradesh, Maharashtra, Punjab, Rajasthan, Tamil Nadu, West Bengal

int main(int argc, char *argv[]){
  const int numexps=10000;  // number of experiments
  //Estimated coverage in the data based on CRS2019 (i.e., SRS 2018)
  const char *statenames[12]={"Andhra Pradesh","Bihar","Haryana","Himachal Pradesh","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Punjab","Rajasthan","Tamil Nadu","West Bengal"};
  const char *statenamesbrief[12]={"AP","BR","HR","HP","KA","KL","MP","MH","PB","RJ","TN","WB"};
  double reg_pre_mean_SRS2018[12]={0.9058,0.5044,0.9729,0.8113,1.0000,0.9760,0.8124,0.6659,0.9911,0.4802,0.9279,0.8294};
  //The change in estimate of registration coverage if we use SRS 2019 instead of SRS 2018
  double reg_SRS2019_mult[12]={1.0,1.06,1.0,1.0,1.0,1.0,1.02,1.0,1.0,1.01,1.0,1.0};
  //Estimated coverage in the data corrected using SRS 2019
  double reg_pre_mean[12];
  double reg_prel[12], reg_prer[12], reg_pre[12];
  double reg_change[12];
  double reg_pand[12];
  //2019 populations
  double pop_pre[12]={52221,119520,28672,7300,65798,35125,82232,122153,29859,77264,75695,96906};
  //2020 populations
  double pop_pand[12]={52504,121302,29077,7347,66322,35307,83374,123295,30099,78273,76049,97516};
  double pop_pand_tot, pop_pand_national=1347121;
  double pop_pand_remaining;
  //2019 with April, May repeated
  double regdth_pre[12]={419895,399425,212083,47000,583400,304554,508924,535850,244628,254068,685773,522396};
  //Up to April 2020-May 2021
  double regdth_pand[12]={626541,504245,269713,52790,694730,303313,704092,788570,291332,299039,809704,658648};
  double regdth_June2019[12]={30214,30440,14946,3285,37403,20505,38978,35405,16515,19766,48868,35373};
  double regdth_June2021[12]={67406,-1,-1,-1, 93797,-1,-1,-1,26656,-1,-1,-1};//-1 means unavailable
  int popJune;
  double excess_June_tot;

  double regdth_pre_tot, regdth_pand_tot;
  double dth_pre[12], mort_pre[12];
  double dth_pand[12], mort_pand[12];
  double dth_pre_tot, dth_pand_tot, excess_tot, excessmort_tot;

  double excessdth[12];
  double excessmort[12];
  //range of variation in pre-pandemic completion
  double regql=0.15,regqr=0.15;
  //absolute change in registration levels
  double regchangemidall=0;
  double regchangemid[12];//={-0.01,-0.01,-0.01,-0.01,-0.01,-0.01,-0.01,-0.01,-0.01,-0.01,-0.01,-0.01};
  double regchangeql=0.05,regchangeqr=0.05;
  double reg_pre_SD=0.02;

  double Excess_total_national, Excess_June_national;

  //different mortality impact in remainder of country
  double mort_var, mort_varl=0.2, mort_varr=0.2;
  double mort_var_June, mort_varl_June=0.2, mort_varr_June=0.2;

  int totsteps=0;

  std::default_random_engine generator;

  int timeint;
  time_t timepoint;
  int i,j,k,t, w;
  FILE *fd;
  int ispec=7;//omit one
  char fname[30];

  for(w=-1;w<12;w++){//what to omit
    ispec=w;
    for(i=0;i<12;i++)
      regchangemid[i]=regchangemidall;

    //range of pre-pandemic registration levels
    pop_pand_tot=0;regdth_pre_tot=0;regdth_pand_tot=0;popJune=0;
    for(i=0;i<12;i++){
      if(i==ispec){continue;}
      reg_pre_mean[i]=reg_pre_mean_SRS2018[i]*reg_SRS2019_mult[i];//corrected using SRS2019
      reg_prel[i]=reg_pre_mean[i] - regql*reg_pre_mean[i];//lower limit
      reg_prer[i]=reg_pre_mean[i] + regqr*(1-reg_pre_mean[i]);//upper limit
      pop_pand_tot+=pop_pand[i];
      if(regdth_June2021[i]>0)
	popJune+=pop_pand[i];

      regdth_pre_tot+=regdth_pre[i];
      regdth_pand_tot+=regdth_pand[i];
    }

    if(w==-1)
      strcpy(fname, "TT");
    else
      strcpy(fname, statenamesbrief[w]);
    strcat(fname, "_sim.csv");

    if(!(fd=fopen(fname, "w"))){
      fprintf(stderr, "Could not open file \"%s\" for writing. EXITING.\n", fname);
      exit(0);
    }

    //random seeding
    timeint = time(&timepoint); /*convert time to an integer */
    srand(timeint);
    generator.seed(timeint);


    //Central estimates
    dth_pre_tot=0;dth_pand_tot=0;excess_tot=0;excess_June_tot=0;
    for(i=0;i<12;i++){
      if(i==ispec){continue;}
      reg_pre[i]=reg_pre_mean[i];

      reg_change[i]=regchangemid[i];

      reg_pand[i]=reg_pre[i]+reg_change[i];

      dth_pre[i]=regdth_pre[i]/reg_pre[i];
      mort_pre[i]=dth_pre[i]/pop_pre[i];
      dth_pand[i]=regdth_pand[i]/reg_pand[i];
      mort_pand[i]=dth_pand[i]/pop_pand[i];
      excessdth[i]=dth_pand[i]-mort_pre[i]*pop_pand[i];
      excessmort[i]=excessdth[i]/pop_pand[i]; //per 1K population
      dth_pre_tot+=dth_pre[i];
      dth_pand_tot+=dth_pand[i];
      excess_tot+=excessdth[i];

      //June
      if(regdth_June2021[i]>0)
	excess_June_tot+=regdth_June2021[i]/reg_pand[i]-(regdth_June2019[i]/pop_pre[i]/reg_pre[i])*pop_pand[i];
    }
    excessmort_tot=excess_tot/pop_pand_tot;

    pop_pand_remaining=pop_pand_national-pop_pand_tot;
    mort_var=0;
    mort_var_June=0;
    Excess_total_national=excess_tot+(1.0+mort_var)*excessmort_tot*pop_pand_remaining;
    Excess_June_national=excess_June_tot+(1.0+mort_var_June)*excess_June_tot/popJune*(pop_pand_national-popJune);

    fprintf(stderr, "%.0f, %.0f, %.0f, %.4f, %.4f, %.4f, %.0f, %.4f, %.0f\n", dth_pre_tot, dth_pand_tot, excess_tot, excessmort_tot, regdth_pre_tot/dth_pre_tot*100, regdth_pand_tot/dth_pand_tot*100, Excess_total_national, Excess_total_national/pop_pand_national, Excess_total_national+Excess_June_national);
    //End of central estimates

    totsteps=0;
    while(totsteps<numexps){

      dth_pre_tot=0;dth_pand_tot=0;excess_tot=0;excess_June_tot=0;
      for(i=0;i<12;i++){
	if(i==ispec){continue;}
	reg_pre[i]=unif(reg_prel[i], reg_prer[i], generator);

	// //pre-pandemic registration levels chosen from beta distribution
	// //with SD=reg_pre_SD
	// //alpha=mu(mu(1-mu)/var-1), beta = (1-mu)(mu(1-mu)/var-1)
	// //assumes that mu(1-mu) > var
	// if(fabs(reg_pre_mean[i]-1.0)>0.01)
	// 	t=reg_pre_mean[i]*(1.0-reg_pre_mean[i])/reg_pre_SD/reg_pre_SD-1.0;
	// else
	// 	t=100.0;
	// reg_pre[i]=betad(reg_pre_mean[i]*t, (1.0-reg_pre_mean[i])*t, generator);


	reg_change[i]=unif(-regchangeql+regchangemid[i], regchangeqr+regchangemid[i], generator);

	reg_pand[i]=reg_pre[i]+reg_change[i];
	if(reg_pand[i]>1.0)
	  reg_pand[i]=1.0;

	dth_pre[i]=regdth_pre[i]/reg_pre[i];
	mort_pre[i]=dth_pre[i]/pop_pre[i];
	dth_pand[i]=regdth_pand[i]/reg_pand[i];
	mort_pand[i]=dth_pand[i]/pop_pand[i];
	excessdth[i]=dth_pand[i]-mort_pre[i]*pop_pand[i];
	excessmort[i]=excessdth[i]/pop_pand[i]; //per 1K population
	dth_pre_tot+=dth_pre[i];
	dth_pand_tot+=dth_pand[i];
	excess_tot+=excessdth[i];


	//June
	if(regdth_June2021[i]>0)
	  excess_June_tot+=regdth_June2021[i]/reg_pand[i]-(regdth_June2019[i]/pop_pre[i]/reg_pre[i])*pop_pand[i];


      }
      excessmort_tot=excess_tot/pop_pand_tot;

      pop_pand_remaining=pop_pand_national-pop_pand_tot;
      mort_var=unif(-mort_varl, mort_varr, generator);
      mort_var_June=unif(-mort_varl_June, mort_varr_June, generator);
      Excess_total_national=(excess_tot+(1.0+mort_var)*excessmort_tot*pop_pand_remaining);
      Excess_June_national=(excess_June_tot+(1.0+mort_var_June)*excess_June_tot/popJune*(pop_pand_national-popJune));

      fprintf(fd, "%.0f, %.0f, %.0f, %.4f, %.4f, %.4f, %.0f, %.4f, %.0f\n", dth_pre_tot, dth_pand_tot, excess_tot, excessmort_tot, regdth_pre_tot/dth_pre_tot*100, regdth_pand_tot/dth_pand_tot*100, Excess_total_national, Excess_total_national/pop_pand_national, Excess_total_national+Excess_June_national);
      totsteps++;

    }

    fclose(fd);
  }


  return 0;
}
