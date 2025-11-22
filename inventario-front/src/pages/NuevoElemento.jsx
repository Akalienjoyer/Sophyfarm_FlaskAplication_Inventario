import { useState } from "react";
import axios from "../api/axios";
import { useNavigate } from "react-router-dom";

export default function NuevoProducto() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    sku_elemnto: "",
    nmbre_elemnto: "",
    dscrpcion_elemnto: "",
    lote_elemnto: "-",
    ctgria_elemnto: 1,
    und_elemnto: 1,
    exstncia_elemnto: 0,
    prsntacion_elemnto: "-",
    lbrtorio_elemnto: "-",
    cntrolado_elemnto: "N",
    bdga_elemnto: 1,
    precio_venta_ac: 0,
    precio_venta_an: 0,
    costo_venta: 0,
    mrgen_utldad: 0,
    tiene_iva: "N",
    stock_minimo: 0,
    stock_maximo: 9999,
    estdo_elmnto: "A"
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const guardar = async () => {
    try {
      await axios.post("/elementos/", form);
      alert("Producto creado con éxito");
      navigate("/inventario");
    } catch (e) {
      console.error(e);
      alert("Error al crear producto");
    }
  };

  return (
    <div className="max-w-xl mx-auto bg-white p-6 shadow rounded mt-6">

      <h2 className="text-2xl font-bold mb-4">Nuevo Producto</h2>

      <div className="mb-3">
        <label className="block font-semibold">SKU</label>
        <input
          name="sku_elemnto"
          value={form.sku_elemnto}
          onChange={handleChange}
          className="w-full border px-3 py-2 rounded"
        />
      </div>

      <div className="mb-3">
        <label className="block font-semibold">Nombre</label>
        <input
          name="nmbre_elemnto"
          value={form.nmbre_elemnto}
          onChange={handleChange}
          className="w-full border px-3 py-2 rounded"
        />
      </div>

      <div className="mb-3">
        <label className="block font-semibold">Descripción</label>
        <textarea
          name="dscrpcion_elemnto"
          value={form.dscrpcion_elemnto}
          onChange={handleChange}
          className="w-full border px-3 py-2 rounded"
        />
      </div>

      <div className="mb-3">
        <label className="block font-semibold">Stock</label>
        <input
          type="number"
          name="exstncia_elemnto"
          value={form.exstncia_elemnto}
          onChange={handleChange}
          className="w-full border px-3 py-2 rounded"
        />
      </div>

      <div className="mb-3">
        <label className="block font-semibold">Precio</label>
        <input
          type="number"
          name="precio_venta_ac"
          value={form.precio_venta_ac}
          onChange={handleChange}
          className="w-full border px-3 py-2 rounded"
        />
      </div>

      <button
        onClick={guardar}
        className="bg-green-600 text-white px-4 py-2 rounded mt-3"
      >
        Guardar Producto
      </button>

    </div>
  );
}
