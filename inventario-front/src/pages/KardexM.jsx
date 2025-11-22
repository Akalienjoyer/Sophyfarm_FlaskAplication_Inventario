import { useState } from "react";
import axios from "../api/axios";

export default function KardexPorTipo() {
  const [tipo, setTipo] = useState("");
  const [movimientos, setMovimientos] = useState([]);

  const tipos = [
    { id: 1, nombre: "Entrada por compra" },
    { id: 2, nombre: "Entrada por Devolución" },
    { id: 3, nombre: "Entrada por Transferencia" },
    { id: 4, nombre: "Entrada por Ajuste" },
    { id: 5, nombre: "Salida por Venta" },
    { id: 6, nombre: "Salida por Transferencia" },
    { id: 7, nombre: "Salida por Ajuste" }
  ];

  const cargarMovimientos = async () => {
    if (!tipo) {
      alert("Seleccione un tipo de movimiento");
      return;
    }

    try {
      const res = await axios.get(`/movimientos/search?tpo_mvnto=${tipo}`);
      setMovimientos(res.data.items);
    } catch (err) {
      console.error(err);
      alert("Error cargando movimientos");
    }
  };

  const descargarPDF = async () => {
    if (!tipo) {
      alert("Seleccione un tipo de movimiento");
      return;
    }

    try {
      const res = await axios.get(`/reportes/movimientos?tpo_mvnto=${tipo}`, {
        responseType: "blob"
      });

      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.download = `movimientos_tipo_${tipo}.pdf`;
      link.click();

    } catch (err) {
      console.error(err);
      alert("Error descargando PDF");
    }
  };

  return (
    <div className="max-w-5xl mx-auto p-6 bg-white shadow rounded mt-6">

      <h1 className="text-3xl font-bold mb-4">
        Movimientos por Tipo
      </h1>

      {/* Selector del tipo */}
      <div className="mb-4">
        <label className="block font-semibold">Tipo de movimiento</label>
        <select
          value={tipo}
          onChange={(e) => setTipo(e.target.value)}
          className="w-full border px-3 py-2 rounded"
        >
          <option value="">Seleccione...</option>
          {tipos.map(t => (
            <option key={t.id} value={t.id}>
              {t.id} — {t.nombre}
            </option>
          ))}
        </select>
      </div>

      {/* Botones */}
      <div className="flex gap-4 mb-6">
        <button
          onClick={cargarMovimientos}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Buscar Movimientos
        </button>

        <button
          onClick={descargarPDF}
          className="bg-green-700 text-white px-4 py-2 rounded"
        >
          Descargar PDF
        </button>
      </div>

      {/* Tabla */}
      {movimientos.length === 0 ? (
        <p className="text-gray-500">No hay movimientos registrados.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full border">
            <thead className="bg-gray-200">
              <tr>
                <th className="border px-2 py-1">Fecha</th>
                <th className="border px-2 py-1">Elemento</th>
                <th className="border px-2 py-1">Cantidad</th>
                <th className="border px-2 py-1">Costo</th>
                <th className="border px-2 py-1">Usuario</th>
                <th className="border px-2 py-1">Stock Anterior</th>
                <th className="border px-2 py-1">Stock Nuevo</th>
                <th className="border px-2 py-1">Obs</th>
              </tr>
            </thead>

            <tbody>
              {movimientos.map((m) => (
                <tr key={m.id}>
                  <td className="border px-2 py-1">
                    {new Date(m.fcha_mvnto).toLocaleString()}
                  </td>
                  <td className="border px-2 py-1">
                    {m.elemento_nombre}
                  </td>
                  <td className="border px-2 py-1">
                    {m.cntdad_elemnto}
                  </td>
                  <td className="border px-2 py-1">
                    {m.costo_untario}
                  </td>
                  <td className="border px-2 py-1">
                    {m.id_usrio}
                  </td>
                  <td className="border px-2 py-1">
                    {m.stock_anterior}
                  </td>
                  <td className="border px-2 py-1">
                    {m.stock_nuevo}
                  </td>
                  <td className="border px-2 py-1">
                    {m.obsrvaciones_mvnto}
                  </td>
                </tr>
              ))}
            </tbody>

          </table>
        </div>
      )}
    </div>
  );
}
