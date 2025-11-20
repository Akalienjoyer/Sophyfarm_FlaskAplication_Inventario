-- ======================================================
--  DATOS INICIALES
-- ======================================================

-- UNIDADES
INSERT INTO unidad (id, nmbre_undad, estdo_undad) VALUES
(1, 'GALONES', 'A'),
(2, 'LITROS',  'A'),
(3, 'UNIDAD',  'A');

-- CATEGORÍAS
INSERT INTO categoria_producto (id, nombre_ctgria, estdo_ctgria) VALUES
(1, 'Analgesicos', 'A'),
(2, 'Antibioticos', 'A'),
(3, 'Antigripales', 'A'),
(4, 'Gastrointestinales', 'A'),
(5, 'Suplementos', 'A');

-- TIPOS DE MOVIMIENTO
INSERT INTO tipomov (tpo_mvnto, dscrpcion_tpo, estdo_tpo) VALUES
(1, 'Entrada por Compras', 'A'),
(2, 'Entrada por Devolución', 'A'),
(3, 'Entrada por Transferencia', 'A'),
(4, 'Entrada por Ajuste', 'A'),
(5, 'Salida por Venta', 'A'),
(6, 'Salida por Transferencia', 'A'),
(7, 'Salida por Ajuste', 'A');

-- ELEMENTOS (20 registros realistas)
INSERT INTO elemento (
    sku_elemnto, nmbre_elemnto, dscrpcion_elemnto, lote_elemnto,
    ctgria_elemnto, und_elemnto, exstncia_elemnto, prsntacion_elemnto,
    lbrtorio_elemnto, cntrolado_elemnto, bdga_elemnto,
    precio_venta_ac, precio_venta_an, costo_venta, mrgen_utldad,
    tiene_iva, stock_minimo, stock_maximo, estdo_elmnto
) VALUES
('E001','Ibuprofeno 400mg','Caja x10','L2025A',1,3,50,'Caja x10','Genfar','N',1,3000,2500,2000,40,'N',5,200,'A'),
('E002','Acetaminofen 500mg','Caja x16','L2025B',1,3,120,'Caja x16','MK','N',1,2500,2300,1500,50,'N',5,300,'A'),
('E003','Omeprazol 20mg','Caja x14','L2025C',4,3,80,'Caja x14','La Santé','N',1,9000,8500,7000,25,'N',5,150,'A'),
('E004','Amoxicilina 500mg','Caja x12','L2025D',2,3,70,'Caja x12','Genfar','N',1,14000,13000,10000,30,'N',5,150,'A'),
('E005','Diclofenaco Gel 1%','Tubo 30g','L2025E',1,3,40,'Tubo 30g','MK','N',1,6500,6200,4500,35,'N',3,100,'A'),
('E006','Loratadina 10mg','Caja x10','L2025F',3,3,90,'Caja x10','Sura','N',1,4500,4200,3000,33,'N',5,200,'A'),
('E007','Vitamina C 500mg','Frasco x30','L2025G',5,3,200,'Frasco x30','Nature´s Garden','N',1,12000,11000,8000,30,'N',10,500,'A'),
('E008','Sales de Rehidratación','Sobre x1','L2025H',4,3,150,'Sobre x1','MK','N',1,2000,1800,1000,40,'N',20,500,'A'),
('E009','Jarabe Antigripal','Frasco 120ml','L2025I',3,2,35,'Frasco 120ml','Genfar','N',1,9500,9000,7000,25,'N',3,100,'A'),
('E010','Desloratadina 5mg','Caja x10','L2025J',3,3,60,'Caja x10','Genfar','N',1,8500,8000,6000,30,'N',3,150,'A'),
('E011','Acetaminofen Infantil 2.4%','Frasco 120ml','L2025K',1,2,45,'Frasco 120ml','MK','N',1,7000,6500,5000,28,'N',3,100,'A'),
('E012','Ketoconazol Shampoo 2%','Frasco 120ml','L2025L',5,2,22,'Frasco 120ml','La Santé','N',1,15500,15000,12000,22,'N',2,80,'A'),
('E013','Antiséptico Yodado','Frasco 60ml','L2025M',5,2,70,'Frasco 60ml','MK','N',1,5500,5000,3000,40,'N',5,200,'A'),
('E014','Alcohol Antiséptico 70%','Frasco 100ml','L2025N',5,2,90,'Frasco 100ml','MK','N',1,3500,3200,2000,40,'N',10,300,'A'),
('E015','Algodón Hidrófilo 50g','Bolsa x1','L2025O',5,3,100,'Bolsa x1','Genérico','N',1,2500,2400,1500,40,'N',10,300,'A'),
('E016','Guantes de Nitrilo Talla M','Caja x100','L2025P',5,3,30,'Caja x100','Genérico','N',1,30000,29000,25000,20,'S',5,80,'A'),
('E017','Mascarilla Quirúrgica','Caja x50','L2025Q',5,3,150,'Caja x50','Genérico','N',1,10000,9000,7000,30,'S',20,300,'A'),
('E018','Gel Antibacterial','Frasco 300ml','L2025R',5,2,40,'Frasco 300ml','Genérico','N',1,8500,8000,5000,41,'S',5,150,'A'),
('E019','Suero Oral 500ml','Botella 500ml','L2025S',4,2,25,'Botella 500ml','MK','N',1,4500,4200,3000,33,'N',3,80,'A'),
('E020','Jarabe Expectorante','Frasco 120ml','L2025T',3,2,30,'Frasco 120ml','MK','N',1,9000,8500,6000,35,'N',3,100,'A');

-- =========================
-- MOVIMIENTOS DE PRUEBA
-- =========================

-- 1) Entrada por compra (elemento 1 – Acetaminofén)
INSERT INTO mvmnto_invntario 
(id_elmnto, tpo_mvnto, cntdad_elemnto, costo_untario, fcha_mvnto, id_usrio, estdo_mvnto,
 obsrvaciones_mvnto, stock_anterior, stock_nuevo, valor_total, reversed_from)
VALUES
(1, 1, 50, 1200, NOW() - INTERVAL '7 days', 1, 'A',
 'Compra proveedor MK', 110, 160, 60000, NULL);

-- 2) Salida por venta (elemento 1)
INSERT INTO mvmnto_invntario VALUES
(DEFAULT, 1, 5, 20, 2000, NOW() - INTERVAL '6 days', 1, 'A',
 'Venta mostrador', 160, 140, 40000, NULL);

-- 3) Entrada por ajuste (+5 unidades, elemento 2)
INSERT INTO mvmnto_invntario VALUES
(DEFAULT, 2, 4, 5, 3000, NOW() - INTERVAL '5 days', 1, 'A',
 'Ajuste inventario', 30, 35, 15000, NULL);

-- 4) Salida por ajuste (-3 unidades, elemento 3)
INSERT INTO mvmnto_invntario VALUES
(DEFAULT, 3, 7, 3, 3000, NOW() - INTERVAL '4 days', 1, 'A',
 'Rotura / pérdida', 20, 17, 9000, NULL);

-- 5) Entrada por compra (elemento 4)
INSERT INTO mvmnto_invntario VALUES
(DEFAULT, 4, 1, 15, 3500, NOW() - INTERVAL '4 days', 1, 'A',
 'Ingreso proveedor Genfar', 15, 30, 52500, NULL);

-- 6) Salida por venta (elemento 5)
INSERT INTO mvmnto_invntario VALUES
(DEFAULT, 5, 5, 10, 3000, NOW() - INTERVAL '3 days', 1, 'A',
 'Venta mostrador', 60, 50, 30000, NULL);

-- 7) Entrada por transferencia (elemento 6)
INSERT INTO mvmnto_invntario VALUES
(DEFAULT, 6, 3, 8, 2500, NOW() - INTERVAL '3 days', 1, 'A',
 'Transferencia de bodega', 40, 48, 20000, NULL);

-- 8) Salida por venta (elemento 7)
INSERT INTO mvmnto_invntario VALUES
(DEFAULT, 7, 5, 12, 7000, NOW() - INTERVAL '2 days', 1, 'A',
 'Venta mayorista', 25, 13, 84000, NULL);

-- 9) Entrada por compra (elemento 8)
INSERT INTO mvmnto_invntario VALUES
(DEFAULT, 8, 1, 20, 9000, NOW() - INTERVAL '1 days', 1, 'A',
 'Ingreso de proveedor Sandoz', 35, 55, 180000, NULL);

-- 10) Salida por venta (elemento 1 – reversión posible)
INSERT INTO mvmnto_invntario VALUES
(DEFAULT, 1, 5, 5, 2000, NOW(), 1, 'A',
 'Venta rápida mostrador', 140, 135, 10000, NULL);
