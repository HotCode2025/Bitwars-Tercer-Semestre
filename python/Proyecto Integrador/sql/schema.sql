CREATE TABLE clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(30),
    email VARCHAR(255)
);

CREATE TABLE proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(30),
    email VARCHAR(255)
);

CREATE TABLE servicios (
    id_servicio SERIAL PRIMARY KEY,
    nombre_servicio VARCHAR(100) NOT NULL,
    duracion_minutos INTEGER NOT NULL,
    precio NUMERIC(10,2) NOT NULL
);

CREATE TABLE turnos (
    id_turno SERIAL PRIMARY KEY,

    id_cliente INTEGER NOT NULL,
    id_proveedor INTEGER NOT NULL,
    id_servicio INTEGER NOT NULL,

    fecha_turno TIMESTAMP NOT NULL,

    estado VARCHAR(20) NOT NULL DEFAULT 'PENDIENTE',

    notas TEXT,

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_turno_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente),

    CONSTRAINT fk_turno_proveedor
        FOREIGN KEY (id_proveedor)
        REFERENCES proveedores(id_proveedor),

    CONSTRAINT fk_turno_servicio
        FOREIGN KEY (id_servicio)
        REFERENCES servicios(id_servicio),

    CONSTRAINT chk_estado_turno
        CHECK (
            estado IN (
                'PENDIENTE',
                'CONFIRMADO',
                'COMPLETADO',
                'CANCELADO',
                'NO_ASISTIO'
            )
        )
);

CREATE TABLE pagos (
    id_pago SERIAL PRIMARY KEY,

    id_turno INTEGER NOT NULL,

    monto NUMERIC(10,2) NOT NULL,

    metodo_pago VARCHAR(30),

    estado VARCHAR(20) NOT NULL DEFAULT 'PENDIENTE',

    fecha_pago TIMESTAMP,

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_pago_turno
        FOREIGN KEY (id_turno)
        REFERENCES turnos(id_turno),

    CONSTRAINT chk_estado_pago
        CHECK (
            estado IN (
                'PENDIENTE',
                'PAGADO',
                'REEMBOLSADO'
            )
        )
);


