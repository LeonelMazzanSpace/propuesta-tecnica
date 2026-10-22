# Inserción de imágenes desde Chrome

`insertInlineImage` de la API exige una URL pública, y el material del cliente es confidencial. Por eso las imágenes se pegan desde el navegador sobre un marcador de texto (`{{F1}}`, `{{F2}}`…) que el lote de texto dejó en un párrafo `img` centrado.

## Pasos

1. Cargar la skill `claude-in-chrome` y las herramientas en una sola búsqueda: `tabs_context_mcp`, `navigate`, `computer`, `find`, `javascript_tool`, `file_upload`, `browser_batch`, `tabs_close_mcp`. Si hay varios navegadores conectados, preguntar cuál usar (normalmente el de Linux, donde están los archivos) y usar `select_browser`.
2. Abrir el documento en una pestaña nueva del grupo.
3. Crear un input de archivos propio en la página y cargarle los PNG de `images/pngs/` en el orden de los marcadores (los que en `images/IMAGENES.md` tienen figura asignada):

```js
await new Promise(r => setTimeout(r, 3000));
(() => { let i = document.getElementById('claude-img-input');
  if (!i) { i = document.createElement('input'); i.type = 'file'; i.multiple = true; i.id = 'claude-img-input';
    i.setAttribute('aria-label', 'claude image input');
    i.style.cssText = 'position:fixed;left:0;bottom:0;width:120px;height:24px;z-index:99999;opacity:0.01';
    document.body.appendChild(i); }
  return !!document.querySelector('.docs-texteventtarget-iframe'); })()
```

   Después: `find` "file input labeled claude image input" y `file_upload` con las rutas (pueden estar en el scratchpad).

4. Para cada marcador, en un `browser_batch`: `ctrl+f`, **esperar 1,5 s**, `ctrl+a` (para reemplazar la búsqueda anterior), escribir el marcador, **esperar 2 s**, `Return`, **esperar 2 s** y tomar una captura **con la barra de búsqueda todavía abierta**. Confirmar que la barra dice "1 of 1" y que el marcador se ve resaltado en la página. Si no se ve, repetir la búsqueda en lugar de pegar.
5. Recién con la selección confirmada, en el siguiente `browser_batch`: `Escape`, esperar 1 s y pegar la imagen N (índice desde 0). En el mismo lote se puede pasar a buscar el marcador siguiente y terminar con la captura de confirmación:

```js
(() => { const f = document.getElementById('claude-img-input').files[N];
  const dt = new DataTransfer(); dt.items.add(f);
  const doc = document.querySelector('.docs-texteventtarget-iframe').contentDocument;
  const t = doc.activeElement || doc.body;
  t.dispatchEvent(new ClipboardEvent('paste', {clipboardData: dt, bubbles: true, cancelable: true}));
  return f.name; })()
```

6. Después de la última, quitar el input (`document.getElementById('claude-img-input').remove()`), cerrar la pestaña y verificar por API con `verify_doc.py`: tantas imágenes como marcadores había, 0 marcadores restantes y portada intacta.

Docs ajusta la imagen pegada al ancho de la página (468 pt) y respeta el párrafo centrado del marcador, así que no hace falta redimensionarla.

## Errores conocidos

- **No hacer clic en el documento antes de `ctrl+f`.** Si la barra de búsqueda tarda en abrir, el texto y la imagen terminan en la posición del cursor (una vez cayó en la portada). Si pasa: `Escape` y `ctrl+z` hasta restaurar, y comparar la portada contra una lectura anterior.
- Si la captura no muestra el marcador seleccionado, no pegar. Repetir la búsqueda (a veces la vista queda en otra parte del documento aunque la búsqueda haya terminado).
- `file_upload` solo acepta archivos que el usuario compartió con la sesión o que están en el scratchpad o en la carpeta de trabajo.
- Para reemplazar imágenes ya insertadas: leer el documento, listar los índices de los `inlineObjectElement` en orden (la figura N es la N-ésima) y, en un solo lote con `requiredRevisionId`, borrar el carácter de cada imagen que cambió (`[i, i+1]`) e insertar su marcador `{{FN}}` en `i`, de mayor a menor índice. Cargar en el input solo esos PNG, en el orden de los marcadores, y pegar como arriba. Al verificar, los ids de los objetos insertados cambian: así se confirma que se reemplazaron.
- La extensión de Chrome puede desconectarse en medio del lote. Volver a llamar a `tabs_context_mcp`, comprobar que el input sigue con sus archivos (`files.length`) y retomar desde el marcador pendiente.
