"""
Created on Dec 2 2020

@author: Changze Han
"""

'''
    For Volatility project 
        after splitting Volatility data into two parts, calcualte the co-vol separately for each part
        then for specific positions, do a fisher test between two parts
    
    
    Input: two rows of co-volatility data. 
    
    steps: 
        convert two columns of co-volatility to 2 rows
        copy to this program as 2 inputs
        convert value to 0 and 1 based on threshold 
        build a confusion matrix out of it
        then perform 2x2 fisher test on the matrix 
        
'''
import re
from sklearn.metrics import confusion_matrix
import scipy.stats as stats

# Inputs ================================================================================================
part1_values = "0.81443299	0.012133227	0.169873795	0.224961932	0.147348465	0.239475605	0.117602589	0.260708322	0.187516392	0.244918232	0.039010878	0.074307738	0.22818868	0.187739852	0.41081897	0.433642246	0.661726804	0.41081897	0.197744559	0.268684827	0.232634164	0.294566546	0.536346989	0.268684827	0.065300818	0.268424036	0.260708322	0.22564996	0.169628554	0.236268342	0.189151336	0.169628554	0.061015263	0.089175885	0.81443299	0.81443299	0.305412371	0.003751046	0.81443299	0.18556701	1	1	1	0.661726804	1	0.294272276	0.22564996	0.349711489	0.169873795	0.305412371	0.349711489	1	1	0.305412371	0.18556701	1	0.376139447	0.81443299	0.268424036	0.048256006	0.281289676	0.034532617	0.317385081	0.433642246	0.048256006	0.81443299	1	0.232634164	1	1	0.661726804	0.81443299	0.81443299	0.81443299	0.18556701	0.536346989	0.419653787	0.661726804	0.661726804	0.017317932	1	0.41081897	0.81443299	0.309212196	0.023307122	0.419653787	0.063245045	0.281289676	0.389478013	0.22564996	1	0.185049331	0.305412371	0.349711489	0.158708643	0.81443299	0.419653787	0.661726804	0.235590245	0.18556701	0.232634164	0.310332079	1	0.18556701	0.305412371	0.268424036	0.305412371	0.127252876	0.376139447	0.294566546	1	0.81443299	0.18556701	0.039010878	0.661726804	0.81443299	0.410530878	1	0.81443299	0.661726804	0.419653787	1	1	0.18556701	0.376139447	0.81443299	0.433642246	0.281289676	0.661726804	0.208776802	0.18556701	0.116061642	0.053068077	0.099102727	0.000224877	0.032411725	0.041871992	0.009684126	0.058449982	0.036263961	0.005932893	0.035526492	0.043516753	0.208529491	0.134105699	0.005932893	0.202579315	0.108182	0.205160532	0.05800945	0.175637431	0.162008947	0.023943114	0.047957351	0.309212196	0.095439657	0.81443299	0.41081897	1	0.252220144	0.063055036	0.095439657	0.316574391	0.197251567	0.011565583	0.07333472	0.270038544	0.236268342	0.013855679	0.116114135	0.142474341	0.135117934	0.048256006	1	0.310332079	0.136050438	0.661726804	0.152665698	0.067631524	1	0.116061642	0.15763759	0.209688201	0.309212196	0.16059754	0.124513521	0.187069041	0.121966534	0.212026233	0.162008947	0.136050438	0.268424036	0.661726804	0.158708643	0.260708322	1	0.065300818	0.410530878	0.661726804	0.316574391	0.310332079	0.41081897	0.41081897	0.376139447	0.81443299	0.81443299	1	0.178701978	0.419653787	1	0.410530878	1	0.81443299	0.18556701	0.18556701	0.536346989	0.661726804	0.81443299	0.158708643	1	0.305412371	1	0.81443299	0.376139447	0.41081897	0.41081897	0.433642246	1	0.232634164	0.08566072	0.316574391	0.049740704	0.81443299	0.116114135	0.81443299	0.214022124	0.81443299	0.242326505	1	0.162008947	0.095439657	0.419653787	0.032860825	0.232634164	0.305412371	0.81443299	1	0.661726804	0.032860825	1	0.536346989	0.0976323	1	0.419653787	0.065300818	0.661726804	0.536346989	0.305412371	0.136050438	0.81443299	1	0.305412371	0.661726804	0.305412371	0.305412371	0.41081897	0.41081897	0.155774375	0.100235054	0.175509693	0.147348465	0.023943114	0.376139447	0.136050438	0.067631524	0.197589179	0.095439657	0.116114135	0.007558197	0.433642246	0.127252876	0.00536528	0.661726804	0.136050438	0.410530878	0.039010878	1	0.128582669	0.217332974	0.049740704	0.252220144	0.13816914	0.410530878	0.114416782	1	0.049740704	0.661726804	0.349711489	0.178701978	0.328586908	0.349711489	0.41081897	0.536346989	0.017124396	0.008816172	0.127252876	0.191152033	0.023338311	0.81443299	0.376139447	0.039010878	0.235590245	0.410530878	0.202042066	0.134647737	0.0976323	0.296645283	0.197589179	0.389478013	0.261967706	0.310332079	0.0976323	1	0.074307738	0.187739852	0.305412371	0.233933799	0.81443299	0.213726567	0.661726804	0.114416782	0.158708643	0.100291253	0.003569375	0.012071735	0.005285913	1	0.030006885	0.106677405	0.263684696	0.81443299	0.11557095	0.036425362	0.039653428	0.063245045	0.05440869	0.08197911	0.81443299	0.036393606	0.062418167	0.197589179	0.316574391	0.085289592	0.271558461	0.233933799	0.162008947	0.218306422	0.389478013	0.060656244	0.41081897	0.019088021	0.216589955	0.213726567	0.063055036	1	0.661726804	1	0.309212196	0.661726804	0.294272276	0.116114135	0.209688201	0.018605188	0.296645283	0.305412371	0.536346989	1	0.361039935	0.536346989	0.661726804	0.376139447	0.305412371	0.18556701	1	0.168174325	0.188080048	0.100235054	0.085289592	0.376139447	0.305412371	0.168174325	0.116114135	0.228166799	0.232634164	0.130596912	0.068213938	0.193708232	0.130596912	0.149497035	0.168816096	0.077617552	0.041871992	0.071828302	0.035526492	0.015358854	0.07896185	0.061245448	0.051823072	0.058449982	0.016190503	7.81364E-05	0.12522519	0.095439657	0.07333472	0.419653787	0.22564996	0.18556701	0.296645283	0.18556701	0.376139447	0.18556701	0.328586908	0.158708643	0.305412371	0.294272276	1	0.81443299	0.178701978	0.433642246	0.661726804	0.002054921	0.661726804	0.294566546	0.81443299	0.661726804	0.08197911	1	0.41081897	0.100291253	0.661726804	0.008228251	0.81443299	0.009425154	0.81443299	0.033723234	0.81443299	0.15763759	0.661726804	0.81443299	1	0.294272276	0.235590245	0.433642246	0.41081897	0.376139447	0.81443299	1	0.361039935	0.006022312	0.036263961	0.02910784	0.112134984	0.029989551	0.118785144	0.536346989	0.036425362	0.305412371	0.305412371	1	0.309212196	0.661726804	0.81443299	0.309212196	0.376139447	0.310332079	0.661726804	0.661726804	0.81443299	0.349711489	0.536346989	0.316574391	0.81443299	0.376139447	0.536346989	1	1	0.294272276	0.536346989	0.197589179	0.114553657	0.410530878	0.81443299	0.389478013	0.661726804	0.239475605	0.349711489	0.81443299	0.361039935	0.096524808	0.349711489	0.317385081	1	0.661726804	0.41081897	0.433642246	0.310332079	0.361039935	0.22564996	0.41081897	0.81443299	0.136050438	0.023943114	0.187739852	0.15763759	0.661726804	0.294566546	0.084814277	0.268424036	0.410530878	1	0.08197911	1	0.81443299	0.180519968	1	0.305412371	0.81443299	0.389478013	0.536346989	1	0.661726804	0.661726804	0.281289676	0.185049331	0.419653787	0.18556701	0.305412371	0.005534455	0.661726804	0.433642246	1	0.232634164	0.661726804	0.433642246	0.187739852	0.305412371	0.661726804	0.376139447	0.18556701	0.81443299	0.661726804	0.063055036	0.536346989	0.536346989	0.536346989	0.389478013	0.661726804	1	0.376139447	0.305412371	1	0.41081897	0.389478013	0.536346989	0.536346989	0.536346989	0.032860825	1	0.536346989	1	1	1	1	0.18556701	0.81443299	0.81443299	0.81443299	0.81443299	0.41081897	0.81443299	0.81443299	0.158708643	0.41081897	0.281289676	0.419653787	1	0.316574391	0.41081897	0.81443299	0.661726804	1	0.349711489	0.81443299	0.433642246	1	1	0.661726804	0.536346989	0.661726804	0.127252876	0.389478013	0.661726804	0.81443299	0.361039935	1	0.226702823	0.81443299	0.376139447	1	0.410530878	0.062418167	0.389478013	1	0.305412371	0.389478013	0.263684696	0.22818868	0.294566546	0.1580406	0.06292923	0.81443299	0.536346989	0.205558423	0.232634164	0.294566546	1	1	0.309212196	0.389478013	1	0.232634164	0.252019565	0.009540704	0.18556701	0.063055036	0.158708643	0.81443299	0.81443299	0.193708232	0.100291253	0.18556701	0.661726804	0.227583997	1	0.268424036	0.376139447	0.242326505	0.232634164	0.81443299	0.071837177	1	1	1	0.158708643	0.81443299	0.661726804	0.127252876	0.100235054	0.81443299	0.81443299	0.003298654	0.81443299	0.433642246	0.294566546	1	0.317385081	0.152665698	0.433642246	0.81443299	0.268684827	1	0.18556701	0.198512673	0.661726804	0.187739852	0.147348465	1	0.661726804	0.661726804	0.81443299	1	0.024690225	0.22564996	0.433642246	0.18556701	0.185049331	0.095439657	0.047957351	0.18556701	0.039010878	0.305412371	0.122372458	0.81443299	0.536346989	0.410530878	0.661726804	0.084814277	0.260708322	0.056605641	0.188080048	0.158708643	0.433642246	0.15763759	0.28016499	0.023943114	0.22818868	0.232634164	1	0.536346989	0.536346989	0.661726804	0.81443299	0.81443299	0.389478013	0.039010878	0.268424036	0.81443299	0.376139447	0.197589179	0.067631524	0.536346989	0.28016499	0.049740704	0.232634164	0.271558461	0.294272276	0.349711489	0.376139447	0.08197911	0.188080048	0.114553657	0.316574391	0.235590245	0.263684696	0.268424036	0.376139447	0.81443299	0.361039935	0.317385081	0.252220144	0.317385081	0.135117934	0.017317932	0.389478013	0.070164538	0.047957351	0.232634164	0.361039935	0.19647578	1	0.389478013	0.661726804	0.188080048	0.039010878	0.268424036	0.661726804	0.067631524	1	0.305412371	0.419653787	0.328586908	0.349711489	0.158708643	0.361039935	0.536346989	0.361039935	0.536346989	0.268424036	0.024690225	0.376139447	0.41081897	0.41081897	0.349711489	0.22564996	0.536346989	0.187739852	0.116114135	0.084814277	0.232634164	0.271558461	0.41081897	0.41081897	0.135117934	0.81443299	0.376139447	0.235590245	0.81443299	0.661726804	0.305412371	0.127252876	0.01603565	0.232634164	0.268424036	0.305412371	0.410530878	0.095439657	0.317385081	0.376139447	0.81443299	0.136050438	0.661726804	0.032860825	0.263684696	0.419653787	1	0.018605188	0.271558461	0.221812059	0.81443299	0.419653787	0.07333472	0.296645283	0.536346989	0.131900642	0.128582669	0.027209509	0.209688201	0.361039935	0.188080048	0.24043196	0.281289676	0.065300818	0.180519968	0.41081897	0.032860825	0.661726804	0.536346989	0.100235054	0.309212196	0.328586908	0.121966534	0.052441025	0.410530878	0.111988321	0.116061642	0.226702823	0.232634164	0.389478013	0.178701978	0.271558461	0.047957351	0.252220144	1	0.317385081	1	0.389478013	0.81443299	0.41081897	0.305412371	0.316574391	0.661726804	0.039010878	0.154661328	0.419653787	0.188080048"
part2_values = "0.600651112	0.10990858	0.208833891	0.264743671	0.255941452	0.264743671	0.22781879	0.078619629	0.260950709	0.078619629	0.423382768	0.071322036	0.246619282	0.383394327	0.337866251	0.337866251	0.383394327	0.504802531	0.231545988	0.185849459	0.414178794	0.295943139	0.264175258	0.18410268	0.254407259	0.170101808	0.315104392	0.002458501	0.225608911	0.085822147	0.18719857	0.110802539	0.079708601	0.349524263	0.504802531	1	0.600651112	0.504802531	1	1	0.845360825	1	0.845360825	1	1	0.085822147	0.223019351	0.40886881	0.291098245	0.40886881	0.100641011	1	1	0.845360825	0.713273196	0.845360825	0.309349061	0.504802531	0.095710853	0.095710853	0.205054235	0.215109698	0.302699986	0.407098815	0.137542521	1	0.845360825	0.254407259	1	1	0.713273196	0.713273196	1	0.845360825	1	0.845360825	1	0.407098815	1	0.315104392	0.845360825	0.504802531	0.600651112	0.041515171	0.017198439	0.374085428	0.107812313	0.315104392	0.295943139	0.27931712	0.845360825	0.074556935	1	0.223019351	0.713273196	1	0.111481833	0.845360825	0.187048269	0.845360825	0.423382768	0.600651112	1	0.713273196	0.394590851	0.295943139	0.337866251	0.100641011	0.264175258	0.205054235	1	1	0.264175258	0.383394327	0.003086001	0.845360825	0.185849459	1	0.154639175	0.100641011	0.264175258	0.845360825	0.845360825	1	0.337866251	0.845360825	0.713273196	0.185849459	0.845360825	0.128219565	0.154639175	0.245406838	0.137973178	0.224174258	0.184153403	0.116585275	0.184153403	0.229814796	0.194143482	0.122193352	0.247064202	0.247376152	0.229814796	0.190520979	0.131393779	0.199081483	0.199081483	0.170229967	0.220249917	0.202158536	0.21948641	0.186618267	0.309349061	0.16568299	0.407098815	0.223019351	0.264175258	0.600651112	0.845360825	0.144728965	0.255941452	0.309349061	0.052171301	0.107812313	0.291098245	0.14106494	3.76704E-05	0.270730693	0.225558967	0.171107798	0.109785628	0.026060688	0.187048269	0.713273196	0.322606878	0.407098815	0.246619282	0.072099858	0.111481833	0.845360825	0.22781879	0.213125501	0.054175084	0.187048269	0.017758395	0.124904047	0.173849267	0.209470627	0.055428929	0.039701845	0.383394327	0.185849459	0.713273196	0.27696261	0.08590375	1	0.383394327	0.600651112	0.600651112	0.322606878	0.185849459	0.264175258	0.058396636	0.713273196	0.845360825	1	1	0.111481833	0.383394327	0.713273196	0.144288188	0.845360825	0.600651112	1	0.845360825	0.337866251	0.264175258	0.845360825	0.111481833	1	0.154639175	0.154639175	0.264175258	0.713273196	0.144288188	0.383394327	0.713273196	0.845360825	0.309349061	0.270730693	0.266628713	0.110802539	0.713273196	0.194837937	0.264175258	0.270730693	1	0.074556935	1	0.072099858	0.407098815	0.264175258	0.845360825	0.383394327	0.600651112	0.845360825	1	1	0.845360825	0.845360825	0.713273196	0.163035316	1	0.845360825	0.383394327	0.713273196	0.713273196	1	0.600651112	1	1	1	1	1	0.383394327	0.504802531	0.170101808	0.017198439	0.235301293	0.240475824	0.123516212	0.22781879	0.713273196	0.600651112	0.111481833	0.03800517	0.22781879	0.026060688	0.010541104	0.100641011	0.004587423	0.163035316	0.337866251	0.423382768	0.100641011	0.354352969	1	0.085807214	0.055428929	0.00410152	0.40886881	0.085312712	0.600651112	0.15127494	0.845360825	0.245406838	0.845360825	0.264175258	0.024690225	0.144288188	0.383394327	0.337866251	0.000776333	0.097408825	0.124402046	0.407098815	0.18410268	0.161148321	0.713273196	0.713273196	0.504802531	0.297567954	0.845360825	0.085312712	0.302699986	0.163035316	0.27931712	0.309349061	0.246619282	0.001957634	0.187048269	0.22781879	0.600651112	0.229814796	0.14077391	0.407098815	0.247376152	0.264175258	0.260950709	1	0.024690225	0.309349061	0.024690225	0.202158536	0.061879877	0.116585275	1	0.176543417	0.116585275	0.10990858	0.713273196	0.018924856	0.223130536	0.049958445	0.002561456	0.209470627	0.349524263	0.845360825	0.170229967	0.142998908	0.064411262	0.297567954	0.00523645	0.060558181	0.047321391	0.005350626	0.270038544	0.40886881	0.131393779	0.394590851	0.000625586	0.085807214	0.010541104	0.223019351	1	1	0.845360825	0.315104392	0.600651112	0.018546648	0.315441402	0.060558181	0.337866251	0.349524263	0.845360825	0.40886881	0.845360825	0.137542521	1	0.845360825	0.845360825	1	1	1	0.15127494	0.315441402	0.27696261	0.205698429	0.713273196	0.264175258	0.018824919	0.040407566	0.047321391	0.002458501	0.052668073	0.031945668	0.027355019	0.082301307	0.215547195	0.215547195	0.165957641	0.146927449	0.171950945	0.015508256	0.094413383	0.010205433	0.061447807	0.000257815	0.136845778	0.101825999	0.037951454	0.131393779	0.208833891	0.067776465	0.414178794	0.104416946	0.845360825	0.161148321	0.600651112	0.414178794	0.845360825	0.322606878	0.394590851	0.845360825	0.163035316	0.845360825	0.845360825	0.315441402	0.713273196	0.845360825	0.394590851	0.845360825	0.185849459	1	0.713273196	1	0.845360825	0.144288188	0.003971167	1	0.20920099	0.504802531	0.197118494	1	0.170660262	1	0.243601418	0.713273196	0.845360825	1	0.407098815	0.026060688	0.154639175	0.137542521	0.713273196	1	0.845360825	0.058396636	0.000343754	0.002556303	0.015110591	0.027355019	0.000901814	0.021544251	0.383394327	0.170229967	0.845360825	0.337866251	1	0.394590851	1	0.845360825	0.104416946	0.713273196	0.123516212	0.600651112	1	0.713273196	0.600651112	0.504802531	0.297567954	1	0.154639175	0.354352969	1	1	0.185849459	0.600651112	0.315441402	0.297567954	0.185849459	0.264175258	0.264175258	1	0.187048269	0.845360825	0.154639175	0.354352969	0.215958018	0.407098815	0.315104392	0.713273196	0.713273196	0.383394327	0.713273196	0.713273196	0.337866251	0.600651112	0.374085428	0.713273196	0.08590375	0.208833891	0.26662309	0.123516212	0.383394327	0.414178794	0.239182943	0.713273196	0.414178794	0.845360825	0.337866251	0.713273196	0.845360825	0.374085428	0.845360825	0.845360825	0.264175258	0.337866251	1	0.713273196	0.154639175	1	0.845360825	0.213125501	0.295943139	0.154639175	1	0.383394327	0.845360825	0.144288188	0.713273196	0.116220321	0.600651112	0.713273196	0.504802531	0.845360825	0.713273196	0.845360825	0.264175258	1	1	0.22781879	0.713273196	0.264175258	0.504802531	0.254407259	0.600651112	0.845360825	0.600651112	0.264175258	1	0.264175258	0.713273196	0.383394327	1	0.713273196	1	0.845360825	0.845360825	1	0.264175258	0.058396636	1	1	0.713273196	0.713273196	0.845360825	0.845360825	0.354352969	1	1	0.40886881	0.264175258	0.254407259	0.504802531	0.504802531	0.243601418	0.845360825	0.600651112	1	0.845360825	0.264175258	0.264175258	0.504802531	1	0.504802531	1	0.713273196	0.713273196	1	0.354352969	0.845360825	1	0.407098815	0.845360825	0.264743671	0.383394327	0.600651112	1	0.100641011	0.064915218	0.383394327	1	0.383394327	0.00947835	0.142595952	0.264743671	0.161148321	0.176543417	0.122193352	0.154639175	0.845360825	0.096356585	0.394590851	0.40886881	1	1	0.40886881	0.322606878	0.845360825	0.600651112	0.040407566	0.423382768	0.713273196	0.053021593	0.600651112	1	0.264175258	0.128219565	0.27696261	0.845360825	0.845360825	0.215958018	0.154639175	0.600651112	0.058396636	0.235301293	0.383394327	0.144288188	0.123516212	0.845360825	1	0.845360825	0.322606878	0.264175258	0.383394327	0.246619282	0.309349061	0.845360825	0.713273196	0.170101808	0.337866251	0.337866251	0.354352969	1	0.08590375	0.207257947	0.845360825	0.713273196	0.22781879	1	1	0.170660262	0.154639175	0.297567954	0.207257947	0.713273196	1	0.845360825	0.504802531	0.154639175	0.221506931	0.163035316	0.845360825	1	0.302699986	0.100641011	0.297567954	0.383394327	0.504802531	0.600651112	0.315441402	0.845360825	0.414178794	0.414178794	0.713273196	0.270730693	0.383394327	0.094553705	0.137542521	0.205054235	0.504802531	0.111481833	0.170101808	0.600651112	0.187048269	0.383394327	0.713273196	0.504802531	0.713273196	0.845360825	0.154639175	0.264175258	0.264175258	0.600651112	0.383394327	0.845360825	0.845360825	0.0658406	0.297567954	1	0.260950709	0.315441402	0.185849459	0.144728965	0.297567954	0.383394327	0.407098815	0.337866251	0.052171301	0.02344683	0.187048269	0.137542521	0.0658406	0.185849459	0.337866251	0.154639175	0.08590375	0.123516212	0.137542521	0.254407259	0.213125501	0.291098245	1	0.0658406	0.322606878	0.414178794	0.374085428	0.187048269	0.845360825	0.394590851	0.600651112	0.22781879	0.383394327	0.337866251	0.713273196	0.111481833	0.264175258	0.010768174	0.03800517	0.297567954	1	0.294643068	0.383394327	0.600651112	0.27931712	0.407098815	0.414178794	0.309349061	1	0.27931712	0.407098815	0.600651112	0.026060688	0.383394327	0.208833891	0.053021593	0.14106494	0.407098815	0.22781879	0.144288188	0.254407259	0.394590851	0.154639175	0.600651112	0.022963223	0.337866251	0.713273196	0.144288188	0.123516212	0.15621636	0.154639175	0.297567954	0.504802531	0.374085428	0.040777096	0.085822147	0.423382768	0.423382768	0.06194982	0.154639175	1	0.161148321	0.713273196	0.713273196	0.40886881	0.052171301	0.25998146	0.504802531	0.295943139	0.27696261	0.322606878	0.713273196	0.27696261	0.225608911	0.161148321	0.079708601	0.297567954	0.223019351	0.20920099	0.254407259	0.423382768	0.423382768	0.264175258	0.504802531	0.264175258	0.022551546	0.060558181	0.185849459	0.010571553	0.00077981	0.011837032	0.27931712	0.243601418	0.221506931	0.243601418	0.322606878	0.026060688	0.315441402	0.123516212	0.085822147	0.297567954	0.010768174	0.040777096	0.337866251	0.297567954	0.154639175	0.264175258	0.713273196	0.111481833	0.600651112	0.383394327	0.309349061	0.264175258	0.504802531"

# cutoff for each part, >cutoff then 0, otherwise 1
part1_cutoff = 0.05
part2_cutoff = 0.05
# ========================================================================================================

# convert to list
part1_values = re.sub("\s+", ",", part1_values).split(',')
part1_values =[float(i) for i in part1_values]

part2_values = re.sub("\s+", ",", part2_values).split(',')
part2_values =[float(i) for i in part2_values]


# check len
if len(part1_values) != len(part2_values):
    raise Exception("ERROR: check length")

# apply cutoff
for i in range(len(part1_values)):
    if part1_values[i] > part1_cutoff:
        part1_values[i] = 0
    else:
        part1_values[i] = 1

for i in range(len(part2_values)):
    if part2_values[i] > part2_cutoff:
        part2_values[i] = 0
    else:
        part2_values[i] = 1


def main():


    data_matrix = confusion_matrix(part1_values, part2_values)
    print(f"\n  data_matrix: {data_matrix}")

    # calculate fisher exact p value:
    oddsratio, pvalue = stats.fisher_exact(data_matrix)
    print(f"  fisher exact test: {pvalue}")


main()


