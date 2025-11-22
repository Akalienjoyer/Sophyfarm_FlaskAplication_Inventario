import { Link, Outlet } from "react-router-dom";

export default function Dashboard() {
  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <aside className="w-64 bg-white shadow-md p-4">
        <h1 className="text-2xl font-bold mb-6">SophyFarm</h1>
        <nav className="flex flex-col gap-3">
          <Link className="hover:text-blue-600" to="/inventario">📦 Inventario</Link>
          <Link className="hover:text-blue-600" to="/NuevoElemento">➕ Nuevo Producto</Link>
          <Link className="hover:text-blue-600" to="/movimientos">🔃 Movimientos</Link>
          <Link className="hover:text-blue-600" to="/kardex">📊 Kardex - Producto</Link>
          <Link className="hover:text-blue-600" to="/kardexM">📊 Kardex - Movimiento</Link>
        </nav>
      </aside>

      {/* Content */}
      <main className="flex-1 p-6 overflow-y-auto">
        <Outlet />
      </main>
    </div>
  );
}
