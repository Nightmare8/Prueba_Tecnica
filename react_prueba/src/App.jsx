import {useState, useEffect } from "react"

const datos = [{'Ean3': {'nombre_producto': 'Product6', 'datos_query': ('SKU6', 'Product6', 'Ean3', 'Paris', 2.0), 'markets': ['Paris'], 'rango_precios': [34.0, 2.0]}}, {'Ean2': {'nombre_producto': 'Product2', 'datos_query': ('SKU2', 'Product2', 'Ean2', 'Falabella', 4.0), 'markets': ['Falabella'], 'rango_precios': [4.0, 4.0]}}, {'Ean1': {'nombre_producto': 'Product4', 'datos_query': ('SKU4', 'Product4', 'Ean1', 'Paris', 14.0), 'markets': ['Paris', 'Falabella'], 'rango_precios': [14.0, 2.0]}}]

function App() {

  const [productos, setProductos] = useState(datos);
  console.log(productos)
  
  useEffect(() => {

  },[productos])

  const handleFilter = (e) => {
    //Filtrar por el nombre
    //Si no esta escrito nada, mostrar todos los productos
    if (e.target.value === "") {
      setProductos(datos)
      return
    } else{
      //Recorrer el objeto
      const filtered = Object.keys(datos[0]).filter((ean) => 
        //Handle case sensitive
        datos[0][ean].nombre_producto.toLowerCase().includes(e.target.value.toLowerCase())
      )
      //Crear un objeto con los productos filtrados
      const filteredProducts = {}
      filtered.forEach((ean) => {
        filteredProducts[ean] = datos[0][ean]
      })
      setTimeout(() => {
        console.log(filteredProducts)
      }, 1000)
      //Actualizar el estado
      setProductos([filteredProducts])
    }
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
