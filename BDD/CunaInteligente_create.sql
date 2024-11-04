-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2024-11-04 00:41:45.04

-- tables
-- Table: bebe
CREATE TABLE bebe (
    id_bebe int  NOT NULL,
    nombre varchar(255)  NOT NULL,
    fechaDeNacimiento datetime  NOT NULL,
    peso float(25,2)  NOT NULL,
    HoraUltimaComida datetime  NOT NULL,
    movimientoCuna boolean  NOT NULL,
    temperatura float(25,2)  NOT NULL,
    humedad boolean  NOT NULL,
    usuario_id_usuario int  NOT NULL,
    CONSTRAINT bebe_pk PRIMARY KEY (id_bebe)
);

-- Table: registroHumedad
CREATE TABLE registroHumedad (
    id_registroHumedad int  NOT NULL,
    fecha datetime  NOT NULL,
    tiempoHumedad int  NOT NULL,
    horaUltimaComida datetime  NOT NULL,
    bebe_id_bebe int  NOT NULL,
    CONSTRAINT registroHumedad_pk PRIMARY KEY (id_registroHumedad)
);

-- Table: registroLLanto
CREATE TABLE registroLLanto (
    id_registroLLanto int  NOT NULL,
    fecha datetime  NOT NULL,
    tiempoLLanto float(25,2)  NOT NULL,
    temperaturaActual float(25,2)  NOT NULL,
    movimientoCuna boolean  NOT NULL,
    humedad boolean  NOT NULL,
    ultimaComida datetime  NOT NULL,
    bebe_id_bebe int  NOT NULL,
    CONSTRAINT registroLLanto_pk PRIMARY KEY (id_registroLLanto)
);

-- Table: usuario
CREATE TABLE usuario (
    id_usuario int  NOT NULL,
    usuario varchar(255)  NOT NULL,
    contrasena varchar(255)  NOT NULL,
    CONSTRAINT usuario_pk PRIMARY KEY (id_usuario)
);

-- foreign keys
-- Reference: registroHumedad_bebe (table: registroHumedad)
ALTER TABLE registroHumedad ADD CONSTRAINT registroHumedad_bebe FOREIGN KEY registroHumedad_bebe (bebe_id_bebe)
    REFERENCES bebe (id_bebe);

-- Reference: registroLLanto_bebe (table: registroLLanto)
ALTER TABLE registroLLanto ADD CONSTRAINT registroLLanto_bebe FOREIGN KEY registroLLanto_bebe (bebe_id_bebe)
    REFERENCES bebe (id_bebe);

-- Reference: registros_usuario (table: bebe)
ALTER TABLE bebe ADD CONSTRAINT registros_usuario FOREIGN KEY registros_usuario (usuario_id_usuario)
    REFERENCES usuario (id_usuario);

-- End of file.

