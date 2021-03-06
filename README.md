ERCOT Sample Apps
=================

Bundled in this package is a sample application that demonstrates basic 
functionality of the Grok API.  Three models are created predicting 1, 4, and 
96 time steps ahead, representing 15 mins., 1 hr., and 1 day respectively using
the scraped data for training.

    python -m ercot.scraper "http://mis.ercot.com/misapp/GetReports.do?reportTypeId=12340&reportTitle=System-Wide%20Demand&showHTMLView=&mimicKey"
    system_wide_demand --key=YOUR_API_KEY_HERE "data/SYSWIDEDEMANDNP6235_csv/*"

Output will look something like this:

    data/SYSWIDEDEMANDNP6235_csv/201304* 2013-04-23T09:50:52 project created ( 18b0c03a-aaba-46a6-8605-34baefab544c )
    data/SYSWIDEDEMANDNP6235_csv/201304* 2013-04-23T09:50:52 stream created ( edbcc652-a790-4cd1-980f-d9668df27bed )
    Appending historical data to stream... Done.
    data/SYSWIDEDEMANDNP6235_csv/201304* 2013-04-23T09:50:52 model created ( ce86576f-6c4f-4d18-89cf-be336f852317 )
    data/SYSWIDEDEMANDNP6235_csv/201304* 2013-04-23T09:50:52 +1hr model created ( b2b1b024-c99e-49f4-a8d7-497a534fef41 )
    data/SYSWIDEDEMANDNP6235_csv/201304* 2013-04-23T09:50:52 +24hrs model created ( 6263f7ac-074b-44ee-a779-d4d8d26d0c39 )
    Swarming . . . . Done!

    Model                                                           | Error
    ----------------------------------------------------------------|-----------------
    data/SYSWIDEDEMANDNP6235_csv/201304* 2013-04-23T09:50:52        | 1494.50462972
    data/SYSWIDEDEMANDNP6235_csv/201304* 2013-04-23T09:50:52 +1hr   | 5.92383507901
    data/SYSWIDEDEMANDNP6235_csv/201304* 2013-04-23T09:50:52 +24hrs | 6.31714403344