create database Samsung

use Samsung

CREATE TABLE Estudiantes (
    EstudianteID INT PRIMARY KEY,
    Nombre VARCHAR(100),
    Apellido VARCHAR(100),
    Usuario VARCHAR(50) UNIQUE,
    Contraseña VARCHAR(100)
);

CREATE TABLE Profesores (
    ProfesorID INT PRIMARY KEY,
    Nombre VARCHAR(100),
    Apellido VARCHAR(100),
    Usuario VARCHAR(50) UNIQUE,
    Contraseña VARCHAR(100)
);

-- Luego, volver a crear la tabla con la columna CalificacionID como identidad
CREATE TABLE Calificaciones (
    CalificacionID INT PRIMARY KEY IDENTITY,
    EstudianteID INT,
    ProfesorID INT,
    CursoID INT,
    Calificacion FLOAT,
    FOREIGN KEY (EstudianteID) REFERENCES Estudiantes(EstudianteID),
    FOREIGN KEY (ProfesorID) REFERENCES Profesores(ProfesorID),
    FOREIGN KEY (CursoID) REFERENCES Cursos(CursoID)
);

Select * from Calificaciones

CREATE TABLE Cursos (
    CursoID INT PRIMARY KEY,
    Nombre VARCHAR(100)
);

INSERT INTO Cursos (CursoID, Nombre) VALUES (1, 'Ciencias');
INSERT INTO Cursos (CursoID, Nombre) VALUES (2, 'Tecnología');
INSERT INTO Cursos (CursoID, Nombre) VALUES (3, 'Medio Ambiente');
INSERT INTO Cursos (CursoID, Nombre) VALUES (4, 'Arte');
INSERT INTO Cursos (CursoID, Nombre) VALUES (5, 'Matemáticas');
INSERT INTO Cursos (CursoID, Nombre) VALUES (6, 'Artes');
INSERT INTO Cursos (CursoID, Nombre) VALUES (7, 'Física');
INSERT INTO Cursos (CursoID, Nombre) VALUES (8, 'Química');
INSERT INTO Cursos (CursoID, Nombre) VALUES (9, 'Lengua');
INSERT INTO Cursos (CursoID, Nombre) VALUES (10, 'Historia');

CREATE TABLE Calificaciones (
    CalificacionID INT PRIMARY KEY,
    EstudianteID INT,
    ProfesorID INT,
    CursoID INT,
    Calificacion FLOAT,
    FOREIGN KEY (EstudianteID) REFERENCES Estudiantes(EstudianteID),
    FOREIGN KEY (ProfesorID) REFERENCES Profesores(ProfesorID),
    FOREIGN KEY (CursoID) REFERENCES Cursos(CursoID)
);



