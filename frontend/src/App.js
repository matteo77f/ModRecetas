import { useState } from 'react';
import './App.css';

function App() {
  const [recipeText, setRecipeText] = useState('');
  const [preferences, setPreferences] = useState('Hacerla más saludable');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [fileInfo, setFileInfo] = useState('');
  const [imageFile, setImageFile] = useState(null);

  const readTextFile = (file) => {
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = () => {
        setError('No se pudo leer el archivo.');
        resolve('');
      };
      reader.readAsText(file);
    });
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;
    setError('');

    const isImage = file.type.startsWith('image/');
    const isText = file.type === 'text/plain' || file.name.toLowerCase().endsWith('.txt');

    if (isImage) {
      setRecipeText('');
      setImageFile(file);
      setFileInfo(`Imagen seleccionada: ${file.name}`);
      return;
    }

    setImageFile(null);
    setFileInfo(`Documento seleccionado: ${file.name}`);

    if (isText) {
      const content = await readTextFile(file);
      setRecipeText(content || '');
      return;
    }

    setRecipeText(`Archivo seleccionado: ${file.name}. Procesa este documento en el backend para extraer la receta.`);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    if (!recipeText.trim() && !imageFile) {
      setError('Debes ingresar el texto de la receta o subir una imagen.');
      return;
    }

    setLoading(true);
    try {
      let response;
      if (imageFile) {
        const formData = new FormData();
        formData.append('image', imageFile);
        formData.append('preferences', preferences);
        response = await fetch('/api/recommend', {
          method: 'POST',
          body: formData,
        });
      } else {
        response = await fetch('/api/recommend', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ recipe_text: recipeText, preferences }),
        });
      }

      const contentType = response.headers.get('content-type') || '';
      let data;

      if (contentType.includes('application/json')) {
        data = await response.json();
      } else {
        const text = await response.text();
        throw new Error(text || 'Error en la API: la respuesta no es JSON.');
      }

      if (!response.ok) {
        throw new Error(data.error || 'Error en la API');
      }
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <header className="topbar">
        <h1>ModRecetas</h1>
        <p>Recetas más saludables con IA.</p>
      </header>

      <main className="content-grid">
        <section className="input-panel">
          <h2>Cargar receta</h2>
          <form onSubmit={handleSubmit}>
            <label>
              Texto de receta
              <textarea
                value={recipeText}
                onChange={(e) => setRecipeText(e.target.value)}
                rows="10"
                placeholder="Pega aquí la receta o descríbela..."
              />
            </label>

            <div className="file-input-group">
              <label className="file-label">Subir documento o imagen</label>
              <input
                type="file"
                accept=".pdf,.docx,.txt,image/*"
                onChange={handleFileUpload}
              />
            </div>

            {fileInfo && <div className="file-info">{fileInfo}</div>}

            <label>
              Preferencia
              <input
                value={preferences}
                onChange={(e) => setPreferences(e.target.value)}
              />
            </label>
            <button type="submit" disabled={loading}>
              {loading ? 'Procesando...' : 'Enviar'}
            </button>
            {error && <div className="alert error">{error}</div>}
          </form>
        </section>

        <section className="result-panel">
          <h2>Resultado</h2>
          {result ? (
            <div className="recipe-result">
              <div className="card">
                <h3>Ingredientes originales</h3>
                <ul>
                  {result.original_ingredients.map((item, index) => (
                    <li key={index}>
                      <span className="strike">{item.name}</span> — {item.quantity}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="card">
                <h3>Ingredientes modificados</h3>
                <ul>
                  {result.modified_ingredients.map((item, index) => (
                    <li key={index}>{item.name} — {item.quantity}</li>
                  ))}
                </ul>
              </div>

              <div className="card">
                <h3>Pasos modificados</h3>
                <ol>
                  {result.modified_steps.map((step, index) => (
                    <li key={index}>{step}</li>
                  ))}
                </ol>
              </div>

              {result.warnings.length > 0 && (
                <div className="alert warning">
                  <h4>Advertencias</h4>
                  <ul>
                    {result.warnings.map((warning, index) => (
                      <li key={index}>{warning}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ) : (
            <div className="placeholder">Envía una receta para ver la recomendación.</div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
