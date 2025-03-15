# Certification Exam Practice

This project is designed to provide a platform for users to practice for certification exams. It includes features for user authentication, exam management, and a user-friendly interface built with Streamlit.

## Project Structure

```
certification_exam_practice/
├── app/
│   ├── auth/                # Authentication module
│   ├── database/            # Database module
│   ├── exams/               # Exam logic module
│   ├── ui/                  # User interface module
│   └── utils/               # Utility functions
├── scripts/                 # SQL scripts for database setup
├── docker/                  # Docker configuration
├── .env                     # Environment variables
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

## Features

- **User Authentication**: Secure login and registration processes.
- **Exam Management**: Create, manage, and take certification exams.
- **User Interface**: Intuitive UI built with Streamlit for a seamless user experience.
- **Database Integration**: PostgreSQL database for storing user and exam data.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/certification_exam_practice.git
   cd certification_exam_practice
   ```

2. Set up a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Configure the database connection in the `.env` file.

4. Run the database setup scripts:
   ```
   psql -U yourusername -f scripts/create_db.sql
   psql -U yourusername -f scripts/seed_db.sql
   ```

5. Start the application:
   ```
   python app/main.py
   ```

## Usage

- Access the application through your web browser at `http://localhost:5000`.
- Follow the prompts to register or log in and start taking exams.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.




Cosas que tengo pendientes de hacer en el proyecto::
- Cargar datos de preguntas y demas de la certificacion
- Las pruebas del login y la parte de auth las tenemos.
- Mejorar la parte de los examenes, todas las funciones tendran que estar autenticadas.
- Incluir funciones nuevas que tengan sentido:
   - Listar certifiaciones.
   - Crear certificaciones.
   - Crear preguntas para una certifiacion
   - Crear un examen
   - Subir las respuestas de un examen.
   - ETC.

Con esto quedaria lista la aplicacion, mejorariamos el redmine, probariamos que se ejecuta todo en docker sin el mayor problema y podriamos subirla a git