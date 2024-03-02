# UBC Flow

## Description

Have you ever wanted to take an upper-year course but realized you never took a pre-requisite that now jeopardizes your whole degree? We present UBC FLOW, a generative AI-powered, academic advising service.

**Motivation**

The problem our team decided to tackle using UBC Flow was streamlining the creation of timetables geared towards each student's career interests. While the SSC has all the available resources needed, it can be difficult to navigate the interface to satisfy prerequisites and find optimal course descriptions and professors. With our new technology, users can now create their ideal timetable with the click of a button, providing what interests they may have and what they hope to pursue in the future. They can specify course content and times to suit their individual needs best. On top of that, our AI bot will help ensure students can receive timely academic advising, slightly relieving the pressure of busy academic advisors. 

We utilized a basic web scraper to grab data from the UBC SSC, sorting based on course codes and sections. Our scraped data is processed initially as a JSON file, which will be then passed into PG Vector format in a Vector Database. We take in the user configuration data (prompt, interests, courses etc) and pass this information to the Langchain API. This is given to Amazon Bedrock and our chosen Formation Model, Anthropic Claude. This choice was due to the model's extensive token limits, allowing us to pass all of our data accurately, as we needed to pass in thousands of tokens. Finally, the response is passed through the Streamlit UI for the user to receive their prescribed academic advising. 

## Impact

For usage, students can ask course questions related to the computer science field (ie CPSC, DSCI, MATH, STATS, etc). Our web scraping stores course names, sections, timings and professors, allowing our generative AI to adapt and respond, providing students with the most accurate answer to their queries. 

    ```
## Credits

alberto-escobar
stevenxu27
montajesaj1
