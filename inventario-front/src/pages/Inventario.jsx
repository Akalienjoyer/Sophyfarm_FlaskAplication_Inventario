import React, { useState, useEffect, useCallback } from "react";
import axios from "../api/axios"; 

const useToast = () => {
    const [message, setMessage] = useState('');
    const [isVisible, setIsVisible] = useState(false);
    const [isError, setIsError] = useState(false);

    const showToast = useCallback((msg, error = false) => {
        setMessage(msg);
        setIsError(error);
        setIsVisible(true);
        setTimeout(() => {
            setIsVisible(false);
            setMessage('');
        }, 3000);
    }, []);

    const Toast = () => isVisible && (
        <div className={`fixed bottom-5 right-5 p-4 rounded-lg shadow-xl text-white font-semibold transition-opacity duration-300 ${isError ? 'bg-red-600' : 'bg-green-600'} z-[100]`}>
            {message}
        </div>
    );

    return { showToast, Toast };
};

const ConfirmationModal = ({ isOpen, onClose, title, message, onConfirm, item }) => {
    if (!isOpen || !item) return null;

    const handleConfirm = () => {
        onConfirm(item);
        onClose();
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-60 flex justify-center items-center z-[90]">
            <div className="bg-white p-6 rounded-xl shadow-2xl w-full max-w-sm animate-in zoom-in-75">
                <h3 className="text-xl font-bold mb-4 text-gray-800 border-b pb-2">{title}</h3>
                <p className="mb-6 text-gray-700">{message}</p>
                <div className="flex justify-end space-x-3">
                    <button 
                        onClick={onClose} 
                        className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-2 px-4 rounded-lg transition duration-150"
                    >
                        Cancelar
                    </button>
                    <button 
                        onClick={handleConfirm} 
                        className="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-150"
                    >
                        Confirmar
                    </button>
                </div>
            </div>
        </div>
    );
};


const EditProductModal = ({ isOpen, onClose, product, onUpdate, showToast }) => {
    if (!isOpen || !product) return null;

    const [formData, setFormData] = useState({
    sku_elemnto: '',
    nmbre_elemnto: '',
    prsntacion_elemnto: '',
    lbrtorio_elemnto: '',
    lote_elemnto: '',
    costo_venta: 0,
    precio_venta_ac: 0,
    peso_elemnto: 0,
    dscrpcion_elemnto: '',
    estdo_elmnto: 'A',
    ctgria_elemnto: '',
});

useEffect(() => {
        if (product) {
            setFormData({
                sku_elemnto: product.sku_elemnto || '',
                nmbre_elemnto: product.nmbre_elemnto || '',
                prsntacion_elemnto: product.prsntacion_elemnto || '',
                lbrtorio_elemnto: product.lbrtorio_elemnto || '',
                lote_elemnto: product.lote_elemnto || '',
                costo_venta: product.costo_venta || 0,
                precio_venta_ac: product.precio_venta_ac || 0,
                peso_elemnto: product.peso_elemnto || 0,
                dscrpcion_elemnto: product.dscrpcion_elemnto || '',
                estdo_elmnto: product.estdo_elmnto || 'A',
                ctgria_elemnto: product.ctgria_elemnto || '',
            });
        }
    }, [product]);


    const [isLoading, setIsLoading] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            const dataToUpdate = {
    sku_elemnto: formData.sku_elemnto,
    nmbre_elemnto: formData.nmbre_elemnto,
    prsntacion_elemnto: formData.prsntacion_elemnto,
    lbrtorio_elemnto: formData.lbrtorio_elemnto,
    lote_elemnto: formData.lote_elemnto,
    costo_venta: parseFloat(formData.costo_venta),
    precio_venta_ac: parseFloat(formData.precio_venta_ac),
    peso_elemnto: parseFloat(formData.peso_elemnto),
    dscrpcion_elemnto: formData.dscrpcion_elemnto,
    estdo_elmnto: formData.estdo_elmnto,
    ctgria_elemnto: formData.ctgria_elemnto,
};



            const response = await axios.put(`/elementos/${product.id}`, dataToUpdate);

            onUpdate(product.id, response.data);
            showToast("Producto actualizado exitosamente.", false);
            onClose();

        } catch (error) {
            console.error("Error al actualizar el producto:", error);
            showToast("Error al actualizar el producto. Intente de nuevo.", true);
        } finally {
            setIsLoading(false);
        }
    };


    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50 p-4">
            <div className="bg-white w-full max-w-lg md:max-w-xl p-6 rounded-xl shadow-2xl relative animate-in zoom-in-50">
                
                <h2 className="text-3xl font-extrabold text-gray-800 mb-6 border-b pb-2">
                    Visualizar / Actualizar Elemento
                </h2>

                <button
                    onClick={onClose}
                    className="absolute top-4 right-4 text-gray-500 hover:text-gray-900 text-2xl font-bold transition duration-150"
                    disabled={isLoading}
                    aria-label="Cerrar modal"
                >
                    &times;
                </button>

                <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    
                    <div>
                        <label className="block text-sm font-medium text-gray-700">SKU (Código)</label>
                        <input
                            type="text"
                            name="sku_elemnto"
                            value={formData.sku_elemnto}
                            onChange={handleChange}
                            required
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border focus:ring-indigo-500 focus:border-indigo-500"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Nombre del Elemento</label>
                        <input
                            type="text"
                            name="nmbre_elemnto"
                            value={formData.nmbre_elemnto}
                            onChange={handleChange}
                            required
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border focus:ring-indigo-500 focus:border-indigo-500"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700">Precio de Venta ($)</label>
                        <input
                            type="number"
                            name="precio_venta_ac"
                            value={formData.precio_venta_ac}
                            onChange={handleChange}
                            step="0.01"
                            min="0"
                            required
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border focus:ring-indigo-500 focus:border-indigo-500"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700">Categoria</label>
                        <select
                            name="ctgria_elemnto"
                            value={formData.ctgria_elemnto}
                            onChange={handleChange}
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border focus:ring-indigo-500 focus:border-indigo-500"
                        >
                            <option value="1">Analgesicos</option>
                            <option value="2">Antibioticos</option>
                            <option value="3">Antigripales</option>
                            <option value="4">Gastrointestinales</option>
                            <option value="5">Suplementos</option>
                        </select>
                    </div>

                    <div>
                            <label className="block text-sm font-medium text-gray-700">Presentación</label>
                            <input
                                type="text"
                                name="prsntacion_elemnto"
                                value={formData.prsntacion_elemnto}
                                onChange={handleChange}
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border focus:ring-indigo-500 focus:border-indigo-500"
                            />
                        </div>

                        <div>
                            <label>Laboratorio</label>
                            <input
                                type="text"
                                name="lbrtorio_elemnto"
                                value={formData.lbrtorio_elemnto}
                                onChange={handleChange}
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border focus:ring-indigo-500 focus:border-indigo-500"
                            />
                        </div>

                        <div>
                            <label>Lote</label>
                            <input
                                type="text"
                                name="lote_elemnto"
                                value={formData.lote_elemnto}
                                onChange={handleChange}
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border focus:ring-indigo-500 focus:border-indigo-500"
                            />
                        </div>

                        <div>
                            <label>Costo Compra</label>
                            <input
                                type="number"
                                step="0.01"
                                name="costo_venta"
                                value={formData.costo_venta}
                                onChange={handleChange}
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border focus:ring-indigo-500 focus:border-indigo-500"
                            />
                        </div>

                    
                    <div className="md:col-span-2">
                        <label className="block text-sm font-medium text-gray-700">Descripción</label>
                        <textarea
                            name="descripcion_elemnto"
                            value={formData.dscrpcion_elemnto}
                            onChange={handleChange}
                            rows="2"
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border focus:ring-indigo-500 focus:border-indigo-500"
                        />
                    </div>

                    <div className="md:col-span-2">
                        <label className="block text-sm font-medium text-gray-700">Estado</label>
                        <select
                            name="estdo_elmnto"
                            value={formData.estdo_elmnto}
                            onChange={handleChange}
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border focus:ring-indigo-500 focus:border-indigo-500"
                        >
                            <option value="A">Activo</option>
                            <option value="I">Inactivo</option>
                        </select>
                    </div>

                    <div className="md:col-span-2 flex justify-end gap-3 pt-4 border-t mt-4">
                        <button
                            type="button"
                            onClick={onClose}
                            disabled={isLoading}
                            className="bg-gray-500 hover:bg-gray-600 text-white font-semibold py-2 px-4 rounded-lg transition duration-150 shadow-md"
                        >
                            Cancelar
                        </button>
                        <button
                            type="submit"
                            disabled={isLoading}
                            className="bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-150 shadow-md disabled:opacity-50"
                        >
                            {isLoading ? 'Guardando...' : 'Guardar Cambios'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};


export default function Inventario() {
    const [items, setItems] = useState([]);
    const { showToast, Toast } = useToast();

    const [kardexOpen, setKardexOpen] = useState(false);
    const [kardexData, setKardexData] = useState([]);
 
    const [editModalOpen, setEditModalOpen] = useState(false);
    const [productoActual, setProductoActual] = useState(null); 

    const [isConfirmModalOpen, setIsConfirmModalOpen] = useState(false);
    const [itemToToggle, setItemToToggle] = useState(null); 

    const TIPOS_MOV = {
        1: "Entrada por compra",
        2: "Entrada por Devolución",
        3: "Entrada por Transferencia",
        4: "Entrada por Ajuste",
        5: "Salida por Venta",
        6: "Salida por Transferencia",
        7: "Salida por Ajuste"
    };

    const fetchItems = useCallback(() => {
        axios.get("/elementos")
            .then(res => setItems(res.data))
            .catch(err => {
                console.error("Error al obtener elementos:", err);
                showToast("Error al cargar el inventario.", true);
            });
    }, [showToast]);

    useEffect(() => {
    fetchItems();
}, [fetchItems]);


useEffect(() => {
    items.forEach(item => {
        if(item.exstncia_elemnto === 1){
            showToast(`⚠️ STOCK BAJO: ${item.nmbre_elemnto} solo 1 unidad`, true);
        }
    });
}, [items, showToast]);



    const handleLocalUpdate = (updatedId, updatedData) => {
        setItems(prevItems => prevItems.map(x => 
            x.id === updatedId ? { ...x, ...updatedData } : x
        ));
    };

    const toggleEstadoAction = async (item) => {
        const nuevoEstado = item.estdo_elmnto === "A" ? "I" : "A";
        const estadoTexto = nuevoEstado === "A" ? "ACTIVO" : "INACTIVO";
        
        try {
   
            await axios.put(`/elementos/${item.id}`, { estdo_elmnto: nuevoEstado });

            handleLocalUpdate(item.id, { estdo_elmnto: nuevoEstado });
            showToast(`Estado de ${item.nmbre_elemnto} actualizado a ${estadoTexto}`, false);

        } catch (e) {
            console.error("Error al actualizar el estado:", e);
            showToast("Error al actualizar el estado", true);
        } finally {
             setItemToToggle(null); 
        }
    };

    const initToggleEstado = (item) => {
        setItemToToggle(item);
        setIsConfirmModalOpen(true);
    };


    const openEditModal = async (item) => {
    try {
        const res = await axios.get(`/elementos/${item.id}`);
        setProductoActual(res.data);
        setEditModalOpen(true);
    } catch (e) {
        console.error(e);
        showToast("Error cargando información del producto", true);
    }
    };

    const closeEditModal = () => {
        setEditModalOpen(false);
        setProductoActual(null);
    }

    const abrirKardex = async (item) => {
        setKardexData([]); 
        setProductoActual(item);
        setKardexOpen(true);

        try {
            const res = await axios.get(`/movimientos/kardex/${item.id}`);

            const lista = res.data.items.map(m => ({
                fecha: m.fcha_mvnto?.split("T")[0],
                tipo: TIPOS_MOV[m.tpo_mvnto] || "Desconocido",
                cantidad: m.cntdad_elemnto,
                stock_final: m.stock_nuevo,
                costo: m.costo_untario
            }));

            setKardexData(lista);

        } catch (e) {
            console.error("Error cargando el Kardex:", e);
            showToast("Error cargando el Kardex", true);
            setKardexData([]); 
        }
    };

    return (

        

        <div className="p-4 bg-gray-50 min-h-screen font-sans">
            <h1 className="text-3xl font-extrabold text-gray-800 mb-6">Inventario de Productos</h1>


<button
  onClick={async () => {
    try {
      const res = await axios.get("/reportes/elementos", {
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.download = "reporte_elementos.pdf";
      link.click();
    } catch (err) {
      console.error(err);
      alert("Error descargando reporte");
    }
  }}
  className="bg-red-600 text-white px-4 py-2 rounded mb-4"
>
  Descargar reporte de elementos (PDF)
</button>


            <div className="overflow-x-auto shadow-xl rounded-xl">
                <table className="min-w-full bg-white">
                    <thead className="bg-indigo-600 text-white sticky top-0">
                        <tr>
                            <th className="p-3 text-left">SKU</th>
                            <th className="p-3 text-left">Nombre</th>
                            <th className="p-3 text-left">Stock</th>
                            <th className="p-3 text-left">Precio Venta</th>
                            <th className="p-3 text-left">Estado</th>
                            <th className="p-3 w-64 text-left">Acciones</th>
                        </tr>
                    </thead>

                    <tbody>
                        {items.length > 0 ? (
                            items.map(el => (
                                <tr key={el.id} className="border-b hover:bg-indigo-50 transition duration-150">
                                    <td className="p-3 text-sm font-medium text-gray-700">{el.sku_elemnto}</td>
                                    <td className="p-3 text-sm font-semibold text-gray-800">{el.nmbre_elemnto}</td>
                                    <td className="p-3 text-sm font-bold text-center">
                                            {el.exstncia_elemnto <= 1 ? (
                                                <span className="bg-red-600 text-white px-2 py-1 rounded-lg animate-pulse">
                                                    ⚠️ {el.exstncia_elemnto}
                                                </span>
                                            ) : (
                                                <span className={el.exstncia_elemnto <= 5 ? 'text-red-500' : 'text-green-700'}>
                                                    {el.exstncia_elemnto}
                                                </span>
                                            )}
                                        </td>

                                    <td className="p-3 text-sm">${parseFloat(el.precio_venta_ac).toFixed(2)}</td>

                                    <td className="p-3">
                                        {el.estdo_elmnto === "A" ? (
                                            <span className="inline-block bg-green-100 text-green-800 text-xs font-semibold px-2 py-1 rounded-full">Activo</span>
                                        ) : (
                                            <span className="inline-block bg-red-100 text-red-800 text-xs font-semibold px-2 py-1 rounded-full">Inactivo</span>
                                        )}
                                    </td>

                                    <td className="p-3 flex gap-2 flex-wrap">
                                        
                                        {/* Botón Editar / Ver */}
                                        <button
                                            className="bg-indigo-600 hover:bg-indigo-700 text-white px-3 py-1 text-sm rounded-lg transition duration-150 shadow-md"
                                            onClick={() => openEditModal(el)}
                                        >
                                            Editar / Ver
                                        </button>
                                        
                                        {/* Botón Kardex */}
                                        <button
                                            className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 text-sm rounded-lg transition duration-150 shadow-md"
                                            onClick={() => abrirKardex(el)}
                                        >
                                            Kardex
                                        </button>

                                        {/* Botón Activar / Inactivar - Usa el inicializador */}
                                        <button
                                            className={`px-3 py-1 text-sm rounded-lg text-white transition duration-150 shadow-md
                                                ${el.estdo_elmnto === "A" ? "bg-red-600 hover:bg-red-700" : "bg-green-600 hover:bg-green-700"}
                                            `}
                                            onClick={() => initToggleEstado(el)}
                                        >
                                            {el.estdo_elmnto === "A" ? "Inactivar" : "Activar"}
                                        </button>
                                    </td>
                                </tr>
                            ))
                        ) : (
                            <tr>
                                <td colSpan="6" className="text-center p-8 text-lg text-gray-500 italic">
                                    Cargando datos o no hay elementos en el inventario...
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>


            {/* ---------------- MODAL KARDEX ---------------- */}
            {kardexOpen && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-40 p-4">
                    <div className="bg-white w-full max-w-lg md:max-w-3xl lg:max-w-4xl p-6 rounded-xl shadow-2xl relative animate-in zoom-in-50">
                        
                        <h2 className="text-2xl font-bold mb-4 text-gray-800 border-b pb-2">
                            Kardex de {productoActual?.nmbre_elemnto}
                        </h2>
                        
                        <button
                            onClick={() => setKardexOpen(false)}
                            className="absolute top-4 right-4 text-gray-500 hover:text-gray-900 text-2xl font-bold transition duration-150"
                            aria-label="Cerrar kardex"
                        >
                            &times;
                        </button>

                        <div className="overflow-x-auto max-h-[70vh]">
                            <table className="w-full border-collapse border border-gray-300">
                                <thead className="bg-gray-200 sticky top-0">
                                    <tr>
                                        <th className="p-3 border border-gray-300 text-left text-sm font-semibold">Fecha</th>
                                        <th className="p-3 border border-gray-300 text-left text-sm font-semibold">Tipo</th>
                                        <th className="p-3 border border-gray-300 text-center text-sm font-semibold">Cantidad</th>
                                        <th className="p-3 border border-gray-300 text-right text-sm font-semibold">Stock Final</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {kardexData.length > 0 ? (
                                        kardexData.map((mov, i) => (
                                            <tr key={i} className="border-b hover:bg-yellow-50">
                                                <td className="p-3 border text-sm">{mov.fecha}</td>
                                                <td className="p-3 border text-sm">
                                                    <span className={`font-medium ${mov.tipo.startsWith('Entrada') ? 'text-green-600' : 'text-red-600'}`}>
                                                        {mov.tipo}
                                                    </span>
                                                </td>
                                                <td className="p-3 border text-center text-sm">{mov.cantidad}</td>
                                                <td className="p-3 border text-center text-sm font-bold text-indigo-700">{mov.stock_final}</td>
                                            </tr>
                                        ))
                                    ) : (
                                        <tr>
                                            <td colSpan="4" className="text-center p-6 text-gray-500 italic">
                                                Cargando movimientos o no hay datos registrados.
                                            </td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </div>

                        <div className="flex justify-end mt-6">
                            <button
                                className="bg-red-600 hover:bg-red-700 text-white font-semibold px-4 py-2 rounded-lg transition duration-150 shadow-md"
                                onClick={() => setKardexOpen(false)}
                            >
                                Cerrar
                            </button>
                        </div>
                    </div>
                </div>
            )}
            
            {/* ---------------- MODAL EDICIÓN/VISUALIZACIÓN ---------------- */}
            <EditProductModal 
                isOpen={editModalOpen}
                onClose={closeEditModal}
                product={productoActual}
                onUpdate={handleLocalUpdate}
                showToast={showToast}
            />

            {/* ---------------- MODAL DE CONFIRMACIÓN ---------------- */}
            {itemToToggle && (
                <ConfirmationModal
                    isOpen={isConfirmModalOpen}
                    onClose={() => setIsConfirmModalOpen(false)}
                    onConfirm={toggleEstadoAction}
                    item={itemToToggle}
                    title="Confirmar Cambio de Estado"
                    message={`¿Estás seguro de que deseas cambiar el estado de "${itemToToggle.nmbre_elemnto}" a ${itemToToggle.estdo_elmnto === "A" ? "INACTIVO" : "ACTIVO"}?`}
                />
            )}

            {/* Componente de notificación Toast */}
            <Toast />
        </div>
    );
}