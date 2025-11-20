-- ======================================================
--  SCHEMA – SophyFarm Inventario (Profesional)
-- ======================================================

-- ==========================
-- TABLA: unidad
-- ==========================
DROP TABLE IF EXISTS unidad CASCADE;

CREATE TABLE unidad (
    id SERIAL PRIMARY KEY,
    nmbre_undad VARCHAR(20) NOT NULL,
    estdo_undad VARCHAR(1) NOT NULL
);

-- ==========================
-- TABLA: categoria_producto
-- ==========================
DROP TABLE IF EXISTS categoria_producto CASCADE;

CREATE TABLE categoria_producto (
    id SERIAL PRIMARY KEY,
    nombre_ctgria VARCHAR(50) NOT NULL,
    estdo_ctgria VARCHAR(1) NOT NULL
);

-- ==========================
-- TABLA: tipomov
-- ==========================
DROP TABLE IF EXISTS tipomov CASCADE;

CREATE TABLE tipomov (
    tpo_mvnto SMALLINT PRIMARY KEY,
    dscrpcion_tpo VARCHAR(40) NOT NULL,
    estdo_tpo VARCHAR(1) NOT NULL
);

-- ==========================
-- TABLA: elemento
-- ==========================
DROP TABLE IF EXISTS elemento CASCADE;

CREATE TABLE elemento (
    id SERIAL PRIMARY KEY,
    sku_elemnto VARCHAR(20) NOT NULL,
    nmbre_elemnto VARCHAR(40) NOT NULL,
    dscrpcion_elemnto VARCHAR(60) NOT NULL,
    lote_elemnto VARCHAR(60) NOT NULL,

    ctgria_elemnto SMALLINT NOT NULL REFERENCES categoria_producto(id),
    und_elemnto SMALLINT NOT NULL REFERENCES unidad(id),

    exstncia_elemnto INT NOT NULL,
    prsntacion_elemnto VARCHAR(80) NOT NULL,
    lbrtorio_elemnto VARCHAR(60) NOT NULL,
    cntrolado_elemnto VARCHAR(1) NOT NULL,
    bdga_elemnto INT NOT NULL,
    precio_venta_ac NUMERIC(10,0) NOT NULL,
    precio_venta_an NUMERIC(10,0) NOT NULL,
    costo_venta NUMERIC(10,0) NOT NULL,
    mrgen_utldad DOUBLE PRECISION NOT NULL,
    tiene_iva VARCHAR(1) NOT NULL,
    stock_minimo INT NOT NULL,
    stock_maximo INT NOT NULL,
    estdo_elmnto VARCHAR(1) NOT NULL
);

-- ==========================
-- TABLA: mvmnto_invntario (versión profesional completa)
-- ==========================
DROP TABLE IF EXISTS mvmnto_invntario CASCADE;

CREATE TABLE mvmnto_invntario (
    id SERIAL PRIMARY KEY,

    -- foreign keys principales
    id_elmnto INT NOT NULL REFERENCES elemento(id) ON DELETE CASCADE,
    tpo_mvnto SMALLINT NOT NULL REFERENCES tipomov(tpo_mvnto),

    -- datos de la transacción
    cntdad_elemnto INT NOT NULL,
    costo_untario NUMERIC(10,0) NOT NULL,
    fcha_mvnto TIMESTAMP NOT NULL DEFAULT NOW(),
    id_usrio SMALLINT NOT NULL,

    -- estado, notas
    estdo_mvnto VARCHAR(1) NOT NULL,
    obsrvaciones_mvnto VARCHAR(80) NOT NULL,

    -- columnas extra para kardex profesional
    stock_anterior INTEGER,
    stock_nuevo INTEGER,
    valor_total NUMERIC(14, 2),

    -- referencia si movimiento fue revertido
    reversed_from INTEGER,
    CONSTRAINT fk_reversed_from FOREIGN KEY (reversed_from)
        REFERENCES mvmnto_invntario(id)
);

-- índices para optimizar consultas de kardex
CREATE INDEX IF NOT EXISTS idx_mov_elemento_fecha
  ON mvmnto_invntario (id_elmnto, fcha_mvnto DESC);

CREATE INDEX IF NOT EXISTS idx_mov_tipo
  ON mvmnto_invntario (tpo_mvnto);

