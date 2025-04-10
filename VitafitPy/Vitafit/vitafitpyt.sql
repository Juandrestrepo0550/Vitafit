CREATE DATABASE IF NOT EXISTS vitafitpyt;

USE vitafitpyt;

CREATE TABLE IF NOT EXISTS usuarios (
    id bigint(12) NOT NULL AUTO_INCREMENT,
    nombres varchar(128) NOT NULL,
    apellidos varchar(128) NOT NULL,
    correo varchar(200) NOT NULL,
    nickname varchar(20) NOT NUll,
    Edad DATE NOT NULL,
    peso DECIMAL(5,2) NOT NULL,
    altura DECIMAL(5,2) NOT NULL,
    contrasena varchar(128) NOT NULL,
    rol enum('admin','user', 'trainer', 'nutricionista') NOT NULL DEFAULT 'user',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    recuperarcontraseña varchar(128) DEFAULT NULL,
    token varchar(128) DEFAULT NULL,
    token_expiracion TIMESTAMP DEFAULT NULL,
    estado enum('activo', 'inactivo') NOT NULL DEFAULT 'activo',
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS historial_personal_usuario (
    id BIGINT(12) UNSIGNED NOT NULL AUTO_INCREMENT,
    usuario_id BIGINT(12) NOT NULL,
    peso_anterior DECIMAL(5,2) NOT NULL,
    altura_anterior DECIMAL(5,2) NOT NULL,
    fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS rutinas (
    id BIGINT(12) NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(128) NOT NULL,
    descripcion varchar(255) NOT NULL,
    cantidad_ejercicios TINYINT(4) NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS ejercicios (
    id MEDIUMINT(6) NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(80) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    aporte_muscular Varchar(255) NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS planes_nutricionales (
    id MEDIUMINT(6) NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(80) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    cantidad_comidas TINYINT(4) NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS recetas (
    id BIGINT(10) NOT NULL AUTO_INCREMENT,
    ingredientes VARCHAR(255) NOT NULL,
    pasos VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS comidas (
    id BIGINT(12) NOT NULL AUTO_INCREMENT,
    descripcion VARCHAR(255) NOT NULL,
    numero_comida TINYINT(4) NOT NULL,
    id_receta BIGINT(10) NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (id_receta) REFERENCES recetas(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS usuarios_rutinas (
    id BIGINT(12) NOT NULL AUTO_INCREMENT,
    id_usuario BIGINT(12) NOT NULL,
    id_rutina BIGINT(12) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY (id_rutina) REFERENCES rutinas(id)
);



CREATE TABLE IF NOT EXISTS planes_comidas (
    id_plan MEDIUMINT(6) NOT NULL,
    id_comida BIGINT(12) NOT NULL,
    PRIMARY KEY (id_plan, id_comida),
    FOREIGN KEY (id_plan) REFERENCES planes_nutricionales(id),
    FOREIGN KEY (id_comida) REFERENCES comidas(id)
);


CREATE TABLE IF NOT EXISTS rutina_ejercicio (
    id_rutina BIGINT(12) NOT NULL,
    id_ejercicio MEDIUMINT(6) NOT NULL,
    cantidad_ejercicios TINYINT(4) NOT NULL,
    PRIMARY KEY (id_rutina, id_ejercicio),
    FOREIGN KEY (id_rutina) REFERENCES rutinas(id),
    FOREIGN KEY (id_ejercicio) REFERENCES ejercicios(id)
);

DROP TABLE IF EXISTS planes_usuario;

CREATE TABLE IF NOT EXISTS planes_usuario (
    id_usuario BIGINT(12) NOT NULL,
    id_plan_nutricional MEDIUMINT(6) NOT NULL,
    PRIMARY KEY (id_usuario, id_plan_nutricional),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY (id_plan_nutricional) REFERENCES planes_nutricionales(id)
);