#
# Weight factor for each media
# Algorithm: For the 1st order approximation, those weight factors are drawn from empirical experience.
#            In future, those weight factors shall be derived by actually regression of collected data.
#
# "gg index en", "gg index hk", "gg news","gg site", "bd index ch", "bd index en", "bd news ch", "bd news en", "bd site", "yh index en", "yh index jp"
wf_china_marketing_list = [3, 4, 2, 3, 8, 2, 7, 2, 7, 0, 0] # list of weight factors for China marketing
wf_asia_marketing_list =  [6, 3, 6, 6, 6, 4, 5, 2, 6, 4, 3] # list of weight factors for Asia marketing
wf_japan_marketing_list = [5, 2, 5, 5, 1, 1, 1, 2, 1, 8, 6] # list of weight factors for Japan marketing

