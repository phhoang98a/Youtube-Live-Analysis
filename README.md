# Youtube-Live-Analysis
Crawl live chat comments from a live YouTube video, analyze their sentiment, and display the video stream and real-time comments in a React frontend.

## Tech Stack
<img src="https://github.com/user-attachments/assets/e6c74701-3208-4ffe-ac2a-cd6b6cd9bfd9" height=100 />
<img src="https://github.com/user-attachments/assets/ed708e2f-ed22-4739-b106-290677f7b395" height=100 />
<img src="https://github.com/user-attachments/assets/73eea9d1-ce9d-4488-9729-b1e37bf06d16" height=100 />
<img src="https://github.com/user-attachments/assets/6f341224-3cb6-4d82-9a34-42cca89f2d98" height=100 />
<img src="https://github.com/user-attachments/assets/7b8cad2a-a5d8-4c64-99de-839a70ba44c2" height=100 />
<img src="https://github.com/user-attachments/assets/c0841552-e117-4b18-8e99-4225effe8602" height=100 />
<img src="https://github.com/user-attachments/assets/20af4151-275c-4b09-ad63-974afa3cacc7" height=100 />

## Architecture
![Diagram drawio (1)](https://github.com/user-attachments/assets/2689e492-eadb-49b9-9c98-f9cc69fe61c8)

## Demo
https://github.com/user-attachments/assets/b547d259-72c5-425f-8899-efff8f4d30f2

Green: Positive, Red: Negative, Blue: Neutral

## Setup Instructions
- Git clone
```bash
git clone https://github.com/phhoang98a/Youtube-Live-Analysis.git
```
- Start up all the services defined in the `docker-compose.yml` file
```bash
docker-compose up -d                                                     
```
- Create a ``.env``  and fill in your settings (Refer to `.example-env`)
- Run `bash run_all.sh` from cmd to start all services.
