Initial_data = LOAD 'optimised_wea_pred_BD/part*' as (location, temp_date, act_temp, pred_temp);


Remove_u = FOREACH Initial_data GENERATE REPLACE(location, '[u"]', '') ;

STORE Remove_u INTO 'output1.txt';

Sec_data = LOAD 'output1.txt' as (location, temp_date, act_temp, pred_temp);

Remove_char = FOREACH Sec_data GENERATE REPLACE(location,'[\\\'\\(\\)]+','');

STORE Remove_char INTO 'output2.txt';

final_data = LOAD 'output2.txt' as (location, temp_date, act_temp, pred_temp);

B = FOREACH final_data GENERATE REPLACE(location, '[-]', ' ') ;

STORE B INTO 'output_final.txt';
