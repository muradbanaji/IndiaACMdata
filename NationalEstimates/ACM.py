#!/usr/bin/env python

#Run with, for example, python ACM.py

import csv

###
### Gather the data
###

#The following file contains national and sub-national
#demographic data, including death registration data
file = open('IndiaRegCoverPop.csv')
demo_data = csv.reader(file)
regional_data_desc = []
regional_data_desc = next(demo_data)
regional_data =[]
for row in demo_data:
        regional_data.append(row)
numregions=len(regional_data)
#print ("number of regions = " + repr(numregions))

#
#The following file includes the raw monthly registration data
#
file1 = open('TwelveStates.csv')
monthly_data = csv.reader(file1)
statdat=[];statdat = next(monthly_data)
numstates=len(statdat)-1
months = []
for row in monthly_data:
        months.append(row)
nummonths=len(months)

#Name the list of states whose data is used
STAR12="STARS"

#totals
dat18=[]; dat19=[]; dat20=[]; datbase14=[]; datpand14=[]; datbasewave1=[]; datbasewave2=[]; datpandwave1=[]; datpandwave2=[];
#registered deaths, coverage, population
reg18=[]; reg19=[];cov18=[]; cov19=[];pop19=[]; pop20=[]; pop21=[]
#June data
regbasejune=[];regpandjune=[]
#estimated total deaths, coverage in the data
dth18=[]; dth19=[];cov18dat=[]; cov19dat=[]

#get indices from the demographic data file
for x in range(len(regional_data_desc)):
        if regional_data_desc[x]=="2018 registered deaths":
                reg18ind=x
        elif regional_data_desc[x]=="2019 registered deaths":
                reg19ind=x
        elif regional_data_desc[x]=="2018 estimated coverage":
                cov18ind=x
        elif regional_data_desc[x]=="2019 estimated coverage":
                cov19ind=x
        elif regional_data_desc[x]=="2019 estimated population (1000)":
                pop19ind=x
        elif regional_data_desc[x]=="2020 estimated population (1000)":
                pop20ind=x
        elif regional_data_desc[x]=="2021 estimated population (1000)":
                pop21ind=x

#National population
for y in range(numregions):
        if regional_data[y][0]=="India":
                pop19nat=int(regional_data[y][pop19ind])
                pop20nat=int(regional_data[y][pop20ind])
                reg18nat=int(regional_data[y][reg18ind])
                reg19nat=int(regional_data[y][reg19ind])
#print("National population (1000): " + repr(pop20nat))


#demographic data for STAR12
statelist=[]
for x in range(numstates):
        for y in range(numregions):
                if regional_data[y][0]==statdat[x+1]:
                        reg18.append(int(regional_data[y][reg18ind]))
                        reg19.append(int(regional_data[y][reg19ind]))
                        cov18.append(float(regional_data[y][cov18ind]))
                        cov19.append(float(regional_data[y][cov19ind]))
                        pop19.append(int(regional_data[y][pop19ind]))
                        pop20.append(int(regional_data[y][pop20ind]))
                        pop21.append(int(regional_data[y][pop21ind]))
                        statelist.append(statdat[x+1])

#National estimated deaths (2018,19)
dth18nat=0;dth19nat=0
for y in range(numregions):
        if regional_data[y][0]!="India":
                dth18nat+=float(regional_data[y][reg18ind])/(float(regional_data[y][cov18ind])/100.0)
                dth19nat+=float(regional_data[y][reg19ind])/(float(regional_data[y][cov19ind])/100.0)

logf=open("BasicData.csv", "w")
logf.write("National data:,\n")
logf.write("Estimated 2019 population, " + "{:.0f}".format(pop19nat)+"\n")
logf.write("Estimated 2020 population, " + "{:.0f}".format(pop20nat)+"\n")
logf.write("Estimated yearly population growth, " + "{:.1f}".format(100*(float(pop20nat)/float(pop19nat)-1))+"%\n")
logf.write("Registered deaths in 2018, " + "{:.0f}".format(reg18nat)+"\n")
logf.write("Registered deaths in 2019, " + "{:.0f}".format(reg19nat)+"\n")
logf.write("Est. total deaths in 2018 based on subnational data, " + "{:.0f}".format(dth18nat) +"\n")
logf.write("Est. total deaths in 2019 based on subnational data, " + "{:.0f}".format(dth19nat)+"\n")

#National coverage
cov18nat=float(reg18nat)/dth18nat;cov19nat=float(reg19nat)/dth19nat;
logf.write("Est. registration coverage in 2018 based on subnational data, " + "{:.1f}".format(cov18nat*100.0)+"%\n")
logf.write("Est. registration coverage in 2019 based on subnational data, " + "{:.1f}".format(cov19nat*100.0)+"%\n\n")

logf.write(STAR12 + " (states whose data is used), \"" + ", ".join(statelist)+"\"\n")

junepop=0;numjune=0;

#available data: 36=Jan 2018
for x in range(1,numstates+1):
        tot=0;
        for y in range(36,48):#Jan 2018+12
                tot+=int(months[y][x])
        dat18.append(tot)
        tot=0;
        for y in range(48,60):#Jan 2019+12
                tot+=int(months[y][x])
        dat19.append(tot)
        datbase14.append(tot+int(months[51][x])+int(months[52][x]))
        tot=0
        for y in range(60,72):#Jan 2020+12
                tot+=int(months[y][x])
        dat20.append(tot)
        tot=0
        for y in range(63,77):
                tot+=int(months[y][x])
        datpand14.append(tot)
        tot=0
        for y in range(48,50):
                tot+=int(months[y][x])
        for y in range(51,60):
                tot+=int(months[y][x])
        datbasewave1.append(tot)
        tot=0
        for y in range(50,53):
                tot+=int(months[y][x])
        datbasewave2.append(tot)
        tot=0
        for y in range(63,74):
                tot+=int(months[y][x])
        datpandwave1.append(tot)
        tot=0
        for y in range(63,77):
                tot+=int(months[y][x])
        datpandwave2.append(tot)

        #June data where available
        if(months[77][x]!=""):
                numjune+=1;junepop+=pop20[x-1]
                regbasejune.append(int(months[53][x]))
                regpandjune.append(int(months[77][x]))
        else:
                regbasejune.append(0);
                regpandjune.append(0);



#total deaths and coverage in the data (2018, 19) in each state
for x in range(numstates):
        dth18.append(int(round(float(reg18[x])/float(cov18[x])*100.0)))
        dth19.append(int(round(float(reg19[x])/float(cov19[x])*100.0)))
        cov18dat.append(float(dat18[x])/float(dth18[x]))
        cov19dat.append(float(dat19[x])/float(dth19[x]))

#Totals
pop20t=sum(pop20);
dat19t=sum(dat19);reg19t=sum(reg19);dth19t=sum(dth19);cov19datt=float(dat19t)/float(dth19t);
dat18t=sum(dat18);reg18t=sum(reg18);dth18t=sum(dth18);cov18datt=float(dat18t)/float(dth18t);
datbase14t=sum(datbase14);datpand14t=sum(datpand14);
logf.write("\nFraction of 2020 national population in " + STAR12 + ", " + "{:.1f}".format(100*float(pop20t)/float(pop20nat))+"%\n");
logf.write("Fraction of estimated 2019 deaths in "+STAR12+", " + "{:.1f}".format(100*float(dth19t)/float(dth19nat))+"%\n");
logf.write("Est. 2018 registration coverage in "+STAR12+", " + "{:.1f}".format(100*float(reg18t)/float(dth18t))+"%\n");
logf.write("Est. 2019 registration coverage in "+STAR12+", " + "{:.1f}".format(100*float(reg19t)/float(dth19t))+"%\n");
logf.write("Est. 2018 registration coverage outside "+STAR12+", " + "{:.1f}".format(100*float(reg18nat-reg18t)/float(dth18nat-dth18t))+"%\n");
logf.write("Est. 2019 registration coverage outside "+STAR12+", " + "{:.1f}".format(100*float(reg19nat-reg19t)/float(dth19nat-dth19t))+"%\n");
logf.write("Est. 2018 coverage in the data in "+STAR12+", " + "{:.1f}".format(100*float(dat18t)/float(dth18t))+"%\n");
logf.write("Est. 2019 coverage in the data in "+STAR12+", " + "{:.1f}".format(100*float(dat19t)/float(dth19t))+"%\n");
logf.write("Crude 14 month P-score in "+STAR12+", " + "{:.1f}".format((float(datpand14t)/float(datbase14t)-1)*100.0) + "%\n");

logf.close()

#Basic State-level data table
f = open("StateOutput.csv", "w")
f.write("state, 2019 registered deaths, 2019 est. registration coverage (%), 2019 est. deaths, 2019 deaths in available data, 2019 est. coverage in the data\n")
for x in range(numstates):
        f.write(statdat[x+1] + ", " + repr(reg19[x]) + "," + repr(cov19[x]) + "," + repr(dth19[x]) + "," + repr(dat19[x]) + "," + "{:.1f}".format(100.0*cov19dat[x])+"\n")
f.write("All," + repr(reg19t) + "," + "{:.1f}".format(100*float(reg19t)/float(dth19t)) + "," + repr(dth19t) + "," + repr(dat19t) + "," + "{:.1f}".format(100.0*cov19datt) +"\n")
f.close()

#monthly excesses (simple)
fm = open("MonthlyExcessRel2019.csv", "w")
fm.write(",")
for x in range(numstates):
        fm.write(statdat[x+1]+",")
fm.write("STAR12 xs (mortality-based extrapolation for June 21),national xs (mortality-based extrapolation)\n")
for y in range(62,77):#March 2020
        tot=0
        fm.write (months[y][0]+",")
        #base_delay=24 if y>72 else 12
        if y>=72:
                base_delay=24
        else:
                base_delay=12
        for x in range(numstates):
                fm.write ("{:.0f}".format((float(months[y][x+1])-float(months[y-base_delay][x+1]))/cov19dat[x])+",")
                tot+=(float(months[y][x+1])-float(months[y-base_delay][x+1]))/cov19dat[x]
        fm.write("{:.0f}".format(tot)+","+"{:.0f}".format(tot*float(pop20nat)/float(pop20t))+"\n")

fm.write (months[77][0]+",")
tot=0
for x in range(numstates):
        if(months[77][x+1]!=""):
                fm.write ("{:.0f}".format((float(months[77][x+1])-float(months[77-24][x+1]))/cov19dat[x])+",")
                tot+=(float(months[77][x+1])-float(months[77-24][x+1]))/cov19dat[x];
        else:
                fm.write (",")
fm.write("{:.0f}".format(tot*float(pop20t)/float(junepop))+","+"{:.0f}".format(tot*float(pop20nat)/float(junepop))+"\n")

fm.close()

### Loop
f1 = open("simulations.csv", "w")
f1.write ("May(m)=mortality based extrapolation for April 20-May 21,,,,\nJune(m)=mortality based extrapolation for April 20-June 21,,,,\nMay(p)=P-score based extrapolation for April 20-May 21,,,,\nJune(p)=P-score based extrapolation for April 20-June 21,,,,\n")
for tt in range(7):
        #dthbase14=expected deaths; dthpand14=estimated total deaths
        dthraw14=[];dthbase14=[];dthpand14=[];xs14=[];xs14pc=[];Pscore14=[]
        #baseline and pandemic period coverage
        basecov14=[];pandcov14=[]
        #June 2021
        dthbasejune=[];dthpandjune=[];xsjune=[];xsjunepc=[];Pscorejune=[]

        #Parameters:
        #basecor: fractional correction to baseline coverage
        #pandcor: fractional correction to pandemic coverage
        #dthrise: fractional natural change in expected deaths
        #surge_diff: 0.05=rest of country 5% worse affected, etc
        #defaults
        if tt==0:
                dthrise_nat=0.0;basecor_nat=0.0;pandcor_nat=0.0;surge_diff=0.0;tag="baseline"
        elif tt==1:
                dthrise_nat=0.02;basecor_nat=0.0;pandcor_nat=0.05;surge_diff=-0.2;tag="optimistic"
        elif tt==2:
                dthrise_nat=0.0;basecor_nat=-0.05;pandcor_nat=-0.05;surge_diff=0.2;tag="pessimistic"
        elif tt==3:
                dthrise_nat=0.01;basecor_nat=0.0;pandcor_nat=0.0;surge_diff=0.0;tag="small mortality rise"
        elif tt==4:
                dthrise_nat=0.0;basecor_nat=-0.01;pandcor_nat=0.0;surge_diff=0.0;tag="small overestimation of baseline coverage"
        elif tt==5:
                dthrise_nat=0.0;basecor_nat=0.0;pandcor_nat=-0.01;surge_diff=0.0;tag="small decrease in pandemic coverage"
        elif tt==6:
                dthrise_nat=0.0;basecor_nat=0.0;pandcor_nat=0.0;surge_diff=0.01;tag="slightly higher mortality impact outside "+STAR12+""
        else:
                dthrise_nat=0.0;basecor_nat=0.0;pandcor_nat=0.0;surge_diff=0.0

        f1.write(",,,,\n*********,,,,\nSimulation " + repr(tt+1) + " (" + tag + "),,,,\nexpected rise in deaths: " + repr(dthrise_nat*100) + "%,,,,\nbaseline registration shift: " + repr(basecor_nat*100) + "%,,,,\nadditional pandemic registration shift: " + repr(pandcor_nat*100) + "%,,,,\nvariation in mortality impact outside "+STAR12+": " + repr(surge_diff*100) + "%,,,,\n");

        #We can, in theory, have different corrections in different states
        basecor=[];pandcor=[];dthrise=[]
        dth19C=[];#estimated deaths in each state in 2019 corrected
        #Excess in each state
        for x in range(numstates):
                #parameters
                basecor.append(basecor_nat);pandcor.append((1+basecor_nat)*(1+pandcor_nat)-1);dthrise.append(dthrise_nat)
                #compute coverage and mortality April 2020-May 2021
                basecov14.append(min((1.0+basecor[x])*cov19dat[x], 1.0))#baseline coverage
                pandcov14.append(min((1.0+pandcor[x])*cov19dat[x], 1.0))#pandemic coverage
                dthraw14.append(float(datbase14[x])/basecov14[x])#raw baseline period deaths
                dthbase14.append((1.0+dthrise[x])*dthraw14[x])#expected deaths, given rise in population, etc
                dthpand14.append(float(datpand14[x])/pandcov14[x])#pandemic deaths
                xs14.append(int(round(dthpand14[x]-dthbase14[x])))#excess
                xs14pc.append(float(xs14[x])/float(pop20[x]))#excess per 1K
                Pscore14.append(float(xs14[x])/float(dthbase14[x]))#P-score
                dth19C.append(int(round(float(dat19[x])/basecov14[x])))
                #June 2021
                dthbasejune.append((1.0+dthrise[x])*float(regbasejune[x])/basecov14[x])
                dthpandjune.append(float(regpandjune[x])/pandcov14[x])
                xsjune.append(int(round(dthpandjune[x]-dthbasejune[x])))
                xsjunepc.append(float(xsjune[x])/float(pop20[x]))
                if dthbasejune[x]>0:
                        Pscorejune.append(float(xsjune[x])/float(dthbasejune[x]))
                else:
                        Pscorejune.append(0);

        #Compute the expected rise in mortality for use in national calculations
        exp_dthrise=sum(dthbase14)/float(sum(dthraw14))-1.0;
        
        #If we assume a baseline error, apply this nationally to get a corrected national estimate of baseline mortality
        dth19natC=dth19nat/(1+basecor_nat)
        dth19Ct=sum(dth19C)#corrected total deaths in 2019

        xs14t=sum(xs14);xs14pct=xs14t/float(pop20t);Pscore14t=float(xs14t)/float(sum(dthbase14));
        xsjunet=sum(xsjune);xsjunepct=float(xsjunet)/float(junepop);Pscorejunet=float(xsjunet)/float(sum(dthbasejune));
        f1.write("April 2020-May 2021 P-score in "+STAR12+": " + "{:.1f}".format(Pscore14t*100.0) + "%"+",,,,\n");
        f1.write("April 2020-May 2021 excess mortality in "+STAR12+": " + "{:.2f}".format(float(xs14pct)) + " per 1K"+",,,,\n");
        f1.write("June 2021 P-score in available data: " + "{:.1f}".format(Pscorejunet*100.0) + "%"+",,,,\n");
        f1.write("June 2021 excess mortality in available data: " + "{:.2f}".format(float(xsjunepct)) + " per 1K"+",,,,\n");
        
        
        #f = open("StateOutput1.csv", "w")
        #f.write("state, 2019 data, 2019 registered, 2019 estimated total, coverage in the data, baseline data, pandemic data, excess, excess per 1K, P-score\n")
        #for x in range(numstates):
                #f.write(statdat[x+1] + ", " + repr(dat19[x]) + "," + repr(reg19[x]) + "," + repr(dth19C[x]) + "," + "{:.2f}".format(100.0*cov19dat[x]) + "," + repr(datbase14[x]) + "," + repr(datpand14[x]) + "," + repr(xs14[x])+ "," + "{:.2f}".format(xs14pc[x]) + "," + "{:.1f}".format(Pscore14[x]*100.0)+"\n")
        

        #f.write("All," + repr(dat19t) + "," + repr(reg19t) + "," + repr(dth19Ct) + "," + "{:.2f}".format(100.0*cov19datt) + "," + repr(datbase14t) + "," + repr(datpand14t) + "," + repr(xs14t)+ "," + "{:.2f}".format(xs14pct) + "," + "{:.1f}".format(Pscore14t*100.0)+"\n")
        #f.close()

        COV19May=331915;COV19June=399493;
        #National extrapolations: based on mortality and based on surge
        xs14nat=int(round(xs14pct*(pop20t+(1.0+surge_diff)*(pop20nat-pop20t))));
        xs15nat=xs14nat+int(round(xsjunepct*(pop20t+(1.0+surge_diff)*(pop20nat-pop20t))));
        xs14natP=int(round(14.0/12.0*Pscore14t*(1.0+exp_dthrise)*(dth19Ct+(1.0+surge_diff)*(dth19natC-dth19Ct))))
        xs15natP=xs14natP+int(round(1.0/12.0*Pscorejunet*(1.0+exp_dthrise)*(dth19Ct+(1.0+surge_diff)*(dth19natC-dth19Ct))))
        xs14natpc=float(xs14nat)/float(pop20nat);xs15natpc=float(xs15nat)/float(pop20nat);
        xs14natPpc=float(xs14natP)/float(pop20nat);xs15natPpc=float(xs15natP)/float(pop20nat);
        xs14natsurge=float(xs14nat)/((1.0+exp_dthrise)*float(dth19natC)*14/12)*100;
        xs15natsurge=float(xs15nat)/((1.0+exp_dthrise)*float(dth19natC)*15/12)*100;
        xs14natPsurge=float(xs14natP)/((1.0+exp_dthrise)*float(dth19natC)*14/12)*100;
        xs15natPsurge=float(xs15natP)/((1.0+exp_dthrise)*float(dth19natC)*15/12)*100;
        xs14natPY=float(xs14nat)/((1.0+exp_dthrise)*float(dth19natC))*100;
        xs15natPY=float(xs15nat)/((1.0+exp_dthrise)*float(dth19natC))*100;
        xs14natPPY=float(xs14natP)/((1.0+exp_dthrise)*float(dth19natC))*100;
        xs15natPPY=float(xs15natP)/((1.0+exp_dthrise)*float(dth19natC))*100;
        xs14natCOV19=float(xs14nat)/COV19May;xs15natCOV19=float(xs15nat)/COV19June;
        xs14natPCOV19=float(xs14natP)/COV19May;xs15natPCOV19=float(xs15natP)/COV19June;

        f1.write (",May(m),June(m),May(p),June(p)\n")
        f1.write ("Excess," + repr(xs14nat) + "," + repr(xs15nat) + "," + repr(xs14natP) + "," + repr(xs15natP)+"\n")
        f1.write ("Excess per 1K," + "{:.1f}".format(xs14natpc) + "," + "{:.1f}".format(xs15natpc) + "," +  "{:.1f}".format(xs14natPpc) + "," +  "{:.1f}".format(xs15natPpc)+"\n");
        f1.write ("P-score," + "{:.0f}".format(xs14natsurge) + "," + "{:.0f}".format(xs15natsurge) + "," + "{:.0f}".format(xs14natPsurge) + "," + "{:.0f}".format(xs15natPsurge)+"\n");
        f1.write ("Excess as a % of yearly deaths," + "{:.0f}".format(xs14natPY) + "," + "{:.0f}".format(xs15natPY) + "," + "{:.0f}".format(xs14natPPY) + "," + "{:.0f}".format(xs15natPPY)+"\n");
        f1.write ("Ratio of excess to COVID-19 deaths," + "{:.1f}".format(xs14natCOV19) + "," + "{:.1f}".format(xs15natCOV19) + "," + "{:.1f}".format(xs14natPCOV19) + "," + "{:.1f}".format(xs15natPCOV19)+"\n");

### End of loop
        
f1.close()
file.close()
file1.close()

