import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./layout/Dashboard";

import Inventario from "./pages/Inventario";
import Movimientos from "./pages/Movimientos";
import NuevoProducto from "./pages/NuevoElemento";
import Kardex from "./pages/Kardex";
import KardexM from "./pages/KardexM";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />}>
          
          <Route path="inventario" element={<Inventario />} />

          <Route path="NuevoElemento" element={<NuevoProducto />} />

          <Route path="movimientos" element={<Movimientos />} />
        
          <Route path="kardex" element={<Kardex />} />

          <Route path="kardexM" element={<KardexM />} />

        </Route>
      </Routes>
    </BrowserRouter>
  );
}
