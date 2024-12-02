# EasyApply - AI-Powered Job Application Assistant

EasyApply is an open-source web application that streamlines the job application process by helping users manage their job applications, customize resumes, and generate cover letters using AI assistance.

## Features

- **Application Tracking**: Keep track of all your job applications in one place
- **AI-Powered Cover Letters**: Generate customized cover letters using LangChain and OpenAI
- **Resume Management**: Create and maintain multiple versions of your resume
- **PDF Generation**: Export your resumes and cover letters as professional PDFs
- **User Authentication**: Secure user accounts and data protection

## Tech Stack

- **Backend**: Python Flask, SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: MySQL
- **AI Services**: LangChain, OpenAI API
- **Deployment**: Docker, Nginx, Gunicorn
- **Cloud Infrastructure**: AWS (EC2, RDS, Certificate Manager, ALB)

## Getting Started

### Prerequisites

- Python 3.8+
- Docker and Docker Compose
- MySQL
- OpenAI API key

### Local Development Setup

1. Clone the repository
```bash
git clone https://github.com/YourUsername/easy-apply.git
cd easy-apply
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database
```bash
flask db upgrade
```

6. Run the development server
```bash
flask run
```

### Docker Deployment

1. Build and run with Docker Compose
```bash
docker-compose up --build
```

## Configuration

The application requires the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `DATABASE_URL`: MySQL database connection string
- `SECRET_KEY`: Flask secret key
- `Other environment variables`: Check .env.example for all required variables

## Contributing

We welcome contributions! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/A
