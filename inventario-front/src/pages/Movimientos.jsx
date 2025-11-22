import { useEffect, useState } from "react";
import axios from "../api/axios";

export default function Movimientos() {
  const [productos, setProductos] = useState([]);

  const [form, setForm] = useState({
    id_elmnto: "",
    tpo_mvnto: "",
    cntdad_elemnto: 0,
    costo_untario: 0,
    id_usrio: 1,
    obsrvaciones_mvnto: ""
  });

  // Cargar productos
  useEffect(() => {
    axios.get("/elementos")
      .then(res => setProductos(res.data))
      .catch(err => console.error(err));
  }, []);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const registrarMovimiento = async () => {
    try {
      await axios.post("/movimientos", form);
      alert("Movimiento registrado");
      
      setForm({
        id_elmnto: "",
        tpo_mvnto: "",
        cntdad_elemnto: 0,
        costo_untario: 0,
        id_usrio: 1,
        obsrvaciones_mvnto: ""
      });

    } catch (err) {
      console.error(err);
      alert("Error registrando movimiento");
    }
  };

  return (
    <div className="max-w-xl mx-auto p-6 bg-white shadow rounded mt-6">



      <h2 className="text-2xl font-bold mb-4">Registrar Movimiento</h2>

      {/* Producto */}
      <div className="mb-3">
        <label className="block font-semibold">Producto</label>
        <select
          name="id_elmnto"
          value={form.id_elmnto}
          onChange={handleChange}
          className="w-full border px-3 py-2 rounded"
        >
          <option value="">Seleccione...</option>
          {productos.map(p => (
            <option key={p.id} value={p.id}>
              {p.nmbre_elemnto} — Stock: {p.exstncia_elemnto}
            </option>
          ))}
        </select>
      </div>

      {/* Tipo movimiento */}
      <div className="mb-3">
        <label className="block font-semibold">Tipo de movimiento</label>
        <select
          name="tpo_mvnto"
          value={form.tpo_mvnto}
          onChange={handleChange}
          className="w-full border px-3 py-2 rounded"
        >
          <option value="">Seleccione...</option>
          <option value="1">1 — Entrada por compra</option>
          <option value="2">2 — Entrada por Devolución</option>
          <option value="3">3 — Entrada por Transferencia</option>
          <option value="4">4 — Entrada por Ajuste</option>
          <option value="5">5 — Salida por Venta</option>
          <option value="6">6 — Salida por Transferencia</option>
          <option value="7">7 — Salida por Ajuste</option>
        </select>
      </div>

      {/* Cantidad */}
      <div className="mb-3">
        <label className="block font-semibold">Cantidad</label>
        <input
          type="number"
          min="1"
          name="cntdad_elemnto"
          value={form.cntdad_elemnto}
          onChange={handleChange}
          className="w-full border px-3 py-2 rounded"
        />
      </div>

      {/* Costo */}
      <div className="mb-3">
        <label className="block font-semibold">Costo unitario</label>
        <input
          type="number"
          min="0"
          name="costo_untario"
          value={form.costo_untario}
          onChange={handleChange}
          className="w-full border px-3 py-2 rounded"
        />
      </div>

      {/* Observaciones */}
      <div className="mb-3">
        <label className="block font-semibold">Observaciones</label>
        <textarea
          name="obsrvaciones_mvnto"
          value={form.obsrvaciones_mvnto}
          onChange={handleChange}
          className="w-full border px-3 py-2 rounded"
        ></textarea>
      </div>

      <button
        onClick={registrarMovimiento}
        className="bg-blue-600 text-white px-4 py-2 rounded mt-3"
      >
        Registrar Movimiento
      </button>

    </div>
  );
}
