-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2024-11-04 02:40:21.718

-- tables
-- Table: bebe
CREATE TABLE bebe (
    id_bebe int  NOT NULL,
    nombre varchar(255)  NOT NULL,
    fechaDeNacimiento datetime  NOT NULL,
    pesoInicial float(25,2)  NOT NULL,
    usuario_id_usuario int  NOT NULL,
    CONSTRAINT bebe_pk PRIMARY KEY (id_bebe)
);

-- Table: registroAlimentacion
CREATE TABLE registroAlimentacion (
    id_registroAlimentacion int  NOT NULL,
    fecha datetime  NOT NULL,
    tipoComida boolean  NOT NULL,
    bebe_id_bebe int  NOT NULL,
    CONSTRAINT registroAlimentacion_pk PRIMARY KEY (id_registroAlimentacion)
);

-- Table: registroCaracteristicas
CREATE TABLE registroCaracteristicas (
    id_registroCaracteristicas int  NOT NULL,
    fecha datetime  NOT NULL,
    peso float(25,2)  NOT NULL,
    altura float(25,2)  NOT NULL,
    bebe_id_bebe int  NOT NULL,
    CONSTRAINT registroCaracteristicas_pk PRIMARY KEY (id_registroCaracteristicas)
);

-- Table: registroCuna
CREATE TABLE registroCuna (
    id_registroCuna int  NOT NULL,
    fecha datetime  NOT NULL,
    temperatura float(25,2)  NOT NULL,
    humedad boolean  NOT NULL,
    bebe_id_bebe int  NOT NULL,
    CONSTRAINT registroCuna_pk PRIMARY KEY (id_registroCuna)
);

-- Table: registroHumedad
CREATE TABLE registroHumedad (
    id_registroHumedad int  NOT NULL,
    fecha datetime  NOT NULL,
    tiempoHumedad int  NOT NULL,
    registroCuna_id_registroCuna int  NOT NULL,
    CONSTRAINT registroHumedad_pk PRIMARY KEY (id_registroHumedad)
);

-- Table: registroLLanto
CREATE TABLE registroLLanto (
    id_registroLLanto int  NOT NULL,
    fecha datetime  NOT NULL,
    tiempoLLanto float(25,2)  NOT NULL,
    temperaturaActual float(25,2)  NOT NULL,
    humedad boolean  NOT NULL,
    microfono float(25,2)  NOT NULL,
    registroCuna_id_registroCuna int  NOT NULL,
    registroAlimentacion_id_registroAlimentacion int  NOT NULL,
    CONSTRAINT registroLLanto_pk PRIMARY KEY (id_registroLLanto)
);

-- Table: usuario
CREATE TABLE usuario (
    id_usuario int  NOT NULL,
    usuario varchar(255)  NOT NULL,
    contrasenia varchar(255)  NOT NULL,
    CONSTRAINT usuario_pk PRIMARY KEY (id_usuario)
);

-- foreign keys
-- Reference: registroAlimentacion_bebe (table: registroAlimentacion)
ALTER TABLE registroAlimentacion ADD CONSTRAINT registroAlimentacion_bebe FOREIGN KEY registroAlimentacion_bebe (bebe_id_bebe)
    REFERENCES bebe (id_bebe);

-- Reference: registroCaracteristicas_bebe (table: registroCaracteristicas)
ALTER TABLE registroCaracteristicas ADD CONSTRAINT registroCaracteristicas_bebe FOREIGN KEY registroCaracteristicas_bebe (bebe_id_bebe)
    REFERENCES bebe (id_bebe);

-- Reference: registroCuna_bebe (table: registroCuna)
ALTER TABLE registroCuna ADD CONSTRAINT registroCuna_bebe FOREIGN KEY registroCuna_bebe (bebe_id_bebe)
    REFERENCES bebe (id_bebe);

-- Reference: registroHumedad_registroCuna (table: registroHumedad)
ALTER TABLE registroHumedad ADD CONSTRAINT registroHumedad_registroCuna FOREIGN KEY registroHumedad_registroCuna (registroCuna_id_registroCuna)
    REFERENCES registroCuna (id_registroCuna);

-- Reference: registroLLanto_registroAlimentacion (table: registroLLanto)
ALTER TABLE registroLLanto ADD CONSTRAINT registroLLanto_registroAlimentacion FOREIGN KEY registroLLanto_registroAlimentacion (registroAlimentacion_id_registroAlimentacion)
    REFERENCES registroAlimentacion (id_registroAlimentacion);

-- Reference: registroLLanto_registroCuna (table: registroLLanto)
ALTER TABLE registroLLanto ADD CONSTRAINT registroLLanto_registroCuna FOREIGN KEY registroLLanto_registroCuna (registroCuna_id_registroCuna)
    REFERENCES registroCuna (id_registroCuna);

-- Reference: registros_usuario (table: bebe)
ALTER TABLE bebe ADD CONSTRAINT registros_usuario FOREIGN KEY registros_usuario (usuario_id_usuario)
    REFERENCES usuario (id_usuario);

-- End of file.

