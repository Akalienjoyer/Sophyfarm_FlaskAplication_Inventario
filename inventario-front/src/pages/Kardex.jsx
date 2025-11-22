import { useEffect, useState } from "react";
import axios from "../api/axios";

export default function Kardex() {
  const [productos, setProductos] = useState([]);
  const [elementoId, setElementoId] = useState("");
  const [kardex, setKardex] = useState([]);

  // Cargar elementos al iniciar
  useEffect(() => {
    axios
      .get("/elementos")
      .then((res) => setProductos(res.data))
      .catch((err) => console.error(err));
  }, []);

  // Consultar kardex
  const cargarKardex = async () => {
    if (!elementoId) {
      alert("Seleccione un elemento");
      return;
    }

    try {
      const res = await axios.get(
        `/movimientos/kardex/${elementoId}?page=1&per_page=100`
      );
      setKardex(res.data.items);
    } catch (err) {
      console.error(err);
      alert("Error cargando el Kardex");
    }
  };

  // Descargar PDF del kardex
  const descargarPDF = async () => {
    if (!elementoId) {
      alert("Seleccione un elemento primero");
      return;
    }

    try {
      const res = await axios.get(`/reportes/kardex/${elementoId}`, {
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.download = `kardex_elemento_${elementoId}.pdf`;
      link.click();
    } catch (err) {
      console.error(err);
      alert("Error descargando PDF");
    }
  };

  return (
    <div className="max-w-5xl mx-auto p-6 bg-white shadow rounded mt-6">

      <h1 className="text-3xl font-bold mb-4">Kardex de Producto</h1>

      {/* Selector de elemento */}
      <div className="mb-4">
        <label className="block font-semibold">Seleccione un producto</label>
        <select
          value={elementoId}
          onChange={(e) => setElementoId(e.target.value)}
          className="border px-3 py-2 rounded w-full"
        >
          <option value="">Seleccione...</option>
          {productos.map((p) => (
            <option key={p.id} value={p.id}>
              {p.nmbre_elemnto} — Stock: {p.exstncia_elemnto}
            </option>
          ))}
        </select>
      </div>

      {/* Botones */}
      <div className="flex gap-4 mb-6">
        <button
          onClick={cargarKardex}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Cargar Kardex
        </button>

        <button
          onClick={descargarPDF}
          className="bg-green-700 text-white px-4 py-2 rounded"
        >
          Descargar Kardex (PDF)
        </button>
      </div>

      {/* Tabla del kardex */}
      {kardex.length === 0 ? (
        <p className="text-gray-500">No hay movimientos para este elemento.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full border">
            <thead className="bg-gray-200">
              <tr>
                <th className="border px-2 py-1">Fecha</th>
                <th className="border px-2 py-1">Tipo</th>
                <th className="border px-2 py-1">Cantidad</th>
                <th className="border px-2 py-1">Costo</th>
                <th className="border px-2 py-1">Stock Anterior</th>
                <th className="border px-2 py-1">Stock Nuevo</th>
                <th className="border px-2 py-1">Usuario</th>
                <th className="border px-2 py-1">Obs</th>
              </tr>
            </thead>
            <tbody>
              {kardex.map((m) => (
                <tr key={m.id}>
                  <td className="border px-2 py-1">
                    {new Date(m.fcha_mvnto).toLocaleString()}
                  </td>
                  <td className="border px-2 py-1">
                    {m.tipo_nombre || m.tpo_mvnto}
                  </td>
                  <td className="border px-2 py-1">{m.cntdad_elemnto}</td>
                  <td className="border px-2 py-1">{m.costo_untario}</td>
                  <td className="border px-2 py-1">{m.stock_anterior}</td>
                  <td className="border px-2 py-1">{m.stock_nuevo}</td>
                  <td className="border px-2 py-1">{m.id_usrio}</td>
                  <td className="border px-2 py-1">{m.obsrvaciones_mvnto}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
