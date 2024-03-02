# UBC Flow

## Description

Have you ever wanted to take an upper-year course but realized you never took a pre-requisite that now jeopardizes your whole degree? We present UBC FLOW, a generative AI-powered, academic advising service.

## Motivation

The problem our team decided to tackle using UBC Flow was streamlining the creation of timetables geared towards each student's career interests. While the SSC has all the available resources needed, it can be difficult to navigate the interface to satisfy prerequisites and find optimal course descriptions and professors. With our new technology, users can now create their ideal timetable with the click of a button, providing what interests they may have and what they hope to pursue in the future. They can specify course content and times to suit their individual needs best. On top of that, our AI bot will help ensure students can receive timely academic advising, slightly relieving the pressure of busy academic advisors. 

We utilized a basic web scraper to grab data from the UBC SSC, sorting based on course codes and sections. Our scraped data is processed initially as a JSON file, which will be then passed into PG Vector format in a Vector Database. We take in the user configuration data (prompt, interests, courses etc) and pass this information to the Langchain API. This is given to Amazon Bedrock and our chosen Formation Model, Anthropic Claude. This choice was due to the model's extensive token limits, allowing us to pass all of our data accurately, as we needed to pass in thousands of tokens. Finally, the response is passed through the Streamlit UI for the user to receive their prescribed academic advising. 

## Potential Impact

For usage, students can ask course questions related to the computer science field (ie CPSC, DSCI, MATH, STATS, etc). Our web scraping stores course names, sections, timings and professors, allowing our generative AI to adapt and respond, providing students with the most accurate answer to their queries. Due to time constraints, we limited our scraping data only to computer science-related classes, but this technology would be easily applicable across all faculties with the proper storage and optimization. This can help save students tons of time during their course selections, as well as provide early education and awareness of course prerequisites. It allows academic advisors more time to deal with difficult questions, as simpler queries can be answered beforehand by our bot. \\

## Challenges

The biggest challenge we faced was time constraints, as a nine-hour hackathon meant you couldn't be too ambitious. This made many design decisions difficult, as sometimes it would be easier to hard code for demo purposes instead of the optimal implementation. Getting familiarized with Amazon Bedrock was also interesting, as most of us didn't have much experience with AI and cloud computing beforehand. 

## Roadmap

We weren't able to implement many functionalities due to time constraints, but there were a few ideas we could have attempted. The first was scraping all course data, allowing students of any faculty to access this tool. We could also utilize additional web resources such as RateMyProf to allow the ranking of courses based on the professor or add mapping functions to determine commute times and classroom locations. A final functionality is storing your user data and linking your SSC with your completed courses/grade requirements using an application such as Auth0, allowing the user to keep their history and add on to previous conversations. 

## Credits

alberto-escobar
stevenxu27
montajesaj1
