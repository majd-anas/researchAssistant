welcome to your research assistant program 
this project was done by Majd anas 0234815

1-what is the program?
*******************************
WARNING: project must be run inside the project folder[researchAssistant folder]
program should be exited by exit comman (7) to not miss user info
*******************************
this is a research assistant, it gets you research papers from google scholar and into folders with the click of a button.
you choose your own parameters to filter your search and can get up to 20 research papers at once
papers are stored into folders, each folder can be saved to an .CSV file openable by excel. this allows you to view and edit your 
search results with ease 

each paper has a title, number of citations, a list of authors and a short snippet about the paper content
you can manage your folders and papers in your library by performing a set of operations on them

this program comes with previous data: lib.pkl to store the library object and load it keeping user information after exiting the program
(it has some folders stored already you can view them by running the program)

the csv folders contains csv files of folders that were stored into that format

2-how to run the program?

run the main.py file, a ui in the terminal will open where you can choose the operation you want by inputing its number
an operation can be exited by inputting -1


3-external libraries

this program makes use of the Serpapi library to scrape results from google(google scholar)
its documentation can be found here: https://serpapi.com/search-api?gad_source=1&gad_campaignid=22795996758&gclid=CjwKCAjw2rrQBhBuEiwAarLWHaF4uKJkyN2lZ123tJYbjIR_PLmE57WI6FaygcoRMFlg_e-vxPkjZRoCBfsQAvD_BwE


