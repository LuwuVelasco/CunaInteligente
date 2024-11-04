-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2024-11-04 20:40:53.978

-- tables
-- Table: bebe
CREATE TABLE bebe (
    id_bebe int  NOT NULL,
    nombre varchar(255)  NOT NULL,
    apellidoPaterno varchar(255)  NOT NULL,
    apellidoMaterno varchar(255)  NOT NULL,
    fechaDeNacimiento datetime  NOT NULL,
    usuario_id_usuario int  NOT NULL,
    CONSTRAINT cuna_pk PRIMARY KEY (id_bebe)
);

-- Table: datosMesBebe
CREATE TABLE datosMesBebe (
    id_registroCaracteristicas int  NOT NULL,
    peso float(25,2)  NOT NULL,
    altura float(25,2)  NOT NULL,
    fecha datetime  NOT NULL,
    cuna_id_cuna int  NOT NULL,
    CONSTRAINT bebe_pk PRIMARY KEY (id_registroCaracteristicas)
);

-- Table: registroAlimentacion
CREATE TABLE registroAlimentacion (
    id_registroAlimentacion int  NOT NULL,
    fecha datetime  NOT NULL,
    tipoComida boolean  NOT NULL,
    cuna_id_cuna int  NOT NULL,
    CONSTRAINT registroAlimentacion_pk PRIMARY KEY (id_registroAlimentacion)
);

-- Table: registroHumedad
CREATE TABLE registroHumedad (
    id_registroHumedad int  NOT NULL,
    humedad float(25,2)  NOT NULL,
    fecha datetime  NOT NULL,
    cuna_id_cuna int  NOT NULL,
    CONSTRAINT registroHumedad_pk PRIMARY KEY (id_registroHumedad)
);

-- Table: registroLlanto
CREATE TABLE registroLlanto (
    id_registroLlanto int  NOT NULL,
    llanto float(25,2)  NOT NULL,
    razon float(25,2)  NOT NULL,
    fecha datetime  NOT NULL,
    cuna_id_cuna int  NOT NULL,
    CONSTRAINT registroLlanto_pk PRIMARY KEY (id_registroLlanto)
);

-- Table: registroTemperatura
CREATE TABLE registroTemperatura (
    id_registroTemp int  NOT NULL,
    temperatura float(25,2)  NOT NULL,
    fecha datetime  NOT NULL,
    cuna_id_cuna int  NOT NULL,
    CONSTRAINT registroTemperatura_pk PRIMARY KEY (id_registroTemp)
);

-- Table: usuario
CREATE TABLE usuario (
    id_usuario int  NOT NULL,
    username varchar(255)  NOT NULL,
    nombre varchar(255)  NOT NULL,
    apellidoPaterno varchar(255)  NOT NULL,
    apellidoMaterno varchar(255)  NOT NULL,
    gmail varchar(255)  NOT NULL,
    contrasenia varchar(255)  NOT NULL,
    CONSTRAINT usuario_pk PRIMARY KEY (id_usuario)
);

-- foreign keys
-- Reference: bebe_cuna (table: datosMesBebe)
ALTER TABLE datosMesBebe ADD CONSTRAINT bebe_cuna FOREIGN KEY bebe_cuna (cuna_id_cuna)
    REFERENCES bebe (id_bebe);

-- Reference: registroAlimentacion_cuna (table: registroAlimentacion)
ALTER TABLE registroAlimentacion ADD CONSTRAINT registroAlimentacion_cuna FOREIGN KEY registroAlimentacion_cuna (cuna_id_cuna)
    REFERENCES bebe (id_bebe);

-- Reference: registroCuna_bebe (table: registroTemperatura)
ALTER TABLE registroTemperatura ADD CONSTRAINT registroCuna_bebe FOREIGN KEY registroCuna_bebe (cuna_id_cuna)
    REFERENCES bebe (id_bebe);

-- Reference: registroHumedad_cuna (table: registroHumedad)
ALTER TABLE registroHumedad ADD CONSTRAINT registroHumedad_cuna FOREIGN KEY registroHumedad_cuna (cuna_id_cuna)
    REFERENCES bebe (id_bebe);

-- Reference: registroLlanto_cuna (table: registroLlanto)
ALTER TABLE registroLlanto ADD CONSTRAINT registroLlanto_cuna FOREIGN KEY registroLlanto_cuna (cuna_id_cuna)
    REFERENCES bebe (id_bebe);

-- Reference: registros_usuario (table: bebe)
ALTER TABLE bebe ADD CONSTRAINT registros_usuario FOREIGN KEY registros_usuario (usuario_id_usuario)
    REFERENCES usuario (id_usuario);

-- End of file.

