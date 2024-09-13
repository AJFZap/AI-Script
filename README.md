# AI Script with Django

## Web-app that allows the user to get the full script and summary from a given youtube link.

This is a Django-based web application that allows the user to get the full script and summary VIA AI from a given youtube link. Simply input a YouTube link, and the app will process the request and provide the script and the summary and if the user is authenticated then it will be saved on the database. (Eventually it will accept more than just youtube videos.)

## Features

* Gets the full script from a video using AssemblyAI.
* Gets a summary from the created script using Cohere. (Can use OPENAI too since it's all set, just uncommenting OpenAI, commenting the CohereAI and making the prompt will do the trick).
* Simplistic user friendly interface.
* Error handling and validation for Links.
* Authentication and Registration for users if desired.
* Database implementation to store the users and their data, like the videos they provide with links and the summaries and scripts outputs.

## Prerequisites

* Python 3.11
* Django
* Pytubefix (Since pytube still has errors on it's cipher class)
* Assembly AI
* Cohere AI (Or OpenAI).
* Other dependencies listed in requirements.txt

## Technologies Used

* **Database:** Postgresql
* **Backend:** Django, pytubefix
* **Frontend:** Tailwind, HTML, CSS, JQuery, JS
* **Deployment:** Render

## Webpage to check it out!
[AI-Script](https://maximum-lynx-non-profit-14b62243.koyeb.app/)