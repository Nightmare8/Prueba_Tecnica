import {useState, useEffect } from "react"

const datos = [{'Ean3': {'nombre_producto': 'Product6', 'datos_query': ('SKU6', 'Product6', 'Ean3', 'Paris', 2.0), 'markets': ['Paris'], 'rango_precios': [34.0, 2.0]}}, {'Ean2': {'nombre_producto': 'Product2', 'datos_query': ('SKU2', 'Product2', 'Ean2', 'Falabella', 4.0), 'markets': ['Falabella'], 'rango_precios': [4.0, 4.0]}}, {'Ean1': {'nombre_producto': 'Product4', 'datos_query': ('SKU4', 'Product4', 'Ean1', 'Paris', 14.0), 'markets': ['Paris', 'Falabella'], 'rango_precios': [14.0, 2.0]}}]

function App() {

  const [productos, setProductos] = useState(datos);
  const [filter, setFilter] = useState('');
  useEffect(() => {
    //Si no hay texto en el filtro, mostrar todos los productos
    if(filter === '') {
      setProductos(datos);
      return;
    }
    //Filtrar productos y eliminar los que no cumplan con el filtro cada un segundo
    const filteredProducts = productos.filter(producto => {
      return producto[Object.keys(producto)[0]].nombre_producto.toLowerCase().includes(filter.toLowerCase())
    })
    let productAux = productos;
    //Recorrer los productos filtrados y eliminar los que no cumplan con el filtro cada un segundo
    let i = 0;
    const interval = setInterval(() => {
      if (i < productos.length) {
        if (!filteredProducts.includes(productos[i])) {
          //Remover el producto
          productAux = productAux.filter(producto => producto !== productos[i])
          setProductos(productAux)
        }
        i++;
      } else {
        clearInterval(interval)
      }
    }, 1000)

  },[filter, productos])

  const handleFilter = (e) => {
    //Filtrar
    setFilter(e.target.value);
  }
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignContent: "center",
        width: "calc(100vw - 40px)",
        padding: "20px",
      }}
    >
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignContent: "center",
          width: "20%",
        }}
      >
        <h1>Productos</h1>
        <input
          type="text"
          placeholder="Buscar producto"
          onChange={handleFilter}/>

      </div>
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          flexWrap: "wrap",
          justifyContent: "center",
        }}
      >
        {productos.map((producto, index) => {
          return (
            <div
              key={index}
              style={{
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignContent: "center",
                width: "20%",
                margin: "10px",
                padding: "10px",
                border: "1px solid black",
              }}
            >
              <h2>{producto[Object.keys(producto)[0]].nombre_producto}</h2>
              {/* Mercados */}
              {producto[Object.keys(producto)[0]].markets.map((market, index) => (
                <div key={index}>
                  <h3>{market}</h3>

                </div>
              ))}
              {/* Rango de precios */}
              <span>Precio Mayor: {producto[Object.keys(producto)[0]].rango_precios[0]}</span>
              <span>Precio Menor: {producto[Object.keys(producto)[0]].rango_precios[1]}</span>
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default App
